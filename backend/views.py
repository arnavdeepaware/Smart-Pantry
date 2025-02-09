import os
from dotenv import load_dotenv
from supabase import create_client
import streamlit as st

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
#print(SUPABASE_URL)
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
#print(SUPABASE_KEY)



#create supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_ingredients_from_supabase():
    pantry_data = supabase.table('pantry').select('item_name', 'quantity', 'unit', 'days_in_pantry').execute()
    
    if pantry_data.data:
        return pantry_data.data
    else:
        return []