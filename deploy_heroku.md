# 🚀 Guide de déploiement Heroku pour BankToCSV

## Prérequis
1. Compte GitHub
2. Compte Heroku (gratuit)
3. Heroku CLI installé

## Étapes de déploiement

### 1. Installer Heroku CLI
```bash
# Windows (avec Chocolatey)
choco install heroku-cli

# Ou télécharger depuis https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Se connecter à Heroku
```bash
heroku login
```

### 3. Créer une application Heroku
```bash
heroku create banktocsv-app
# Remplacez "banktocsv-app" par le nom de votre choix
```

### 4. Ajouter la base de données PostgreSQL
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 5. Configurer les variables d'environnement
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="votre-secret-key-securise"
```

### 6. Initialiser Git (si pas déjà fait)
```bash
git init
git add .
git commit -m "Initial commit"
```

### 7. Ajouter le remote Heroku
```bash
heroku git:remote -a banktocsv-app
```

### 8. Déployer
```bash
git push heroku main
```

### 9. Exécuter les migrations
```bash
heroku run python manage.py migrate
```

### 10. Créer un superutilisateur
```bash
heroku run python manage.py createsuperuser
```

### 11. Ouvrir l'application
```bash
heroku open
```

## Commandes utiles

### Voir les logs
```bash
heroku logs --tail
```

### Accéder au shell
```bash
heroku run python manage.py shell
```

### Redémarrer l'application
```bash
heroku restart
```

### Voir les variables d'environnement
```bash
heroku config
```

## URL de votre application
Votre application sera accessible à : `https://banktocsv-app.herokuapp.com`

## Notes importantes
- Les fichiers uploadés (PDF) ne sont pas persistants sur Heroku
- Pour la production, utilisez un service de stockage comme AWS S3
- La base de données PostgreSQL est gratuite jusqu'à 10,000 lignes
