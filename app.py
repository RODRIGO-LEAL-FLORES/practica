import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

#crear instancia'
load_dotenv()
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos
class Producto(db.Model):
    __tablename__ = 'productos'

    codigo_barras = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    precio_c = db.Column(db.Numeric(10,2))
    precio_v = db.Column(db.Numeric(10,2))
    descripcion = db.Column(db.String)

    def to_dict(self):
        return {
            'codigo_barras': self.codigo_barras,
            'nombre': self.nombre,
            'precio_c': float(self.precio_c) if self.precio_c else None,
            'precio_v': float(self.precio_v) if self.precio_v else None,
            'descripcion': self.descripcion,
        }


#Ruta raiz
@app.route('/')
def index():
    #retornar los alumnos
    #return 'Hola Mundo'




    #Trae todos los estudiantes
    productos = Producto.query.all()
    return render_template('index.html', productos = productos)

#Ruta /alumnos crear un nuevo alumno
@app.route('/productos/new', methods=['GET','POST'])
def create_producto():
    if request.method == 'POST':
        #Agregar Estudiante
        codigo_barras = request.form['codigo_barras']
        nombre = request.form['nombre']
        precio_c = request.form['precio_c']
        precio_v = request.form['precio_v']
        descripcion = request.form['descripcion']

        nvo_producto =Producto(codigo_barras=codigo_barras, nombre=nombre, precio_c=precio_c, precio_v=precio_v, descripcion=descripcion)

        db.session.add(nvo_producto)
        db.session.commit()

        return redirect(url_for('index'))
    
    #Aqui sigue si es GET
    return render_template('create_producto.html')
    #return render_template('create_estudiante.html')

@app.route('/productos/delete/<string:codigo_barras>')
def delete_producto(codigo_barras):
    producto = Producto.query.get_or_404(codigo_barras)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('index'))

# Actualizar producto
@app.route('/productos/update/<string:codigo_barras>', methods=['GET', 'POST'])
def update_producto(codigo_barras):
    producto = Producto.query.get_or_404(codigo_barras)

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio_c = float(request.form['precio_c'])
        producto.precio_v = float(request.form['precio_v'])
        producto.descripcion = request.form['descripcion']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_producto.html', producto=producto)



#Ruta /alumnos
@app.route('/alumnos')
def getAlumnos():
    return 'Aqui van los alumnos'


if __name__ == '__main__':
    app.run(debug=True)