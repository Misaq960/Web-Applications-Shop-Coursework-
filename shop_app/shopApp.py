from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Session configuration
app.config['SECRET_KEY'] = 'something-secret'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Item model
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    image = db.Column(db.String(64))
    environmentalImpactRating = db.Column(db.Integer)

# Luhn algorithm for card validation
def luhn_check(card_number):
    digits = [int(d) for d in str(card_number)][::-1]
    total = 0

    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d

    return total % 10 == 0

# Home page with sorting
@app.route('/')
def index():
    sort_field = request.args.get('sort')
    sort_order = request.args.get('order')

    query = Item.query

    # Sorting logic
    if sort_field == "name":
        query = query.order_by(Item.name.asc() if sort_order == "asc" else Item.name.desc())
    elif sort_field == "price":
        query = query.order_by(Item.price.asc() if sort_order == "asc" else Item.price.desc())
    elif sort_field == "impact":
        query = query.order_by(Item.environmentalImpactRating.asc() if sort_order == "asc" else Item.environmentalImpactRating.desc())

    items = query.all()
    return render_template('index.html', stocks=items, sort_field=sort_field, sort_order=sort_order)

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

    # Increase quantity if item already exists
    for entry in basket:
        if entry['id'] == item_id:
            entry['qty'] += qty
            session['basket'] = basket
            return render_template('added.html', item=item, qty=qty)

    # Otherwise add new entry
    basket.append({'id': item_id, 'qty': qty})
    session['basket'] = basket

    return render_template('added.html', item=item, qty=qty)

# Remove a single quantity of an item
@app.route('/remove_single/<int:item_id>', methods=['POST'])
def removeSingle(item_id):
    if 'basket' not in session:
        session['basket'] = []

    basket = session['basket']
    remove_qty = int(request.form.get('remove_qty', 1))

    for entry in basket:
        if entry['id'] == item_id:
            entry['qty'] -= remove_qty
            if entry['qty'] <= 0:
                basket.remove(entry)
            break

    session['basket'] = basket
    return redirect('/basket')

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

# Checkout page with validation
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    error = None

    if request.method == 'POST':
        name = request.form.get('name')
        card_number = request.form.get('card_number')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        address = request.form.get('address')

        # Clean card number
        clean_number = card_number.replace(" ", "").replace("-", "")

        # Card number checks
        if not clean_number.isdigit():
            error = "Card number must contain only digits, spaces, or dashes."
        elif len(clean_number) != 16:
            error = "Card number must be exactly 16 digits long."
        elif not luhn_check(clean_number):
            error = "Invalid card number. Please check and try again."

        # CVV checks
        elif not cvv.isdigit():
            error = "CVV must contain only digits."
        elif len(cvv) != 3:
            error = "CVV must be exactly 3 digits."

        # Expiry format check
        elif "/" not in expiry:
            error = "Expiry date must be in MM/YY or MM/YYYY format."

        else:
            parts = expiry.split("/")

            if len(parts) != 2:
                error = "Expiry date must be in MM/YY or MM/YYYY format."
            else:
                month = parts[0]
                year = parts[1]

                # Allow 1-digit month
                if len(month) == 1 and month.isdigit():
                    month = "0" + month

                # Month checks
                if len(month) != 2 or not month.isdigit():
                    error = "Expiry month must be one or two digits (1–12)."
                elif int(month) < 1 or int(month) > 12:
                    error = "Expiry month must be between 01 and 12."

                # Year checks
                elif not year.isdigit():
                    error = "Expiry year must contain only digits."
                elif len(year) == 2:
                    pass
                elif len(year) == 4 and year.startswith("20"):
                    year = year[2:]
                else:
                    error = "Expiry year must be YY or YYYY starting with 20."

                # Check if expiry is in the future
                if error is None:
                    exp_month = int(month)
                    exp_year = int(year) + 2000

                    now = datetime.now()

                    if exp_year < now.year:
                        error = "Card has expired."
                    elif exp_year == now.year and exp_month < now.month:
                        error = "Card has expired."
                    else:
                        return redirect('/order_confirmed')

    return render_template('checkout.html', error=error)

# Order confirmation page
@app.route('/order_confirmed')
def order_confirmed():
    return render_template('orderConfirmed.html')

if __name__ == '__main__':
    app.run(debug=True)
