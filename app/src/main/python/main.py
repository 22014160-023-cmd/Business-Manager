
import json
import sqlite3
from reportlab.pdfgen import canvas
import os

DB_PATH = "/data/data/com.businessmanager.app/databases/business.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY, amount REAL, date TEXT)''')
    conn.commit()
    conn.close()
    return json.dumps({"status": "success"})

def add_sale(json_data):
    data = json.loads(json_data)
    amount = data.get("amount", 0)
    date = data.get("date", "2024-01-01")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sales (amount, date) VALUES (?, ?)", (amount, date))
    conn.commit()
    conn.close()
    return json.dumps({"status": "success"})

def get_sales():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT amount, date FROM sales ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    
    sales = [{"amount": r[0], "date": r[1]} for r in rows]
    return json.dumps({"sales": sales})

def generate_pdf():
    # Example PDF generation (saves to app folder)
    pdf_path = "/data/data/com.businessmanager.app/files/report.pdf"
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, "Business Manager - Daily Report")
    c.drawString(100, 700, "Total Sales: See live feed")
    c.save()
    return json.dumps({"path": pdf_path})
