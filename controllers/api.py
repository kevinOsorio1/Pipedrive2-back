@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response, arggs=args, varrs=vars)
        else:
            raise HTTP(parser.status,parser.error)

    def POST(table_name, object):
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
