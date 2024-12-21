# TRON Viewer
Just an example of working with Tronpy + FastAPI

Use `docker compose build` to build the development environment and `docker compose up` to run it.
The API is accessible at http://localhost:8000. Use POST request to fetch data from TRON network and GET request to get the history of previous POST requests.
When fetching the data, the request body must contain valid JSON data: `{"address": "<TRON address>"}`
Use `docker compose -f docker-compose.tests.yml build` to build the test environment and then `docker compose -f docker-compose.tests.yml up` to run tests.

Environment variables:
- TRON_NETWORK - TRON network name (like `nile`, `shasta` or `tronex`) or URL starting with `http://` or `https://` for private network, or empty for main TRON network
- TRON_API_KEY - API key, if needed. May be empty for test networks
- TRON_TIMEOUT - timeout for requests to TRON network

See `.env.dev` and `tests/.env.tests` for examples.