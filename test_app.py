import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

# TEST CASE CLASS


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = 'postgresql://postgres:abc@localhost:5432/capstoneagency'
        Castingassistant_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJkOThkeXFKU21vUHJEVEw3ejVvUyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbW9oaXQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0NjY1YjU4OTJlODNjMmQxOTJlYjQ0YSIsImF1ZCI6IkNhcHN0b25lQWdlbmN5IiwiaWF0IjoxNjg0NDMwNDg3LCJleHAiOjE2ODQ1MTY4ODYsImF6cCI6IlBVd3lFUzdmMXVnV3RQVVM4bnd0Z2F0ckFxcHd1SlFkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.YAXS9u8dNJ0qRmWccdeR4bo-s4QkjZHwoRoOoC9Ac2IdzlOOsqWE-6CYTAGkQVj2n-u2FBBfK086cls58tSfClvI1yfdiQeMhRhciW19d0C3lCQEDNjwoDWhXsc3i4v2lbrR9ltlVGz9c8wcPdR20KzH0VJsEjMJtWnrl9RFf4vd6jZyP5vy2n6CSADAhCRZYFtv4MHoRFIX-k627syB5I_PrEuK0CGBHb37ZTCOyKR_r3SRpop7kXnFc90zoin1Nmmp7I_IrlsxUTN15jOT7pmaAspqYDcI6XL7PAoCbN_WmF8PhL3u34HM5mEyr7hiiVfJtjmbv9rZrKgxw6A_2g'
        CastingDirector_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJkOThkeXFKU21vUHJEVEw3ejVvUyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbW9oaXQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0NjY1YmExNzA2OWI4M2E5NDFmNDY0OSIsImF1ZCI6IkNhcHN0b25lQWdlbmN5IiwiaWF0IjoxNjg0NDMwNzcxLCJleHAiOjE2ODQ1MTcxNzAsImF6cCI6IlBVd3lFUzdmMXVnV3RQVVM4bnd0Z2F0ckFxcHd1SlFkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.AkDqnLeQ8Sn1XPYGx3MW_7uKX3-9yGRqzmtEYxhd8WMgUnGUkNatq6VRiuOe-yRW9AfpzapXQA0T4cgZDtHRFIqoflAYYI5bDNl8mi20VYjwPbKVFpwSAZV51V90X1bfXIaFhLG08PgkyClxkkeEWSwX4Zh_RMsBVpZYF4-9xwis4aNwoZ3CgV7oeE0i94OgeYhzdXnpDIN5wouMdI6OUWP8cxMdxPRl84zfszs1K2FruXwG8JZdHuUsVXDk10N0Wz236n7oGl6nP9WpNnP76oNJW0bt3CRwWJbJFjAVRdLyRacAM5pJ14qnWpIgYF0GMQp926LWBlQFzozKQqWtNg'
        ExecutiveProducer_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJkOThkeXFKU21vUHJEVEw3ejVvUyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbW9oaXQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0NjY1YmQ5ZDcwZmMzYTY0YjA4OTk3OSIsImF1ZCI6IkNhcHN0b25lQWdlbmN5IiwiaWF0IjoxNjg0NDMwOTMwLCJleHAiOjE2ODQ1MTczMjksImF6cCI6IlBVd3lFUzdmMXVnV3RQVVM4bnd0Z2F0ckFxcHd1SlFkIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Mf8XASw_VyHtKRZy5F_t5wo42nNOYNMeVTyWNu7PIHqqYvdRDuYMTy8fwsf2RoIoyRijrejrzxvaJDxx1ysGgOHTzq3RU-Tv_Eup0I0PNB7cNgd5OivsPRo6MjBX9PZLzbvc_yemq1B0yJusedFCDuF54Plat7-aNiunwkG1LQaSeFDTmMd0IRx56KmGUDU7MPt6Q-tXtyJbKCE_rMoDIDiYMM4sxY3EMDJEQu2tjcfTm2uY45BEr6fL_-urrNcz70qe4n2xfoTEjdhd1r90tpwfxB9w7Bn8soPcLVm7eJ4k5hPOHYmkhfeVDyrs-qguXmNx-nYSMKKOr-sIqGSsJw'

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
