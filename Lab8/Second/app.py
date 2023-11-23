# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.database import db
from flasgger import Swagger
from CRUD import CRUDClass
from flasgger import swag_from
import time
from RAFT import RAFTFactory
import random

from electro_scooters import ElectroScooter

# Defining the service credentials.
service_info = {
    "host": "127.0.0.1",
    "port": 8001
}

# Stopping the start-up of the service for a couple of seconds to chose a candidate.
time.sleep(random.randint(1, 3))
# Creating the CRUD functionalities.
crud = RAFTFactory(service_info).create_server()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database2.db'
    db.init_app(app)

    # Initialize Swagger
    Swagger(app)

    return app


if __name__ == "__main__":
    app = create_app()
    import routes
    app.run(host=service_info["host"], port=service_info["port"])
