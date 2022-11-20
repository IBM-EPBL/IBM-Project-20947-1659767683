from __future__ import print_function
from audioop import add
import datetime
from unicodedata import name
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for, session, flash
from markupsafe import escape
from flask import *
import ibm_db
import sib_api_v3_sdk
from init import randomnumber
from init import id
from init import hello
import datetime



conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=;PORT=;SECURITY=SSL;;UID=;PWD=", '', '')
print(conn)
print("connection successful...")

app = Flask(__name__)
app.secret_key = 'your secret key'


@app.route('/')
def home():
    message = "TEAM ID : PNT2022TMID37544" +" "+ "BATCH ID : B1-1M3E "
    return render_template('index.html',mes=message)


@app.route('/home', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/agentRegister', methods=['POST', 'GET'])
def agentRegister():
    return render_template('agentregister.html')

   

@app.route('/forgotpass', methods=['POST', 'GET'])
def forgotpass():
    return render_template('forgot.html')



@app.route('/forgot', methods=['POST', 'GET'])
def forgot():

    try:
        global randomnumber
        ida = request.form['custid']
  

        pprint(api_response)
        message = "Email send to:"+e+" for password"
        flash(message, "success")

    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        flash("Error in sending mail")
    except:
        flash("Your didn't Signin with this account")
    finally:
        return render_template('forgot.html')

@app.route('/agentforgot', methods=['POST', 'GET'])
def agentforgot():

    try:
        global randomnumber
        ida = request.form['custid']
        print(ida)
        global id
        id = ida
        sql = "SELECT EMAIL,NAME FROM AGENT WHERE id=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, ida)
        ibm_db.execute(stmt)
        emailf = ibm_db.fetch_both(stmt)
        while emailf != False:
            e = emailf[0]
            n = emailf[1]
            break

    
        pprint(api_response)
        message = "Email send to:"+e+" for OTP"
        flash(message, "success")

    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        flash("Error in sending mail")
    except:
        flash("Your didn't Signin with this account")
    finally:
        return render_template('forgot.html')





@app.route('/agentotp', methods=['POST', 'GET'])
def agentotp():
    try:
        otp = request.form['otp']
        cusid = id
        print(id)
        sql = "SELECT PASSWORD FROM AGENT WHERE ID=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, cusid)
        ibm_db.execute(stmt)
        otpf = ibm_db.fetch_both(stmt)
        while otpf != False:
            verify = otpf[0]
            break
        if otp == str(randomnumber):
            msg = "Your Password is "+verify+""
            flash(msg, "success")
            return render_template('forgot.html')
        else:
            flash("Wrong Otp", "danger")
    finally:
        return render_template('forgot.html')




@app.route('/remove', methods=['POST', 'GET'])
def remove():

    otp = request.form['otpv']
    if otp == 'C':
        try:
            insert_sql = f"delete from customer"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.execute(prep_stmt)
            flash("delected successfully the Customer", "success")
        except:
            flash("No data found in Customer", "danger")
        finally:
            return redirect(url_for('signuppage'))
    if otp == 'A':
        try:
            insert_sql = f"delete from AGENT"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.execute(prep_stmt)
            flash("delected successfully the Agents", "success")
        except:
            flash("No data found in Agents", "danger")
        finally:
           return redirect(url_for('signuppage'))

    if otp == 'C':
        try:
            insert_sql = f"delete from AGENT"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.execute(prep_stmt)
            flash("delected successfully the Complaints", "success")
        except:
            flash("No data found in Complaints", "danger")
        finally:
            return redirect(url_for('signuppage'))


@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
    try:
        id = hello
        sql = "SELECT ID,DATE,TOPIC,SERVICE_TYPE,SERVICE_AGENT,DESCRIPTION,STATUS FROM ISSUE WHERE CUSTOMER_ID =?"
        agent = []
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, id)
        ibm_db.execute(stmt)
        otpf = ibm_db.fetch_both(stmt)
        while otpf != False:
            agent.append(otpf)
            otpf = ibm_db.fetch_both(stmt)

        sql = "SELECT COUNT(*) FROM ISSUE WHERE CUSTOMER_ID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, id)
        ibm_db.execute(stmt)
        t = ibm_db.fetch_both(stmt)
        
        return render_template("welcome.html",agent=agent,message=t[0])
    except:
        return render_template("welcome.html")

