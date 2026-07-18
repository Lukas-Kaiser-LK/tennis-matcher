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
- Tavily API and Tavily's research interface
- HTML, CSS and JavaScript
- JSON files for demo player and court data

## Tavily usage and prototype limitation

The intended product flow is to use Tavily live to discover and verify suitable tennis courts for each matched pair. During the hackathon, we found that the untuned API search was less reliable than Tavily's own research interface for this specific local-data task, and we did not have enough time or API budget to tune the live retrieval flow properly.

We therefore used Tavily's research interface to find and verify public-access tennis courts in Berlin, then structured those results into `courts.json`. The demo uses this Tavily-researched dataset so the live experience stays fast and reliable, while OpenAI ranks the most suitable courts for the two players. A future version would replace the static dataset with a fully live Tavily retrieval and verification pipeline.

This is an explicit prototype tradeoff rather than simulated data: the court records were researched with Tavily, but persisted locally for the hackathon demo.

## Project files

- `app.py` - Flask backend and API calls
- `index.html` - frontend interface
- `players.json` - demo player profiles
- `courts.json` - structured Berlin court data researched with Tavily

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

The user submits a tennis profile. OpenAI compares that profile with the demo players and returns ranked matches. When the user opens a match, OpenAI selects suitable courts from the structured Berlin court dataset. Tavily is used both in the current API flow and as the research source for the court dataset.

## Security

No real API keys are included in this repository. Anyone running the project must add their own keys locally.