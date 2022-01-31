from dotenv import load_dotenv
import os

load_dotenv()

env_vars = ["TRANSITLAND_API_KEY"]

env = {key: os.environ[key] for key in env_vars}
