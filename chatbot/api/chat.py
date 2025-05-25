from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import os, json, re
from datetime import datetime, time
import google.generativeai as genai
from dotenv import load_dotenv
import dateparser
from langdetect import detect

# Charger variables d'environnement et configurer Gemini AI
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Chargement des données
AIRPORTS_CSV = r"C:/Users/ADMIN/Desktop/air_paradise_chatbot/data/mapping/airport_mapping.csv"
CONTEXT_PATH = r"C:/Users/ADMIN/Desktop/air_paradise_chatbot/data/rag/context.txt"
airports_df = pd.read_csv(AIRPORTS_CSV)

with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
    RAG_CONTEXT = f.read()

router = APIRouter()

class ChatInput(BaseModel):
    message: str
    history: list[str] = []
def get_iata_code(city_or_code):
    city_or_code = city_or_code.strip().upper()
    if len(city_or_code) == 3:  # Déjà un code IATA ?
        return city_or_code if city_or_code in airports_df['IATA_CODE'].values else None
    match = airports_df[airports_df['CITY'].str.lower() == city_or_code.lower()]
    return match['IATA_CODE'].iloc[0] if not match.empty else None


def parse_date(date_str):
    parsed = dateparser.parse(date_str, settings={"PREFER_DATES_FROM": "future"})
    return parsed.strftime("%Y-%m-%d") if parsed else None

def parse_time(time_str):
    parsed = dateparser.parse(time_str)
    return parsed.strftime("%H:%M") if parsed else None

def is_valid_hour(hhmm):
    try:
        t = datetime.strptime(hhmm, "%H:%M").time()
        return time(6, 0) <= t < time(23, 0)
    except:
        return False

@router.post("/chat")
def chat_handler(input: ChatInput):
    user_msg = input.message.strip()
    context = "\n".join(input.history[-3:])
    lang = detect(user_msg)

    # FAQ simples
    faq = {
        "bagage": "Chaque passager peut embarquer un bagage cabine de 10kg.",
        "check": "L'enregistrement en ligne est ouvert 24h avant le vol.",
        "document": "Un passeport ou une pièce d'identité est requis pour embarquer.",
        "support": "Notre support est joignable à air.paradise.us@gmail.com."
    }
    lower_msg = user_msg.lower()
    for k, rep in faq.items():
        if k in lower_msg:
            return {"summary": rep, "lang": lang}

    # Salutations simples
    if lower_msg in ["salut", "bonjour", "hello", "hi", "bonsoir"]:
        return {"summary": "👋 Bonjour ! Comment puis-je vous aider à réserver un vol ?" if lang.startswith("fr") else "👋 Hello! How can I help you book a flight?", "lang": lang}

    # Prompt selon la langue
    if lang.startswith("en"):
        intro = "You are an assistant for the airline Air Paradise."
        task = """
Extract this JSON:
{
  "ORIGIN_CITY": "...",
  "DESTINATION_CITY": "...",
  "DATE": "...",
  "HEURE": "like 12:30"
}
Respond naturally, then show the JSON. If missing info, ask the user.
Reject flights between 23:00 and 06:00.
"""
    else:
        intro = "Tu es un assistant pour la compagnie aérienne Air Paradise."
        task = """
Extrais ce JSON :
{
  "ORIGIN_CITY": "...",
  "DESTINATION_CITY": "...",
  "DATE": "...",
  "HEURE": "comme 12:30"
}
Commence par une réponse naturelle, puis affiche le JSON. Si info manquante, demande-la.
Refuse les vols entre 23h et 6h.
"""

    prompt = f"""
{intro}

Infos utiles :
{RAG_CONTEXT}

Historique :
{context}

Message utilisateur :
{user_msg}

{task}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text

        # Extraction du JSON dans la réponse
        json_match = re.search(r"\{[\s\S]*?\}", text)
        parsed, missing = {}, []

        if json_match:
            parsed = json.loads(json_match.group())
            origin_city = parsed.get("ORIGIN_CITY")
            destination_city = parsed.get("DESTINATION_CITY")
            date = parse_date(parsed.get("DATE"))
            heure = parse_time(parsed.get("HEURE"))

            origin_iata = get_iata_code(origin_city) if origin_city else None
            dest_iata = get_iata_code(destination_city) if destination_city else None

            if not date:
                missing.append("date de départ" if not lang.startswith("en") else "departure date")
            if not origin_city:
                missing.append("ville de départ" if not lang.startswith("en") else "origin city")
            if not destination_city:
                missing.append("ville d'arrivée" if not lang.startswith("en") else "destination city")
            if not heure:
                missing.append("heure de départ" if not lang.startswith("en") else "departure time")
            elif not is_valid_hour(heure):
                missing.append("heure invalide (vols entre 06h et 23h uniquement)" if not lang.startswith("en") else "invalid time (flights between 06:00 and 23:00 only)")

            if origin_iata == dest_iata and origin_iata:
                missing.append("les aéroports doivent être différents" if not lang.startswith("en") else "origin and destination airports must be different")

            summary = f"✈️ Vol de {origin_iata or origin_city or '...'} → {dest_iata or destination_city or '...'}"
            if date:
                summary += f" le {date}"
            if heure:
                summary += f" à {heure}"

            return {
                "parsed": {
                    "ORIGIN_CITY": origin_city,
                    "DESTINATION_CITY": destination_city,
                    "DATE": date,
                    "HEURE": heure
                },
                "iata_codes": {"origin": origin_iata, "destination": dest_iata},
                "summary": summary,
                "missing": missing,
                "bookable": bool(origin_iata and dest_iata and not missing),
                "lang": lang
            }
        else:
            return {"raw_response": text, "warning": "Pas de JSON compris." if not lang.startswith("en") else "No JSON understood.", "lang": lang}

    except Exception as e:
        return {"error": str(e), "lang": lang}
