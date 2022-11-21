from flask import Flask
from flask_restful import Api

from resources.submissions import Submissions
from resources.image import Image
from resources.jobs import Job

app = Flask(__name__)
api = Api(app)

app.config['JOB_BUCKET'] = 'buggy-job-bucket'

api.add_resource(Submissions, '/submissions')
api.add_resource(Image, '/image')
api.add_resource(Job, '/job')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)