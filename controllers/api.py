@request.restful()
def api():
    response.view = 'generic.json'

    #GET_ALL pipedrive2/api/api/{table_name}.json
    #
    #GET_BY pipedrive2/api/api/{table_name}/id/{id}.json
    #
    #CREATE pipedrive2/api/api/product
    #
    #    {
    #        "id": int,
    #        "name": string,
    #        "code": string,
    #        "description": string,
    #        "unit": string,
    #        "owner_id": int,
    #        "category_id": int,
    #        "category": category,
    #        "owner": user
    #    }
    #
    #UPDATE pipedrive2/api/api/product
    #
    #    {
    #        "name": string,
    #        "code": string,
    #        "description": string,
    #        "unit": string,
    #        "category_id": int,
    #        "category": category,
    #        "owner": user
    #    }
    #
    #SOFT-DELETE pipedrive2/api/api/product/{id}

    
    ##CHRIS##
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
            
    ##CHRIS##
    def POST(table_name,**vars):
        db[table_name].validate_and_insert(**vars)
        return 'Elemento ',table_name, " registrado satisfactoriamente"
    
    ##AGUSTIN##
    def PUT(table_name, record_id,**vars):
        db(db[table_name].id==record_id).update(**vars)
        return locals()
    
    ##AGUSTIN##
    def DELETE(table_name,record_id):
        el = db(db[table_name].id==record_id).select().first()
        if el.status != 0:
            el.update_record(status=0)
            el_name = table_name[0].upper() + table_name[1:] 
            return el_name, ' con id ', record_id, ' eliminado satisfactoriamente.'
        else:
            return 'No se encontraron coincidencias.'
        
        
    return locals()
