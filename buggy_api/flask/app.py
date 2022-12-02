from argparse import Namespace
import os
from project import create_app

if __name__ == "__main__":
   create_app(
      environment=os.environ['APP_ENVIRONMENT'],
      namespace=os.environ['APP_NAMESPACE'],
      account=os.environ['APP_ACCOUNT'],
      region=os.environ['APP_REGION']
   ).run(host='0.0.0.0', port=5002)