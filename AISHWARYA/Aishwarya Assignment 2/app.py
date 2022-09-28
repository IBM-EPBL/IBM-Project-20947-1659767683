from flask import Flask,render_template,request,url_for,flash,redirect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaaaa'

con=sqlite3.connect("database.db")
con.execute("Create table if not exists data(pid integer primary key,title  text , desc text ,link text)")
con.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sign-in')
def signin():
    return render_template('signin.html')

@app.route('/sign-up')
def signup():
    return render_template("signup.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add_jobs')
def add():
    return render_template("add.html")

@app.route('/adddata',methods=['POST','GET'])
def adddata():
    if request.method=='POST':
        try:
            title=request.form['title']
            desc=request.form['desc']
            link=request.form['link']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into data(title,desc,link) values(?,?,?)",(title,desc,link))
            con.commit()
            flash("Job Added Successfully",'success')
        except:
            flash("error in insert operation","danger")
        finally:
            return redirect(url_for("view"))
            con.close()

@app.route('/view_jobs')
def view():
    con=sqlite3.connect('database.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from data")
    data=cur.fetchall()
    con.close
    return render_template("view.html",data=data)

@app.route("/signup", methods=['GET', 'POST'])
def register():
    return render_template('signup.html')


@app.route("/signin", methods=['GET', 'POST'])
def login():
    return render_template('signin.html')

@app.route('/update/<string:id>',methods=['POST','GET'])
def update(id):
    con=sqlite3.connect('database.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from data where pid=?",(id))
    data=cur.fetchone()
    con.close

    if request.method=='POST':
        try:
            title=request.form['title']
            desc=request.form['desc']
            link=request.form['link']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("update data set title=?,desc=?,link=? where pid=?",(title,desc,link,id))
            con.commit()
            flash("update Successfully","success")
        except:
            flash("Error in update","danger")
        finally:
            return redirect(url_for('view'))
            con.close()
    return render_template('update.html',data=data)

@app.route('/delete/<string:id>')
def delete(id):
    try:
        con=sqlite3.connect('database.db')
        cur=con.cursor()
        cur.execute('delete from data where pid=?',(id))
        con.commit()
        flash("record deleted successfully",'success')
    except:
        flash("record delete failed","danger")
    finally:
        return redirect (url_for("view"))
        con.close()

if __name__ == "__main__":
    app.run('0.0.0.0',port=8080,debug=True)