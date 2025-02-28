# Documentation of the communication

The system consists out of four segments
* A database for storage of the different processes
* A backend server which interacts between database/process engine and frontend server
* A frontend server which communicates with the frontend
* A future process engine, which performs the business logic

## Running the flask server which represents the backend (handles queries and connects to the engine)

`python.exe -m source.backend.server`

## Running webserver (presents the webpage)

`python.exe -m source.frontend.frontend`