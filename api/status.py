
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_status():
    return {
        "timestamp": "2025-08-06 20:00:00",
        "structure": "测试结构",
        "score": 5,
        "action": "开多",
        "trades": [
            {"time": "20:00", "direction": "UP", "score": 5, "hit": True, "profit": 0.8},
            {"time": "20:03", "direction": "DOWN", "score": 4, "hit": False, "profit": -1}
        ],
        "winrate_history": [100, 50]
    }

handler = Mangum(app)
