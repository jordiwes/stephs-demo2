from flask import Flask, flash, redirect, render_template, request, session, abort
import ibm_db_dbi as dbi
from ibm_db_dbi import SQL_ATTR_DBC_SYS_NAMING, SQL_TRUE
from ibm_db_dbi import SQL_ATTR_TXN_ISOLATION, SQL_TXN_NO_COMMIT


app = Flask(__name__)

options = {
       SQL_ATTR_TXN_ISOLATION: SQL_TXN_NO_COMMIT,
       SQL_ATTR_DBC_SYS_NAMING: SQL_TRUE,
   }

conn = dbi.connect()
conn.set_option(options)

@app.route("/")
def hello():
   #return "Hello World!"

   cur = conn.cursor()
   query = "select * from supplies"
   cur.execute(query)
   print(query)    
   for row in cur:
       print(row[2])

   print(cur.description[0])

   return render_template('index.html', rows=cur)

@app.route("/name")
def name():
    name = "Steph"
    return render_template('name.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route("/formAddSupply")
def formAddSupply():
    cur = conn.cursor()
    sql = "select * from alan.supplyty"
    cur.execute(sql)

    if not 'user' in session:
        return redirect("/login")
    return render_template('formAddSupply.html', supply_types=cur)

@app.route('/addSupply', methods=['POST'])
def add_supply():
    # read the posted values from the UI
    supply_name = request.form['supply_name']
    supply_brand = request.form['supply_brand']
    errors = {}
    if supply_brand == '':
        errors['supply_brand'] = 'please enter brand'
    if supply_name == '':
        errors['supply_name'] = 'please enter name'
    if not errors:
        return 'Name: ' + supply_name + ' Brand: ' + supply_brand
    else:
        return render_template('formAddSupply.html', errors=errors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            oconn = dbi.connect(user=username, password=password)
        except:
            return render_template('login.html')

        session['user'] = username

        return redirect("/formAddSupply")
    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.secret_key = 'cutcokey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=8299)
