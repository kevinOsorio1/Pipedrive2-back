@request.restful()
def api():
    response.view = 'generic.json'

    #GET_ALL pipedrive2/api/api/product.json
    #GET_BY pipedrive2/api/api/product/id/2.json
    def GET(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            if args[0] == 'product':
                for el in parser.response:
                    category = db(db.category.id == el.category_id).select()
                    user = db(db.user.id == el.owner_id).select()
                    el.category = category[0].name
                    el.owner = user[0].name
            result = {args[0]:parser.response}
            return result
        else:
            raise HTTP(parser.status,parser.error)

    def POST(table_name,**vars):
        db[table_name].validate_and_insert(**vars)
        return 'Elemento ',table_name, " registrado satisfactoriamente"

    def PUT(table_name, record_id,**vars):
        db(db[table_name].id==record_id).update(**vars)
        return db(db.product.id==record_id).select(orderby=db.product.name)

    def DELETE(table_name,record_id):
        prod = db(db[table_name].id==record_id)
        prod.update(status=0)
        return 'Producto ', record_id, ' eliminado'
        
    return locals()
