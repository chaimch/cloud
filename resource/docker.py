import docker
from flask_restful import Resource


class DockerResource(Resource):
    def __init__(self):
        self.docker_client = docker.from_env()
