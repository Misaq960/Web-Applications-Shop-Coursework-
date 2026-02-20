from flask import Flask, render_template, request

app = Flask(__name__)

stocks = [
    { "name": "Hoodie", "price": "£40", "description": "This is a standard white Hollister hoodie", "image": "hoodie.jpeg" },
    { "name": "Headphones", "price": "£60", "description": "This is a mid range bluetooth headphone set.", "image": "headphones.jpeg" },
    { "name": "Speakers", "price": "£50", "description": "This is a standard JBL bluetooth speaker.", "image": "speakers.jpeg" },
]

@app.route('/')
def galleryPage():
    return render_template('index.html', stocks=stocks)
    
@app.route('/stock/<int:stockId>', methods=['GET', 'POST'])
def singleProductPage(stockId):
    stock = stocks[stockId]

    if request.method == 'POST':
        quantity = request.form['quantity']
        return render_template('added.html', stock=stock, quantity=quantity)

    return render_template('SingleTech.html', stock=stock, stockId=stockId)

if __name__ == '__main__':
    app.run(debug=True)
