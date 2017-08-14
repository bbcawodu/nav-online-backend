# Patient Assist Browsing Data Backend Servers

## Installation
- Clone Repository
- Download and install python 2.7 and virtualenv
- Install PostgresSQL and create local database with privileges granted to a user.
- Install the Heroku developer toolbar.

## Local Installation
- Change dir to project directory.
- Start virtual environment
- Run ```pip install -r requirements.txt```
- Add $PORT and $DATABASE_URL environment variables to your local machine and add the project directory to your PYTHONPATH variable.
    - $PORT corresponds to the port number that the crossbar router worker will use to make HTTP connections
    - $DATABASE_URL corresponds to the url that the app will use to connect to your postgres db
        - The format should be: ```postgres://<db username>:<password>@localhost:<postgres port #>/<db name>```
- Make the migrations to your local db using the following command ```alembic upgrade head```
- You can now run the app locally using either of the following commands:
    - ```crossbar start```
    - ```heroku local```
    
## Heroku Deployment Instructions
- Create app, provision db, and connect app to a git repo
- Updates to app will now be connected to commits to the git repo
- NOTE: Don't forget to run migrations on the production db as well

## User Stories for the Backend Servers
- User stories for the backend servers.

    ### [User Stories for the Backend Servers](documentation/user_stories/index.md)

## API Docs
- Documentation for the API that the backend servers provide.

    ### [Connecting to Browsing Data Backend Servers README](documentation/connecting_to_backend_servers.md)
    
    ### [Browsing Data Backend Servers API README - Presence Health](documentation/backend_server_api_documentation/presence_health/index.md)

## Database ERD
- Entity Relational Diagram for the database that the backend servers use.

    ### [Browsing Data Backend Database ERD](documentation/db_erds/full_db_erd.jpg)