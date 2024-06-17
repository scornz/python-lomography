from dotenv import load_dotenv
from lomography.base import Lomography
from lomography.utils.requests import get
from os import environ

load_dotenv()
lomo = Lomography(api_key=environ["LOMOGRAPHY_API_KEY"])
lomo.close()
