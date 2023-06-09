import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies
from dotenv import load_dotenv

# TEST CASE CLASS

load_dotenv()

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = os.environ.get('DATABASE_URL')
        Castingassistant_TOKEN = os.environ.get('ASSISTANT_TOKEN')
        CastingDirector_TOKEN = os.environ.get('DIRECTOR_TOKEN')
        ExecutiveProducer_TOKEN = os.environ.get('PRODUCER_TOKEN')

        self.assistant_auth_header = {'Authorization':'Bearer ' + Castingassistant_TOKEN}
        self.director_auth_header = {'Authorization':'Bearer ' + CastingDirector_TOKEN}
        self.producer_auth_header = {'Authorization':'Bearer ' + ExecutiveProducer_TOKEN}
        self.database_path = DATABASE_URL

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)


# Test data preparation

        self.post_actor = {
            'name': "SRK",
            'age': 55,
            'gender': 'M'
        }

        self.post_actor1 = {
            'name': "Kajol",
            'age': 32,
            'gender': 'F'
        }

        self.post_actor2 = {
            'name': "Amitabh",
            'age': 69,
            'gender': 'M'
        }

        self.actor_without_name = {
            'age': 34,
            'gender': "M"
        }

        self.actor_without_gender = {
            'age': 34,
            'name': "Amitabh"
        }

        self.post_actor_age = {
            'age': 55
        }

        self.post_movie = {
            'title': "KKHH",
            'release_date': "2020-07-12"
        }

        self.post_movie1 = {
            'title': "KHK",
            'release_date': "2030-08-08"
        }

        self.post_movie2 = {
            'title': "DIEHARD",
            'release_date': "2043-06-06"
        }

        self.movie_with_title_missing = {
            'release_date': "2030-10-10"
        }

        self.movie_with_releasedate_missing = {
            'title': "RAMAYANA"
        }

        self.path_releasedate = {
            'release_date': "2035-10-10"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()


# RBAC Test cases:


# RBAC POST movies with wrong Authorization header - Director Role
    def test_post_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.post_movie1, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    def test_post_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.post_movie1, headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    def test_post_movie_right_auth(self):
        res = self.client().post('/movies', json=self.post_movie1, headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_wrong_auth(self):
        res = self.client().delete('/movies/15', headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    def test_delete_movie_wrong_auth1(self):
        res = self.client().delete('/movies/15', headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    def test_delete_movie_right_auth(self):
        res = self.client().post('/movies', json=self.post_movie,headers=self.producer_auth_header)
        data = json.loads(res.data)
        movie_id = data['movie-added']
        # try deleting the movie
        res = self.client().delete('/movies/{}'.format(movie_id), headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)


# Actors endpoint test cases

# Casting Assistant Get Positive Test
    def test_get_actors1(self):
        res = self.client().get('/actors', headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# Director Get Positive Test
    def test_get_actors2(self):
        res = self.client().get('/actors', headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# Producer Get Positive Test
    def test_get_actors3(self):
        res = self.client().get('/actors', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data['total-actors'], 0)

# POST Positive case - Director Role
    def test_post_new_actor1(self):
        res = self.client().post('/actors', json=self.post_actor1, headers=self.director_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['actor_inserted']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# PATCH Positive case - Update age of an existing by Director
    def test_patch_actor(self):
        res = self.client().post('/actors', json=self.post_actor1, headers=self.director_auth_header)
        data = json.loads(res.data)
        actor_id = data['actor_inserted']
        res = self.client().patch('/actors/{}'.format(actor_id),
                                  json=self.post_actor_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor-updated'], actor_id)

# PATCH Negative case - Update age for non-existent actor
    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/99',
                                  json=self.post_actor_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')


# POST Positive case - Producer Role
    def test_post_new_actor2(self):
        res = self.client().post('/actors', json=self.post_actor2, headers=self.producer_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['actor_inserted']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# POST Negative Case - Add actor with missing name
    def test_post_new_actor_name_missing(self):
        res = self.client().post('/actors', json=self.actor_without_name, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add actor with missing gender - Director Role
    def test_post_new_actor_gender_missing(self):
        res = self.client().post('/actors', json=self.actor_without_gender, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing actor - Director Role
    def test_delete_actor(self):
        # add actor first
        res = self.client().post('/actors', json=self.post_actor, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        actor_id = data['actor_inserted']

        # try delete actor 
        res = self.client().delete('/actors/{}'.format(actor_id),
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor-deleted'], actor_id)

# DELETE Negative Case actor not found - Director Role
    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/123', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')



# Movies endpoint test cases - Assistant, Director and Producer role


    def test_get_movies1(self):
        res = self.client().get('/movies', headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertNotEqual(data['total-movies'], 0)

# GET Positive case - Director Role
    def test_get_movies2(self):
        res = self.client().get('/movies',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# GET Positive case - Producer Role
    def test_get_movies3(self):
        res = self.client().get('/movies', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertNotEqual(data['total-movies'], 0)

# POST Positive case - Producer Role
    def test_post_new_movie2(self):
        res = self.client().post('/movies', json=self.post_movie2, headers=self.producer_auth_header)
        data = json.loads(res.data)
        movie = Movies.query.filter_by(id=data['movie-added']).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)

# POST Negative Case - Add movie with missing title
# - Producer Role
    def test_post_new_movie_title_missing(self):
        res = self.client().post('/movies',
                                 json=self.movie_with_title_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case 
    def test_delete_movie(self):
        # add movit first
        res = self.client().post('/movies', json=self.post_movie,headers=self.producer_auth_header)
        data = json.loads(res.data)
        movie_id = data['movie-added']
        # try deleting the movie
        res = self.client().delete('/movies/{}'.format(movie_id), headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-deleted'], movie_id)

# DELETE Negative Case movie not found
    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/77', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update Release Date of by  Director Role
    def test_patch_movie(self):
        res = self.client().post('/movies', json=self.post_movie,headers=self.producer_auth_header)
        data = json.loads(res.data)
        movie_id = data['movie-added']
        res = self.client().patch('/movies/{}'.format(movie_id), json=self.path_releasedate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-updated'], movie_id)

# PATCH Negative case - Update Release Date for non-existent movie by Director Role
    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/222', json=self.path_releasedate, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')



# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()
