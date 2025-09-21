# 🚀 Déploiement Heroku SANS CLI - Guide complet

## 📋 Prérequis
- ✅ Compte GitHub (gratuit)
- ✅ Compte Heroku (gratuit)
- ✅ Votre projet est déjà configuré avec Git

## 🎯 Méthode : GitHub + Interface Web Heroku

### **Étape 1 : Créer un dépôt GitHub**

1. **Allez sur GitHub.com** et connectez-vous
2. **Cliquez sur "New repository"**
3. **Nom du dépôt** : `banktocsv-app` (ou votre choix)
4. **Description** : "Bank Statement Converter for Attijari Bank"
5. **Cochez** "Add a README file"
6. **Cliquez** "Create repository"

### **Étape 2 : Pousser votre code sur GitHub**

Dans votre terminal PowerShell :

```bash
# Ajouter le remote GitHub (remplacez VOTRE_USERNAME)
git remote add origin https://github.com/VOTRE_USERNAME/banktocsv-app.git

# Pousser le code
git branch -M main
git push -u origin main
```

### **Étape 3 : Créer l'application Heroku**

1. **Allez sur** https://dashboard.heroku.com
2. **Cliquez** "New" → "Create new app"
3. **Nom de l'app** : `banktocsv-app` (doit être unique)
4. **Région** : United States
5. **Cliquez** "Create app"

### **Étape 4 : Connecter GitHub à Heroku**

1. **Dans votre app Heroku**, allez dans l'onglet **"Deploy"**
2. **Section "Deployment method"** : Cliquez **"GitHub"**
3. **Connectez votre compte GitHub** si demandé
4. **Recherchez votre dépôt** : `banktocsv-app`
5. **Cliquez** "Connect"

### **Étape 5 : Configurer le déploiement automatique**

1. **Section "Automatic deploys"** :
   - ✅ Cochez "Wait for CI to pass before deploy"
   - ✅ Cochez "Enable Automatic Deploys"
2. **Cliquez** "Enable Automatic Deploys"

### **Étape 6 : Ajouter PostgreSQL**

1. **Onglet "Resources"** dans votre app Heroku
2. **Section "Add-ons"** : Tapez `postgres`
3. **Sélectionnez** "Heroku Postgres" (plan gratuit)
4. **Cliquez** "Submit Order Form"

### **Étape 7 : Configurer les variables d'environnement**

1. **Onglet "Settings"** dans votre app Heroku
2. **Section "Config Vars"** : Cliquez "Reveal Config Vars"
3. **Ajoutez ces variables** :

| KEY | VALUE |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | `votre-cle-secrete-securisee` |

**Pour générer une SECRET_KEY sécurisée :**
```python
import secrets
print(secrets.token_urlsafe(50))
```

### **Étape 8 : Déployer manuellement**

1. **Onglet "Deploy"** dans votre app Heroku
2. **Section "Manual deploy"** :
   - **Branch** : `main`
   - **Cliquez** "Deploy Branch"

### **Étape 9 : Exécuter les migrations**

1. **Onglet "More"** → "Run console"
2. **Tapez** : `python manage.py migrate`
3. **Appuyez** sur Entrée

### **Étape 10 : Créer un superutilisateur**

1. **Dans la même console** :
2. **Tapez** : `python manage.py createsuperuser`
3. **Suivez** les instructions

### **Étape 11 : Tester votre application**

1. **Cliquez** "Open app" dans le dashboard Heroku
2. **Votre app** sera accessible à : `https://banktocsv-app.herokuapp.com`

## 🔧 Commandes utiles (via l'interface web)

### **Console Heroku** (More → Run console)
```bash
# Voir les logs
heroku logs --tail

# Migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

### **Redémarrer l'application**
- **Onglet "More"** → "Restart all dynos"

## 📊 Monitoring

### **Voir les logs**
- **Onglet "More"** → "View logs"

### **Métriques**
- **Onglet "Metrics"** pour voir les performances

## 🚨 Dépannage

### **Problème : Application ne démarre pas**
1. **Vérifiez les logs** : More → View logs
2. **Vérifiez les variables d'environnement** : Settings → Config Vars
3. **Redémarrez** : More → Restart all dynos

### **Problème : Erreur de base de données**
1. **Vérifiez que PostgreSQL est ajouté** : Resources
2. **Exécutez les migrations** : Console → `python manage.py migrate`

### **Problème : Fichiers statiques**
1. **Console** : `python manage.py collectstatic --noinput`
2. **Redémarrez** l'application

## 🎉 Félicitations !

Votre application BankToCSV est maintenant en ligne et accessible à :
**https://banktocsv-app.herokuapp.com**

## 📝 Notes importantes

- ✅ **Déploiement automatique** : Chaque push sur GitHub redéploie automatiquement
- ✅ **Base de données persistante** : PostgreSQL Heroku
- ✅ **Logs en temps réel** : Accessibles via l'interface web
- ⚠️ **Fichiers uploadés** : Ne sont pas persistants (redémarrage = perte)
- 💡 **Pour la production** : Utilisez AWS S3 pour le stockage de fichiers

## 🔄 Mises à jour futures

Pour mettre à jour votre application :
1. **Modifiez votre code localement**
2. **Commit et push** sur GitHub :
   ```bash
   git add .
   git commit -m "Update description"
   git push origin main
   ```
3. **Heroku déploie automatiquement** ! 🚀

