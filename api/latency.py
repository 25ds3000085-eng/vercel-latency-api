import json
import pandas as pd
from http.server import BaseHTTPRequestHandler


# Load data once
df = pd.read_csv("telemetry.csv")


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):

        # Enable CORS
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")

        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)

        data = json.loads(body)

        regions = data["regions"]
        threshold = data["threshold_ms"]

        result = {}

        for region in regions:

            region_data = df[df["region"] == region]

            avg_latency = region_data["latency_ms"].mean()
            p95_latency = region_data["latency_ms"].quantile(0.95)
            avg_uptime = region_data["uptime"].mean()
            breaches = (region_data["latency_ms"] > threshold).sum()

            result[region] = {
                "avg_latency": round(avg_latency, 2),
                "p95_latency": round(p95_latency, 2),
                "avg_uptime": round(avg_uptime, 2),
                "breaches": int(breaches)
            }

        self.send_response(200)
        self.end_headers()

        self.wfile.write(json.dumps(result).encode())