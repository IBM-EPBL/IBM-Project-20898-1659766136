from flask import Flask , request, render_template,redirect,url_for,session
import ibm_db
import re
  
app = Flask(__name__)    
app.secret_key='a'

global resid
global userid
global userType

id=120
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cyv04734;PWD=jVo9OmtWAx7yht51;",' ',' ')

@app.route('/login',methods =["GET","POST"])   
def login_data(): 
    global username
    msg=" "
    if request.method == "POST":
       username = request.form.get("username")
       password = request.form.get("password")
       if username=="admin" and password=="admin123":
          userType="admin"
          msg="Welcome Admin!!"
          return redirect(url_for('admindashboard'))

       sql="SELECT * FROM Customer WHERE Username=? AND Password=?"
       stmt=ibm_db.prepare(conn,sql)
       ibm_db.bind_param(stmt,1,username)
       ibm_db.bind_param(stmt,2,password)
       ibm_db.execute(stmt)
       account=ibm_db.fetch_assoc(stmt)
       if account:
        userType="customer"
        session['Loggedin']=True
        session['id']=account['USERNAME']
        userid=account["USERNAME"]
        session['username']=account["USERNAME"]
        msg='Logged in Successfully!'
        return redirect(url_for('customerdashboard'))
       elif request.method == "POST": 
        sql="SELECT * FROM Agent WHERE Username=? AND Password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        if account:
         userType="agent"
         session['Loggedin']=True
         session['id']=account['USERNAME']
         print(account['USERNAME'])
         userid=account["USERNAME"]
         session['username']=account["USERNAME"]
         msg='Logged in Successfully!'
         return redirect(url_for('agentdashboard'))
       else:
         msg="Authentication Failed! Incorrect Username and Password"
    return render_template("login.html",msg=msg)
       

@app.route('/login')   
def login(): 
  return render_template('login.html'); 

@app.route('/signup')   
def signup():  
    return render_template('signup.html');  

@app.route('/signup',methods =["POST"])   
def signup_data(): 
    msg=" "
    if request.method == "POST":
       username = request.form.get("username")
       email=request.form.get("email")
       password = request.form.get("password")
       sql="SELECT * FROM Customer WHERE Username=? And EmailId=?"
       stmt=ibm_db.prepare(conn,sql)
       ibm_db.bind_param(stmt,1,username)
       ibm_db.bind_param(stmt,2,email)
       ibm_db.execute(stmt)
       account=ibm_db.fetch_assoc(stmt)
       if account:
          msg="Account already exist"
          return render_template('signup.html',msg=msg)
       elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',email): 
          msg="Invalid email address.."
          return render_template('signup.html',msg=msg)
       elif not re.match(r'[A-Za-z0-9]',username):
          msg="Name must be alphanumeric.."
          return render_template('signup.html',msg=msg)
       else:
          id=4000
          condition="SELECT COUNT(CUSTOMERID) FROM CUSTOMER"
          stmt=ibm_db.prepare(conn,condition)
          ibm_db.execute(stmt)
          account=ibm_db.fetch_assoc(stmt)
          count=account['1']
          if count >= 1:
             statement='SELECT CUSTOMERID FROM CUSTOMER ORDER BY CUSTOMERID DESC LIMIT 1'
             stmtt=ibm_db.prepare(conn,statement)
             ibm_db.execute(stmtt)
             acc=ibm_db.fetch_assoc(stmtt)
             lastid=acc['CUSTOMERID']
             id=lastid+1
          insert_sql="INSERT INTO Customer VALUES(?,?,?,?)"
          prep_stmt=ibm_db.prepare(conn,insert_sql)
          ibm_db.bind_param(prep_stmt,1,id)
          ibm_db.bind_param(prep_stmt,2,username)
          ibm_db.bind_param(prep_stmt,3,email)
          ibm_db.bind_param(prep_stmt,4,password)
          ibm_db.execute(prep_stmt)
          msg="You have successfully registered.. please login"
          return render_template('login.html',msg=msg)

    elif request.method=='POST':
        msg="Please Signup the account"
        return render_template('signup.html',msg=msg)
    

@app.route('/addagent')   
def addagent():  
    return render_template('addagent.html'); 

@app.route('/addagent',methods =["GET","POST"])   
def addagent_data(): 
    if request.method == "POST":
       username = request.form.get("username")
       email=request.form.get("email")
       password = request.form.get("password")
       sql="SELECT * FROM Agent WHERE Username=? And EmailId=?"
       stmt=ibm_db.prepare(conn,sql)
       ibm_db.bind_param(stmt,1,username)
       ibm_db.bind_param(stmt,2,email)
       ibm_db.execute(stmt)
       account=ibm_db.fetch_assoc(stmt)
       if account:
          msg="Account already exist"
          return render_template('addagent.html',msg=msg)
       elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',email): 
          msg="Invalid email address.."
          return render_template('addagent.html',msg=msg)
       elif not re.match(r'[A-Za-z0-9]',username):
          msg="Name must be alphanumeric.."
          return render_template('addagent.html',msg=msg)
       else:
          id=5000
          condition="SELECT COUNT(AGENTID) FROM AGENT"
          stmt=ibm_db.prepare(conn,condition)
          ibm_db.execute(stmt)
          account=ibm_db.fetch_assoc(stmt)
          count=account['1']
          if count >= 1:
             statement='SELECT AGENTID FROM AGENT ORDER BY AGENTID DESC LIMIT 1'
             stmtt=ibm_db.prepare(conn,statement)
             ibm_db.execute(stmtt)
             acc=ibm_db.fetch_assoc(stmtt)
             lastid=acc['AGENTID']
             id=lastid+1
          insert="INSERT INTO Agent VALUES(?,?,?,?)"
          prep_stmt1=ibm_db.prepare(conn,insert)
          ibm_db.bind_param(prep_stmt1,1,id)
          ibm_db.bind_param(prep_stmt1,2,username)
          ibm_db.bind_param(prep_stmt1,3,email)
          ibm_db.bind_param(prep_stmt1,4,password)
          ibm_db.execute(prep_stmt1)
          msg="You have successfully registered.."
          return redirect(url_for('admindashboard'))
         
    elif request.method=='POST':
        msg="Please Signup the account"
        return render_template('adashboard.html',userType=userType)


