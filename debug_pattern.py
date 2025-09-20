#!/usr/bin/env python
"""
Script pour déboguer les patterns regex
"""

import re

def test_patterns():
    # Lignes de test du PDF Attijari
    test_lines = [
        "04 08 COMMISSION ENC CHQ 0146467 01 08 2025 0,893",
        "04 08 VERSEMENT ESPECE 091936 05 08 2025 1 640,000",
        "05 08 STE EXTRA PRIX 19 AV H 01 08 2025 6,000",
        "05 08 ENCAISSEMENT CHEQUE 146467 06 08 2025 300,000",
        "SOLDE 1 477,110",
        "TOTAUX 1 704,9 0 3 3 182,013",
        "DONT TVA: 0,570"
    ]
    
    # Pattern actuel
    pattern = r'^\d{2}\s+\d{2}\s+.+\s+\d{2}\s+\d{2}\s+\d{4}\s+[\d\s,]+$'
    
    print("🧪 Test des patterns regex")
    print("=" * 50)
    
    for i, line in enumerate(test_lines, 1):
        match = re.match(pattern, line.strip())
        print(f"{i:2d}. {line}")
        print(f"    Match: {'✅' if match else '❌'}")
        
        if match:
            print(f"    Groups: {match.groups()}")
        print()

if __name__ == "__main__":
    test_patterns()
