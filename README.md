<h1>Pipedrive2-back<h1>

#Replica de prueba en http://agustinfranchetti.pythonanywhere.com/ con las siguientes rutas de endpoints:

#for now, we're going to be foccusing on table "product"

<h2>GET ALL ELEMENTS OF A CERTAIN GROUP<h2>
  
- GET pipedrive2/api/api/{table_name}

  - returns:
  
```json
 {
    "message": "Operacion exitosa",
    "data": {
        "product": [
            {
                "status": 1,
                "category": "calzado",
                "update_time": "2020-12-02 21:33:05",
                "code": "a12",
                "name": "Zapato rojo",
                "description": "zapato timberland",
                "owner_id": 1,
                "owner": "Agustin Franchetti",
                "category_id": 6,
                "id": 1,
                "unit": "US size",
                "add_time": "2020-12-02 15:24:31"
            },
            {...}
        ]
    }
}
```
      
<h2>GET A SPECIFIC ELEMENT BY ID<h2>
  
- GET pipedrive2/api/api/{table_name}/id/{id}
  
  -returns:
  
```json
{
    "message": "Operacion exitosa",
    "data": {
        "product": [
            {
                "status": 1,
                "category": "ropa",
                "update_time": "2020-12-02 18:27:23",
                "code": "123qwe",
                "name": "polera negra L",
                "description": "Polera manga larga negra",
                "owner_id": 1,
                "owner": "Agustin Franchetti",
                "category_id": 5,
                "id": 2,
                "unit": "unidad",
                "add_time": "2020-12-02 15:53:47"
            }
        ]
    }
}
```

<h2>CREATE AN ELEMENT<h2>
  
- POST pipedrive2/api/api/{table_name}

  - Fileds marked with (*) are obligatory
  
```json
{
    "code": "123qwe",
    "name": "polera negra L", (*)
    "description": "Polera manga larga negra",
    "owner_id": 1, (*)
    "category_id": 5, (*)
    "unit": "unidad",
}
```

<h2>UPDATE AN ELEMENT<h2>
  
- PUT pipedrive2/api/api/{table_name}

  -You can update any of the following
  
```json
{
    "code": "string",
    "name": "string",
    "description": "string",
    "category_id": "int",
    "unit": "string" --> unit of meassure (kg, m, cm, etc)
}
```

<h2>SOFT-DELETE AN ELEMENT<h2>
  
- DELETE pipedrive2/api/api/{table_name}/{id}<br>
  
  - If succesful, returns "Product con id 2 eliminado satisfactoriamente.". Else returns an error
