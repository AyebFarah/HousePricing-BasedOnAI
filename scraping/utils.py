import pandas as pd
import re

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
    
def calculate_discount(current, original):
    if current is not None and original is not None and original > 0:
        return round((original - current) / original * 100, 2)
    return 0
