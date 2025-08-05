import requests
import numpy as np
from indicators import calculate_indicators
import random

# 获取 Binance 3分钟K线数据
def get_binance_klines(symbol="BTCUSDT", interval="3m", limit=50):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    closes = [float(k[4]) for k in data]
    highs = [float(k[2]) for k in data]
    lows = [float(k[3]) for k in data]
    return closes, highs, lows

def evaluate_strategy():
    closes, highs, lows = get_binance_klines()

    # 计算指标
    rsi = calculate_indicators.rsi(closes)
    skdj_k, skdj_d = calculate_indicators.skdj(closes)
    macd, macd_signal = calculate_indicators.macd(closes)
    atr = calculate_indicators.atr(highs, lows, closes)
    adx = calculate_indicators.adx(highs, lows, closes)
    upper, middle, lower = calculate_indicators.bollinger(closes)

    # 趋势识别逻辑（趋势/震荡）
    is_trending = adx[-1] > 25 and (upper[-1] - lower[-1]) / middle[-1] > 0.05 and macd[-1] > macd_signal[-1]
    structure = "趋势行情" if is_trending else "震荡行情"

    # 打分系统（简化版）
    score = 0
    if rsi[-1] < 20: score += 1
    if rsi[-1] > 80: score += 1
    if skdj_k[-1] > skdj_d[-1]: score += 1
    if macd[-1] > macd_signal[-1]: score += 1
    if closes[-1] < lower[-1] or closes[-1] > upper[-1]: score += 1
    if atr[-1] > np.mean(atr[-5:]) * 1.2: score += 1

    # 操作建议
    if score >= 5:
        action = "强信号，建议重仓"
    elif score >= 3:
        action = "信号成立，可轻仓"
    else:
        action = "信号不足，观望"

    # 判断方向
    direction = "多单" if rsi[-1] < 30 else "空单"

    # 简化版模拟命中（随机 + 趋势判断）
    hit = random.random() < (0.7 if not is_trending else 0.45)

    return {
        "structure": structure,
        "score": score,
        "direction": direction,
        "action": action,
        "hit": hit
    }
