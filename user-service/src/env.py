import os
from dotenv import load_dotenv

if os.environ.get('ENV') == "dev":
    env_path = os.path.join(os.path.dirname(__file__), '../.env.local')
    load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.environ['DATABASE_URL']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']