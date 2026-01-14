# Microservices - Gestion des Personnes et Santé

## 📋 Architecture

Le projet contient deux microservices Flask:

- **Service Personne** (port 5001): Gère les personnes (CRUD minimal)
- **Service Santé** (port 5002): Gère les données de santé des personnes

Les deux services sont sécurisés avec **JWT (JSON Web Token)**.

## 🚀 Démarrage rapide

### Prérequis

- Docker et Docker Compose installés
- Python 3.9+ (pour le script de test local)

### 1. Lancer les services avec Docker Compose

```bash
cd /path/to/TP_Microservices_Mini_Projet.md
docker-compose up --build
```

Les services démarreront sur:
- Service Personne: http://localhost:5001
- Service Santé: http://localhost:5002

### 2. Tester les API (depuis un autre terminal)

```bash
cd /path/to/TP_Microservices_Mini_Projet.md
python test_api.py
```

## 🔐 Authentification

Tous les endpoints (sauf `/auth/login` et GET `/persons/{id}`) requièrent un token JWT.

### Obtenir un token

```bash
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user123"}'
```

**Réponse:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Utilisez ce token dans l'en-tête `Authorization: Bearer <token>` pour tous les autres appels.

## 📌 Endpoints - Service Personne

### POST /auth/login
Obtenir un token JWT.

**Request:**
```json
{
  "username": "user123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### POST /persons
Créer une nouvelle personne (nécessite JWT).

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Jean Dupont"
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Jean Dupont"
}
```

### GET /persons/{id}
Récupérer les informations d'une personne (pas d'authentification, pour permettre au service santé de vérifier).

**Response (200):**
```json
{
  "id": 1,
  "name": "Jean Dupont"
}
```

**Response (404):**
```json
{
  "error": "Not found"
}
```

### DELETE /persons/{id}
Supprimer une personne (nécessite JWT).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "message": "Deleted"
}
```

## 📊 Endpoints - Service Santé

**Note:** Le service santé vérifie automatiquement que la personne existe avant chaque opération.

### GET /health/{person_id}
Lire les données de santé d'une personne.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "poids": 75.5,
  "taille": 180,
  "frequence_cardiaque": 72,
  "tension": "120/80"
}
```

**Response (404):** Si la personne n'existe pas.

### POST /health/{person_id}
Ajouter des données de santé (ajoute aux données existantes).

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request:**
```json
{
  "poids": 75.5,
  "taille": 180,
  "frequence_cardiaque": 72,
  "tension": "120/80"
}
```

**Response (200):**
```json
{
  "status": "Success",
  "data": {
    "poids": 75.5,
    "taille": 180,
    "frequence_cardiaque": 72,
    "tension": "120/80"
  }
}
```

### PUT /health/{person_id}
Modifier les données de santé (remplace complètement les données).

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request:**
```json
{
  "poids": 76.0,
  "taille": 180,
  "frequence_cardiaque": 70
}
```

**Response (200):**
```json
{
  "status": "Success",
  "data": {
    "poids": 76.0,
    "taille": 180,
    "frequence_cardiaque": 70
  }
}
```

### DELETE /health/{person_id}
Supprimer les données de santé d'une personne.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "message": "Health data deleted"
}
```

## 🧪 Exemples cURL

### 1. Authentification
```bash
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test"}'
```

### 2. Créer une personne
```bash
TOKEN="votre_token_ici"
curl -X POST http://localhost:5001/persons \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Marie Martin"}'
```

### 3. Récupérer une personne
```bash
curl http://localhost:5001/persons/1
```

### 4. Ajouter données de santé
```bash
TOKEN="votre_token_ici"
curl -X POST http://localhost:5002/health/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "poids": 70,
    "taille": 175,
    "frequence_cardiaque": 75,
    "tension": "118/76"
  }'
```

### 5. Lire données de santé
```bash
TOKEN="votre_token_ici"
curl http://localhost:5002/health/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Modifier données de santé
```bash
TOKEN="votre_token_ici"
curl -X PUT http://localhost:5002/health/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"poids": 72, "taille": 175}'
```

### 7. Supprimer données de santé
```bash
TOKEN="votre_token_ici"
curl -X DELETE http://localhost:5002/health/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 8. Supprimer une personne
```bash
TOKEN="votre_token_ici"
curl -X DELETE http://localhost:5001/persons/1 \
  -H "Authorization: Bearer $TOKEN"
```

## 📁 Structure du projet

```
.
├── docker-compose.yml          # Configuration Docker Compose
├── person-service/
│   ├── app.py                  # Service Personne avec CRUD + JWT
│   ├── requirements.txt         # Dépendances Python
│   ├── Dockerfile              # Image Docker
│   └── database.db             # Base de données SQLite
├── health-service/
│   ├── app.py                  # Service Santé avec vérification
│   ├── requirements.txt         # Dépendances Python
│   └── Dockerfile              # Image Docker
├── test_api.py                 # Script de test automatisé
└── README.md                   # Ce fichier
```

## 🔧 Variables d'environnement

Les deux services acceptent les variables d'environnement suivantes:

- `JWT_SECRET_KEY`: Clé secrète pour signer les tokens JWT
- `PERSON_SERVICE_URL`: URL du service Personne (pour le service Santé)
- `FLASK_ENV`: Environnement Flask (development/production)

Ces variables sont définies dans `docker-compose.yml`.

## ⚠️ Notes importantes

1. **Développement vs Production**: La clé JWT est définie dans docker-compose.yml pour faciliter le développement. En production, utilisez une vraie clé secrète et stockez-la de manière sécurisée.

2. **Base de données**: Le service Personne utilise SQLite. Les données sont persistantes dans le conteneur mais perdues si le conteneur est supprimé. Pour la persistance, utilisez les volumes Docker.

3. **Vérification Inter-services**: Le service Santé appelle le service Personne pour vérifier l'existence d'une personne avant chaque opération. Cela assure l'intégrité des données.

4. **Stockage Santé**: Le service Santé utilise un dictionnaire en mémoire. En production, utilisez une vraie base de données.

## 🛑 Arrêter les services

```bash
docker-compose down
```

Pour supprimer aussi les volumes:
```bash
docker-compose down -v
```

## 📝 Logs

Pour voir les logs des services:

```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f person-service
docker-compose logs -f health-service
```

## ✨ Améliorations futures

- [ ] Utiliser une vraie base de données pour le service Santé
- [ ] Ajouter une base de données PostgreSQL partagée
- [ ] Implémenter la pagination pour les listes
- [ ] Ajouter des validations plus strictes
- [ ] Implémenter un système de cache Redis
- [ ] Ajouter des métriques Prometheus
- [ ] Configurer Nginx comme reverse proxy
