from datetime import datetime


@request.restful()
def api():
    response.view = 'generic.json'

    # GET_ALL pipedrive2/api/api/{table_name}.json
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
    # GET_BY pipedrive2/api/api/{table_name}/id/{id}.json
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
    # CREATE pipedrive2/api/api/{table_name}
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
    # UPDATE pipedrive2/api/api/{table_name}
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
    # SOFT-DELETE pipedrive2/api/api/{table_name}/{id}

    ##CHRIS##
    def GET(*args, **vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns, args, vars)
        if parser.status == 200:
            message = "Operacion exitosa"
            # En caso que la consulta sea de productos, se rescatan los nombres de moneda y usuario anexos
            if args[0] == 'product':
                product = []
                for el in parser.response:
                    category = db(db.category.id == el.category_id).select()
                    user = db(db.user.id == el.owner_id).select()
                    el.owner = user[0].name
                    if el.category_id:  # Producto puede registrarse sin categoria, por lo que es necesario validar
                        el.category = category[0].name
                    if el.status == 1:  # Solo se retornaran los productos 'activos' (status = 1)
                        product.append(el)        
                data = {'product': product}
                return dict(message = message, data = data)
            data = {args[0]: parser.response}
            return dict(message = message, data = data)
        else:
            raise HTTP(parser.status, parser.error)

    ##CHRIS##
    def POST(table_name, **vars):
        if vars:  # Se verifica que request contenga datos en el body
            insert_check = db[table_name].validate_and_insert(**vars)
            if insert_check.id:  # Verifica si se genero una id nueva
                message = "Elemento {} registrado satisfactoriamente con id = {}".format(
                    table_name, insert_check.id)
                del insert_check  # Se limpia el outpu
            else:
                message = "No se ha podido registrar el elemento {}. {}".format(
                    table_name, insert_check.errors)
                del insert_check  # Se limpia el outpu
        else:
            message = "No se puede registrar un elemento vacio"
        return locals()

    ##AGUSTIN##
    def PUT(table_name, record_id, **vars):
        for x in vars:
            if x == "id" or x == "owner_id" or x == "status":
                return 'Está intentando modificar un parametro no permitido ("id","owner_id", "status")'

        now = datetime.now()
        db(db[table_name].id == record_id).update(**vars, update_time=now)
        el = db(db[table_name].id == record_id).select().first()
        new_activity(table_name, record_id, el.status, el.status, now)
        return locals()

    ##AGUSTIN##
    def DELETE(table_name, record_id):
        el = db(db[table_name].id == record_id).select().first()
        now = datetime.now()
        if el.status != 0:
            new_activity(table_name, record_id, el.status, 0, now)
            el.update_record(status=0)
            el_name = table_name[0].upper() + table_name[1:]
            return el_name, ' con id ', record_id, ' eliminado satisfactoriamente.'
        else:
            return 'No se encontraron coincidencias.'

    return locals()

##CHRIS##
# Registra una nueva actividad tras actualizar un registro, por UPDATE o DELETE(soft delete)
def new_activity(table_name, record_id, status_old, status_new, now):
    db(db[table_name].id == record_id).update(update_time=datetime.now())
    new_activity = db.activity.validate_and_insert(
        prev_status=status_old,
        new_status=status_new,
        activity_time=now,
        user_id=1)  # Por defecto, hasta que se aplique Auth()
    #  Validacion de referencia de actividad
    if table_name == 'product':
        db(db.activity.id == new_activity.id).update(product_id=record_id)
    if table_name == 'currency':
        db(db.activity.id == new_activity.id).update(currency_id=record_id)
    if table_name == 'variation':
        db(db.activity.id == new_activity.id).update(variation_id=record_id)
    if table_name == 'category':
        db(db.activity.id == new_activity.id).update(category_id=record_id)
    if table_name == 'price':
        db(db.activity.id == new_activity.id).update(price_id=record_id)
    if table_name == 'tax':
        db(db.activity.id == new_activity.id).update(tax_id=record_id)