import requests
import uuid
import sys

BASE_URL = "http://localhost:8000/api"

class WordleAPICLI:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        
    def print_info(self, top_infos: list):
        print(f"  {'words':<6} {'infos'}")
        for i, info_dict in enumerate(top_infos):
            # API returns a list of dicts like {"word": w, "info": info}
            print(f"{i+1} {info_dict['word']:<6} {info_dict['info']:.6f}")

    def start(self):
        print(f"Starting session {self.session_id}...")
        try:
            res = requests.post(f"{BASE_URL}/start", json={"session_id": self.session_id})
            res.raise_for_status()
            data = res.json()
            print(f"Session started! Remaining words: {data['remaining_count']}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to start session. Is the server running? Error: {e}")
            return

        for attempts in range(6):
            # In the API version, we only get top guesses *after* we make a prediction,
            # or we could add an endpoint just to get them. But let's ask for input.
            while True:
                guess = input("Enter the guess: ").lower()
                pattern = input("Enter the pattern: ").upper()
                
                try:
                    res = requests.post(f"{BASE_URL}/predict_next_word", json={
                        "session_id": self.session_id,
                        "guess": guess,
                        "pattern": pattern
                    })
                    
                    if res.status_code == 422: # Validation exception
                        err = res.json()
                        print(f"Invalid input: {err.get('error', 'Unknown error')}")
                        continue
                    
                    res.raise_for_status()
                    data = res.json()
                    
                    if pattern == "GGGGG":
                        print("congratulations, we did it!")
                        self.close()
                        return
                        
                    top_guesses = data.get("best_guesses", [])
                    if top_guesses:
                        self.print_info(top_guesses)
                        
                    remaining_count = data.get("remaining_count", 0)
                    print("Remaining Solutions:", remaining_count)
                    
                    if remaining_count == 0:
                        print(data.get("message", "Today's word isn't in our list, tough luck!"))
                        self.close()
                        return
                        
                    break # Successful guess, move to next attempt
                    
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}")
                    return
        
        print("Out of attempts!")
        self.close()

    def close(self):
        try:
            res = requests.post(f"{BASE_URL}/close", json={"session_id": self.session_id})
            if res.status_code == 200:
                print("Session closed successfully.")
            else:
                print(f"Failed to close session: {res.text}")
        except Exception as e:
            pass

if __name__ == "__main__":
    cli = WordleAPICLI()
    try:
        cli.start()
    except KeyboardInterrupt:
        print("\nExiting...")
        cli.close()
        sys.exit(0)
