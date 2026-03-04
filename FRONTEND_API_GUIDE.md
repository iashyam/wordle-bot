# Frontend API Guide
# Wordle Solver Game API Documentation

This documentation defines the interface required to connect your frontend application to the fast Wordle algorithm engine via HTTP protocols. 
All endpoints exist relative to the core api `url` endpoints. It includes a healthcheck, a test data fetching service, and a game session manager core endpoint set. 

## Endpoints

### Health and Testing
1. **Health Check**  
   - **Route:** `GET /health`  
   - Response: `{"status": "ok"}`

2. **Redis Status Check**
   - **Route:** `GET /redis-status`
   - Response: `{"status": "ok", "redis_keys_count": [current elements count in memory cache]}`

3. **Get Test Data**
   - **Route:** `GET /data/{key}`
   - Parameters: `key` : Optional ID string.  
   - Example Output: `{"key": "your_key", "value": "the fetched value from redis cache if available"}`
   - **Exceptions** : Will return 404 (`NotFoundException`) if the key doesn't exist.

---

### Core Gameplay Session Endpoints

The Game system is completely stateful using randomized sessions attached to `session_id`. Every step returns a standard `GameResponse` payload containing metadata and hints. 

#### Object Definitions

* **GuessInfo**
     - `word` (str): Suggested predicted word 
     - `info` (float): The entropy weight data of the prediction.

* **HistoryItem**
     - `guess` (str): Previous word user inputted 
     - `pattern` (str): Associated color pattern e.g `BGYGB`.

* **GameResponse** (Response object)
    - `session_id` (str): Reference session ID
    - `message` (str): System message detailing connection process or win-failure info
    - `remaining_count` (int?): Elements count representing remaining dictionary possible words matching puzzle history. Nullable.
    - `best_guesses` (List[GuessInfo]?): Sub object dictionary containing all predicted hints based on current state. Nullable.
    - `history` (List[HistoryItem]?): Ordered steps representing full game actions since step 1. Nullable.

#### 1. Start Session
Starts a completely new session from scratch for full dictionary processing.
- **Route:** `POST /start`
- **Body Requirement:**
  ```json
  {
      "session_id": "YOUR-UNIQUE-USER-ID"
  }
  ```
- **Responses:** Returns a complete `GameResponse` object. The `remaining_count` should start near ~23000 elements. The `best_guesses` fields would return optimal word suggestions. If start was completely transparent, it assigns `"message": "Session started"`.

#### 2. Process / Predict the next word
Apply a prediction input constraint (the user's move) against the active session dictionary.
- **Route:** `POST /predict_next_word`
- **Body Requirement:**
  ```json
  {
      "session_id": "YOUR-UNIQUE-USER-ID",
      "guess": "cigar",
      "pattern": "BBYGG" 
  }
  ```
- **Exceptions Mapping:**
      - `404 Not FoundException` - Issued if the `session_id` isn't found in memory cache, requiring the frontend to execute `/start` to reopen interaction loop.
      - `422 ValidationException` - Provided if `guess` formatting fails constraints, or if the `pattern` exceeds / fails 5 letters combinations rules. Also raised when your combination is impossible according to remaining vocabulary items.
      - `500 ServerErrorException` - Redis or algorithm backend failed internal mapping.

- **Responses:** It calculates and returns fully detailed `GameResponse` Object populated with new `remaining_count`, completely sorted `best_guesses`, and updated entire `history`.

#### 3. Close Session
Removes mapping state cache context of an active session manually, preventing redis leakage. Wait till puzzle ends completely to trigger this efficiently!
- **Route:** `POST /close`
- **Body Requirement:**
  ```json
  {
      "session_id": "YOUR-UNIQUE-USER-ID"
  }
  ```
- **Responses:** 
    - Output: `GameResponse` indicating message closure process. Example message output: `"Session closed and cache cleared"`.
- **Exceptions:**
    - `404 Not FoundException` : Triggers when attempting to delete a session_id that has already completed memory life cycle and was scrubbed inside Redis Backend cache!
