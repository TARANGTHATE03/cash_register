# Dukaan Cash Register

A simple Flask + SQLite cash register (cash in / cash out) app, built for
small Indian shops. No accounts, no login — just a fast daily ledger.

## Features
- Add "Cash In" (sales, receipts) and "Cash Out" (expenses, purchases) entries
- Records date, particulars, amount (₹), and payment mode (Cash/UPI/Card/etc.)
- Auto-calculated Total In, Total Out, running Balance
- Today's snapshot (today's in/out at a glance)
- Delete an entry if you made a mistake
- Data stored locally in `cash_register.db` (SQLite) — nothing leaves your machine

## Setup

1. Make sure Python 3.8+ is installed.
2. In this folder, create a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python app.py
   ```
5. Open your browser at: http://127.0.0.1:5000

The SQLite database file (`cash_register.db`) is created automatically the
first time you run the app.

## Project structure
```
cash_register/
├── app.py                # Flask app + routes + SQLite logic
├── requirements.txt
├── cash_register.db      # created automatically on first run
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── style.css
```

## Notes / easy extensions
- To back up your data, just copy `cash_register.db`.
- Ideas to extend: date-range filtering, CSV export, GST-ready invoice
  numbers, multi-user shop staff logins, daily closing report printout.
