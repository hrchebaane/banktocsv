"""
Formulaires pour l'application BankToCSV
"""

from django import forms
from .models import BankStatement


class BankStatementUploadForm(forms.ModelForm):
    """
    Formulaire pour l'upload de relevés bancaires PDF
    """
    
    class Meta:
        model = BankStatement
        fields = ['name', 'pdf_file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du relevé (ex: Relevé Janvier 2024)',
                'required': True
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            })
        }
        labels = {
            'name': 'Nom du relevé',
            'pdf_file': 'Fichier PDF'
        }
    
    def clean_pdf_file(self):
        """
        Validation du fichier PDF
        """
        pdf_file = self.cleaned_data.get('pdf_file')
        
        if pdf_file:
            # Vérifier l'extension
            if not pdf_file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Le fichier doit être un PDF (.pdf)")
            
            # Vérifier la taille (limite à 10MB)
            if pdf_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Le fichier est trop volumineux (max 10MB)")
        
        return pdf_file
    
    def clean_name(self):
        """
        Validation du nom du relevé
        """
        name = self.cleaned_data.get('name')
        
        if not name or not name.strip():
            raise forms.ValidationError("Le nom du relevé est obligatoire")
        
        return name.strip()


class ExportFormatForm(forms.Form):
    """
    Formulaire pour choisir le format d'export
    """
    EXPORT_CHOICES = [
        ('csv', 'CSV'),
        ('excel', 'Excel (.xlsx)'),
    ]
    
    export_format = forms.ChoiceField(
        choices=EXPORT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Format d\'export',
        initial='csv'
    )
