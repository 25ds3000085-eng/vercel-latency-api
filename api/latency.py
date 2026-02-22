from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import numpy as np

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load telemetry
with open("telemetry.json") as f:
    data = json.load(f)


@app.post("/api/latency")
def analyze(payload: dict):

    regions = payload["regions"]
    threshold = payload["threshold_ms"]

    result = {}

    for r in regions:
        records = [x for x in data if x["region"] == r]

        latencies = [x["latency_ms"] for x in records]
        uptimes = [x["uptime"] for x in records]

        result[r] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": sum(1 for x in latencies if x > threshold)
        }

    return result
