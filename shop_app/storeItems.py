from shopApp import app, db, Item

# Initial item data used to populate the database
items = [
    {
        "name": "Hoodie",
        "price": 40,
        "description": "This is a standard white Hollister hoodie",
        "image": "hoodie.jpeg",
        "environmentalImpactRating": 5
    },
    {
        "name": "Headphones",
        "price": 60,
        "description": "This is a mid range bluetooth headphone set.",
        "image": "headphones.jpeg",
        "environmentalImpactRating": 1
    },
    {
        "name": "Speakers",
        "price": 50,
        "description": "This is a standard JBL bluetooth speaker.",
        "image": "speakers.jpeg",
        "environmentalImpactRating": 2
    },
    {
        "name": "Football Boots",
        "price": 70,
        "description": "A pair of durable football boots designed for firm ground play.",
        "image": "football-boots.jpeg",
        "environmentalImpactRating": 4
    }
]

with app.app_context():
    # Reset database and recreate tables
    db.drop_all()
    db.create_all()

    # Insert items into the database
    for item in items:
        new_item = Item(
            name=item["name"],
            price=item["price"],
            description=item["description"],
            image=item["image"],
            environmentalImpactRating=item["environmentalImpactRating"]
        )
        db.session.add(new_item)

    db.session.commit()
    print("Database created and items inserted.")
