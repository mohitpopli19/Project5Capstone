import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abc@localhost:5432/capstoneagency'
SQLALCHEMY_DATABASE_URI = 'postgres://capstoneagency_user:Q7WDFzCqaxiVv7HrvhLCnSB0xYUhBmAW@dpg-chjd1ajhp8u4bdv2bp4g-a/capstoneagency'
