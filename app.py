from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from tavily import TavilyClient
import json

app = Flask(__name__)

OPENAI_API_KEY = "PUT_YOUR_OPENAI_API_KEY_HERE"
TAVILY_API_KEY = "PUT_YOUR_TAVILY_API_KEY_HERE"

openai_client = OpenAI(api_key=OPENAI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

with open("players.json") as f:
    players = json.load(f)
with open("courts.json", encoding="utf-8") as f:
    courts = json.load(f)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/match", methods=["POST"])
def match():
    user = request.json
    profiles_text = json.dumps(players, indent=2)
    user_text = json.dumps(user, indent=2)

    prompt = f"""
You are a tennis matchmaking assistant. Here is a new player looking for a match:

{user_text}

Here are available players:

{profiles_text}

Rank ALL players by compatibility. Return a JSON object with a key "matches" containing an array of all players, each with:
- "name": player's name
- "neighborhood": player's neighborhood
- "level": player's level
- "surfaces": player's surfaces array
- "available_slots": player's slots array
- "match_score": score out of 10
- "reason": one sentence explaining the match

Sort by match_score descending. Only return valid JSON, nothing else.
"""

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    matches = result.get("matches", [])

    top_match_neighborhood = matches[0]["neighborhood"] if matches else user.get("neighborhood", "Berlin")
    tavily_results = tavily_client.search(
        f"public tennis court {top_match_neighborhood} Berlin open without membership booked online",
        max_results=3
    )
    courts = [{"name": r["title"], "url": r["url"]} for r in tavily_results.get("results", [])]

    return jsonify({
        "matches": matches,
        "courts": courts,
        "user": user
    })

@app.route("/court", methods=["POST"])
def court():
    data = request.json or {}

    neighborhood_a = data.get("neighborhood_a", "Berlin")
    neighborhood_b = data.get("neighborhood_b", "Berlin")

    try:
        courts_text = json.dumps(courts, indent=2, ensure_ascii=False)

        prompt = f"""
You are helping two tennis players choose a court in Berlin.

Player 1 lives in: {neighborhood_a}
Player 2 lives in: {neighborhood_b}

Here are the available courts:

{courts_text}

Choose the best 2 courts for these players.

Prefer:
1. courts located near either player's neighborhood
2. courts that non-members can actually book
3. courts with clear booking information
4. courts with fewer guest restrictions

Only select courts from the provided list.
Do not invent any information.

Return valid JSON with a key called "courts".

Each court must contain:
- "name"
- "area", using the court's neighborhood
- "how_to_book"
- "hours"
- "price"
- "notes"
"""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        return jsonify({
            "courts": result.get("courts", [])
        })

    except Exception as e:
        print("Court selection error:", str(e))
        return jsonify({
            "courts": [],
            "error": str(e)
        }), 200

if __name__ == "__main__":
    app.run(debug=True)