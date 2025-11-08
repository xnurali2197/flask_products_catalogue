# Product Catalog - Flask Application

## Project Structure

```
project/
│
├── app.py                          # Main Flask application
├── products.db                     # SQLite database (auto-created)
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Home page
│   ├── product_detail.html        # Product details page
│   ├── add_product.html           # Add product form
│   ├── update_product.html        # Update product form
│   ├── low_stock.html             # Low stock products
│   └── category.html              # Category products
│
└── static/
    └── uploads/                    # Uploaded images folder (auto-created)
```

## Installation

### 1. Install Required Packages

```bash
pip install flask flask-sqlalchemy
```

### 2. Create Project Folders

```bash
mkdir templates
mkdir static
```

### 3. Save Files

Save all the provided files in their respective locations:
- `app.py` in the root directory
- All HTML files in the `templates/` folder

## Running the Application

```bash
python app.py
```

The application will run on `http://127.0.0.1:5000`

## Features

### ✅ All Required Routes

1. **GET /** - Home page with all products
2. **GET /products** - JSON API for all products
3. **GET /product/<id>** - Product details
4. **POST /product/add** - Add new product
5. **GET /products/category/<category>** - Filter by category
6. **GET /products/low-stock** - Products with quantity < 5
7. **POST /product/update/<id>** - Update product
8. **POST /product/delete/<id>** - Delete product
9. **POST /product/buy/<id>** - Buy product (decrease quantity)

### ✨ Additional Features

- **Search functionality** - Search products by name or description
- **Image upload** - Upload custom product images
- **Default category images** - Automatic images if no upload
- **Responsive design** - Beautiful Bootstrap 5 UI
- **Stock management** - Buy button decreases quantity
- **Low stock warnings** - Visual badges for low stock items
- **Category filtering** - Filter products by category

## Usage

### Adding a Product

1. Click "Add Product" in the navigation
2. Fill in the form:
   - Name (required)
   - Price (required)
   - Quantity (required)
   - Category (required)
   - Description (optional)
   - Image (optional - default image will be used if not provided)
3. Click "Add Product"

### Buying a Product

1. Go to product details page
2. Click "Buy Now" button
3. Quantity will decrease by 1
4. If quantity reaches 0, product becomes "Out of Stock"

### Searching Products

1. Use search bar on home page
2. Enter product name or description
3. Results will filter automatically

### Viewing Low Stock

1. Click "Low Stock" in navigation
2. See all products with quantity < 5

## Database Model

```python
class Product(db.Model):
    id = Integer (Primary Key)
    name = String(200)
    price = Float
    category = String(100)
    quantity = Integer
    description = Text
    image = String(300)
    created_date = DateTime
```

## Categories with Default Images

- Electronics
- Clothing
- Food
- Books
- Sports
- Furniture
- Cosmetics
- Toys

Each category has a beautiful default image from Unsplash.

## API Endpoints

### Get All Products (JSON)
```
GET /products
```

Response:
```json
[
  {
    "id": 1,
    "name": "Product Name",
    "price": 99.99,
    "category": "electronics",
    "quantity": 10,
    "description": "Product description",
    "image": "image_url"
  }
]
```

## Technical Requirements Met

✅ Model with fields: id, name, price, category, quantity, description  
✅ Float field (price)  
✅ Integer field (quantity)  
✅ filter(Product.quantity < 5) - Low stock route  
✅ filter_by(category='electronics') - Category route  
✅ SQLite database  
✅ Image upload functionality  
✅ Bootstrap styling  
✅ Search functionality  
✅ Buy product (quantity management)

## Tips

- Database is automatically created on first run
- Upload folder is automatically created
- Supported image formats: PNG, JPG, JPEG, GIF, WEBP
- Max file size: 16MB
- If no image uploaded, category-based default image is used

## Troubleshooting

**Database not created?**
- Make sure SQLite is installed (comes with Python)
- Check write permissions in project folder

**Images not uploading?**
- Check `static/uploads/` folder exists
- Verify file format is supported
- Check file size is under 16MB

**Port already in use?**
- Change port in app.py: `app.run(debug=True, port=5001)`

## License

Free to use for educational purposes.