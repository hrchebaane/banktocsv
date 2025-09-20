#!/usr/bin/env python
"""
Script de test interactif pour adapter le parser Attijari
"""

import sys
import os
from parsers.attijari_parser import AttijariParser

def test_with_real_pdf(pdf_path):
    """
    Teste le parser avec un vrai PDF Attijari
    """
    if not os.path.exists(pdf_path):
        print(f"❌ Fichier non trouvé: {pdf_path}")
        return
    
    print(f"🧪 Test du parser avec: {pdf_path}")
    print("=" * 60)
    
    parser = AttijariParser()
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            result = parser.parse_pdf(pdf_file)
        
        print(f"✅ PDF traité")
        print(f"📊 Transactions trouvées: {result['total_transactions']}")
        print(f"💰 Solde final: {result['final_balance']}")
        
        if result['transactions']:
            print("\n📋 Transactions extraites:")
            for i, transaction in enumerate(result['transactions'][:5], 1):
                print(f"  {i}. {transaction['date_operation']} | {transaction['date_valeur']} | {transaction['libelle'][:30]}... | {transaction['debit']} | {transaction['credit']}")
        else:
            print("\n❌ Aucune transaction extraite")
            print("🔍 Le parser n'a pas détecté de transactions. Il faut adapter les patterns.")
            
            # Analyser le contenu brut
            print("\n🔍 Analyse du contenu brut...")
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        print(f"\n📄 Page {page_num} - Premières lignes:")
                        for i, line in enumerate(lines[:10], 1):
                            print(f"  {i:2d}: {repr(line)}")
                        
                        # Chercher des patterns de dates
                        import re
                        print(f"\n📅 Lignes avec dates (DD/MM/YYYY):")
                        for i, line in enumerate(lines, 1):
                            if re.search(r'\d{2}/\d{2}/\d{4}', line):
                                print(f"  {i:2d}: {repr(line)}")
                        
                        # Chercher des patterns de montants
                        print(f"\n💰 Lignes avec montants:")
                        for i, line in enumerate(lines, 1):
                            if re.search(r'\d+[.,]\d{2}', line):
                                print(f"  {i:2d}: {repr(line)}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_attijari_parser.py <chemin_vers_pdf>")
        print("Exemple: python test_attijari_parser.py releve_attijari.pdf")
        return
    
    pdf_path = sys.argv[1]
    test_with_real_pdf(pdf_path)

if __name__ == "__main__":
    main()
