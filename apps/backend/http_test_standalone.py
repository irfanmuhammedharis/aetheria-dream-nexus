"""
HTTP validation test for /ingest/dream endpoint.
Standalone process - does not interfere with backend terminal.
"""
import json
import http.client
from uuid import uuid4
from pathlib import Path
from datetime import datetime

artifact_dir = Path(__file__).parent.parent.parent / "test" / "artifacts" / "web_ingest_dream_flow" / "cycle-10"
artifact_dir.mkdir(parents=True, exist_ok=True)
result_file = artifact_dir / "http_final_validation.txt"

payload = {
    "dream_id": str(uuid4()),
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp_ingested": datetime.now().isoformat(),
    "input_modality": "text",
    "content_raw": "Flying over a dark ocean under a full moon with phosphorescent waves below"
}

conn = http.client.HTTPConnection("127.0.0.1", 8000, timeout=10)

try:
    headers = {"Content-Type": "application/json"}
    body = json.dumps(payload)
    conn.request("POST", "/ingest/dream", body, headers)
    response = conn.getresponse()
    
    status = response.status
    response_body = response.read().decode("utf-8")
    
    with open(result_file, "w", encoding="utf-8") as f:
        f.write(f"HTTP STATUS: {status} {response.reason}\n")
        f.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
        f.write(f"\nRESPONSE BODY:\n{response_body}\n")
        
        if status == 200:
            f.write("\n=== VALIDATION RESULT: PASS ===\n")
            print(f"[PASS] HTTP {status} - Response body length: {len(response_body)} bytes")
        else:
            f.write("\n=== VALIDATION RESULT: FAIL ===\n")
            print(f"[FAIL] HTTP {status}")
    
except Exception as e:
    with open(result_file, "w", encoding="utf-8") as f:
        f.write(f"CONNECTION FAILED: {type(e).__name__}\n")
        f.write(f"{str(e)}\n")
    print(f"[FAIL] Connection error: {e}")
finally:
    conn.close()
