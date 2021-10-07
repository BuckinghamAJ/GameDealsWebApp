from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql

import json


with open('/Users/adambuckingham/Text_Files/gameDealsConfig.json') as config_file:
  config = json.load(config_file)



db_user = config.get("CheapEscapeDatabase_User")

db_pass = config.get("CheapEscapeDatabase_Password")


#ini
application = Flask(__name__)
secret_JWT_Key = config.get("SQLAlchemy_Key")
application.config['SECRET_KEY'] = secret_JWT_Key
application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@localhost/Game_Deals?charset=utf8mb4"

application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


gameDB = SQLAlchemy(application)


from cheapGameDeals import routes
