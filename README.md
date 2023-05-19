APP is hosted at https://capstoneagency-service-deployment.onrender.com/
In local run it will run at http://127.0.0.1:5000

Since it contains only backend so endpoints are accessible from postman.

Endpoints:
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/

Roles:
Casting Assistant
Can view actors and movies
Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies
Executive Producer
All permissions a Casting Director has and…
Add or delete a movie from the database




Project uses Auth0 authentication to get role details through JWT. Postman collection has been created with jwt in PostmanCollection folder. 

link to generate new token in case required:

https://fsnd-mohit.us.auth0.com/authorize?audience=CapstoneAgency&response_type=token&client_id=PUwyES7f1ugWtPUS8nwtgatrAqpwuJQd&redirect_uri=https://localhost:8080/login-results

Casting Assitant Username - mohitthecastingassistant@gmail.com Password-Jaihanuki1*
Casting Director Username - mohitthecastingdirector@gmail.com Password-Jaihanuki1*
Executive Producer Username - mohittheexecutiveproducer@gmail.com Password-Jaihanuki1*

Some tests may break but that is just because a particular Id may not match. You can change param according to your table id column values for patch and delete to test those specific tests.