from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///building_materials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер файла 16MB

db = SQLAlchemy(app)

class CeramicTile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)

class CustomFurniture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    furniture_for = db.Column(db.String(100), nullable=False)
    furniture_where = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)

class SanitaryWare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)

class RenovationMaterials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)

class IndustrialChemicals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)

class Tools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)

@app.route('/')
def home():
    return redirect(url_for('add_product'))

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        category = request.form['category']
        product_name = request.form['product_name']
        product_type = request.form['product_type']
        size = request.form['size']
        description = request.form['description']
        price = float(request.form['price'])
        photo = request.files['photo']

        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            photo_url = os.path.join('images', filename)
        else:
            photo_url = None

        if category == 'ceramic_tile':
            new_product = CeramicTile(product_name=product_name, product_type=product_type, size=size, description=description, price=price, photo=photo_url)
        elif category == 'custom_furniture':
            new_product = CustomFurniture(furniture_for=product_type, furniture_where=size, name=product_name, size=description, description=price, price=float(photo_url), photo=photo_url)
        elif category == 'sanitary_ware':
            new_product = SanitaryWare(product_name=product_name, product_type=product_type, size=size, description=description, price=price, photo=photo_url)
        elif category == 'renovation_materials':
            new_product = RenovationMaterials(product_name=product_name, product_type=product_type, size=size, description=description, price=price, photo=photo_url)
        elif category == 'industrial_chemicals':
            new_product = IndustrialChemicals(product_name=product_name, product_type=product_type, size=size, description=description, price=price, photo=photo_url)
        elif category == 'tools':
            new_product = Tools(product_name=product_name, product_type=product_type, size=size, description=description, price=price, photo=photo_url)

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('add_product'))

    products = {
        'ceramic_tile': CeramicTile.query.all(),
        'custom_furniture': CustomFurniture.query.all(),
        'sanitary_ware': SanitaryWare.query.all(),
        'renovation_materials': RenovationMaterials.query.all(),
        'industrial_chemicals': IndustrialChemicals.query.all(),
        'tools': Tools.query.all()
    }
    category = request.args.get('category', 'ceramic_tile')  # Default to 'ceramic_tile'
    return render_template('add_product.html', products=products[category])

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = CeramicTile.query.get_or_404(product_id)
    if request.method == 'POST':
        product.product_name = request.form['product_name']
        product.product_type = request.form['product_type']
        product.size = request.form['size']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        photo = request.files['photo']
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            product.photo = os.path.join('images', filename)
        db.session.commit()
        return redirect(url_for('add_product'))
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['GET'])
def delete_product(product_id):
    product = CeramicTile.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('add_product'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
