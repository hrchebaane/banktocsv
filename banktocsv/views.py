from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
import os
import tempfile
from datetime import datetime

from .models import BankStatement, Transaction
from .forms import BankStatementUploadForm, ExportFormatForm
from parsers.attijari_parser import AttijariParser


def index(request):
    """
    Page d'accueil avec convertisseur intégré - Une seule page pour tout faire
    """
    bank_statements = BankStatement.objects.all()[:10]  # Derniers 10 relevés
    
    context = {
        'bank_statements': bank_statements,
        'total_statements': BankStatement.objects.count(),
        'total_transactions': Transaction.objects.count(),
    }
    
    return render(request, 'banktocsv/index.html', context)


def upload_statement(request):
    """
    Vue pour l'upload de relevés bancaires
    """
    if request.method == 'POST':
        form = BankStatementUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Sauvegarder le relevé
                bank_statement = form.save()
                
                # Traiter le PDF avec le parser Attijari
                parser = AttijariParser()
                pdf_file_path = bank_statement.pdf_file.path
                
                with open(pdf_file_path, 'rb') as pdf_file:
                    result = parser.parse_pdf(pdf_file)
                
                # Mettre à jour le relevé avec les données extraites
                bank_statement.total_transactions = result['total_transactions']
                bank_statement.final_balance = result['final_balance']
                bank_statement.processed = True
                bank_statement.save()
                
                # Sauvegarder les transactions en base
                for transaction_data in result['transactions']:
                    Transaction.objects.create(
                        bank_statement=bank_statement,
                        date_operation=transaction_data['date_operation'],
                        date_valeur=transaction_data['date_valeur'],
                        libelle=transaction_data['libelle'],
                        debit=transaction_data['debit'],
                        credit=transaction_data['credit']
                    )
                
                messages.success(
                    request, 
                    f"Relevé traité avec succès ! {result['total_transactions']} transactions extraites."
                )
                
                return redirect('banktocsv:statement_detail', statement_id=bank_statement.id)
                
            except Exception as e:
                messages.error(request, f"Erreur lors du traitement du PDF: {str(e)}")
                # Supprimer le relevé si le traitement a échoué
                if 'bank_statement' in locals():
                    bank_statement.delete()
    else:
        form = BankStatementUploadForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'banktocsv/upload.html', context)


def statement_detail(request, statement_id):
    """
    Détail d'un relevé bancaire avec les transactions
    """
    bank_statement = get_object_or_404(BankStatement, id=statement_id)
    transactions = bank_statement.transactions.all()
    
    context = {
        'bank_statement': bank_statement,
        'transactions': transactions,
    }
    
    return render(request, 'banktocsv/statement_detail.html', context)


def export_statement(request, statement_id):
    """
    Export d'un relevé bancaire en CSV ou Excel
    """
    bank_statement = get_object_or_404(BankStatement, id=statement_id)
    
    if not bank_statement.processed:
        messages.error(request, "Ce relevé n'a pas encore été traité.")
        return redirect('banktocsv:statement_detail', statement_id=statement_id)
    
    if request.method == 'POST':
        form = ExportFormatForm(request.POST)
        
        if form.is_valid():
            export_format = form.cleaned_data['export_format']
            
            # Récupérer les transactions
            transactions = bank_statement.transactions.all()
            
            # Créer le DataFrame
            import pandas as pd
            data = []
            for transaction in transactions:
                data.append({
                    'Date Opération': transaction.date_operation,
                    'Date Valeur': transaction.date_valeur,
                    'Libellé': transaction.libelle,
                    'Débit': float(transaction.debit),
                    'Crédit': float(transaction.credit)
                })
            
            df = pd.DataFrame(data)
            
            # Générer le nom du fichier
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"releve_{bank_statement.name}_{timestamp}"
            
            if export_format == 'csv':
                # Export CSV
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
                
                # Ajouter BOM pour Excel
                response.write('\ufeff')
                df.to_csv(response, index=False, encoding='utf-8-sig')
                
                return response
                
            elif export_format == 'excel':
                # Export Excel
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
                
                # Utiliser openpyxl pour Excel
                from io import BytesIO
                output = BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')
                response.write(output.getvalue())
                
                return response
    else:
        form = ExportFormatForm()
    
    context = {
        'bank_statement': bank_statement,
        'form': form,
    }
    
    return render(request, 'banktocsv/export.html', context)


