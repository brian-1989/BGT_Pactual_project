from app.database import Funds, Users

fund_information = [
    {
        "_id": "1",
        "name": "FPV_BTG_PACTUAL_RECAUDADORA",
        "minimum_amount": 75000,
        "category": "FPV"
    },
    {
        "_id": "2",
        "name": "FPV_BTG_PACTUAL_ECOPETROL",
        "minimum_amount": 125000,
        "category": "FPV"
    },
    {
        "_id": "3",
        "name": "DEUDAPRIVADA",
        "minimum_amount": 50000,
        "category": "FIC"
    },
    {
        "_id": "4",
        "name": "FDO-ACCIONES",
        "minimum_amount": 250000,
        "category": "FIC"
    },
    {
        "_id": "5",
        "name": "FPV_BTG_PACTUAL_DINAMICA",
        "minimum_amount": 100000,
        "category": "FPV"
    }
]

user_information = [
    {
        "_id": "1",
        "name": "Brian Zapata Pino",
        "email": "dzapata397@gmail.com",
        "cellphone": "3122603428",
        "balance": 500000
    }
]

items = [
    {
        "collection": Funds,
        "data": fund_information
    },
    {
        "collection": Users,
        "data": user_information
    }
]

# Insert information into the collection


def initialize_collections():
    for item in items:
        collection = item.get("collection")
        data = item.get("data")
        if collection.count_documents({}) == 0:
            collection.insert_many(data)
