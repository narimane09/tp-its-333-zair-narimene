#!/usr/bin/env python3
"""
Script de test pour les services microservices
Teste tous les endpoints Person et Health avec authentication JWT
"""

import requests
import json
from time import sleep

# URLs des services
PERSON_SERVICE = "http://localhost:5001"
HEALTH_SERVICE = "http://localhost:5002"

# Couleurs pour l'affichage
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_test(message):
    print(f"{BLUE}{'='*60}")
    print(f"TEST: {message}")
    print(f"{'='*60}{RESET}")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{YELLOW}ℹ {message}{RESET}")

# 1. Authentification - Obtenir un token JWT
print_test("1. AUTHENTICATION - Obtenir un token JWT")
try:
    auth_response = requests.post(
        f"{PERSON_SERVICE}/auth/login",
        json={"username": "test_user"},
        timeout=5
    )
    if auth_response.status_code == 200:
        token = auth_response.json()['access_token']
        print_success(f"Token obtenu: {token[:30]}...")
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print_error(f"Erreur: {auth_response.status_code}")
        exit(1)
except Exception as e:
    print_error(f"Impossible de se connecter: {e}")
    exit(1)

# 2. Service PERSONNE - Créer une personne
print_test("2. SERVICE PERSONNE - Créer une personne")
try:
    person_data = {"name": "Jean Dupont"}
    response = requests.post(
        f"{PERSON_SERVICE}/persons",
        json=person_data,
        headers=headers,
        timeout=5
    )
    if response.status_code == 201:
        person = response.json()
        person_id = person['id']
        print_success(f"Personne créée: ID={person_id}, Name={person['name']}")
    else:
        print_error(f"Erreur: {response.status_code} - {response.text}")
        exit(1)
except Exception as e:
    print_error(f"Erreur de connexion: {e}")
    exit(1)

# 3. Service PERSONNE - Récupérer une personne
print_test("3. SERVICE PERSONNE - Récupérer une personne")
try:
    response = requests.get(
        f"{PERSON_SERVICE}/persons/{person_id}",
        timeout=5
    )
    if response.status_code == 200:
        person = response.json()
        print_success(f"Personne récupérée: {person}")
    else:
        print_error(f"Erreur: {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 4. Service PERSONNE - Tester une personne inexistante
print_test("4. SERVICE PERSONNE - Tester une personne inexistante (404)")
try:
    response = requests.get(
        f"{PERSON_SERVICE}/persons/9999",
        timeout=5
    )
    if response.status_code == 404:
        print_success(f"Correctly returned 404 for non-existent person")
    else:
        print_error(f"Expected 404, got {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# Attendre un peu avant de tester le service santé
print_info("Attendre que les services se synchronisent...")
sleep(1)

# 5. Service SANTE - Ajouter des données de santé (POST)
print_test("5. SERVICE SANTE - Ajouter des données de santé (POST)")
try:
    health_data = {
        "poids": 75.5,
        "taille": 180,
        "frequence_cardiaque": 72,
        "tension": "120/80"
    }
    response = requests.post(
        f"{HEALTH_SERVICE}/health/{person_id}",
        json=health_data,
        headers=headers,
        timeout=5
    )
    if response.status_code == 200:
        result = response.json()
        print_success(f"Données de santé ajoutées: {result['data']}")
    else:
        print_error(f"Erreur: {response.status_code} - {response.text}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 6. Service SANTE - Lire les données de santé (GET)
print_test("6. SERVICE SANTE - Lire les données de santé (GET)")
try:
    response = requests.get(
        f"{HEALTH_SERVICE}/health/{person_id}",
        headers=headers,
        timeout=5
    )
    if response.status_code == 200:
        health_data = response.json()
        print_success(f"Données de santé lues: {health_data}")
    else:
        print_error(f"Erreur: {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 7. Service SANTE - Ajouter plus de données (POST - ajout)
print_test("7. SERVICE SANTE - Ajouter plus de données (POST - ajout)")
try:
    more_health_data = {"glucose": 100}
    response = requests.post(
        f"{HEALTH_SERVICE}/health/{person_id}",
        json=more_health_data,
        headers=headers,
        timeout=5
    )
    if response.status_code == 200:
        result = response.json()
        print_success(f"Données ajoutées: {result['data']}")
    else:
        print_error(f"Erreur: {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 8. Service SANTE - Modifier les données (PUT - remplacement)
print_test("8. SERVICE SANTE - Modifier les données (PUT - remplacement)")
try:
    new_health_data = {
        "poids": 76.0,
        "taille": 180,
        "frequence_cardiaque": 70
    }
    response = requests.put(
        f"{HEALTH_SERVICE}/health/{person_id}",
        json=new_health_data,
        headers=headers,
        timeout=5
    )
    if response.status_code == 200:
        result = response.json()
        print_success(f"Données modifiées: {result['data']}")
    else:
        print_error(f"Erreur: {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 9. Service SANTE - Tester avec une personne inexistante
print_test("9. SERVICE SANTE - Tester avec personne inexistante (404)")
try:
    response = requests.get(
        f"{HEALTH_SERVICE}/health/9999",
        headers=headers,
        timeout=5
    )
    if response.status_code == 404:
        print_success(f"Correctly returned 404 for non-existent person")
    else:
        print_error(f"Expected 404, got {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 10. Service SANTE - Supprimer les données (DELETE)
print_test("10. SERVICE SANTE - Supprimer les données (DELETE)")
try:
    response = requests.delete(
        f"{HEALTH_SERVICE}/health/{person_id}",
        headers=headers,
        timeout=5
    )
    if response.status_code == 200:
        print_success(f"Données de santé supprimées")
    else:
        print_error(f"Erreur: {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 11. Service SANTE - Vérifier que les données sont supprimées
print_test("11. SERVICE SANTE - Vérifier suppression")
try:
    response = requests.get(
        f"{HEALTH_SERVICE}/health/{person_id}",
        headers=headers,
        timeout=5
    )
    if response.status_code == 200:
        health_data = response.json()
        if not health_data:
            print_success(f"Données correctement supprimées: {health_data}")
        else:
            print_error(f"Les données n'ont pas été supprimées: {health_data}")
    else:
        print_error(f"Erreur: {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 12. Service PERSONNE - Supprimer la personne
print_test("12. SERVICE PERSONNE - Supprimer la personne")
try:
    response = requests.delete(
        f"{PERSON_SERVICE}/persons/{person_id}",
        headers=headers,
        timeout=5
    )
    if response.status_code == 200:
        print_success(f"Personne supprimée")
    else:
        print_error(f"Erreur: {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

# 13. Service SANTE - Tester après suppression de la personne
print_test("13. SERVICE SANTE - Tester après suppression (404)")
try:
    response = requests.get(
        f"{HEALTH_SERVICE}/health/{person_id}",
        headers=headers,
        timeout=5
    )
    if response.status_code == 404:
        print_success(f"Correctly returned 404 after person deletion")
    else:
        print_error(f"Expected 404, got {response.status_code}")
except Exception as e:
    print_error(f"Erreur: {e}")

print(f"\n{GREEN}{'='*60}")
print("TOUS LES TESTS SONT TERMINÉS!")
print(f"{'='*60}{RESET}\n")
