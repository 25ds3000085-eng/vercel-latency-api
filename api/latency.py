from fastapi import FastAPI

app = FastAPI()

@app.post("/api/latency")
async def latency():
    return {"status": "ok"}