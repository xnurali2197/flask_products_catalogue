from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Default images for categories
CATEGORY_IMAGES = {
    'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400',
    'clothing': 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400',
    'food': 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=400',
    'books': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400',
    'sports': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400',
    'furniture': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400',
    'cosmetics': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400',
    'toys': 'https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=400',
    'default': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
}

# Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text)
    image = db.Column(db.String(300))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def get_image(self):
        if self.image:
            return self.image
        return CATEGORY_IMAGES.get(self.category.lower(), CATEGORY_IMAGES['default'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    search_query = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Product.query
    
    if search_query:
        query = query.filter(
            (Product.name.ilike(f'%{search_query}%')) | 
            (Product.description.ilike(f'%{search_query}%'))
        )
    
    if category:
        query = query.filter_by(category=category)
    
    products = query.order_by(Product.created_date.desc()).all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('index.html', products=products, categories=categories, 
                         search_query=search_query, selected_category=category)

@app.route('/products')
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'quantity': p.quantity,
        'description': p.description,
        'image': p.get_image()
    } for p in products])

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        quantity = int(request.form.get('quantity'))
        description = request.form.get('description')
        
        image_url = None
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = url_for('static', filename=f'uploads/{filename}')
        
        new_product = Product(
            name=name,
            price=price,
            category=category,
            quantity=quantity,
            description=description,
            image=image_url
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

@app.route('/products/category/<category>')
def products_by_category(category):
    products = Product.query.filter_by(category=category).all()
    return render_template('category.html', products=products, category=category)

@app.route('/products/low-stock')
def low_stock():
    products = Product.query.filter(Product.quantity < 5).all()
    return render_template('low_stock.html', products=products)

@app.route('/product/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        product.quantity = int(request.form.get('quantity'))
        product.description = request.form.get('description')
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                product.image = url_for('static', filename=f'uploads/{filename}')
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_detail', id=product.id))
    
    return render_template('update_product.html', product=product)

@app.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/product/buy/<int:id>', methods=['POST'])
def buy_product(id):
    product = Product.query.get_or_404(id)
    
    if product.quantity > 0:
        product.quantity -= 1
        db.session.commit()
        flash(f'{product.name} purchased! Remaining: {product.quantity}', 'success')
    else:
        flash('Product out of stock!', 'danger')
    
    return redirect(url_for('product_detail', id=id))

if __name__ == '__main__':
    app.run(debug=True)