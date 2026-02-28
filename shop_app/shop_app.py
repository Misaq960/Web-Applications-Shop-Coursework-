from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = 'something-secret'

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise SQLAlchemy
db = SQLAlchemy(app)

# Database model for items
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    image = db.Column(db.String(64))

# Home page: list all items
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', stocks=items)

# Single item page
@app.route('/item/<int:item_id>')
def itemPage(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return "Item not found", 404
    return render_template('item.html', item=item)

# Add item to basket
@app.route('/add_to_basket/<int:item_id>', methods=['POST'])
def add_to_basket(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return "Item not found", 404

    qty = int(request.form.get('qty', 1))

    if 'basket' not in session:
        session['basket'] = []

    basket = session['basket']

    # If item already in basket, increase quantity
    found = False
    for entry in basket:
        if entry['id'] == item_id:
            entry['qty'] += qty
            found = True
            break

    if not found:
        basket.append({'id': item_id, 'qty': qty})

    session['basket'] = basket

    return render_template('added.html', item=item, qty=qty)

# Basket page
@app.route('/basket')
def basketPage():
    if 'basket' not in session:
        session['basket'] = []

    basket_items = []
    total = 0

    for entry in session['basket']:
        item = Item.query.get(entry['id'])
        if item is None:
            continue
        qty = entry['qty']
        subtotal = item.price * qty
        total += subtotal

        basket_items.append({
            'item': item,
            'qty': qty,
            'subtotal': subtotal
        })

    return render_template('basket.html', basket=basket_items, total=total)

# Clear basket
@app.route('/clear_basket')
def clearBasket():
    session['basket'] = []
    return redirect('/basket')

if __name__ == '__main__':
    app.run(debug=True)
