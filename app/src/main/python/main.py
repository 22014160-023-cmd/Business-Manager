import json
import sqlite3
from fpdf import FPDF
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
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sales (amount, date) VALUES (?, ?)", (data["amount"], data["date"]))
    conn.commit()
    conn.close()
    return json.dumps({"status": "success"})

def get_sales():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT amount, date FROM sales ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return json.dumps({"sales": [{"amount": r[0], "date": r[1]} for r in rows]})

def generate_pdf():
    pdf_path = "/data/data/com.businessmanager.app/files/report.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Business Manager - Daily Report", ln=1, align='C')
    pdf.output(pdf_path)
    return json.dumps({"path": pdf_path})
