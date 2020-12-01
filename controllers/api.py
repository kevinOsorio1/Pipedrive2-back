@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args):
        #listar productos
        return dict()
    
    def GET(*args, **vars):
        #buscar por id
        return dict()

    def POST(*args, **vars):
        #insertar producto
        return dict()

    def PUT(table_name, record_id,**vars):
        #actualizar producto
        db(db[table_name].id==record_id).update(**vars)
        return db(db.product.id==record_id).select(orderby=db.product.name)

    def DELETE(table_name,record_id):
        prod = db(db[table_name].id==record_id)
        prod.update(status=0)
        return 'Producto ', record_id, ' eliminado'
        
    return locals()
