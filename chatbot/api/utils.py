import dateparser
from datetime import datetime, time
from langdetect import detect

def parse_date(date_str):
    parsed = dateparser.parse(date_str, settings={"PREFER_DATES_FROM": "future"})
    return parsed.strftime("%Y-%m-%d") if parsed else None

def parse_time(time_str):
    parsed = dateparser.parse(time_str)
    return parsed.strftime("%H:%M") if parsed else None

def is_valid_hour(hhmm):
    try:
        t = datetime.strptime(hhmm, "%H:%M").time()
        return time(6, 0) <= t <= time(22, 0)
    except:
        return False

def detect_language(text):
    return detect(text)

def load_faq(path="data/rag/faq.txt"):
    faq = {}
    current = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("[") and line.endswith("]\n"):
                current = line[1:-2].strip().lower()
                faq[current] = ""
            elif current:
                faq[current] += line
    return faq
