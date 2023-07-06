from flask import Flask
from flask import request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL connection details
app.config['MYSQL_HOST'] = 'your_mysql_host'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_mysql_database'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        return add_dream()
    else:
        return print_dream()


def print_dream():
    html = '<html>'
    html += '<head><link rel="stylesheet" type="text/css" href="static/style.css"></head>'
    html += "<h3>List your bucket list. Dream Big Big!!!!!!</h3>"
    html += '''
            <form action="/" method="post">
            <label for="dream">Add item:</label>
            <input type="text" id="dream" name="dream"><br\ ><br\ >
            <input type="submit" value="Submit">
            </form> <br><br>
            '''
    html += "<h4>My bucket list:</h4>"
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT dream FROM bucket_list")
        rows = cur.fetchall()
        
        for row in rows:
            html += f"{row[0]} <br \>"
        
        cur.close()
    except Exception as e:
        html += "An error occurred while retrieving the bucket list."
        print(e)
    
    html += '</html>'
    return html


def add_dream():
    dream = request.form.get('dream')
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bucket_list (dream) VALUES (%s)", (dream,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        html = print_dream()
        html += "<br>An error occurred while adding the dream."
        print(e)
    
    html = print_dream()
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
