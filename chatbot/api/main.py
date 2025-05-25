# chatbot/api/main.py
from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path

from fastapi import FastAPI
from chatbot.api.predict import predict_price
from chatbot.api.schemas import PredictionRequest
from chatbot.api.airport_mapper import get_airport_info
from chatbot.api import chat  # importation fichier chat.py

app = FastAPI(title="Air Paradise API")

# Inclure le router
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Air Paradise ✈️"}

@app.post("/predict")
def predict_endpoint(payload: PredictionRequest):
    price = predict_price(payload.dict())
    return {"predicted_price": price}

@app.get("/map-airport")
def airport_mapping(code: str):
    return get_airport_info(code)
