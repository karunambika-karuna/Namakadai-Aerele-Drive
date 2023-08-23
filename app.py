import MySQLdb
from flask import Flask, jsonify,render_template,redirect, url_for,request
from flask_mysqldb import MySQL

app = Flask(__name__) 
@app.route('/')
def entry():
    return render_template('entry.html')
@app.route('/chooseform',methods=['POST'])
def chooseform():
    submit=request.form.get('submitbutton')
    if submit == 'UpdateCashbalance':
        return render_template('company.html')
    elif submit == 'AddPurchase':
        return render_template('purchasemaster.html')
    elif submit == 'AddSales':
        return render_template('salesmaster.html')
    elif submit == 'Viewproducts':
        return render_template('productmaster.html')
    
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Karuna#22'
app.config['MYSQL_DB']='namakadai'

mysql=MySQL(app)

@app.route('/purchasemaster',methods=['GET','POST'])
def purchasemaster():
   if request.method=='POST':
       productid=request.form.get('product_id')
       productname=request.form.get('productname')
       quantity=request.form.get('qty')
       rate=request.form.get('rate')
       amount=request.form.get('amount')
       cur= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cur.execute('SELECT product_id FROM productmaster where product_id=%s',(productid,))
       result=cur.fetchone()
       if result:
           cur.execute('INSERT INTO purchase_master(product_id,qty,rate,amount) VALUES (%s,%s,%s,%s)',(productid,quantity,rate,amount))
           mysql.connection.commit()
           cur.execute("""UPDATE productmaster set productmaster.qty=productmaster.qty+(%s) where productmaster.product_id=%s""",(quantity,productid))
           mysql.connection.commit()
           return "Done"
       else:
           cur.execute('INSERT  into productmaster(product_id,productname,qty) VALUES(%s,%s,%s)',(productid,productname,quantity))
           mysql.connection.commit()
           cur.execute('INSERT INTO purchase_master(product_id,qty,rate,amount) VALUES (%s,%s,%s,%s)',(productid,quantity,rate,amount))
           mysql.connection.commit()
           return "suces"
   cur.execute("update company set cash_balance-=%s",(amount))
   mysql.connection.commit()
   mysql.connection.close()
   return render_template('purchasemaster.html')
@app.route('/company',methods=['GET','POST'])
def company():
     if request.method=='POST':
       name=request.form.get('company_name')
       cash_balance=request.form.get('cash_balance')
       id=request.form.get('company_id')
       cur= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cur.execute("Insert into company(company_name,cash_balance,company_id) values(%s,%s,%s)",(name,cash_balance,id))
       mysql.connection.commit()
       cur.close()
       return "success"
     return render_template('company.html')

@app.route('/salesmaster',methods=['GET','POST'])
def salesmaster():
    if request.method=='POST':
        productid=request.form.get('product_id')
        productname=request.form.get('productname')
        quantity=request.form.get('qty')
        rate=request.form.get('rate')
        amount=request.form.get('amount')
        cur= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT product_id FROM productmaster where product_id=%s',(productid,))
        result=cur.fetchone()
        if result:
           cur.execute('INSERT INTO sales_master(product_id,qty,rate,amount) VALUES (%s,%s,%s,%s)',(productid,quantity,rate,amount))
           mysql.connection.commit()
           cur.execute("""UPDATE productmaster set productmaster.qty=productmaster.qty-(%s) where productmaster.product_id=%s""",(quantity,productid))
           mysql.connection.commit()
           return "Done"
        else:
           cur.execute('INSERT  into productmaster(product_id,productname,qty) VALUES(%s,%s,%s)',(productid,productname,quantity))
           mysql.connection.commit()
           cur.execute('INSERT INTO sales_master(product_id,qty,rate,amount) VALUES (%s,%s,%s,%s)',(productid,quantity,rate,amount))
           mysql.connection.commit()
           return "suces"

    cur.execute("update company set cash_balance+=%s  WHERE company_name='Namakadai'",(amount))
    mysql.connection.commit()
    mysql.connection.close()
    return render_template('salesmaster.html')

@app.route('/productmaster',methods=['GET','POST'])  
def productmaster():
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cur.execute("SELECT * FROM productmaster")
     data=cur.fetchall()
     return render_template('productmaster.html',data=data)
if __name__ == '__main__':
    app.run(debug=True)
 