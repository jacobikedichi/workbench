### Comments ###

_This project is intended to showcase Django Rest Framework at work._


A comment API using the Django REST Framework. It allows users to submit comments associated with a predifined content URLs, or retrieve a list of comments associated with a content URL.  
Content URL:  
/Facebook  
/BestBuy  
/Walmart  

The specs below are used to design the application, puting limitation on how (often) users interact with our system.

* All requests goes through the Django REST Framework.
* A Create (POST) end-point takes the following fields and save them to the database: Username, Comment, content URL.
* A List (GET) end-point takes a content URL and return a list of all previously submitted comments matching that content URL.
* Any IP Address adding more than 2 comments in 1 minute gets their request rejected and locked out for 5 minutes.
* Any Comment that is an exact duplicate of an existing comment posted within the last 24 hours gets rejected and the originating IP Address gets locked out for 1 minute.
* The API uses a rate limiter (throtler) to prevent users from making more than 20 requests (POST and GET) per minute.

##### Configuration notes #####
By default, we are using the default SQLite database configuration that our django application came with. This is encouraged for local development use.  
In other deployment environment (i.e. Production, Staging, Testing and Development), we are storing all secrets/values in a .env file at the root of this application. Of course the .evn file is not, and should never be checked into source control.  
Our favorite litmus test in making sure that there is a clear seperation between code and sensitive configuration data is this: Can we make or source code an open source project without compromising sensitive information?  

If you wish to set this project up with a more industrial RDMS system (i.e. MySQL, PostgreSQL, Orancle, etc), go ahead and create a .env file at the root of this project. In your .env file, add a section called 'database' and define the following paramters: DB\_ENGINE, DB\_NAME, DB\_USER, DB\_PASSWORD, DB\_HOST, DB\_PORT.  
For example:  

[database]  
DB\_ENGINE = "engine value"  
DB\_NAME = "db name"  
DB\_USER = "db user"  
DB\_PASSWORD = "my db password!"  
DB\_HOST = "db host"  
DB\_PORT = "port"  

If you are using PostgreSQL, be sure to install the following dependencies: build-dep, python-psycopg2. On an ubuntu system, do:
```bash
 sudo apt-get build-dep python-psycopg2 #psql dependencies
 sudo apt-get install postgresql-client #psql client
```
