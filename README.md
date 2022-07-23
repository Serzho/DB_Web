# Database_Server
## Server
Database server with API and authentication.   
Using SQLAlchemy, FastAPI and Unicorn 

## Installation requirements  
`$pip install -r requirements.txt`  

## Starting
Server starting by server/server.py  
Database with auth information saving in file server/tmp/auth.db
Database for users saving in file server/tmp/database.db

## Functional
For using database you shoud auth by `/auth [name] [password]`
For adding and deletion new users you must auth to user with admin root
In database saving information by KEY:VALUE, also table in database contains ID, ID of author, time of creation

## Client
Client starting by client/client.py  
Using requests.   
Print `/help` to get list of supported commands   
