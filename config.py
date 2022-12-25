from app import app
from flaskext.mysql import MySQL

mySQL = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'rest-py'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mySQL.init_app(app)