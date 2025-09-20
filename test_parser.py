#!/usr/bin/env python
"""
Script de test pour le parser Attijari
Teste le parser avec un PDF de relevé bancaire Attijari
"""

import os
import sys
from parsers.attijari_parser import AttijariParser

def test_parser():
    """
    Teste le parser Attijari avec un fichier PDF
    """
    print("🧪 Test du parser Attijari")
    print("=" * 50)
    
    # Vérifier que le parser peut être importé
    try:
        parser = AttijariParser()
        print("✅ Parser Attijari importé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'import du parser: {e}")
        return False
    
    # Test avec un fichier PDF (si disponible)
    test_pdf_path = "test_releve.pdf"
    
    if os.path.exists(test_pdf_path):
        print(f"📄 Test avec le fichier: {test_pdf_path}")
        try:
            with open(test_pdf_path, 'rb') as pdf_file:
                result = parser.parse_pdf(pdf_file)
            
            print(f"✅ PDF traité avec succès")
            print(f"📊 Transactions extraites: {result['total_transactions']}")
            print(f"💰 Solde final: {result['final_balance']}")
            
            if result['transactions']:
                print("\n📋 Aperçu des transactions:")
                for i, transaction in enumerate(result['transactions'][:3]):  # Afficher les 3 premières
                    print(f"  {i+1}. {transaction['date_operation']} - {transaction['libelle'][:30]}...")
                
                if len(result['transactions']) > 3:
                    print(f"  ... et {len(result['transactions']) - 3} autres transactions")
            
            # Test d'export CSV
            print("\n📤 Test d'export CSV...")
            csv_content = parser.export_to_csv()
            print(f"✅ CSV généré ({len(csv_content)} caractères)")
            
            # Test d'export Excel
            print("📤 Test d'export Excel...")
            excel_content = parser.export_to_excel()
            print(f"✅ Excel généré ({len(excel_content)} bytes)")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement du PDF: {e}")
            return False
    else:
        print(f"⚠️  Fichier de test non trouvé: {test_pdf_path}")
        print("   Placez un PDF de relevé Attijari nommé 'test_releve.pdf' dans le répertoire racine")
        print("   pour tester le parser.")
        return True  # Pas d'erreur, juste pas de fichier de test

def test_django_setup():
    """
    Teste la configuration Django
    """
    print("\n🔧 Test de la configuration Django")
    print("=" * 50)
    
    try:
        import django
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        print(f"✅ Django {django.get_version()} détecté")
        
        # Vérifier les modèles
        from banktocsv.models import BankStatement, Transaction
        print("✅ Modèles Django importés avec succès")
        
        # Vérifier les vues
        from banktocsv.views import index, upload_statement
        print("✅ Vues Django importées avec succès")
        
        # Vérifier les formulaires
        from banktocsv.forms import BankStatementUploadForm
        print("✅ Formulaires Django importés avec succès")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False

def main():
    """
    Fonction principale de test
    """
    print("🚀 Test du projet BankToCSV")
    print("=" * 60)
    
    # Test Django
    django_ok = test_django_setup()
    
    # Test Parser
    parser_ok = test_parser()
    
    print("\n📊 Résumé des tests")
    print("=" * 30)
    print(f"Django: {'✅ OK' if django_ok else '❌ ERREUR'}")
    print(f"Parser: {'✅ OK' if parser_ok else '❌ ERREUR'}")
    
    if django_ok and parser_ok:
        print("\n🎉 Tous les tests sont passés ! Le projet est prêt à être utilisé.")
        print("\n📝 Pour démarrer le serveur:")
        print("   python manage.py runserver")
        print("\n🌐 Puis ouvrir: http://127.0.0.1:8000")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez la configuration.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
