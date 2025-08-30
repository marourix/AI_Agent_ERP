@echo off
chcp 65001 >nul
title Atracio ERP Agent - N8N Launcher

echo.
echo ========================================
echo    Atracio ERP Agent - N8N Launcher
echo ========================================
echo.

:: Vérifier si Docker est installé
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker n'est pas installé ou n'est pas en cours d'exécution.
    echo Veuillez installer Docker Desktop et le démarrer.
    echo.
    pause
    exit /b 1
)

:: Vérifier si Docker Compose est installé
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose n'est pas installé.
    echo Veuillez l'installer ou mettre à jour Docker Desktop.
    echo.
    pause
    exit /b 1
)

echo ✅ Docker et Docker Compose détectés
echo.

:: Vérifier si les fichiers nécessaires existent
if not exist "docker-compose.yml" (
    echo ❌ Fichier docker-compose.yml non trouvé.
    echo Assurez-vous d'être dans le bon répertoire.
    echo.
    pause
    exit /b 1
)

if not exist "atracio_n8n_workflow.json" (
    echo ❌ Fichier atracio_n8n_workflow.json non trouvé.
    echo Assurez-vous d'être dans le bon répertoire.
    echo.
    pause
    exit /b 1
)

echo ✅ Fichiers de configuration trouvés
echo.

:: Menu principal
:menu
echo 📋 Menu de démarrage:
echo.
echo 1. 🚀 Démarrer tous les services
echo 2. 🛑 Arrêter tous les services
echo 3. 🔄 Redémarrer les services
echo 4. 📊 Voir les logs
echo 5. 🧪 Tester les services
echo 6. 🌐 Ouvrir n8n dans le navigateur
echo 7. 📚 Afficher l'aide
echo 8. ❌ Quitter
echo.

set /p choice="Sélectionnez une option (1-8): "

if "%choice%"=="1" goto start_services
if "%choice%"=="2" goto stop_services
if "%choice%"=="3" goto restart_services
if "%choice%"=="4" goto show_logs
if "%choice%"=="5" goto test_services
if "%choice%"=="6" goto open_n8n
if "%choice%"=="7" goto show_help
if "%choice%"=="8" goto exit
goto invalid_choice

:start_services
echo.
echo 🚀 Démarrage des services Atracio...
echo.
docker-compose up -d
if %errorlevel% equ 0 (
    echo.
    echo ✅ Services démarrés avec succès !
    echo.
    echo 📱 Accès aux services:
    echo    n8n: http://localhost:5678 (admin/atracio123)
    echo    API ERP: http://localhost:5000
    echo.
    echo ⏳ Attente que les services soient prêts...
    timeout /t 30 /nobreak >nul
    
    echo.
    echo 🎯 Services prêts ! Vous pouvez maintenant:
    echo    1. Ouvrir n8n dans votre navigateur
    echo    2. Importer le workflow atracio_n8n_workflow.json
    echo    3. Tester avec le script test_n8n_workflow.py
    echo.
) else (
    echo.
    echo ❌ Erreur lors du démarrage des services.
    echo Vérifiez les logs avec: docker-compose logs
    echo.
)
pause
goto menu

:stop_services
echo.
echo 🛑 Arrêt des services...
docker-compose down
if %errorlevel% equ 0 (
    echo ✅ Services arrêtés avec succès !
) else (
    echo ❌ Erreur lors de l'arrêt des services.
)
echo.
pause
goto menu

:restart_services
echo.
echo 🔄 Redémarrage des services...
docker-compose restart
if %errorlevel% equ 0 (
    echo ✅ Services redémarrés avec succès !
) else (
    echo ❌ Erreur lors du redémarrage des services.
)
echo.
pause
goto menu

:show_logs
echo.
echo 📊 Affichage des logs...
echo Appuyez sur Ctrl+C pour arrêter l'affichage des logs
echo.
docker-compose logs -f
goto menu

:test_services
echo.
echo 🧪 Test des services...
echo.

:: Test n8n
echo 🔍 Test de n8n...
curl -s http://localhost:5678/healthz >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ n8n fonctionne correctement
) else (
    echo ❌ n8n ne répond pas
)

:: Test API ERP
echo 🔍 Test de l'API ERP...
curl -s http://localhost:5000/Atracio >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ API ERP fonctionne correctement
) else (
    echo ❌ API ERP ne répond pas
)

echo.
echo 🎯 Tests terminés !
echo.
pause
goto menu

:open_n8n
echo.
echo 🌐 Ouverture de n8n dans le navigateur...
start http://localhost:5678
echo ✅ n8n ouvert dans le navigateur
echo.
pause
goto menu

:show_help
echo.
echo 📚 Aide - Atracio ERP Agent avec n8n
echo ======================================
echo.
echo 🚀 DÉMARRAGE RAPIDE:
echo    1. Sélectionnez l'option 1 pour démarrer tous les services
echo    2. Attendez que les services soient prêts (environ 30 secondes)
echo    3. Ouvrez n8n dans votre navigateur (option 6)
echo    4. Connectez-vous avec admin/atracio123
echo    5. Importez le workflow atracio_n8n_workflow.json
echo.
echo 📁 FICHIERS IMPORTANTS:
echo    - atracio_n8n_workflow.json : Workflow n8n principal
echo    - docker-compose.yml : Configuration des services
echo    - README_N8N.md : Documentation complète
echo    - test_n8n_workflow.py : Script de test Python
echo.
echo 🔧 COMMANDES UTILES:
echo    - docker-compose up -d : Démarrer les services
echo    - docker-compose down : Arrêter les services
echo    - docker-compose logs -f : Voir les logs en temps réel
echo.
echo 🌐 PORTS UTILISÉS:
echo    - 5678 : n8n
echo    - 5000 : API ERP Atracio
echo    - 5432 : PostgreSQL
echo.
echo 📞 SUPPORT:
echo    Consultez README_N8N.md pour la documentation complète
echo.
pause
goto menu

:invalid_choice
echo.
echo ❌ Choix invalide. Veuillez sélectionner une option entre 1 et 8.
echo.
pause
goto menu

:exit
echo.
echo 👋 Au revoir !
echo.
exit /b 0

