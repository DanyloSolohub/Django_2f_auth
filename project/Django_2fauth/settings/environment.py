import environ
import os

current_path = environ.Path(__file__) - 1
site_root = current_path - 2

env = environ.Env()
environ.Env.read_env(env_file=os.path.join(site_root, '.env'))

