import os
import json
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth
from dotenv import load_dotenv


Number_Of_Questions_Per_Page = 12
load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # app.config.from_object('config')
    setup_db(app)
    CORS(app)

    '''
    CORS Headers
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    def pagination_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * Number_Of_Questions_Per_Page
        end = start + Number_Of_Questions_Per_Page

        formatted_record = [record.format() for record in selection]
        page_records = formatted_record[start:end]

        return page_records

    '''
    Test Method
    '''

    @app.route('/', methods=['GET'])
    def get_init():
        return jsonify({
            'success': True,
            'SampleTest': 'Hello from Capstone Agency'
        })

    '''
    Implemented endpoint GET /actors
    - it will GET all actors with their description
        - it will require the 'get:actors' permission
        - returns status code 200 and json {"success": True,
            "actors": actors, "total-actors": len(actors)} where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''

    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.order_by(Actors.id).all()
            return jsonify({
                'success': True,
                'actors': [record.format() for record in actors],
                'total-actors': len(actors)
            })
        except Exception:
            abort(422)

    '''
    Implemented endpoint POST /actors
        - it will create a new row in the Actors table
        - it will require the 'post:actors' permission
        - returns status code 200 and json {"success": True,
            "actor_inserted": new_actor.id} where actor is Id of the inserted actor
            the newly created actor
            or appropriate status code indicating reason for failure
    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def post_actors(payload):
        new_actor = request.get_json()
        actor_name = new_actor.get('name')
        actor_gender = new_actor.get('gender')
        actor_age = new_actor.get('age')

        if (actor_name is None) or (actor_gender is None) or (actor_age is None):
            abort(422)

        try:
            new_actor = Actors(name=actor_name,
                               gender=actor_gender,
                               age=actor_age)
            new_actor.insert()

            return jsonify({
                "success": True,
                "actor_inserted": new_actor.id
            })

        except Exception:
            abort(422)

    '''
    Implemented endpoint PATCH /actors/<id>
        - where <id> is the existing actors id
        - it will respond with a 404 error if <id> is not found
        - it will update the corresponding row for <id> and require 'patch:actors' permission
        - returns status code 200 and json {"success": True,
            "actor-updated": actor.id} where actor-updated is updated actor id
            the updated actor or appropriate status code indicating
            reason for failure
    '''

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def patch_actors(payload, id):
        actor = Actors.query.filter(Actors.id == id).first()
        if not actor:
            abort(404)

        updated_actor_details = request.get_json()

        if updated_actor_details is None:
            abort(422)

        try:
            if 'name' in updated_actor_details:
                actor.name = updated_actor_details['name']

            if 'gender' in updated_actor_details:
                actor.gender = updated_actor_details['gender']

            if 'age' in updated_actor_details:
                actor.age = updated_actor_details['age']

            actor.update()

            return jsonify({
                "success": True,
                "actor-updated": actor.id
            })

        except Exception:
            abort(422)

    '''
    Implemented endpoint DELETE /actors/<id>
        - where <id> is the existing actors id
        - it will delete the corresponding row for <id>
        - it will respond with a 404 error if <id> is not found
        - it will require the 'delete:actors' permission
        - returns status code 200 and json {"success": True,
            "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actors(payload, id):
        actor = Actors.query.filter(Actors.id == id).first()
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                "success": True,
                "actor-deleted": actor.id
            })

        except Exception:
            abort(422)

    '''
    Implemented endpoint GET /movies
        - it will GET all movies with their release date
        - it will require the 'get:movies' permission
        - returns status code 200 and json {"success": True,
            "movies": movies, 'total-movies': len(movies)} where movies is the list of movies and total-movies is total number of movies
            or appropriate status code indicating reason for failure
    '''

    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.order_by(Movies.id).all()
            return jsonify({
                'success': True,
                'movies': [record.format() for record in movies],
                'total-movies': len(movies)
            })
        except Exception:
            abort(422)

    '''
    Implemented endpoint POST /movies
        - it will create a new row in the Movies table
        - it will require the 'post:movies' permission
        - returns status code 200 and json {"success": True,
            "movies": movies} where movie is an array containing only 
            the newly created movie
            or appropriate status code indicating reason for failure
    '''

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movies(payload):
        add_movie = request.get_json()
        movie_title = add_movie.get('title')
        movie_rls_date = add_movie.get('release_date')

        if movie_title is None:
            abort(422)

        if movie_rls_date is None:
            abort(422)

        try:
            new_movie = Movies(title=movie_title,
                               release_date=movie_rls_date)
            new_movie.insert()

            return jsonify({
                "success": True,
                "movie-added": new_movie.id
            })

        except Exception:
            abort(422)

    '''
    Implemented endpoint PATCH /movies/<id>
        - where <id> is the existing movies id
        - it will respond with a 404 error if <id> is not found
        - it will update the corresponding row for <id>
        - it will require the 'patch:movies' permission
        - returns status code 200 and json {"success": True,
            "movie-updated": movies} where movie-update is an Id of the movie updated
            the updated actor or appropriate status code indicating
            reason for failure
    '''

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def patch_movies(payload, id):
        movie = Movies.query.filter(Movies.id == id).first()

        if not movie:
            abort(404)

        updated_movie_details = request.get_json()

        try:
            if 'title' in updated_movie_details:
                movie.title = updated_movie_details['title']

            if 'release_date' in updated_movie_details:
                movie.release_date = updated_movie_details['release_date']

            movie.update()

            return jsonify({
                "success": True,
                "movie-updated": movie.id
            })

        except Exception:
            abort(422)

    '''
    Implemented endpoint DELETE /movies/<id>
        - where <id> is the existing movies id
        - it will delete the corresponding row for <id>
        - it will require the 'delete:movies' permission
        - returns status code 200 and json {"success": True,
            "delete": id} where id is the id of the deleted movie
            or appropriate status code indicating reason for failure
    '''

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movies(payload, id):
        movie = Movies.query.filter(Movies.id == id).first()

        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                "success": True,
                "movie-deleted": movie.id
            })

        except Exception:
            abort(422)

    '''
    Error handlers for possible errors including 400, 401, 403,
    404, 405, 422 and 500.
    '''

    @app.errorhandler(400)
    def badRequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def notAllowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not Allowed"
        }), 405

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def accessForbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Access Denied/Forbidden"
        }), 403

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def serverError(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error
        }), e.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
