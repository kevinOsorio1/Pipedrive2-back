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

    def PUT(*args, **vars):
        #actualizar producto
        return dict()

    def DELETE(table_name,record_id):
        db(db[table_name].id==record_id).update(status=0)
        return 'Producto ', record_id, ' eliminado'

    return locals()
