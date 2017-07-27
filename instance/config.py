# configurations for my app

import uuid

# Enable Flask's debugging features. Should be False in production
DEBUG = True

# Sessions configurations
SESSION_TYPE = 'filesystem'
SECRET_KEY = str(uuid.uuid4())

# Database Configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://bucketlist_api:easyPassword@localhost:5432/bucketlist_app'
