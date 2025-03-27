from flask import Flask, render_template, request, redirect, url_for
import snowflake.connector
from snowflake.connector import DictCursor

my_db_params = {
  "account" : "FUKSKIX-MJ13450",
  "user" : "PUBLIC_USER",
  "password" : "Publicpassword2!",
  "role" : "LAB_6",
  "warehouse" : "COMPUTE_WH",
  "database" : "AIDI_2004_LAB_6",
  "schema" : "PUBLIC",
  }
conn = snowflake.connector.connect(
        **my_db_params
        )
cursor = conn.cursor()
dict_cur = conn.cursor(DictCursor)

app = Flask(__name__)

# Route to display the form
@app.route('/')
def customer():
    return render_template('index.html')

# Route to handle form submission
@app.route('/create', methods=['POST'])
def print_data():
    print('data', request.form);
    params = request.form.to_dict();
    params['amount_due'] = float(params.get('amount_due'));
    print('data dict', params);
    #insert into db
    query = """
    INSERT into student(student_id, first_name, last_name, dob, amount_due)
    VALUES ( %(student_id)s , %(first_name)s , %(last_name)s , %(dob)s , %(amount_due)s )
    """
    cursor.execute(query,params)
    return redirect( url_for('records'))

@app.route('/records' , methods=['GET'])
def records() :
    query = """
    SELECT *
    FROM student;
    """
    res = dict_cur.execute(query).fetchall()
    print('res', res)
    return render_template("records.html", result=res)

@app.route('/read/<student_id>', methods=['GET'])
def read(student_id) :
    query = """
    SELECT * 
    FROM student
    WHERE student_id = %(student_id)s
    """
    params = {
            'student_id' : student_id,
            }
    res = dict_cur.execute(query,params).fetchall();
    return render_template('student.html',data=res[0])

@app.route('/update',methods=['POST'])
def update() :
    params = request.form.to_dict();
    print('params ', params)
    params['amount'] = float(params.get('amount_due'));
    print('data dict', params);
    query = """
    UPDATE student
    SET first_name = %(first_name)s,
        last_name = %(last_name)s,
        dob = %(dob)s,
        amount_due = %(amount_due)s 
    WHERE student_id = %(student_id)s
    """
    res = dict_cur.execute(query,params);
    return redirect('/records');

@app.route('/delete/<student_id>', methods=['POST'])
def delete(student_id) :
    query = """
    DELETE 
    FROM student
    WHERE student_id = %(student_id)s
    """
    params = {
            'student_id' : student_id,
            }
    res = dict_cur.execute(query,params);
    return redirect('/records');

if __name__ == '__main__':
    app.run(debug=True)