def download_csv(request, statement_id):
    """
    Téléchargement direct en CSV
    """
    bank_statement = get_object_or_404(BankStatement, id=statement_id)
    
    if not bank_statement.processed:
        raise Http404("Relevé non traité")
    
    # Récupérer les transactions
    transactions = bank_statement.transactions.all()
    
    # Créer le CSV
    import csv
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="releve_{bank_statement.name}.csv"'
    
    # Ajouter BOM pour Excel
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow(['Date Opération', 'Date Valeur', 'Libellé', 'Débit', 'Crédit'])
    
    for transaction in transactions:
        writer.writerow([
            transaction.date_operation,
            transaction.date_valeur,
            transaction.libelle,
            float(transaction.debit),
            float(transaction.credit)
        ])
    
    return response


def download_excel(request, statement_id):
    """
    Téléchargement direct en Excel
    """
    bank_statement = get_object_or_404(BankStatement, id=statement_id)
    
    if not bank_statement.processed:
        raise Http404("Relevé non traité")
    
    # Récupérer les transactions
    transactions = bank_statement.transactions.all()
    
    # Créer le DataFrame
    import pandas as pd
    data = []
    for transaction in transactions:
        data.append({
            'Date Opération': transaction.date_operation,
            'Date Valeur': transaction.date_valeur,
            'Libellé': transaction.libelle,
            'Débit': float(transaction.debit),
            'Crédit': float(transaction.credit)
        })
    
    df = pd.DataFrame(data)
    
    # Export Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="releve_{bank_statement.name}.xlsx"'
    
    from io import BytesIO
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    response.write(output.getvalue())
    
    return response


def delete_statement(request, statement_id):
    """
    Suppression d'un relevé bancaire
    """
    bank_statement = get_object_or_404(BankStatement, id=statement_id)
    
    if request.method == 'POST':
        try:
            # Supprimer le fichier PDF du système de fichiers
            if bank_statement.pdf_file:
                bank_statement.pdf_file.delete(save=False)
            
            # Supprimer le relevé (les transactions seront supprimées automatiquement via CASCADE)
            statement_name = bank_statement.name
            bank_statement.delete()
            
            messages.success(request, f"Le relevé '{statement_name}' a été supprimé avec succès.")
            return redirect('banktocsv:index')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression du relevé: {str(e)}")
            return redirect('banktocsv:statement_detail', statement_id=statement_id)
    
    # Si GET, rediriger vers la page de détail
    return redirect('banktocsv:statement_detail', statement_id=statement_id)


def confirm_delete_statement(request, statement_id):
    """
    Page de confirmation de suppression d'un relevé bancaire
    """
    bank_statement = get_object_or_404(BankStatement, id=statement_id)
    
    context = {
        'bank_statement': bank_statement,
    }
    
    return render(request, 'banktocsv/confirm_delete.html', context)


def converter(request):
    """
    Page unique du convertisseur - Upload, traitement et export en une seule page
    """
    context = {}
    return render(request, 'banktocsv/converter.html', context)


