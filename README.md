# FSND-capstone API

## About

This project demonstrates the API of a Capstone Agenct enabling retrieval, posting, patching and deleting Actors and Movies. The backend is designed to work for three types of users: Casting Assistant, Casting Director and Executive Producer. 

Authorization of users is enabled via Auth0 in which two seperate roles (Casting Assistant, Casting Director and Executive Producer) have been created and assigned seperate permissions.

The endpoints and how to send requests to these endpoints for actors and movies are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl or postman since there is no frontend for the app yet.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the warranty-tracker directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Gunicorn](https://pypi.org/project/gunicorn/)Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX. It’s a pre-fork worker model ported from Ruby’s Unicorn project. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resource usage, and fairly speedy.

# Deployment on Render

You need to deploy a Flask app and Postgres database on Render Console in the following steps:

1 Create a Render account
2 Set up a Database Service with Postgres
3 Configure Environment variables in Render
4 Deploy a Flask app with Render's Web Service and connect it with Database Service hosted 

Refer following URL for more details (https://render.com/docs/web-services)


## Running the server

To run the server, execute:

```bash
$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

**APP is hosted at render URL** https://capstoneagency-service-deployment.onrender.com/
**In local run it will run at** http://127.0.0.1:5000

Since I didn't build a frontend for the applicatio,n the endpoints have to be tested using curl or Postman. 


#### Project dependencies, local development and hosting instructions,

All dependencies are defined in requirements.txt file and use following command to install it:

pip install -r requirements.txt

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

Sourcing `setup.sh` sets some environment variables used by the app.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the this file to find the application.

## Models:

- **Movies** model defined with attributes title and release date
- **Actors** model defined with attributes name, age and gender

**AUTH0_DOMAIN**, **ALGORITHMS** and **API_AUDIENCE** are all available in the `setup.sh` file for reference.
Json Web Tokens: You can find **JWTs** for each role in the `setup.sh` file to run the app locally.


**Roles**: Below mentioned 3 roles have been setup in Auth0 and following permissions as shown for each role below are also defined in Auth0.

- **Casting Assistant** \* get:actors and get:movies
- **Casting Director**
  _ All permissions a Casting Assistant has and
  _ post:actors and delete:actors along with patch:actors and patch:movies
- **Executive Producer**
  _ All permissions a Casting Director has and
  _ post:movies and delete:movies



## API ARCHITECTURE AND TESTING
### Endpoint Library

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user. 

A token needs to be passed to each endpoint. 

The token can be retrived by following these steps:
Project uses Auth0 authentication to get role details through JWT. Postman collection has been created with jwt in PostmanCollection folder. 

Project uses Auth0 authentication to get role details through JWT. Postman collection has been created with jwt in PostmanCollection folder. 

link to generate new token in case required:

https://fsnd-mohit.us.auth0.com/authorize?audience=CapstoneAgency&response_type=token&client_id=PUwyES7f1ugWtPUS8nwtgatrAqpwuJQd&redirect_uri=https://localhost:8080/login-results

creds for different roles:

Casting Assitant Username - mohitthecastingassistant@gmail.com Password-Jaihanuki1*
Casting Director Username - mohitthecastingdirector@gmail.com Password-Jaihanuki1*
Executive Producer Username - mohittheexecutiveproducer@gmail.com Password-Jaihanuki1*

Some tests may break but that is just because a particular Id may not match. You can change param according to your table id column values for patch and delete to test those specific tests.


#### GET '/movies'
Returns a list of all available Movies.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://127.0.0.1:5000/movies 
Sample response output:
{
    "movies": [
        {

            "id": 52,
            "release_date": "Wed, 07 Aug 2030 18:30:00 GMT",
            "title": "KHK"
        },
        {
            "id": 53,
            "release_date": "Fri, 05 Jun 2043 18:30:00 GMT",
            "title": "DIEHARD"
        }
    ],
    "success": true,
    "total-movies": 2
}

#### POST '/movies'
Post a new movie with title and release date.
Sample curl: 
curl http://localhost:5000/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{
"title":"KANK",
"release_date":"1926-02-02"
}'
Sample response output:
{
    "movie-added": 4,
    "success": true
}

#### PATCH '/movies/{movie_id}'
Patch a movie with details.
Sample curl:
curl http://localhost:5000/movies/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{
"title":"KANK",
"release_date":"1926-02-02"
}''
{
    "movie-updated": 1,
    "success": true
}

#### DELETE '/movies/{movie_id}'
Deletes the Movie with id passed and returns success with MOvie id deleted.
curl http://localhost:5000/movies/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
    "movie-deleted": 1,
    "success": true
}

 
#### GET '/movies'
Returns a list of all available actors.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://127.0.0.1:5000/actors 
Sample response output:
{
    "actors": [
        {
            "age": 55,
            "gender": "Male",
            "id": 6,
            "name": "SRK"
        },
        {
            "age": 66,
            "gender": "Female",
            "id": 7,
            "name": "HEma"
        },
        {
            "age": 55,
            "gender": "Male",
            "id": 8,
            "name": "SRK"
        },
        {
            "age": 66,
            "gender": "Female",
            "id": 9,
            "name": "HEma"
        },
        {
            "age": 55,
            "gender": "Male",
            "id": 10,
            "name": "SRK"
        }
    ],
    "success": true,
    "total-actors": 5
}

#### POST '/actors'
Post a new movie with title and release date.
Sample curl: 
curl http://localhost:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{
 "name" : "KajolDevgan",
            "gender": "F",
            "age": 41
}'
Sample response output:
{
    "actor-added": 4,
    "success": true
}

#### PATCH '/actors/{actor_id}'
Patch a actor with details.
Sample curl:
curl http://localhost:5000/actors/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{
"title":"KANK",
"release_date":"1926-02-02"
}''
{
    "actor-updated": 1,
    "success": true
}

#### DELETE '/actors/{actor_id}'
Deletes the Actor with id passed and returns success with Actor id deleted.
curl http://localhost:5000/actors/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
    "actor-deleted": 1,
    "success": true
}






## Testing
There are 25 unittests in test_app.py. To run this file use:
```
dropdb capstoneagency
createdb capstoneagency
python -m unittest test_app.py
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.
Further, the file 'CapstoneAgency.postman_environment.json' contains postman tests containing tokens for specific roles.
To run this file, follow the steps:
1. Go to postman application.
2. Load the collection --> Import -> Capstone Agency/CapstoneAgency.postman_collection.json
3. Click on the runner, select the collection and run all the tests.

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT TOken for different roles

The JWT token contains the permissions for the all 3 roles mentioned in ROles section above.

## DEPLOYMENT
The app is hosted live on Render at the URL: 
https://capstoneagency-service-deployment.onrender.com/

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman

### Thank You!
