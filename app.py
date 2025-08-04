from flask import Flask, render_template, request
import requests
import mysql.connector
import json

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="db-password",
        database="currencydb"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    currencies = json.load(open('currencies.json'))
    result = None
    if request.method == 'POST':
        base = request.form['base']
        target = request.form['target']
        amount = float(request.form['amount'])
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url).json()
        rate = response['rates'].get(target)
        if rate:
            result = amount * rate
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO conversions (base_currency, target_currency, amount, converted_amount, rate) VALUES (%s, %s, %s, %s, %s)",
                           (base, target, amount, result, rate))
            conn.commit()
            conn.close()
    return render_template('index.html', currencies=currencies, result=result)

@app.route('/history')
def history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT base_currency, target_currency, amount, converted_amount, rate, timestamp FROM conversions ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template('history.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
