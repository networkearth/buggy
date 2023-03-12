"""
App Runner
"""

import os
from project import create_app

if __name__ == "__main__":
    create_app(
        api_uri=os.environ['INATURALIST_API'],
        webapp_uri=os.environ['INATURALIST_WEBAPP'],
        backup_path=os.environ['BUGGY_BACKUP_PATH']
    ).run(host='0.0.0.0', port=5002)
