@echo off
echo 🚀 Déploiement de BankToCSV sur Heroku
echo =====================================

echo.
echo 1. Vérification de la configuration...
python manage.py check
if %errorlevel% neq 0 (
    echo ❌ Erreur de configuration Django
    pause
    exit /b 1
)

echo.
echo 2. Collecte des fichiers statiques...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de la collecte des fichiers statiques
    pause
    exit /b 1
)

echo.
echo 3. Ajout des fichiers au Git...
git add .
git commit -m "Deploy to Heroku - $(date)"

echo.
echo 4. Déploiement sur Heroku...
git push heroku main
if %errorlevel% neq 0 (
    echo ❌ Erreur lors du déploiement
    pause
    exit /b 1
)

echo.
echo 5. Exécution des migrations...
heroku run python manage.py migrate

echo.
echo ✅ Déploiement terminé avec succès !
echo.
echo 🌐 Votre application est disponible à :
heroku apps:info --json | findstr "web_url"
echo.
echo 📋 Commandes utiles :
echo   - Voir les logs : heroku logs --tail
echo   - Redémarrer : heroku restart
echo   - Ouvrir l'app : heroku open
echo.
pause
