# Origin Backend Take-Home Assignment - Matheus Mansour

Python FastAPI

### Technologies

- Python 3.9
- FastApi - Framework
- Docker - Project Structure
- Docker-compose - Development Environment
- Poetry - Libraries management tool for Python.


### How to use?

1. Clone this repository
2. Install the required technologies (Python, Docker, Poetry, Make)
3. Setup your .env file in root directory, defining your local FASTAPI_PORT (e.g. FASTAPI_PORT=8080)
4. Build docker image and run application: `make build` or the equivalent command in Makefile.
5. Check the logs with `make logs` or the equivalent command in Makefile.
6. Run the tests with `make tests` or the equivalent command in Makefile.
7. In your browser call: [Swagger Localhost](http://0.0.0.0:8080/docs/) to check the API Swagger
8. Check the logs with `make logs` or the equivalent command in Makefile.
9. Start making your calls :)


### Main technical decisions and relevant comments

The main technical decision made in order to build this API was to use a  robust file structure to make it as general and extensible as possible.
Every class and function has been located as to allow for future API endpoints and versions to be built upon it.

Every method in the RiskProfileService class has been built as to be unit
testable and return granular information (e.g. risk scores).
