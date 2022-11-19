from flask import Flask
from flask_restful import Api

from resources.submissions import Submissions
from resources.image import Image

app = Flask(__name__)
api = Api(app)

api.add_resource(Submissions, '/submissions')
api.add_resource(Image, '/image')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)