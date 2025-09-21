#!/usr/bin/env python3
"""
Script pour générer une SECRET_KEY Django sécurisée
"""

import secrets
import string

def generate_secret_key():
    """Génère une SECRET_KEY Django sécurisée"""
    # Caractères autorisés pour Django SECRET_KEY
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    
    # Génère une clé de 50 caractères
    secret_key = ''.join(secrets.choice(chars) for _ in range(50))
    
    return secret_key

if __name__ == "__main__":
    print("🔐 Génération d'une SECRET_KEY Django sécurisée")
    print("=" * 50)
    
    secret_key = generate_secret_key()
    
    print(f"SECRET_KEY générée :")
    print(f"'{secret_key}'")
    print()
    print("📋 Instructions :")
    print("1. Copiez cette clé")
    print("2. Dans Heroku Dashboard → Settings → Config Vars")
    print("3. Ajoutez : SECRET_KEY = votre_clé_ici")
    print("4. Ou utilisez la commande : heroku config:set SECRET_KEY='votre_clé'")
    print()
    print("⚠️  IMPORTANT : Gardez cette clé secrète et ne la partagez jamais !")

