from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_mysqldb import MySQL
import time


#Mysql Connection
app = Flask(__name__)
app.config['MYSQL_HOST']= 'localhost' 
app.config['MYSQL_USER']= 'root' 
app.config['MYSQL_PASSWORD']= 'localhost' 
app.config['MYSQL_DB']= 'Venta' 
mysql = MySQL(app)


#Session
app.secret_key = 'mysecretkey'



@app.route('/')
def index():
	return render_template('Login.html')



@app.route('/pago')
def pago():
	id= session['uno']
	cur = mysql.connection.cursor()
	cur.execute('select sum(subtotal_pro) from renglon_venta where  id_ven="'+id+'"')
	subtotal = cur.fetchone()
	total = str(subtotal[0])
	print(total)
	cur.execute('update venta set total_ven = "'+total+'", status_ven=1 where id_ven= "'+id+'" ')
	mysql.connection.commit()
	flash(total)
	return render_template("Pago.html")


@app.route('/venta')
def venta():
	cur = mysql.connection.cursor()
	fecha = time.strftime("%Y-%m-%d")
	cur.execute('insert into venta values(null, "'+fecha+'" , 0, 0)')
	mysql.connection.commit()
	cur.execute('select last_insert_id()')
	cve = cur.fetchone()
	session['uno'] = str(cve[0])
	flash(fecha)
	return render_template('Inicio.html')


@app.route('/verificar', methods=['POST'])	
def verificar():
	if request.method == 'POST':
		user = request.form['user']
		password = request.form['password']
		fecha = time.strftime("%Y-%m-%d")
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM  usuario WHERE usuario_usu = %s and password_usu = %s',(user, password))
		datos = cur.fetchall()
		if datos:
			return redirect(url_for('venta'))
		else:
			flash('No existe ese usuario')
			return redirect(url_for('index'))


@app.route('/articulo', methods=['POST'])
def articulo():
	if request.method == 'POST':
		id= session['uno']
		codigo = request.form['codigo']
		cantidad = request.form['cantidad']
		cur = mysql.connection.cursor()
		cur.execute('select precio_pro from producto where codigo_pro ="'+codigo+'"')
		precio = cur.fetchone()
		print(precio[0]*cantidad)
		subtotal = (str(precio[0]))
		sub = int(cantidad) * int(subtotal)
		cur.execute('insert into renglon_venta values(null, "'+codigo+'", '+str(id)+','+cantidad+', '+str(sub)+', 1)')
		mysql.connection.commit()

		cur.execute('SELECT * FROM renglon_venta  rv join producto  p on p.codigo_pro= rv.codigo_pro where id_ven = '+id+'  order by id_reg')
		var = cur.fetchall()
		return render_template('Inicio.html', contact = var)  



if __name__ ==  '__main__':
	app.run(debug = True)