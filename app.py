from flask import Flask, render_template, request
from math import isfinite

app = Flask(__name__)

BRAND = {
    "name": "Nexus Ledger",
    "tagline": "Fintech & Trading Innovation",
    "primary": "#5271ff",
    "dark": "#0f1221",
    "light": "#f7f9ff",
}

def safe_float(val, default=0.0):
    try:
        f = float(val)
        return f if isfinite(f) else default
    except Exception:
        return default

@app.route("/", methods=["GET", "POST"])
def index():
    context = {"brand": BRAND, "results": None, "errors": []}

    if request.method == "POST":
        mode = request.form.get("mode", "forex")
        account = safe_float(request.form.get("account"))
        risk_pct = safe_float(request.form.get("risk_pct"))
        take_profit = request.form.get("take_profit")  # optional field, used below

        if account <= 0:
            context["errors"].append("Account size must be greater than 0.")
        if risk_pct <= 0 or risk_pct > 100:
            context["errors"].append("Risk % must be between 0 and 100.")

        risk_amount = account * (risk_pct / 100.0)

        if mode == "forex":
            stop_pips = safe_float(request.form.get("stop_pips"))
            pip_value = safe_float(request.form.get("pip_value"), 10.0)  # default $10 per pip per standard lot
            if stop_pips <= 0:
                context["errors"].append("Stop loss (pips) must be greater than 0 for Forex.")
            if pip_value <= 0:
                context["errors"].append("Pip value per standard lot must be greater than 0.")

            if not context["errors"]:
                lot_size = risk_amount / (stop_pips * pip_value)  # standard lots
                # Mini & micro equivalents for convenience
                mini_lots = lot_size * 10
                micro_lots = lot_size * 100

                # RR if TP pips given
                rr = None
                rr_note = None
                tp_pips = safe_float(request.form.get("tp_pips"))
                if tp_pips > 0:
                    rr = tp_pips / stop_pips
                    rr_note = f"Risk/Reward = {rr:.2f}:1 based on TP {tp_pips:.1f} pips and SL {stop_pips:.1f} pips."

                context["results"] = {
                    "mode": "forex",
                    "risk_amount": risk_amount,
                    "stop_pips": stop_pips,
                    "pip_value": pip_value,
                    "lot_size": lot_size,
                    "mini_lots": mini_lots,
                    "micro_lots": micro_lots,
                    "rr": rr,
                    "rr_note": rr_note
                }

        elif mode == "crypto":
            entry = safe_float(request.form.get("entry"))
            stop = safe_float(request.form.get("stop"))
            if entry <= 0 or stop <= 0:
                context["errors"].append("Entry and Stop must be greater than 0 for Crypto.")
            if entry == stop:
                context["errors"].append("Entry and Stop cannot be equal.")

            if not context["errors"]:
                stop_distance = abs(entry - stop)
                qty = risk_amount / stop_distance  # quantity of asset
                position_value = qty * entry
                rr = None
                rr_note = None
                tp_price = safe_float(request.form.get("tp_price"))
                if tp_price > 0:
                    reward = abs(tp_price - entry)
                    if stop_distance > 0:
                        rr = reward / stop_distance
                        rr_note = f"Risk/Reward = {rr:.2f}:1 based on TP {tp_price:.4f} and SL {stop:.4f}."

                context["results"] = {
                    "mode": "crypto",
                    "risk_amount": risk_amount,
                    "entry": entry,
                    "stop": stop,
                    "qty": qty,
                    "position_value": position_value,
                    "rr": rr,
                    "rr_note": rr_note
                }
        else:
            context["errors"].append("Invalid mode selected.")

    return render_template("index.html", **context)

if __name__ == "__main__":
    # Debug mode for local testing; change host/port as needed
    app.run(host="127.0.0.1", port=5000, debug=True)