def process_upload(request):
    """
    Traitement direct de l'upload de fichier sans base de données
    """
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        
        if not pdf_file:
            return JsonResponse({
                'success': False,
                'message': 'Aucun fichier PDF fourni'
            })
        
        # Vérifier le type de fichier
        if not pdf_file.name.lower().endswith('.pdf'):
            return JsonResponse({
                'success': False,
                'message': 'Le fichier doit être un PDF'
            })
        
        # Vérifier la taille du fichier (max 10MB)
        if pdf_file.size > 10 * 1024 * 1024:
            return JsonResponse({
                'success': False,
                'message': 'Le fichier est trop volumineux (max 10MB)'
            })
        
        try:
            # Traiter le PDF avec le parser Attijari
            parser = AttijariParser()
            result = parser.parse_pdf(pdf_file)
            
            # Préparer les données des transactions
            transactions_data = []
            for transaction_data in result['transactions']:
                transactions_data.append({
                    'date_operation': transaction_data['date_operation'],
                    'date_valeur': transaction_data['date_valeur'],
                    'libelle': transaction_data['libelle'],
                    'debit': float(transaction_data['debit']),
                    'credit': float(transaction_data['credit'])
                })
            
            return JsonResponse({
                'success': True,
                'message': f"Relevé traité avec succès ! {result['total_transactions']} transactions extraites.",
                'data': {
                    'total_transactions': result['total_transactions'],
                    'final_balance': float(result['final_balance']) if result['final_balance'] else None,
                    'transactions': transactions_data
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f"Erreur lors du traitement du PDF: {str(e)}"
            })
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


def download_direct(request):
    """
    Téléchargement direct des données traitées sans base de données
    """
    if request.method == 'POST':
        import json
        import pandas as pd
        from io import BytesIO
        
        # Récupérer les données depuis le POST
        transactions_data = request.POST.get('transactions_data')
        format_type = request.POST.get('format_type', 'csv')
        
        if not transactions_data:
            return JsonResponse({'success': False, 'message': 'Aucune donnée fournie'})
        
        try:
            # Parser les données JSON
            transactions = json.loads(transactions_data)
            
            # Créer le DataFrame
            df = pd.DataFrame(transactions)
            
            # Renommer les colonnes pour l'affichage
            df.columns = ['Date Opération', 'Date Valeur', 'Libellé', 'Débit', 'Crédit']
            
            # Générer le nom du fichier
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"releve_attijari_{timestamp}"
            
            if format_type == 'csv':
                # Export CSV
                response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
                response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
                
                # Ajouter BOM pour Excel
                response.write('\ufeff')
                df.to_csv(response, index=False, encoding='utf-8-sig')
                
                return response
                
            elif format_type == 'excel':
                # Export Excel
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
                
                # Utiliser openpyxl pour Excel
                output = BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')
                response.write(output.getvalue())
                
                return response
            
            return JsonResponse({'success': False, 'message': 'Format non supporté'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur lors de la génération du fichier: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


def download_file(request, statement_id, format_type):
    """
    Téléchargement de fichier en CSV ou Excel
    """
    bank_statement = get_object_or_404(BankStatement, id=statement_id)
    
    if not bank_statement.processed:
        raise Http404("Relevé non traité")
    
    # Récupérer les transactions
    transactions = bank_statement.transactions.all()
    
    # Créer le DataFrame
    import pandas as pd
    data = []
    for transaction in transactions:
        data.append({
            'Date Opération': transaction.date_operation,
            'Date Valeur': transaction.date_valeur,
            'Libellé': transaction.libelle,
            'Débit': float(transaction.debit),
            'Crédit': float(transaction.credit)
        })
    
    df = pd.DataFrame(data)
    
    # Générer le nom du fichier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"releve_{bank_statement.name}_{timestamp}"
    
    if format_type == 'csv':
        # Export CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        # Ajouter BOM pour Excel
        response.write('\ufeff')
        df.to_csv(response, index=False, encoding='utf-8-sig')
        
        return response
        
    elif format_type == 'excel':
        # Export Excel
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        
        # Utiliser openpyxl pour Excel
        from io import BytesIO
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        response.write(output.getvalue())
        
        return response
    
    raise Http404("Format non supporté")
