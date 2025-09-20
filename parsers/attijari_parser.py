"""
Parser pour les relevés bancaires Attijari Tunisie
Utilise pdfplumber pour extraire les données des PDF natifs
"""

import pdfplumber
import pandas as pd
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import io


class AttijariParser:
    """
    Parser spécialisé pour les relevés bancaires Attijari Tunisie
    """
    
    def __init__(self):
        self.transactions = []
        self.final_balance = None
        
    def parse_pdf(self, pdf_file) -> Dict:
        """
        Parse un fichier PDF de relevé bancaire Attijari
        
        Args:
            pdf_file: Fichier PDF (peut être un objet file ou un chemin)
            
        Returns:
            Dict contenant les transactions et le solde final
        """
        try:
            with pdfplumber.open(pdf_file) as pdf:
                all_text = ""
                
                # Extraire tout le texte de toutes les pages
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        all_text += page_text + "\n"
                
                # Parser le contenu
                self._parse_content(all_text)
                
                return {
                    'transactions': self.transactions,
                    'final_balance': self.final_balance,
                    'total_transactions': len(self.transactions)
                }
                
        except Exception as e:
            raise Exception(f"Erreur lors du parsing du PDF: {str(e)}")
    
    def _parse_content(self, text: str):
        """
        Parse le contenu textuel du PDF pour extraire les transactions
        
        Args:
            text: Contenu textuel du PDF
        """
        lines = text.split('\n')
        
        # Variables pour détecter les sections
        in_transactions = False
        transaction_started = False
        
        for line in lines:
            line = line.strip()
            
            # Détecter le début de la section des transactions
            if self._is_transaction_header(line):
                in_transactions = True
                transaction_started = True
                continue
            
            # Détecter la fin de la section des transactions (solde final)
            # Ne s'arrêter que si c'est le solde final (pas le solde de début)
            if in_transactions and self._is_balance_line(line) and not line.startswith('SOLDE AU'):
                self._extract_final_balance(line)
                break
            
            # Parser les lignes de transaction
            if in_transactions and transaction_started and self._is_transaction_line(line):
                transaction = self._parse_transaction_line(line)
                if transaction:
                    self.transactions.append(transaction)
    
    def _is_transaction_header(self, line: str) -> bool:
        """
        Détecte si la ligne est un en-tête de section de transactions
        """
        header_patterns = [
            r'date.*libellé.*valeur.*débit.*crédit',
            r'date.*libelle.*valeur.*debit.*credit',
            r'date.*valeur.*debit.*credit',
            r'date.*valeur.*débit.*crédit',
        ]
        
        line_lower = line.lower()
        return any(re.search(pattern, line_lower) for pattern in header_patterns)
    
    def _is_transaction_line(self, line: str) -> bool:
        """
        Détecte si la ligne contient une transaction
        Format Attijari: DD MM LIBELLE DD MM YYYY MONTANT
        """
        # Vérifier que ce n'est pas une ligne de solde ou de totaux
        if any(keyword in line.upper() for keyword in ['SOLDE', 'TOTAUX', 'REPORT', 'DONT TVA', 'ECHEANCE']):
            return False
        
        # Pattern pour les transactions Attijari
        # Format: 04 08 COMMISSION ENC CHQ 0146467 01 08 2025 0,893
        # ou: 04 08 VERSEMENT ESPECE 091936 05 08 2025 1 640,000
        attijari_pattern = r'^\d{2}\s+\d{2}\s+.+\s+\d{2}\s+\d{2}\s+\d{4}\s+[\d\s,]+$'
        
        return bool(re.match(attijari_pattern, line.strip()))
    
    def _is_balance_line(self, line: str) -> bool:
        """
        Détecte si la ligne contient le solde final
        """
        balance_patterns = [
            r'^SOLDE\s+[\d\s,]+$',  # SOLDE 1 477,110
            r'^SOLDE\s+AU\s+\d{2}/\d{2}/\d{4}',  # SOLDE AU 31/07/2025 2,589
        ]
        
        line_upper = line.upper().strip()
        return any(re.search(pattern, line_upper) for pattern in balance_patterns)
    
    def _parse_transaction_line(self, line: str) -> Optional[Dict]:
        """
        Parse une ligne de transaction pour extraire les données
        Format Attijari: DD MM LIBELLE DD MM YYYY MONTANT
        
        Args:
            line: Ligne de transaction
            
        Returns:
            Dict contenant les données de la transaction ou None si parsing échoue
        """
        try:
            # Pattern pour extraire les composants Attijari
            # Format: 04 08 COMMISSION ENC CHQ 0146467 01 08 2025 0,893
            pattern = r'^(\d{2})\s+(\d{2})\s+(.+?)\s+(\d{2})\s+(\d{2})\s+(\d{4})\s+([\d\s,]+)$'
            
            match = re.search(pattern, line.strip())
            if not match:
                return None
            
            day_op = match.group(1)
            month_op = match.group(2)
            libelle = match.group(3).strip()
            day_val = match.group(4)
            month_val = match.group(5)
            year_val = match.group(6)
            amount_str = match.group(7).strip()
            
            # Construire les dates
            date_operation = f"{year_val}-{month_op.zfill(2)}-{day_op.zfill(2)}"
            date_valeur = f"{year_val}-{month_val.zfill(2)}-{day_val.zfill(2)}"
            
            # Parser le montant
            amount = self._parse_amount(amount_str)
            
            # Déterminer si c'est un débit ou un crédit selon le libellé
            libelle_upper = libelle.upper()
            
            # Mots-clés pour les crédits (entrées d'argent)
            credit_keywords = [
                'VERSEMENT', 'ENCAISSEMENT', 'VIR RECU', 'VIREMENT RECU', 
                'REMISE', 'DEPOT', 'CREDIT', 'RECEPTION'
            ]
            
            # Mots-clés pour les débits (sorties d'argent)
            debit_keywords = [
                'COMMISSION', 'FRAIS', 'COTISATION', 'PRELEVEMENT', 'RETRAIT',
                'GAB', 'ACHAT', 'PAIEMENT', 'VIR EMIS', 'VIREMENT EMIS',
                'STE ', 'SOCIETE', 'HOTEL', 'RESTAURANT', 'SUPERMARCHE'
            ]
            
            is_credit = any(keyword in libelle_upper for keyword in credit_keywords)
            is_debit = any(keyword in libelle_upper for keyword in debit_keywords)
            
            if is_credit and not is_debit:
                # C'est un crédit
                debit = 0.0
                credit = amount
            elif is_debit and not is_credit:
                # C'est un débit
                debit = amount
                credit = 0.0
            else:
                # Par défaut, considérer comme un débit
                debit = amount
                credit = 0.0
            
            return {
                'date_operation': date_operation,
                'date_valeur': date_valeur,
                'libelle': libelle,
                'debit': debit,
                'credit': credit
            }
            
        except Exception as e:
            print(f"Erreur lors du parsing de la ligne: {line} - {str(e)}")
            return None
    
    def _parse_amount(self, amount_str: str) -> float:
        """
        Parse un montant depuis une chaîne de caractères
        Format Attijari: "1 640,000" ou "0,893"
        
        Args:
            amount_str: Chaîne contenant le montant
            
        Returns:
            Montant en float
        """
        # Nettoyer la chaîne : supprimer les espaces et remplacer virgule par point
        amount_str = amount_str.replace(' ', '').replace(',', '.')
        return float(amount_str)
    
    def _parse_date(self, date_str: str) -> str:
        """
        Parse une date depuis une chaîne DD/MM/YYYY
        
        Args:
            date_str: Date au format DD/MM/YYYY
            
        Returns:
            Date au format YYYY-MM-DD
        """
        try:
            # Parser la date DD/MM/YYYY
            day, month, year = date_str.split('/')
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        except:
            return date_str
    
    def _extract_final_balance(self, line: str):
        """
        Extrait le solde final de la ligne
        Format Attijari: "SOLDE 1 477,110" ou "SOLDE AU 31/07/2025 2,589"
        
        Args:
            line: Ligne contenant le solde final
        """
        try:
            # Pattern pour extraire le solde final Attijari
            # Format: SOLDE 1 477,110 ou SOLDE AU 31/07/2025 2,589
            balance_pattern = r'^SOLDE(?:\s+AU\s+\d{2}/\d{2}/\d{4})?\s+([\d\s,]+)$'
            
            match = re.search(balance_pattern, line.upper().strip())
            if match:
                balance_str = match.group(1).strip()
                self.final_balance = self._parse_amount(balance_str)
            else:
                # Fallback : chercher un montant simple dans la ligne
                # Format: 1 477,110 (avec espaces et virgule)
                amount_pattern = r'(\d+\s+\d{3},\d{3})'
                amounts = re.findall(amount_pattern, line)
                
                if amounts:
                    # Prendre le premier montant trouvé
                    balance_str = amounts[0].strip()
                    self.final_balance = self._parse_amount(balance_str)
        except Exception as e:
            print(f"Erreur lors de l'extraction du solde final: {str(e)}")
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convertit les transactions en DataFrame pandas
        
        Returns:
            DataFrame pandas contenant les transactions
        """
        if not self.transactions:
            return pd.DataFrame(columns=['date_operation', 'date_valeur', 'libelle', 'debit', 'credit'])
        
        df = pd.DataFrame(self.transactions)
        
        # Ajouter une colonne pour le solde final si disponible
        if self.final_balance is not None:
            df.loc[len(df)] = {
                'date_operation': '',
                'date_valeur': '',
                'libelle': 'SOLDE FINAL',
                'debit': 0.0 if self.final_balance >= 0 else abs(self.final_balance),
                'credit': self.final_balance if self.final_balance >= 0 else 0.0
            }
        
        return df
    
    def export_to_csv(self, output_path: str = None) -> str:
        """
        Exporte les données en CSV
        
        Args:
            output_path: Chemin de sortie (optionnel)
            
        Returns:
            Contenu CSV en string
        """
        df = self.to_dataframe()
        
        if output_path:
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            return f"Fichier CSV exporté vers: {output_path}"
        else:
            # Retourner le contenu CSV en string
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
            return csv_buffer.getvalue()
    
    def export_to_excel(self, output_path: str = None) -> bytes:
        """
        Exporte les données en Excel
        
        Args:
            output_path: Chemin de sortie (optionnel)
            
        Returns:
            Contenu Excel en bytes
        """
        df = self.to_dataframe()
        
        if output_path:
            df.to_excel(output_path, index=False, engine='openpyxl')
            return f"Fichier Excel exporté vers: {output_path}"
        else:
            # Retourner le contenu Excel en bytes
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            return excel_buffer.getvalue()


def parse_attijari_pdf(pdf_file) -> Dict:
    """
    Fonction utilitaire pour parser un PDF Attijari
    
    Args:
        pdf_file: Fichier PDF
        
    Returns:
        Dict contenant les données extraites
    """
    parser = AttijariParser()
    return parser.parse_pdf(pdf_file)
