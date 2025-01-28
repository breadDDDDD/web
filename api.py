from flask import Flask, jsonify, request
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
import os

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
                'name': 'file',
                'in': 'body',
                'required': True,
                'description': 'JSON payload with data',
                'schema': {
                    'type': 'object',
                    'properties': {
                        
                        'Name': {'type': 'string'}
                    },
                    'required': [ 'Name']
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

    

class excel(Resource):
    @swag_from({
        'responses': {
            200: {'description': 'Success'},
            404: {'description': 'File not found'}
        },
        'parameters': [
            {
                'name': 'filename',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Name file',
            }
        ]
    })
    
    def get(self):
        uploads_dir = 'uploads'
        filename = request.args.get('filename')

        if filename:
            file_path = os.path.join(uploads_dir, filename)
            if os.path.exists(file_path):
                return {"filename": filename, "message": "File found"}, 200
            else:
                return {"error": f"File {filename} not found"}, 404
        else:
            if not os.path.exists(uploads_dir):
                return {"error": "directionary does not exist"}, 404
            
            files = os.listdir(uploads_dir)
            return {"files": files}, 200

        
    @swag_from({
        'responses': {
            200: {'description': 'File uploaded successfully'},
            400: {'description': 'Error in file upload'}
        },
        'parameters': [
            {
                'name': 'file',
                'in': 'formData',
                'type': 'file',
                'required': True,
                'description': 'Upload an Excel file',
            }
        ]
    })
    
    def post(self):
        file = request.files['file']

        if file.filename == '':
            return {"error": "No selected file"}, 400

        save_path = os.path.join('uploads', file.filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)

        return {"message": f"File saved to {save_path}"}, 200
    
    @swag_from({
            'responses': {
                200: {'description': 'Success'},
                404: {'description': 'File not found'}
            },
            'parameters': [
                {
                    'name': 'filename',
                    'in': 'query',
                    'type': 'string',
                    'required': True,
                    'description': 'Name file',
                }
            ]
        })
    def delete(self):
        dir = 'uploads'
        file = request.args.get('filename')
        if file:
            file_path = os.path.join(dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                return {"filename": file, "message": "File deleted"}, 200
            else:
                return {"error": f"File {file} not found"}, 404
        else:
            if not os.path.exists(dir):
                return {"error": "Uploads directory does not exist"}, 404

class excel_all(Resource):
    @swag_from({
        'responses' : {
            200:{'description': 'succesful'},
            404 : {'d3escription' : 'failed'}
        }
    })
    def get(self):
        path ='uploads'
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return{"files": files}, 200
    
class function(Resource):
    @swag_from({
        'responses': {
            200: {'description': 'File uploaded successfully'},
            400: {'description': 'Error in file upload'}
        },
        'parameters': [
            {
                'name': 'file',
                'in': 'formData',
                'type': 'file',
                'required': True,
                'description': 'Upload an Excel file',
            }
        ]
    })
    def post(self):
        file = request.files['file']
        if file.filename =='':
            return {'description': 'error no file'},400
        file_proc = "uploadedFile.csv"
        file.save(file_proc)
        df = pd.read_csv(file_proc)
        target_val = df.iloc[:, -1]
        target = pd.DataFrame(target_val)
        target.to_csv(f"download\\target_val.csv")
        os.remove(file_proc)

        return {"message": "File saved"},200
    
    
class fuction_saving_pick(Resource):
    @swag_from({
         'responses' : {
            200:{'description': 'succesful'},
            404 : {'d3escription' : 'failed'}
        }
    })
    def get(self):
        dir = 'download'
        file_name = "target_val.csv"
        file_path = os.path.join(dir, file_name)
        file = pd.read_csv(file_path)
        file.to_csv(f"{os.getenv('USERPROFILE')}\\Downloads\\Target_val.csv")
        return {"message": "file has been saved"},200 
    
    @swag_from({
         'responses' : {
            200:{'description': 'succesful'},
            404 : {'d3escription' : 'failed'}
        }
    })
    def delete(self):
        dir = 'download'
        file = "target_val.csv"
        
        if file:
            file_path = os.path.join(dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                return{"message": "deleted"},200
            else:
                return{"message":"no file here"},400
        else:
            return{"message": "empty"},400

api.add_resource(Welcome, '/')
api.add_resource(name, '/name')
api.add_resource(excel, '/excel')
api.add_resource(excel_all, '/excel/all')
api.add_resource(function, '/function/target')
api.add_resource(fuction_saving_pick, '/function/gettingTarget')




if __name__ == '__main__':
    app.run(debug=True)