from django.db import models
from django.utils import timezone


class BankStatement(models.Model):
    """
    Modèle pour stocker les informations des relevés bancaires
    """
    name = models.CharField(max_length=255, verbose_name="Nom du relevé")
    pdf_file = models.FileField(upload_to='bank_statements/', verbose_name="Fichier PDF")
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="Date d'upload")
    total_transactions = models.IntegerField(default=0, verbose_name="Nombre de transactions")
    final_balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Solde final")
    processed = models.BooleanField(default=False, verbose_name="Traité")
    
    class Meta:
        verbose_name = "Relevé bancaire"
        verbose_name_plural = "Relevés bancaires"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.name} - {self.uploaded_at.strftime('%d/%m/%Y %H:%M')}"


class Transaction(models.Model):
    """
    Modèle pour stocker les transactions individuelles
    """
    bank_statement = models.ForeignKey(BankStatement, on_delete=models.CASCADE, related_name='transactions')
    date_operation = models.DateField(verbose_name="Date opération")
    date_valeur = models.DateField(verbose_name="Date valeur")
    libelle = models.TextField(verbose_name="Libellé")
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Débit")
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Crédit")
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['date_operation']
    
    def __str__(self):
        return f"{self.date_operation} - {self.libelle[:50]}"
