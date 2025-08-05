 from flask import Flask, jsonify, send_file
from strategy_logic import evaluate_strategy
import csv
import time
import os

app = Flask(__name__)

# 模拟交易数据缓存
trade_log = []
winrate_history = []

@app.route("/api/status")
def get_status():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # 策略评分
    result = evaluate_strategy()
    
    # 模拟交易逻辑（评分大于等于3就开单）
    if result["score"] >= 3:
        trade = {
            "time": now,
            "direction": result["direction"],
            "score": result["score"],
            "hit": result["hit"],
            "profit": 0.8 if result["hit"] else -1
        }
        trade_log.append(trade)
        
        # 更新 CSV
        with open("data/trade_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([trade["time"], trade["direction"], trade["score"], trade["hit"], trade["profit"]])

        # 胜率记录更新
        last_n = [t["hit"] for t in trade_log[-20:]]
        winrate = round(sum(last_n) / len(last_n) * 100, 2) if last_n else 0
        winrate_history.append(winrate)

    # 输出前端所需数据
    return jsonify({
        "timestamp": now,
        "structure": result["structure"],
        "score": result["score"],
        "action": result["action"],
        "trades": trade_log[-30:],
        "winrate_history": winrate_history[-30:]
    })

@app.route("/api/export")
def export_csv():
    filename = "data/trade_log.csv"
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "direction", "score", "hit", "profit"])
    return send_file(filename, mimetype="text/csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
