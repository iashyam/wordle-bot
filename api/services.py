from api.core.redis_client import get_client
from api.exceptions import ServerErrorException, NotFoundException, ValidationException
from src.solver import WordleSolver
from src.load_data import Data
from src.utils import Functions
import json

data_instance = Data()
func_instance = Functions()

class WordleService:
    def __init__(self):
        pass

    async def ping_redis(self):
        try:
            client = await get_client()
            db_size = await client.dbsize()
            return {"status": "ok", "redis_keys_count": db_size}
        except Exception as e:
            raise ServerErrorException(f"Failed to connect to Redis: {str(e)}")

    async def get_test_data(self, key: str):
        client = await get_client()
        val = await client.get(key)
        if not val:
            raise NotFoundException(f"Key '{key}' not found in Redis.")
        return val.decode("utf-8")

    async def start_session(self, session_id: str):
        client = await get_client()
        words = data_instance.words
        session_data = {
            "words": words,
            "history": []
        }
        await client.set(session_id, json.dumps(session_data))
        solver = WordleSolver()
        best_guesses = solver.get_best_guesses(n=5)
        top_guesses_formatted = [{"word": w, "info": info} for w, info in best_guesses]
        return {
            "session_id": session_id,
            "message": "Session started",
            "remaining_count": len(data_instance.words),
            "best_guesses": top_guesses_formatted
        }

    async def predict_next_word(self, session_id: str, guess: str, pattern: str):
        guess = guess.lower()
        pattern = pattern.upper()

        client = await get_client()
        val = await client.get(session_id)
        if not val:
            raise NotFoundException(f"Session '{session_id}' not found. Please start a new session.")

        session_data = json.loads(val.decode("utf-8"))
        words = session_data.get("words", [])
        history = session_data.get("history", [])

        solver = WordleSolver(starting_words=words)
        
        try:
            solver.update_state(guess, pattern)
        except ValueError as ve:
            raise ValidationException(str(ve))
        except Exception as e:
            raise ServerErrorException(f"Failed to update state: {str(e)}")

        new_words = solver.words
        
        # Get best guesses from the updated remaining words
        solver_next = WordleSolver(starting_words=new_words)
        if new_words:
            # We ONLY compute best guesses if there are remaining words
            best_guesses = solver_next.get_best_guesses(n=5)
        else:
            best_guesses = []

        history.append({"guess": guess, "pattern": pattern})
        session_data["words"] = new_words
        session_data["history"] = history
        
        await client.set(session_id, json.dumps(session_data))

        top_guesses_formatted = [{"word": w, "info": info} for w, info in best_guesses]

        return {
            "session_id": session_id,
            "history": history,
            "remaining_count": len(new_words),
            "best_guesses": top_guesses_formatted,
            "message": "Success" if len(new_words) > 0 else "Today's word isn't in our list, tough luck!"
        }

    async def close_session(self, session_id: str):
        client = await get_client()
        result = await client.delete(session_id)
        if result == 0:
            raise NotFoundException(f"Session '{session_id}' not found.")
        return {"session_id": session_id, "message": "Session closed and cache cleared"}

service = WordleService()
