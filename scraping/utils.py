import pandas as pd
import re
from datetime import datetime, timedelta

def save_to_csv(products, filename):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\nDonnées sauvegardées dans {filename}")
    return df

def normalize_price(price_str):
    if not price_str:
        return None
    cleaned = re.sub(r"[^\d,\.]", "", price_str)
    if cleaned.count(",") == 1 and cleaned.count(".") > 1:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif cleaned.count(",") == 1 and cleaned.count(".") == 0:
        cleaned = cleaned.replace(",", ".")
    try:
        return float(cleaned)
    except:
        return None
    
from datetime import datetime, timedelta
import re

def parse_relative_date(text):
    """Convert relative date in English or French to YYYY-MM-DD"""
    now = datetime.today()
    text = text.lower().strip()
    
    # English
    match = re.search(r"(\d+)\s+(minute|minutes|hour|hours|day|days|month|months)\s+ago", text)
    if match:
        value, unit = int(match.group(1)), match.group(2)
        if unit.startswith("minute"):
            return (now - timedelta(minutes=value)).strftime("%Y-%m-%d")
        elif unit.startswith("hour"):
            return (now - timedelta(hours=value)).strftime("%Y-%m-%d")
        elif unit.startswith("day"):
            return (now - timedelta(days=value)).strftime("%Y-%m-%d")
        elif unit.startswith("month"):
            return (now - timedelta(days=30*value)).strftime("%Y-%m-%d")
    
    # French
    match_fr = re.search(r"il y a (\d+)\s*(minute|minutes|heure|heures|jour|jours|mois)", text)
    if match_fr:
        value, unit = int(match_fr.group(1)), match_fr.group(2)
        if unit.startswith("minute"):
            return (now - timedelta(minutes=value)).strftime("%Y-%m-%d")
        elif unit.startswith("heure"):
            return (now - timedelta(hours=value)).strftime("%Y-%m-%d")
        elif unit.startswith("jour"):
            return (now - timedelta(days=value)).strftime("%Y-%m-%d")
        elif unit.startswith("mois"):
            return (now - timedelta(days=30*value)).strftime("%Y-%m-%d")
    
    return None


def extract_number(text):
    """Extrait le premier nombre trouvé dans une chaîne"""
    if not text:
        return None
    numbers = re.findall(r"\d+", str(text).replace(",", "").replace(" ", ""))
    return int(numbers[0]) if numbers else None
