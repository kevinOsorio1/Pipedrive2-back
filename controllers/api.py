@request.restful()
def api():
    response.view = 'generic.json'

    #GET_ALL pipedrive2/api/api/{table_name}.json
    #
    #    {
    #    "message": "Operacion exitosa",
    #    "data": {
    #        "currency": [
    #            {
    #                "id": 1,
    #                "code": "CLP",
    #                "name": "Pesos Chilenos",
    #                "symbol": "CLP$",
    #                "decimal_points": 0,
    #                "status": 1,
    #                "add_time": "2020-12-02 10:55:15",
    #                "update_time": null
    #            },
    #            { ... }
    #    }
    #
    #GET_BY pipedrive2/api/api/{table_name}/id/{id}.json
    #
    #    {
    #    "message": "Operacion exitosa",
    #    "data": {
    #        "currency": [
    #            {
    #                "id": 1,
    #                "code": "CLP",
    #                "name": "Pesos Chilenos",
    #                "symbol": "CLP$",
    #                "decimal_points": 0,
    #                "status": 1,
    #                "add_time": "2020-12-02 10:55:15",
    #                "update_time": null
    #            },
    #            { ... }
    #    }
    #
    #CREATE pipedrive2/api/api/{table_name}
    #
    #    {
    #        "table_name": "currency",
    #        "vars": {
    #                   "decimal_points": "0",
    #                   "name": "test",
    #                   "code": "qaw123",
    #                   "symbol": "CLP$"
    #                },
    #        "message": "Elemento currency registrado satisfactoriamente con id = 3"
    #    }
    #
    #UPDATE pipedrive2/api/api/{table_name}
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
    #SOFT-DELETE pipedrive2/api/api/{table_name}/{id}
    
    ##CHRIS##
    def GET(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            if args[0] == 'product': #        En caso que la consulta sea de productos, se rescatan los nombres de moneda y usuario anexos
                for el in parser.response:
                    category = db(db.category.id == el.category_id).select()
                    user = db(db.user.id == el.owner_id).select()
                    el.owner = user[0].name
                    if el.category_id:#       Producto puede registrarse sin categoria, por lo que es necesario validar
                        el.category = category[0].name
                del el, category, user#       Se limpia el output
            message = "Operacion exitosa"
            data = {args[0]:parser.response}
            del patterns, parser, args, vars# Se limpia el output
            return locals()
        else:
            raise HTTP(parser.status,parser.error)
            
    ##CHRIS##
    def POST(table_name,**vars):
        if vars:#                           Se verifica que request contenga datos en el body
            insert_check = db[table_name].validate_and_insert(**vars)
            if insert_check.id:#             Verifica si se genero una id nueva
                message = f"Elemento {table_name} registrado satisfactoriamente con id={insert_check.id}"
                del insert_check#            Se limpia el outpu
            else:
                message = f"No se ha podido registrar el elemento {table_name}. {insert_check.errors}"
                del insert_check#            Se limpia el outpu
        else:
            message = "No se puede registrar un elemento vacio"
        return locals()
    
    ##AGUSTIN##
    def PUT(table_name, record_id,**vars):
        for el in vars:
            if el == "id" or el == "owner_id" or el == "status":
                return 'Está intentando modificar un parametro no permitido ("id","owner_id", "status")'
                       
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
