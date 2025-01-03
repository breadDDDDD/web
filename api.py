from flask import Flask, jsonify, request
import numpy as np
import matplotlib.pyplot as plt
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3
}
swagger = Swagger(app)
name_user_data = [
    {'Id': 0, 'Name': 'jane doe',},
    ]

class Welcome(Resource):
    @swag_from({
        'responses': {200: {}}
    })
    def get(self):
        return {'message': 'hello'}

class name(Resource):
    @swag_from({
        'responses': {200: {'description': 'Name user data successfully fetched'}}      
    })
    def get(self):
        return name_user_data
    
    @swag_from({
        'responses': {
            201: {'description': 'Name user data successfully added'},
            404: {'description': 'error'}
        },
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'description': 'JSON payload with name data',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'Id': {'type': 'integer'},
                        'Name': {'type': 'string'}
                    },
                    'required': ['Id', 'Name']
                }
            }
        ]
    })
    def post(self):
        data = request.get_json()
        new_id = name_user_data[-1]['Id'] + 1
        new_user = {'Id': new_id, 'Name': data['Name'],}
        name_user_data.append(new_user)
        return new_user, 201
    
api.add_resource(Welcome, '/')
api.add_resource(name, '/name')



if __name__ == '__main__':
    app.run(debug=True)