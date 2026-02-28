import asyncio
from fastapi.testclient import TestClient
from api.main import app
import api.core.redis_client as redis_client

# We want to mock the redis client in case Redis isn't actually running
# Wait, actually let's try calling it natively to see if it works.

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

    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_api()
