import asyncio
from fastapi.testclient import TestClient
from api.main import app
import api.core.redis_client as redis_client
import uuid

def test_api():
    try:
        with TestClient(app) as client:
            print("--- Startup successful ---")
            
            res1 = client.get("/")
            print("GET / ->", res1.status_code, res1.json())
            
            res2 = client.get("/api/health")
            print("GET /api/health ->", res2.status_code, res2.json())
            
            # This should throw a 404 NotFoundException because key isn't there
            res3 = client.get("/api/data/some-missing-key")
            print("GET /api/data/some-missing-key ->", res3.status_code, res3.json())

            # Test Wordle Endpoints
            session_id = str(uuid.uuid4())
            print(f"\n--- Testing Session Endpoints (Session ID: {session_id}) ---")
            
            # 1. Start session
            res_start = client.post("/api/start", json={"session_id": session_id})
            print("POST /api/start ->", res_start.status_code, res_start.json())

            # 2. Predict next word (valid guess)
            res_predict = client.post("/api/predict_next_word", json={
                "session_id": session_id,
                "guess": "cigar",
                "pattern": "BBYBB"
            })
            if res_predict.status_code == 200:
                print("POST /api/predict_next_word (cigar, BBYBB) ->", res_predict.status_code, res_predict.json()["remaining_count"], "words left")
            else:
                print("POST /api/predict_next_word (cigar, BBYBB) ->", res_predict.status_code, res_predict.json())

            # 3. Predict next word (invalid guess format)
            res_predict_inv = client.post("/api/predict_next_word", json={
                "session_id": session_id,
                "guess": "too_long",
                "pattern": "BBYBB"
            })
            print("POST /api/predict_next_word (invalid guess format) ->", res_predict_inv.status_code, res_predict_inv.json())

            # 4. Predict next word (word not in remaining list)
            res_predict_not_in_list = client.post("/api/predict_next_word", json={
                "session_id": session_id,
                "guess": "cigar",
                "pattern": "BBYBB"
            })
            print("POST /api/predict_next_word (guess not in remaining list) ->", res_predict_not_in_list.status_code, res_predict_not_in_list.json())

            # 5. Close session
            res_close = client.post("/api/close", json={"session_id": session_id})
            print("POST /api/close ->", res_close.status_code, res_close.json())
            
            # 6. Predict next word (after closing)
            res_predict_closed = client.post("/api/predict_next_word", json={
                "session_id": session_id,
                "guess": "slate",
                "pattern": "BBYBB"
            })
            print("POST /api/predict_next_word (after close) ->", res_predict_closed.status_code, res_predict_closed.json())

    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_api()
