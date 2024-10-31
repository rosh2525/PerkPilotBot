import google.generativeai as genai
import os
import sqlite3

api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure to set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")
conn = sqlite3.connect('student_discounts.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM discounts')
rows = cursor.fetchall()

x = input("Hi! Welcome to PerkPilotBot. What are you looking for?")
response = model.generate_content(f"these are the current offers {rows}, from these answer this prompt and remember that your name is PerkPilotBot and dont mention MyUnidays or StudentBeans and also give link to the website (logo column contains the link) if you cant find an appropriate website based on the offers list i gave, then just say that there are no currently offers {x}")
print(response.text)