@app.route('/adashboard',methods =["GET","POST"])   
def admindashboard():
      agent = []  
      statementa="SELECT TICKETID,TICKETNAME,PRIORITY,DATE,STATUS,CUSTOMERNAME,AGENTNAME FROM TicketDetails"
      stmta=ibm_db.prepare(conn,statementa)
      ibm_db.execute(stmta)
      adminaccount=ibm_db.fetch_both(stmta)
      while adminaccount != False:
        agent.append(adminaccount)
        adminaccount = ibm_db.fetch_both(stmta)

      return render_template("adashboard.html",adminaccount=agent)

      

@app.route('/cdashboard',methods =["GET","POST"])   
def customerdashboard(): 
      customer=[]
      statement1="SELECT TICKETID,TICKETNAME,PRIORITY,DATE,STATUS,AGENTNAME FROM TicketDetails WHERE CUSTOMERNAME=?"
      stmt1=ibm_db.prepare(conn,statement1)
      ibm_db.bind_param(stmt1,1,username)
      ibm_db.execute(stmt1)
      customeraccount=ibm_db.fetch_both(stmt1)
      while customeraccount != False:
        customer.append(customeraccount)
        customeraccount = ibm_db.fetch_both(stmt1)
        
      return render_template("cdashboard.html",customeraccount=customer)

    

@app.route('/aadashboard',methods =["GET","POST"])   
def agentdashboard():
      agent=[]
      statement2="SELECT TICKETID,TICKETNAME,PRIORITY,DATE,STATUS,CUSTOMERNAME FROM TicketDetails WHERE AGENTNAME=?"
      stmt2=ibm_db.prepare(conn,statement2)  
      ibm_db.bind_param(stmt2,1,username)
      ibm_db.execute(stmt2)
      agentaccount=ibm_db.fetch_both(stmt2)
      while agentaccount != False:
        agent.append(agentaccount)
        agentaccount = ibm_db.fetch_both(stmt2)
        
      return render_template("agentdashboard.html",agentaccount=agent) 
      
 

@app.route('/ticketform')   
def ticketform():  
    return render_template("ticketform.html") 

@app.route('/ticketform',methods =["GET","POST"])   
def ticketform_data():  
    msg=""
    ticketId=2001
    condition="SELECT COUNT(TICKETID) FROM TicketDetails"
    stmt=ibm_db.prepare(conn,condition)
    ibm_db.execute(stmt)
    account=ibm_db.fetch_assoc(stmt)
    count=account['1']
    if count >= 1:
        statement='SELECT TICKETID FROM TicketDetails ORDER BY TICKETID DESC LIMIT 1'
        stmtt=ibm_db.prepare(conn,statement)
        ibm_db.execute(stmtt)
        acc=ibm_db.fetch_assoc(stmtt)
        ticketlastid=acc['TICKETID']
        ticketId=ticketlastid+1
   
    if request.method == "POST":
       ticketname = request.form.get("ticketname")
       producttype=request.form.get("producttype")
       priority = request.form.get("priority")
       description = request.form.get("description")
       date = request.form.get("date")
       place = request.form.get("place")
       status = request.form.get("status")
       agent='-'
       resolution='-'
       insert_sql="INSERT INTO TicketDetails VALUES(?,?,?,?,?,?,?,?,?,?,?)"
       prep_stmt=ibm_db.prepare(conn,insert_sql)
       ibm_db.bind_param(prep_stmt,1,ticketId)
       ibm_db.bind_param(prep_stmt,2,ticketname)
       ibm_db.bind_param(prep_stmt,3,producttype)
       ibm_db.bind_param(prep_stmt,4,priority)
       ibm_db.bind_param(prep_stmt,5,description)
       ibm_db.bind_param(prep_stmt,6,date)
       ibm_db.bind_param(prep_stmt,7,place)
       ibm_db.bind_param(prep_stmt,8,status)
       ibm_db.bind_param(prep_stmt,9,username)
       ibm_db.bind_param(prep_stmt,10,agent)
       ibm_db.bind_param(prep_stmt,11,resolution)
       ibm_db.execute(prep_stmt)
       msg="Issue Ticket created"

    return redirect(url_for('customerdashboard'))


@app.route('/logout')    
def logout(): 
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None) 
    return redirect(url_for('login'))  
  
if __name__ =='__main__':  
    app.run(debug = True)  