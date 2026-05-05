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
    },
    {
        "name": "Panic! At the Disco - Vices & Virtues Vinyl",
        "price": 100,
        "description": "A vinyl of the hit Album 'Vices & Virtues' by Panic! At the Disco.",
        "image": "VicesandVirtuesVinyl.jpeg",
        "environmentalImpactRating": 1
    },
    {
        "name": "Graphic Sonic the Hedgehog Poster",
        "price": 30,
        "description": "A minimalistic poster of Sonic the Hedgehog with modern/flat illustration with a bit of vector art mixed.",
        "image": "SonicPoster.jpeg",
        "environmentalImpactRating": 3
    },
        {
        "name": "Minecraft Torch LED Key Ring",
        "price": 5,
        "description": "Minecraft torch key ring with a LED light you can turn on and off by the press of a button.",
        "image": "MinecraftTorchKeyRing.jpeg",
        "environmentalImpactRating": 3
    },
    {
        "name": "Pokémon Plushie Set",
        "price": 60,
        "description": "Starter Pokémon Plushie set (Inc. Pikachu)",
        "image": "pokemonplushieset.jpeg",
        "environmentalImpactRating": 2
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