@app.route('/loginagent', methods=['GET', 'POST'])
def loginagent():
    if request.method == 'POST':
        try:
            global loginagent 
            id = request.form['idn']
            loginagent = id
            password = request.form['password']

            sql = f"select * from AGENT where id='{escape(id)}' and password='{escape(password)}'"
            stmt = ibm_db.exec_immediate(conn, sql)
            data = ibm_db.fetch_both(stmt)
            
            if data:
                session["name"] = escape(id)
                session["password"] = escape(password)
                return redirect(url_for("agentwelcome"))

            else:
                flash("Mismatch in credetials", "danger")
        except:
            flash("Error in Insertion operation", "danger")

    return render_template("signinpageagent.html")

@app.route('/delete/<ID>')
def delete(ID):
    sql = f"select * from customer where Id='{escape(ID)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    student = ibm_db.fetch_row(stmt)
    if student:
        sql = f"delete from customer where id='{escape(ID)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        
        flash("Delected Successfully", "success")
        return redirect(url_for("admin"))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        try:
            x = datetime.datetime.now()
            y = x.strftime("%Y-%m-%d %H:%M:%S")
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            phonenumber = request.form['phonenumber']
            sql = "SELECT * FROM customer WHERE email = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)

            if account:
                flash("Record Aldready found", "success")
            else:
                insert_sql = "insert into customer(name,email,password,phonenumber,DATE)values(?,?,?,?,?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, name)
                ibm_db.bind_param(prep_stmt, 2, email)
                ibm_db.bind_param(prep_stmt, 3, password)
                ibm_db.bind_param(prep_stmt, 4, phonenumber)
                ibm_db.bind_param(prep_stmt, 5, y)
                ibm_db.execute(prep_stmt)
                flash("Your Information Stored Successful. Kindly check mail for Id !", "success")
                sql = "SELECT id FROM Customer WHERE email=?"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, email)
                ibm_db.execute(stmt)
                hi = ibm_db.fetch_tuple(stmt)

                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key['api-key'] = ''

                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuration))
                subject = "Registering Account"
                html_content = " <html><body><h1>Thanks for Registering into Customer Care Registry</h1> <h2>Your Account Id is :"+str(hi[0])+"</h2><h2>Please kindly login with this Id</h2> <h2>With Regards:</h2><h3>Customer Care Registry</h3> </body></html>"
                sender = {"name": "IBM CUSTOMER CARE REGISTRY",
                  "email": "ibmdemo6@yahoo.com"}
                to = [{"email": email, "name": name}]
                reply_to = {"email": "ibmdemo6@yahoo.com", "name": "IBM"}
                headers = {"Some-Custom-Name": "unique-id-1234"}
                params = {"parameter": "My param value",
                  "subject": "Email Verification"}
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=to, reply_to=reply_to, headers=headers, html_content=html_content, params=params, sender=sender, subject=subject)

                api_response = api_instance.send_transac_email(send_smtp_email)

                pprint(api_response)

        except:
            flash("Error in Insertion Operation", "danger")
        finally:
            return redirect(url_for("signuppage"))
            con.close()

    return render_template('signuppage.html')






@app.route('/agentwelcome', methods=['POST', 'GET'])
def agentwelcome():
    # try:
        id = loginagent
        sql = "SELECT NAME FROM AGENT WHERE ID =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, id)
        ibm_db.execute(stmt)
        hi = ibm_db.fetch_tuple(stmt)
        while hi != False:
            type = hi[0]
            name = type 
            break

        str = name+id
        sql = "SELECT ISSUE.ID,ISSUE.DATE,ISSUE.TOPIC,ISSUE.SERVICE_TYPE,ISSUE.SERVICE_AGENT,ISSUE.DESCRIPTION,ISSUE.STATUS,ISSUE.ADDRESS,ISSUE.CUSTOMER_ID,CUSTOMER.NAME,CUSTOMER.PHONENUMBER FROM ISSUE FULL OUTER JOIN CUSTOMER ON CUSTOMER.ID = ISSUE.CUSTOMER_ID WHERE ISSUE.SERVICE_AGENT = ?" 
        agent = []
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, str)
        ibm_db.execute(stmt)
        otpf = ibm_db.fetch_both(stmt)
        while otpf != False:
            agent.append(otpf)
            otpf = ibm_db.fetch_both(stmt)

        
        sql = "SELECT COUNT(*) FROM ISSUE WHERE SERVICE_AGENT = ?"
        stmt5 = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt5, 1, str)
        ibm_db.execute(stmt5)
        t = ibm_db.fetch_both(stmt5)

        
        return render_template("agentwelcome.html",agent=agent,message=t[0])
    # except:
    #     flash("No record found","danger")
    #     return render_template("agentwelcome.html")

    

