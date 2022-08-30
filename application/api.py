from application import app
from flask_restful import Resource,Api

api = Api(app)
#test api
class Helloworld(Resource):
    def get(self):
        return {"data": "Hello World"}

api.add_resource(Helloworld,"/helloworld")

