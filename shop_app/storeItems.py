from shop_app import app, db, Item

items = [
    {
        "name": "Hoodie",
        "price": 40,
        "description": "This is a standard white Hollister hoodie",
        "image": "hoodie.jpeg"
    },
    {
        "name": "Headphones",
        "price": 60,
        "description": "This is a mid range bluetooth headphone set.",
        "image": "headphones.jpeg"
    },
    {
        "name": "Speakers",
        "price": 50,
        "description": "This is a standard JBL bluetooth speaker.",
        "image": "speakers.jpeg"
    }
]

with app.app_context():
    db.drop_all()      # clears old data if you re-run
    db.create_all()    # creates tables

    for item in items:
        new_item = Item(
            name=item["name"],
            price=item["price"],
            description=item["description"],
            image=item["image"]
        )
        db.session.add(new_item)

    db.session.commit()
    print("Database created and items inserted.")