@app.route('/viewagent/<ID>', methods=['GET', 'POST'])
def viewagent(ID):
    try:
        id = int(ID)
        global customerid
        customerid = id
        idn = str(id)
        global services
        sql = "SELECT SERVICE_TYPE FROM ISSUE WHERE ID =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, id)
        ibm_db.execute(stmt)
        hi = ibm_db.fetch_tuple(stmt)
        while hi != False:
            type = hi[0]
            services = type 
            break
        
        sql = "SELECT NAME,ID FROM AGENT WHERE SERVICE_AGENT =?"
        agent = []
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, services)
        ibm_db.execute(stmt)
        otpf = ibm_db.fetch_both(stmt)
        while otpf != False:
            agent.append(otpf)
            otpf = ibm_db.fetch_both(stmt)
    
        flash("Successful","success")
        return render_template("agentapply.html",agent=agent,id=idn)
    except:
        flash("No record found","danger")
        return render_template('agentapply.html')

@app.route('/updatethis/<ID>', methods=['GET', 'POST'])
def updatethis(ID):
        
        agentid = ID 
        print(customerid)
        print(agentid)
        status  = "Agent Alloted"
       
        sql = "SELECT NAME,EMAIL FROM AGENT WHERE ID =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, agentid)
        ibm_db.execute(stmt)
        hi = ibm_db.fetch_tuple(stmt)
        while hi != False:
            msg = hi[0]
            email = hi[1]
            str1 = msg
            emailid = email 
                
            break
        mail = emailid  
        print(mail)
        final = str1 + agentid
        sql = "UPDATE ISSUE SET SERVICE_AGENT = ?,STATUS = ? WHERE ID = ? AND SERVICE_TYPE = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, final)
        ibm_db.bind_param(stmt,2,status)
        ibm_db.bind_param(stmt,3,customerid)
        ibm_db.bind_param(stmt,4,services)
        ibm_db.execute(stmt)
        flash("Successful","success")
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = ''

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))
        subject = "Agent Alloted for you Account"
        html_content = " <html><body><h1>Agent has be alloted for your Ticket</h1> <h2>Your Agent Id is :"+str(agentid)+"</h2> <div><h2>Your servicetype is:</h2>"+services+"<h3>Your Token id :"+str(customerid)+"</h3><h2>With Regards:</h2><h3>Customer Care Registry</h3> </body></html>"
        sender = {"name": "IBM CUSTOMER CARE REGISTRY",
              "email": "ibmdemo6@yahoo.com"}
        to = [{"email": mail, "name": "Agent"}]
        reply_to = {"email": "ibmdemo6@yahoo.com", "name": "IBM"}
        headers = {"Some-Custom-Name": "unique-id-1234"}
        params = {"parameter": "My param value",
                  "subject": "Email Verification"}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, reply_to=reply_to, headers=headers, html_content=html_content, params=params, sender=sender, subject=subject)
        api_response = api_instance.send_transac_email(send_smtp_email)

        pprint(api_response)
        return redirect(url_for('admin'))
  

@app.route('/completed/<DESCRIPTION>', methods=['GET', 'POST'])
def completed(DESCRIPTION):
    status ="Completed"
    try:

        sql = "UPDATE ISSUE SET STATUS = ? WHERE DESCRIPTION =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,status)
        ibm_db.bind_param(stmt,2,DESCRIPTION)
        ibm_db.execute(stmt)

        flash("Successful","success")
        return redirect(url_for('agentwelcome'))
    except:
        flash("No record found","danger")
        return redirect(url_for('agentwelcome'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
