# configurations for my app

import uuid

# Enable Flask's debugging features. Should be False in production
DEBUG = True
SESSION_TYPE = 'filesystem'
SECRET_KEY = str(uuid.uuid4())
