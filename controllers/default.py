from gluon.tools import Service
service = Service()

def call():
    session.forget()
    return service()

def monedas():
    monedas = db(db.currency.status != 0).select(orderby=db.currency.code)
    return locals()

def categorias():
    categorias = db(db.category.status != 0).select(orderby=db.category.name)
    return locals()

def producto():
    categorias = db(db.product.status != 0).select(orderby=db.product.name)
    return locals()

@service.json
def producto(id):
    producto = db(db.product.id == id).select()
    return producto