#!/usr/bin/env python
"""
Script de debug pour analyser le contenu d'un PDF Attijari
"""

import pdfplumber
import sys

def debug_pdf_content(pdf_path):
    """
    Analyse le contenu d'un PDF pour comprendre sa structure
    """
    print(f"🔍 Analyse du PDF: {pdf_path}")
    print("=" * 60)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"📄 Nombre de pages: {len(pdf.pages)}")
            
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"\n📖 PAGE {page_num}")
                print("-" * 40)
                
                # Extraire le texte brut
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    print(f"📝 Nombre de lignes: {len(lines)}")
                    
                    # Afficher les premières lignes
                    print("\n🔤 Premières lignes:")
                    for i, line in enumerate(lines[:20], 1):
                        print(f"{i:2d}: {repr(line)}")
                    
                    # Chercher des patterns de dates
                    import re
                    date_patterns = [
                        r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
                        r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
                        r'\d{2}\.\d{2}\.\d{4}', # DD.MM.YYYY
                    ]
                    
                    print("\n📅 Lignes contenant des dates:")
                    for i, line in enumerate(lines, 1):
                        for pattern in date_patterns:
                            if re.search(pattern, line):
                                print(f"{i:2d}: {repr(line)}")
                                break
                    
                    # Chercher des patterns de montants
                    amount_patterns = [
                        r'\d+[.,]\d{2}',  # 1234.56 ou 1234,56
                        r'\d+\s+[.,]\d{2}',  # 1234 .56
                    ]
                    
                    print("\n💰 Lignes contenant des montants:")
                    for i, line in enumerate(lines, 1):
                        for pattern in amount_patterns:
                            if re.search(pattern, line):
                                print(f"{i:2d}: {repr(line)}")
                                break
                    
                    # Chercher des mots-clés Attijari
                    keywords = [
                        'attijari', 'banque', 'compte', 'solde', 'débit', 'crédit',
                        'opération', 'valeur', 'libellé', 'montant', 'tnd', 'dt'
                    ]
                    
                    print("\n🔑 Lignes contenant des mots-clés:")
                    for i, line in enumerate(lines, 1):
                        line_lower = line.lower()
                        for keyword in keywords:
                            if keyword in line_lower:
                                print(f"{i:2d}: {repr(line)}")
                                break
                    
                    # Afficher toutes les lignes (pour analyse complète)
                    print(f"\n📋 TOUTES LES LIGNES (page {page_num}):")
                    print("-" * 40)
                    for i, line in enumerate(lines, 1):
                        print(f"{i:3d}: {line}")
                
                else:
                    print("❌ Aucun texte extrait de cette page")
    
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python debug_pdf.py <chemin_vers_pdf>")
        print("Exemple: python debug_pdf.py test_releve.pdf")
        return
    
    pdf_path = sys.argv[1]
    debug_pdf_content(pdf_path)

if __name__ == "__main__":
    main()
