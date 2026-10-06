from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime, date
import os

app = Flask(__name__)
app.secret_key = "x7Kp9Qm2Lz8Vn4Rj6Tq1Ws5Yb3Hd0Fc8"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cash_register.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            particulars TEXT NOT NULL,
            entry_type TEXT NOT NULL CHECK(entry_type IN ('IN', 'OUT')),
            amount REAL NOT NULL,
            payment_mode TEXT NOT NULL DEFAULT 'Cash',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()

    entries = conn.execute(
        "SELECT * FROM entries ORDER BY entry_date DESC, id DESC"
    ).fetchall()

    total_in = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) AS t FROM entries WHERE entry_type='IN'"
    ).fetchone()["t"]

    total_out = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) AS t FROM entries WHERE entry_type='OUT'"
    ).fetchone()["t"]

    today_str = date.today().isoformat()

    today_in = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) AS t FROM entries WHERE entry_type='IN' AND entry_date=?",
        (today_str,),
    ).fetchone()["t"]

    today_out = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) AS t FROM entries WHERE entry_type='OUT' AND entry_date=?",
        (today_str,),
    ).fetchone()["t"]

    conn.close()

    balance = total_in - total_out
    today_net = today_in - today_out

    return render_template(
        "index.html",
        entries=entries,
        total_in=total_in,
        total_out=total_out,
        balance=balance,
        today_in=today_in,
        today_out=today_out,
        today_net=today_net,
        today_str=today_str,
    )


@app.route("/add", methods=["POST"])
def add_entry():
    entry_date = request.form.get("entry_date") or date.today().isoformat()
    particulars = request.form.get("particulars", "").strip()
    entry_type = request.form.get("entry_type")
    amount_raw = request.form.get("amount")
    payment_mode = request.form.get("payment_mode", "Cash")

    if not particulars or entry_type not in ("IN", "OUT") or not amount_raw:
        flash("Please fill in all fields correctly.", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount_raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number.", "error")
        return redirect(url_for("index"))

    conn = get_db()
    conn.execute(
        """INSERT INTO entries (entry_date, particulars, entry_type, amount, payment_mode, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (entry_date, particulars, entry_type, amount, payment_mode, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()

    flash("Entry added to the register.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    conn = get_db()
    conn.execute("DELETE FROM entries WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()
    flash("Entry deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
