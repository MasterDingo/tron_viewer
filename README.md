# TRON Viewer
Just an example of working with Tronpy + FastAPI

Use `docker compose build` to build the development environment and `docker compose up` to run it.
The API is accessible at http://localhost:8000. Use POST request to fetch data from TRON network and GET request to get the history of previous POST requests.
When fetching the data, the request body must contain valid JSON data: `{"address": "<TRON address>"}`
Use `docker compose -f docker-compose.tests.yml build` to build the test environment and then `docker compose -f docker-compose.tests.yml up` to run tests.
Production environment is available after `docker compose build` && `docker compose up`.

Environment variables:
- TRON_NETWORK - TRON network name (like `nile`, `shasta` or `tronex`) or URL starting with `http://` or `https://` for private network, or empty for main TRON network
- TRON_API_KEY - API key, if needed. May be empty for test networks
- TRON_TIMEOUT - timeout for requests to TRON network
Production environment has 2 additional variables:
- SSL_CERTIFICATE - file name of SSL ceritficate
- SSL_CERTIFICATE_KEY - file name of SSL certificate private key

Certificate must be inside the folder `ssl/certs` and the private key inside of `ssl/private`.
If you are not planning to use SSL and want to just stick to HTTP, just leave those environment variables empty.

See `.env.dev`, `.env.prod.example` and `tests/.env.tests` for examples.