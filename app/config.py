from os import environ as env, path
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRETS_ENV= env['secretkey']
    USERNAME_ENV= env['ruser']
    PASSWORD_ENV= env['rpassword']    

class DevConfig(Config):
    FLASK_ENV = "development" 


class ProdConfig(Config):
    FLASK_ENV = "production" 


config = {
    'dev': DevConfig,
    'prod' : ProdConfig,
    'default' : DevConfig
}