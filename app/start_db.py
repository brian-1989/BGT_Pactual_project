from app.database import Funds, Users

fund_information = [
    {
        "_id": "1",
        "nombre": "FPV_BTG_PACTUAL_RECAUDADORA",
        "monto_minimo": 75000,
        "categoria": "FPV"
    },
    {
        "_id": "2",
        "nombre": "FPV_BTG_PACTUAL_ECOPETROL",
        "monto_minimo": 125000,
        "categoria": "FPV"
    },
    {
        "_id": "3",
        "nombre": "DEUDAPRIVADA",
        "monto_minimo": 50000,
        "categoria": "FIC"
    },
    {
        "_id": "4",
        "nombre": "FDO-ACCIONES",
        "monto_minimo": 250000,
        "categoria": "FIC"
    },
    {
        "_id": "5",
        "nombre": "FPV_BTG_PACTUAL_DINAMICA",
        "monto_minimo": 100000,
        "categoria": "FPV"
    }
]

user_information = [
    {
        "_id": "1",
        "nombre": "Brian Zapata Pino",
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
