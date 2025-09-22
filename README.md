# BankToCSV - Convertisseur de Relevés Bancaires Attijari

Un MVP Django pour convertir automatiquement les relevés bancaires PDF d'Attijari Tunisie en fichiers CSV ou Excel.

## 🚀 Fonctionnalités

- **Interface unifiée** : Une seule page pour tout faire - upload, conversion et téléchargement
- **Upload simplifié** : Glisser-déposer ou sélection de fichier PDF
- **Extraction automatique** : Utilise pdfplumber pour extraire les données des PDF natifs
- **Colonnes extraites** :
  - Date opération
  - Date valeur
  - Libellé
  - Débit
  - Crédit
  - Solde final
- **Export multiple** : CSV et Excel (.xlsx) en un clic
- **Interface moderne** : Bootstrap 5 avec design responsive et animations
- **Expérience fluide** : Traitement en temps réel sans rechargement de page

## 📋 Prérequis

- Python 3.8+
- Django 5.2.6
- pdfplumber
- pandas
- openpyxl
- Pillow

## 🛠️ Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd banktocsv
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Créer un superutilisateur (optionnel)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application**
   Ouvrir http://127.0.0.1:8000 dans votre navigateur

## 📁 Structure du projet

```
banktocsv/
├── banktocsv/                 # Application Django principale
│   ├── models.py              # Modèles BankStatement et Transaction
│   ├── views.py               # Vues pour upload, traitement, export
│   ├── forms.py               # Formulaires d'upload et d'export
│   ├── urls.py                # URLs de l'application
│   └── templates/             # Templates HTML
│       └── banktocsv/
│           ├── base.html      # Template de base
│           ├── index.html     # Page d'accueil
│           ├── upload.html    # Page d'upload
│           ├── statement_detail.html  # Détail du relevé
│           └── export.html    # Page d'export
├── parsers/                   # Parsers pour différents formats
│   ├── __init__.py
│   └── attijari_parser.py     # Parser spécialisé Attijari
├── banktocsv_project/         # Configuration Django
│   ├── settings.py
│   └── urls.py
├── media/                     # Fichiers uploadés (créé automatiquement)
├── requirements.txt           # Dépendances Python
└── manage.py
```

## 🔧 Utilisation

### Expérience simplifiée - Une seule page !

1. **Accéder à l'application** : Ouvrir http://127.0.0.1:8000
2. **Upload du PDF** : 
   - Glisser-déposer votre relevé PDF Attijari
   - Ou cliquer pour sélectionner un fichier
3. **Conversion automatique** : 
   - Cliquer sur "Convertir en CSV/Excel"
   - Le système traite automatiquement le fichier
4. **Téléchargement** : 
   - Voir l'aperçu des transactions extraites
   - Télécharger en CSV ou Excel en un clic
   - Option "Nouveau fichier" pour traiter un autre relevé

**C'est tout !** Plus besoin de naviguer entre différentes pages.

## 🎯 Format PDF supporté

Le système est optimisé pour les relevés bancaires Attijari avec la structure suivante :

```
Date Opération | Date Valeur | Libellé | Débit | Crédit
01/01/2024     | 01/01/2024  | Virement| 0.00  | 1000.00
02/01/2024     | 02/01/2024  | Retrait | 50.00 | 0.00
...
Solde final: 950.00 TND
```

## ⚠️ Limitations

- **PDF natifs uniquement** : Les PDF scannés (images) ne sont pas supportés
- **Format Attijari** : Optimisé pour la structure standard Attijari
- **Taille limitée** : Maximum 10MB par fichier
- **Développement** : Version MVP, non optimisée pour la production

## 🚧 Améliorations futures

- Support d'autres banques tunisiennes
- Interface d'administration Django
- API REST
- Authentification utilisateur
- Historique des exports
- Validation avancée des PDF
- Support des PDF scannés (OCR)
- Mode hors-ligne (PWA)
- Traitement par lots de plusieurs fichiers

## 🐛 Dépannage

### Erreur d'upload
- Vérifier que le fichier est un PDF natif
- Vérifier la taille (max 10MB)
- Vérifier que le format correspond à Attijari

### Erreur d'extraction
- Le PDF doit contenir du texte sélectionnable
- La structure doit correspondre au format Attijari standard
- Vérifier les logs Django pour plus de détails

### Problème de dépendances
```bash
# Réinstaller dans l'environnement virtuel
pip install --upgrade pip
pip install -r requirements.txt
```

## 📝 Notes techniques

- **Parser** : Utilise des expressions régulières pour extraire les données
- **Base de données** : SQLite en développement, facilement migrable vers PostgreSQL
- **Sécurité** : Validation des fichiers, limitation de taille
- **Performance** : Traitement synchrone, idéal pour des volumes modérés

## 📄 Licence

Ce projet est un MVP développé pour des besoins spécifiques. Utilisez selon vos besoins.

## 🤝 Contribution

Ceci est un projet MVP. Pour des améliorations ou corrections, contactez l'équipe de développement.

---

**BankToCSV** - Simplifiez la conversion de vos relevés bancaires ! 🏦📊
