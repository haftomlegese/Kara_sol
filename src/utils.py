import os
from dotenv import load_dotenv

def load_env_vars():
    load_dotenv()

def get_env_var(var_name):
    return os.getenv(var_name)

