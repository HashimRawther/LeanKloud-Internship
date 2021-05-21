from flask import render_template, Flask, request
from flask_restplus import Api, Resource
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

login = api.namespace("login", "Logs in user and creates appropriate routes")
User = api.namespace("user", "Only READ permissions for normal user")
Admin = api.namespace("admin", "READ & WRITE permissions for Admin")

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "enaywnbd"
app.config['MYSQL_DB'] = "leankloud"

mysql = MySQL(app)

@login.route('/')
class Login(Resource):
    # def get(self):
    #     return render_template('index.html')

    def post(self):
        uname = request.form['username']
        pwd = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("select * from users")
        users = cur.fetchall()
        print(users)
        for user in users:
            if( user[0] == uname):
                if(user[1] == pwd):
                    if(user[2] == "write"):
                        @Admin.route('/')
                        class admin_task(Resource):
                            def get(self):
                                return "hello admin"
                    else:
                        @User.route('/')
                        class user_task(Resource):
                            def get(self):
                                return "hello user"
                    cur.close()

                    return 
                else:
                    cur.close()
                    return "Wrong Password"
        cur.close()
        return "Not Authorized"

if( __name__ == '__main__'):
    app.run(debug=True)