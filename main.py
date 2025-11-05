# main.py
from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Récupère la clé et le token depuis les variables d'environnement (Replit Secrets)
TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")

if not TRELLO_KEY or not TRELLO_TOKEN:
    app.logger.warning("TRELLO_KEY or TRELLO_TOKEN not set. Set them in Replit Secrets.")

@app.route("/", methods=["GET"])
def hello():
    return "Trello Proxy v1.2 alive. POST JSON to /trello to create card with optional member assignment. GET /members/<board_id> to list members.", 200

@app.route("/trello", methods=["POST"])
def trello_proxy():
    """
    Attendu: JSON body { "idList": "...", "name": "...", "desc": "...", "idMembers": [...] }
    Le proxy envoie un POST application/x-www-form-urlencoded vers Trello.
    idMembers est optionnel et peut être une liste d'IDs de membres ou un seul ID.
    """
    if not TRELLO_KEY or not TRELLO_TOKEN:
        return jsonify({"error": "TRELLO_KEY or TRELLO_TOKEN not configured"}), 500

    data = {}
    # Accept JSON or form
    if request.is_json:
        payload = request.get_json()
    else:
        # fallback to form data
        payload = request.form.to_dict()

    id_list = payload.get("idList") or payload.get("id_list") or payload.get("list_id")
    name = payload.get("name") or payload.get("title")
    desc = payload.get("desc") or payload.get("description") or payload.get("body", "")
    members = payload.get("idMembers") or payload.get("members") or payload.get("assignees", [])

    if not id_list or not name:
        return jsonify({
            "error": "idList and name are required. Example JSON: {\"idList\":\"...\",\"name\":\"Titre\",\"desc\":\"...\",\"idMembers\":[\"member_id1\",\"member_id2\"]}"
        }), 400

    # Build form data expected by Trello
    form = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "idList": id_list,
        "name": name,
        "desc": desc
    }
    
    # Ajouter les membres si spécifiés (optionnel)
    if members:
        # Convertir en liste si c'est une chaîne
        if isinstance(members, str):
            members = [members]
        # Joindre les IDs des membres avec des virgules
        form["idMembers"] = ",".join(members)

    # Call Trello API
    r = requests.post("https://api.trello.com/1/cards", data=form, timeout=15)

    # Relay status + body
    try:
        return jsonify({
            "status_code": r.status_code,
            "trello_response": r.json()
        }), r.status_code
    except ValueError:
        # Non-json response
        return (r.text, r.status_code, {"Content-Type": "text/plain; charset=utf-8"})

@app.route("/lists/<board_id>", methods=["GET"])
def lists_for_board(board_id):
    """Optionnel : obtenir les listes d'un board (GET)"""
    if not TRELLO_KEY or not TRELLO_TOKEN:
        return jsonify({"error": "TRELLO_KEY or TRELLO_TOKEN not configured"}), 500

    r = requests.get(
        f"https://api.trello.com/1/boards/{board_id}/lists",
        params={"key": TRELLO_KEY, "token": TRELLO_TOKEN},
        timeout=15
    )
    try:
        return jsonify(r.json()), r.status_code
    except ValueError:
        return (r.text, r.status_code, {"Content-Type": "text/plain; charset=utf-8"})

@app.route("/members/<board_id>", methods=["GET"])
def members_for_board(board_id):
    """Obtenir les membres d'un board avec leurs IDs (GET)"""
    if not TRELLO_KEY or not TRELLO_TOKEN:
        return jsonify({"error": "TRELLO_KEY or TRELLO_TOKEN not configured"}), 500

    r = requests.get(
        f"https://api.trello.com/1/boards/{board_id}/members",
        params={"key": TRELLO_KEY, "token": TRELLO_TOKEN},
        timeout=15
    )
    try:
        members = r.json()
        # Simplifier la réponse pour ne garder que les infos utiles
        simplified_members = [
            {
                "id": member["id"],
                "username": member["username"],
                "fullName": member["fullName"],
                "initials": member.get("initials", "")
            }
            for member in members
        ]
        return jsonify(simplified_members), r.status_code
    except ValueError:
        return (r.text, r.status_code, {"Content-Type": "text/plain; charset=utf-8"})

if __name__ == "__main__":
    # Support pour déploiement (Render, Heroku, etc.) avec port dynamique
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)