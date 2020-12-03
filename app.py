# import flask
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	produk = db.Column(db.String(100), nullable=False)
	tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

	def __repr__(self):
		return "<produk %r>" % self.id

	def __init__(self,produk):
		self.produk = produk

@app.route("/",methods=['POST','GET'])
def index():
	if(request.method == 'POST'):
		produk = request.form['produk']
		tambah_produk = Product(produk=produk)

		try:
			db.session.add(tambah_produk)
			db.session.commit()
			return redirect("/")
		except:
			print("Tidak Ada Data")
	else:
		products = Product.query.order_by(Product.id).all()
		return render_template("index.html",products=products)

@app.route('/hapus/<int:id>')
def hapus(id):
	hapus_produk = Product.query.get_or_404(id)

	try:
		db.session.delete(hapus_produk)
		db.session.commit()
		return redirect("/")

	except:
		print("tidak ada produk")

@app.route('/ubah/<int:id>',methods=['POST','GET'])
def ubah(id):
	products = Product.query.get_or_404(id)

	if(request.method == "POST"):
		products.produk = request.form['produk']

		try:
			db.session.commit()
			return redirect("/")

		except:
			print("Tidak ada data yang diubah")

	else:
		return render_template("ubah.html",products=products)

if(__name__ == "__main__"):
	app.run(debug=True)