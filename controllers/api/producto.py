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

    def PUT(*args, **vars):
        #actualizar producto
        return dict()

    def DELETE(*args, **vars):
        #softdelete producto
        return dict()

    return locals()