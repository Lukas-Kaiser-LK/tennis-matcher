# Tennis Matcher Berlin

A lightweight hackathon prototype that helps tennis players in Berlin find compatible partners and suitable public-access courts.

## What it does

- collects a player's neighborhood, skill level, preferred surface and availability
- uses the OpenAI API to rank compatible players from `players.json`
- uses the OpenAI API to select suitable courts from `courts.json`
- uses Tavily API search in the matchmaking flow
- displays suggested courts with booking information, hours, prices and guest restrictions

## Technologies

- Python
- Flask
- OpenAI API
- Tavily API
- HTML, CSS and JavaScript
- JSON files for demo player and court data

## Project files

- `app.py` - Flask backend and API calls
- `index.html` - frontend interface
- `players.json` - demo player profiles
- `courts.json` - structured Berlin court data

## Setup

1. Clone the repository.
2. Install the dependencies:

```bash
pip3 install -r requirements.txt
```

3. Open `app.py` and replace these placeholders with your own API keys:

```python
OPENAI_API_KEY = "PUT_YOUR_OPENAI_API_KEY_HERE"
TAVILY_API_KEY = "PUT_YOUR_TAVILY_API_KEY_HERE"
```

4. Run the app:

```bash
python3 app.py
```

5. Open this address in your browser:

```text
http://127.0.0.1:5000
```

## How it works

The user submits a tennis profile. OpenAI compares that profile with the demo players and returns ranked matches. When the user opens a match, OpenAI selects suitable courts from the structured Berlin court dataset. Tavily is also used in the matchmaking flow for tennis-court search.

## Security

No real API keys are included in this repository. Anyone running the project must add their own keys locally.
