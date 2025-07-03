import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_source_engine():
  return create_engine(os.getenv('SOURCE_DB_URL'))

def get_target_engine():
  return create_engine(os.getenv('TARGET_DB_URL'))