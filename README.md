# FSND-capstone

## CASTING AGENCY

This Application will allow to add movies and actors details that can help agency to maintain database and hire actors for different movies.

**APP is hosted at** https://capstoneagency-service-deployment.onrender.com/
**In local run it will run at** http://127.0.0.1:5000

Since it contains only backend so endpoints are accessible through postman collection in the repo. 

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.


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


## Endpoints:

```python
GET /actors &  /movies
DELETE /actors/<int:id> & /movies/<int:id>
POST /actors & /movies
PATCH /actors/<int:id> & /movies/<int:id>
```

All  Endpoints are created in `app.py` file.

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


**AUthentication Setup**

Project uses Auth0 authentication to get role details through JWT. Postman collection has been created with jwt in PostmanCollection folder. 

link to generate new token in case required:

https://fsnd-mohit.us.auth0.com/authorize?audience=CapstoneAgency&response_type=token&client_id=PUwyES7f1ugWtPUS8nwtgatrAqpwuJQd&redirect_uri=https://localhost:8080/login-results

creds for different roles:

Casting Assitant Username - mohitthecastingassistant@gmail.com Password-Jaihanuki1*
Casting Director Username - mohitthecastingdirector@gmail.com Password-Jaihanuki1*
Executive Producer Username - mohittheexecutiveproducer@gmail.com Password-Jaihanuki1*

Some tests may break but that is just because a particular Id may not match. You can change param according to your table id column values for patch and delete to test those specific tests.

### Thank You!
