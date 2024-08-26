from dotenv import load_dotenv
import os
from pathlib import Path

config_dir = Path(__file__).resolve().parent
print(config_dir)
load_dotenv(dotenv_path=config_dir.parent.parent / '.env')

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
