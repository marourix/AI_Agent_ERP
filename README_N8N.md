# Atracio ERP Agent - Workflow N8N

Ce document explique comment utiliser le workflow n8n pour automatiser les interactions avec votre agent chatbot Atracio ERP.

## 🚀 Installation et Configuration

### Prérequis
- n8n installé et configuré
- Votre serveur ERP Atracio en cours d'exécution sur `http://localhost:5000`
- L'agent Atracio configuré et fonctionnel

### Import du Workflow
1. Ouvrez votre instance n8n
2. Allez dans "Workflows" → "Import from file"
3. Sélectionnez le fichier `atracio_n8n_workflow.json`
4. Cliquez sur "Import"

## 📋 Structure du Workflow

Le workflow se compose des éléments suivants :

### 1. Webhook Trigger
- **URL**: `/atracio-webhook`
- **Méthode**: POST
- **Déclencheur principal** du workflow

### 2. Validation des Entrées
- Vérifie que les données requises sont présentes
- Valide le format des paramètres selon l'action

### 3. Conditions de Routage
- `check_stock` - Vérifier le niveau de stock
- `create_purchase_order` - Créer un bon de commande
- `check_order_status` - Vérifier le statut d'une commande
- `get_all_stock` - Obtenir tous les stocks
- `get_all_orders` - Obtenir toutes les commandes
- `get_all_purchase_orders` - Obtenir tous les bons de commande

### 4. Appels API
- Chaque condition déclenche l'appel approprié à votre serveur ERP
- Utilise les endpoints définis dans `erp_server.py`

### 5. Formatage des Réponses
- Chaque réponse API est formatée pour une meilleure lisibilité
- Gestion des erreurs et des cas d'échec

### 6. Réponse Finale
- Consolidation de toutes les réponses
- Retour au client via le webhook

## 🔧 Utilisation

### Format des Requêtes

#### Vérifier le Stock
```json
{
  "action": "check_stock",
  "sku": "SKU123"
}
```

#### Créer un Bon de Commande
```json
{
  "action": "create_purchase_order",
  "sku": "SKU456",
  "quantity": 50
}
```

#### Vérifier le Statut d'une Commande
```json
{
  "action": "check_order_status",
  "order_id": "ORD001"
}
```

#### Obtenir Tous les Stocks
```json
{
  "action": "get_all_stock"
}
```

#### Obtenir Toutes les Commandes
```json
{
  "action": "get_all_orders"
}
```

#### Obtenir Tous les Bons de Commande
```json
{
  "action": "get_all_purchase_orders"
}
```

### Exemples d'Utilisation

#### cURL
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

#### JavaScript/Node.js
```javascript
const response = await fetch('http://localhost:5678/webhook/atracio-webhook', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    action: 'check_stock',
    sku: 'SKU123'
  })
});

const result = await response.json();
console.log(result);
```

#### Python
```python
import requests

response = requests.post(
    'http://localhost:5678/webhook/atracio-webhook',
    json={
        'action': 'check_stock',
        'sku': 'SKU123'
    }
)

result = response.json()
print(result)
```

## 🔄 Intégrations Possibles

### 1. Slack
- Créer un bot Slack qui utilise le webhook
- Permettre aux utilisateurs de vérifier le stock via des commandes Slack

### 2. Discord
- Intégration avec un bot Discord
- Commandes vocales ou textuelles

### 3. Microsoft Teams
- Webhook Teams pour les notifications
- Intégration avec les canaux de l'équipe

### 4. Email
- Déclenchement automatique par email
- Notifications de stock bas

### 5. Planification
- Vérifications automatiques quotidiennes du stock
- Rapports hebdomadaires des commandes

## 🛠️ Personnalisation

### Ajouter de Nouvelles Actions
1. Créer une nouvelle condition dans le workflow
2. Ajouter l'appel API correspondant
3. Créer le nœud de formatage de réponse
4. Connecter au nœud de réponse finale

### Modifier les Endpoints
- Mettre à jour les URLs dans les nœuds HTTP Request
- Adapter les paramètres selon votre API

### Ajouter de la Logique Métier
- Utiliser les nœuds Code pour des calculs complexes
- Intégrer des bases de données externes
- Ajouter des validations métier

## 📊 Monitoring et Logs

### Logs n8n
- Toutes les exécutions sont loggées dans n8n
- Possibilité de voir les données d'entrée/sortie
- Debugging facile des erreurs

### Métriques
- Nombre d'exécutions par action
- Temps de réponse
- Taux de succès/échec

## 🚨 Gestion des Erreurs

Le workflow gère automatiquement :
- **Erreurs de validation** : Paramètres manquants ou invalides
- **Erreurs API** : Problèmes de connexion au serveur ERP
- **Erreurs de formatage** : Problèmes dans le traitement des données

### Codes d'Erreur
- `400` : Paramètres invalides
- `404` : Ressource non trouvée
- `500` : Erreur serveur interne

## 🔐 Sécurité

### Recommandations
- Utiliser HTTPS en production
- Implémenter une authentification (API keys, JWT)
- Limiter l'accès aux webhooks
- Valider toutes les entrées

### Variables d'Environnement
```bash
# Dans n8n
ERP_API_URL=http://localhost:5000
WEBHOOK_SECRET=your-secret-key
```

## 📈 Évolutions Futures

### Fonctionnalités à Ajouter
- [ ] Authentification et autorisation
- [ ] Rate limiting
- [ ] Cache Redis pour les requêtes fréquentes
- [ ] Notifications push
- [ ] Intégration avec des ERP externes
- [ ] Dashboard de monitoring
- [ ] Rapports automatisés

### Intégrations Avancées
- [ ] SAP
- [ ] Oracle ERP
- [ ] Microsoft Dynamics
- [ ] Salesforce
- [ ] HubSpot

## 🆘 Support et Dépannage

### Problèmes Courants

#### Le webhook ne répond pas
- Vérifier que n8n est en cours d'exécution
- Contrôler les logs n8n
- Vérifier l'URL du webhook

#### Erreurs de connexion à l'API ERP
- S'assurer que `erp_server.py` est en cours d'exécution
- Vérifier l'URL dans les nœuds HTTP Request
- Contrôler les logs du serveur ERP

#### Réponses vides ou incorrectes
- Vérifier le format des données d'entrée
- Contrôler les nœuds de formatage
- Tester les endpoints API individuellement

### Ressources Utiles
- [Documentation n8n](https://docs.n8n.io/)
- [Documentation Flask](https://flask.palletsprojects.com/)
- [GitHub n8n](https://github.com/n8n-io/n8n)

## 📝 Licence

Ce workflow est fourni sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer selon vos besoins.

