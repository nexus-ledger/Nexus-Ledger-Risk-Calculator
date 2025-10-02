# Nexus Ledger Risk Calculator

A sleek, open-source **Forex lot size + Crypto dollar position** calculator built with Flask — by Nexus Ledger.

<img width="1198" height="676" alt="github" src="https://github.com/user-attachments/assets/4c13b20c-6171-4651-b1c5-8e16617b91e6" />


## ✨ Features
- **Forex mode**: Account size + risk% + stop (pips) + pip value → **standard lot size** (with mini/micro equivalents)
- **Crypto mode**: Account size + risk% + entry + stop → **quantity** and **position value**
- Instant **Risk $** and optional **Risk/Reward** metrics
- Beautiful, responsive UI with Nexus Ledger branding

## 🧮 Formulas
**Forex (standard lots):**
```
Risk $ = Account × (Risk% / 100)
Lot Size = Risk $ / (Stop (pips) × Pip Value per 1.00 lot)
```
_Default pip value for most USD-quoted pairs ≈ **$10 per pip** per 1.00 lot. For JPY pairs ~ **$9.13**. For non-USD quotes, check broker._

**Crypto:**
```
Risk $ = Account × (Risk% / 100)
Quantity = Risk $ / |Entry − Stop|
Position $ = Quantity × Entry
```

## 🚀 Local Run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install flask
python app.py
# open http://127.0.0.1:5000
```

## 🧩 Project Structure
```
Nexus-Ledger-Risk-Calculator/
├── app.py
├── templates/
│   └── index.html
├── static/
└── README.md
```


## 🔗 Links
- Website: https://www.nexusledger.org
- Instagram: https://www.instagram.com/nexus.ledger

---

If this helps you, drop a ⭐ on GitHub and share it with your trading friends.
