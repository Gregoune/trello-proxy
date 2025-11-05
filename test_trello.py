#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

print(f"Testing Trello API with key: {TRELLO_KEY[:8]}...")

# Test simple: récupérer les boards de l'utilisateur
url = "https://api.trello.com/1/members/me/boards"
params = {
    "key": TRELLO_KEY,
    "token": TRELLO_TOKEN
}

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        boards = response.json()
        print(f"✅ Connexion réussie ! Vous avez {len(boards)} boards.")
        
        if boards:
            print("\nVos boards Trello:")
            for board in boards[:3]:  # Affiche les 3 premiers
                print(f"  - {board['name']} (ID: {board['id']})")
        else:
            print("Aucun board trouvé.")
    else:
        print(f"❌ Erreur: {response.text}")
        
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")