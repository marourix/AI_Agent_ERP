# 🚀 Déploiement Rapide - Atracio ERP Agent avec n8n

## 📋 Résumé du Projet

Votre agent chatbot Atracio ERP est maintenant configuré pour fonctionner avec **n8n**, une plateforme d'automatisation puissante. Cela vous permet de :

- ✅ **Automatiser** toutes les interactions avec votre ERP
- ✅ **Intégrer** avec d'autres plateformes (Slack, Discord, Teams, etc.)
- ✅ **Planifier** des tâches récurrentes
- ✅ **Monitorer** les performances et les erreurs
- ✅ **Évoluer** facilement avec de nouvelles fonctionnalités

## 🎯 Démarrage en 5 Minutes

### 1. **Démarrage Automatique (Recommandé)**
```bash
# Sur Windows
start_n8n.bat

# Sur Linux/Mac
chmod +x deploy.sh
./deploy.sh
```

### 2. **Démarrage Manuel**
```bash
# Démarrer les services
docker-compose up -d

# Attendre que les services soient prêts
# Ouvrir http://localhost:5678 dans votre navigateur
# Login: admin / atracio123
```

## 📁 Fichiers Créés

| Fichier | Description |
|---------|-------------|
| `atracio_n8n_workflow.json` | **Workflow n8n principal** - À importer dans n8n |
| `docker-compose.yml` | Configuration Docker pour tous les services |
| `README_N8N.md` | **Documentation complète** du workflow |
| `test_n8n_workflow.py` | Script de test Python pour vérifier le fonctionnement |
| `deploy.sh` | Script de déploiement Linux/Mac |
| `start_n8n.bat` | Script de démarrage Windows |
| `env.example` | Variables d'environnement n8n |

## 🔧 Actions Disponibles

Votre workflow n8n gère automatiquement :

| Action | Description | Exemple |
|--------|-------------|---------|
| `check_stock` | Vérifier le niveau de stock d'un SKU | `{"action": "check_stock", "sku": "SKU123"}`
| `create_purchase_order` | Créer un bon de commande | `{"action": "create_purchase_order", "sku": "SKU456", "quantity": 50}`
| `check_order_status` | Vérifier le statut d'une commande | `{"action": "check_order_status", "order_id": "ORD001"}`
| `get_all_stock` | Obtenir tous les stocks | `{"action": "get_all_stock"}`
| `get_all_orders` | Obtenir toutes les commandes | `{"action": "get_all_orders"}`
| `get_all_purchase_orders` | Obtenir tous les bons de commande | `{"action": "get_all_purchase_orders"}`

## 🌐 Accès aux Services

| Service | URL | Identifiants |
|---------|-----|--------------|
| **n8n** | http://localhost:5678 | `admin` / `atracio123` |
| **API ERP** | http://localhost:5000 | Aucun (API publique) |
| **PostgreSQL** | localhost:5432 | `n8n` / `atracio123` |

## 🧪 Test Rapide

### Test avec cURL
```bash
# Vérifier le stock
curl -X POST http://localhost:5678/webhook/atracio-webhook \
  -H "Content-Type: application/json" \
  -d '{"action": "check_stock", "sku": "SKU123"}'

# Créer un bon de commande
curl -X POST http://localhost:5678/webhook/atracio-webhook \
  -H "Content-Type: application/json" \
  -d '{"action": "create_purchase_order", "sku": "SKU456", "quantity": 100}'
```

### Test avec Python
```bash
python test_n8n_workflow.py
```

## 🔄 Intégrations Possibles

### Plateformes de Communication
- **Slack** : Bot pour vérifier le stock via commandes
- **Discord** : Intégration avec serveurs d'équipe
- **Microsoft Teams** : Webhooks pour notifications
- **Email** : Rapports automatiques quotidiens

### Planification
- **Vérifications quotidiennes** du stock
- **Rapports hebdomadaires** des commandes
- **Alertes automatiques** de stock bas
- **Synchronisation** avec calendriers

### Systèmes Externes
- **SAP**, **Oracle ERP**, **Microsoft Dynamics**
- **Salesforce**, **HubSpot**
- **Bases de données** externes
- **APIs** tierces

## 🚨 Dépannage Rapide

### Problème : n8n ne démarre pas
```bash
# Vérifier les logs
docker-compose logs n8n

# Redémarrer
docker-compose restart n8n
```

### Problème : API ERP ne répond pas
```bash
# Vérifier que le serveur ERP fonctionne
python erp_server.py

# Tester l'API
curl http://localhost:5000/Atracio
```

### Problème : Webhook ne fonctionne pas
1. Vérifier que le workflow est **activé** dans n8n
2. Contrôler que l'URL du webhook est correcte
3. Vérifier les logs d'exécution dans n8n

## 📈 Prochaines Étapes

### Phase 1 : Mise en Production
- [ ] Configurer HTTPS avec certificats SSL
- [ ] Implémenter l'authentification JWT
- [ ] Ajouter le rate limiting
- [ ] Configurer les sauvegardes automatiques

### Phase 2 : Évolutions
- [ ] Dashboard de monitoring
- [ ] Notifications push
- [ ] Intégration avec ERP externes
- [ ] Rapports avancés

### Phase 3 : Intelligence Artificielle
- [ ] Prédiction de la demande
- [ ] Optimisation automatique des stocks
- [ ] Analyse prédictive des commandes
- [ ] Chatbot intelligent

## 📞 Support

- **Documentation complète** : `README_N8N.md`
- **Scripts de test** : `test_n8n_workflow.py`
- **Logs en temps réel** : `docker-compose logs -f`
- **Interface web** : http://localhost:5678

## 🎉 Félicitations !

Votre agent Atracio est maintenant **beaucoup plus puissant** avec n8n ! Vous pouvez :

- Automatiser toutes vos tâches ERP
- Intégrer avec vos outils existants
- Créer des workflows complexes
- Monitorer et optimiser vos processus

**Bon déploiement ! 🚀**

