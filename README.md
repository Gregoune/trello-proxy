# Trello Proxy API

Un proxy Flask simple pour l'API Trello qui permet de créer des cartes et récupérer des listes via des requêtes HTTP.

## Fonctionnalités

- ✅ Créer des cartes Trello via POST JSON
- ✅ Récupérer les listes d'un board
- ✅ Gestion des erreurs et validation
- ✅ Support des variables d'environnement

## Endpoints

### `GET /`
Retourne le statut du service.

### `POST /trello`
Crée une nouvelle carte Trello.

**Body JSON requis :**
```json
{
  "idList": "id_de_la_liste_trello",
  "name": "Titre de la carte",
  "desc": "Description optionnelle"
}
```

### `GET /lists/<board_id>`
Récupère toutes les listes d'un board Trello.

## Configuration

Créez un fichier `.env` avec vos clés Trello :

```env
TRELLO_KEY=votre_clé_api_trello
TRELLO_TOKEN=votre_token_trello
```

Obtenez vos clés sur : https://trello.com/app-key

## Installation locale

```bash
pip install -r requirements.txt
python main.py
```

Le serveur sera accessible sur http://localhost:3000

## Déploiement

### Render
1. Connectez votre repo GitHub à Render
2. Ajoutez les variables d'environnement `TRELLO_KEY` et `TRELLO_TOKEN`
3. Déployez avec le fichier `render.yaml` inclus

### Railway
1. Connectez votre repo à Railway
2. Ajoutez les variables d'environnement
3. Railway utilise automatiquement le `Procfile`

### Vercel
```bash
vercel secrets add trello_key "votre_clé"
vercel secrets add trello_token "votre_token"
vercel --prod
```

## Exemple d'utilisation

```bash
# Créer une carte
curl -X POST https://votre-app.render.com/trello \
  -H "Content-Type: application/json" \
  -d '{"idList": "abc123", "name": "Ma tâche", "desc": "Description"}'

# Lister les boards
curl https://votre-app.render.com/lists/board_id
```