import datetime, json
from json import JSONEncoder
from flask import render_template, Flask, request, redirect, make_response
from flask_restplus import Api, Resource, reqparse, inputs
from flask_mysqldb import MySQL


app = Flask(__name__)
api = Api(app)

user_type = "user"

login = api.namespace("login", "Logs in user and creates appropriate routes")
task_route = api.namespace("tasks", "View / Create / Modify tasks")

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "enaywnbd"
app.config['MYSQL_DB'] = "leankloud"

mysql = MySQL(app)

# Argument parsers for handling request Body
cred_parser = reqparse.RequestParser()
cred_parser.add_argument("username", type = str, help = "Username of user" , required=True)
cred_parser.add_argument("password", type = str, help = "Password of user" , required=True)

task_parser = reqparse.RequestParser()
task_parser.add_argument("task", type = str, required=True)
task_parser.add_argument("due", type = inputs.date, required=True)
task_parser.add_argument("status", type = str, required=True)

status_parser = reqparse.RequestParser()
status_parser.add_argument("status", type = str, required=True)

# GET for getting all tasks
# POST for adding a task
@task_route.route('')
class task_getAll_postOne(Resource):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute("select * from tasks")
        tasks = cur.fetchall()
        task_list =  []
        for task in tasks:
            new_task = dict()
            new_task['task_id'] = task[0]
            new_task['task'] = task[1]
            new_task['due'] = task[2].strftime('%Y-%m-%d')
            new_task['status'] = task[3]
            #task = json.dumps(task, default =str)
            task_list.append(new_task)
        return task_list
        
    def post(self):
        global user_type
        db = mysql.connection
        cur = db.cursor()
        task_details = task_parser.parse_args()

        task = task_details['task']
        due = task_details['due']
        due = due.date()
        # print(due)
        #due = datetime.date()
        status = task_details['status']

        # Getting the state of task list from DB 
        # Increment task_id
        cur.execute("select max(taskid) from tasks")
        taskid = cur.fetchone()
        taskid = taskid[0] + 1
        # print(taskid)
        cur.execute("""insert into tasks values(%s, %s, %s, %s)""", (taskid, task, due, status))
        db.commit()
        return  "Task Added"
        # if user_type == "admin":
        #     pass
        # else:
        #     return "Only Admins can create / modify"

# GET a specific task using task_id
# PUT to change task status using task_id
@task_route.route('/<string:task_id>')
class task_individual(Resource):

    def get(self, task_id):
        cur = mysql.connection.cursor()
        cur.execute("""select * from tasks where taskid = %s""", (task_id))
        task = cur.fetchone()
        print(task)
        new_task = dict()
        new_task['task_id'] = task[0]
        new_task['task'] = task[1]
        new_task['due'] = task[2].strftime('%Y-%m-%d')
        new_task['status'] = task[3]

        return new_task

    def put(self, task_id):
        global user_type
        db = mysql.connection
        cur = db.cursor()
        status_details = status_parser.parse_args()

        status = status_details['status']
        cur = mysql.connection.cursor()

        cur.execute("""update tasks set status = %s where taskid = %s""", (status, task_id))
        db.commit()
        return  "Task Status Modified"
        # if user_type == "admin":
        #     pass
        # else:
        #     return "Only Admins can create / modify"

# Logs in user
# Sets global user_type appropriately
@login.route('')
class Login(Resource):
    # def get(self):
    #     headers = {'Content-Type': 'text/html'}
    #     return make_response(render_template('index.html'),200,headers)
    #     # return render_template('index.html')

    def post(self):
        global user_type
        creds = cred_parser.parse_args()
        uname = creds['username']
        pwd = creds['password']

        cur = mysql.connection.cursor()
        cur.execute("select * from users")
        users = cur.fetchall()

        for user in users:
            if( user[0] == uname):
                if(user[1] == pwd):
                    if(user[2] == "write"):
                        user_type = "admin"
                        return "Welcome Admin"
                    else:
                        user_type = "user"
                        return "Welcome User"
                    
                else:
                    cur.close()
                    return "Wrong Password"
        cur.close()
        return "Not Authorized"

if( __name__ == '__main__'):
    app.run(debug=True)