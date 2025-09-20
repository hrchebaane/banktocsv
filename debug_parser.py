#!/usr/bin/env python
"""
Script de debug pour le parser Attijari
"""

import pdfplumber
from parsers.attijari_parser import AttijariParser

def debug_parser():
    """
    Debug du parser Attijari étape par étape
    """
    print("🔍 Debug du parser Attijari")
    print("=" * 50)
    
    parser = AttijariParser()
    
    with open('banktocsv_project/model_attijari.pdf', 'rb') as pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            all_text = ""
            
            # Extraire tout le texte
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"
            
            lines = all_text.split('\n')
            
            print(f"📄 Total de lignes: {len(lines)}")
            
            # Chercher l'en-tête
            print("\n🔍 Recherche de l'en-tête...")
            for i, line in enumerate(lines, 1):
                if parser._is_transaction_header(line):
                    print(f"✅ En-tête trouvé ligne {i}: {repr(line)}")
                    break
            else:
                print("❌ Aucun en-tête trouvé")
            
            # Chercher les transactions
            print("\n🔍 Recherche des transactions...")
            transaction_count = 0
            for i, line in enumerate(lines, 1):
                if parser._is_transaction_line(line):
                    transaction_count += 1
                    if transaction_count <= 5:  # Afficher les 5 premières
                        print(f"✅ Transaction {transaction_count} ligne {i}: {repr(line)}")
            
            print(f"📊 Total transactions détectées: {transaction_count}")
            
            # Chercher le solde
            print("\n🔍 Recherche du solde...")
            for i, line in enumerate(lines, 1):
                if parser._is_balance_line(line):
                    print(f"✅ Solde trouvé ligne {i}: {repr(line)}")
                    break
            else:
                print("❌ Aucun solde trouvé")

if __name__ == "__main__":
    debug_parser()
