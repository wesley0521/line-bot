from supabase import create_client, Client
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_order_to_supabase(user_id, user_name, cheese, financier_original, financier_choco, financier_tea, pudding, payment, pickup_date, pickup_time, pickup_location):
    tw_now = datetime.utcnow() + timedelta(hours=8)

    data = {
        "user_id": user_id,
        "user_name": user_name,
        "cheese_cake": cheese,
        "financier_original": financier_original,
        "financier_choco": financier_choco,
        "financier_tea": financier_tea,
        "pudding": pudding,
        "payment_method": payment,
        "pickup_date": pickup_date,
        "pickup_time": pickup_time,
        "pickup_location": pickup_location,
        "timestamp": tw_now.isoformat()
    }

    result = supabase.table("orders").insert(data).execute()
    print(result)
