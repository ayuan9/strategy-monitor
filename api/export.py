
from fastapi import FastAPI
from mangum import Mangum
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def export_csv():
    csv_data = "time,direction,score,hit,profit\n20:00,UP,5,True,0.8\n"
    return PlainTextResponse(csv_data, media_type="text/csv")

handler = Mangum(app)
