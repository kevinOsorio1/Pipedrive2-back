##db = DAL('mysql://root@localhost:3306/pypedrive2', migrate=True, fake_migrate=False)             #puerto:3306 Chris / puerto:8080 Agustin
#
#Se implementa mongoengine
db = DAL('mongodb+srv://ungeorgi:Ft5nVEERVGrYUNl4@ungeorgi-0.y7dq8.mongodb.net/pypedrive_refactor?retryWrites=true&w=majority')


from gluon.contrib.appconfig import AppConfig
from gluon.tools import Crud
crud = Crud(db)

db.define_table('user',
    Field('name','string'),
    Field('email','string'),
    Field('add_time', 'datetime'),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('category',
    Field('name','string'),
    Field('status', 'integer'),
    format='%(name)s')

db.define_table('currency',
    Field('code','string'),
    Field('name','string'),
    Field('symbol','string'),
    Field('decimal_points', 'integer'),
    Field('status', 'integer'),
    Field('add_time', 'datetime'),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('product',
    Field('name','string'),
    Field('code','string'),
    Field('description', 'string'),
    Field('unit','string'),
    Field('owner_id','reference user'),
    Field('category_id','reference category'),
    Field('status', 'integer'),
    Field('prices', 'list:reference product_price'),
    Field('tax', 'list:reference tax'),
    Field('variations', 'list:reference variations'),
    Field('add_time', 'datetime'),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('variation',
    Field('name','string'),
    Field('status', 'integer'),
    Field('prices', 'list:reference variation_price'),
    Field('add_time', 'datetime'),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('price',
    Field('ammount','double'),
    Field('currency_id','reference currency'),
    Field('cost','double'),
    Field('status', 'integer'),
    Field('add_time', 'datetime'),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('product_price',
    Field('price_id','reference price'),
    Field('overhead_cost','double'),
    Field('add_time', 'datetime'),
    Field('update_time', 'datetime'))

db.define_table('variation_price',
    Field('name','string'),
    Field('price_id','reference price'),
    Field('add_time', 'datetime'),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('tax',
    Field('name','string'),
    Field('ammount','double'),
    Field('type', 'integer'),
    Field('status', 'integer'),
    Field('add_time', 'datetime'),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('activity',
    Field('prev_status', "integer"),
    Field('new_status', "integer"),
    Field('activity_time', 'datetime'),
    Field('user_id','reference user'),
    Field('category_id','reference category'),
    Field('product_id','reference product'),
    Field('variation_id','reference variation'),
    Field('price_id','reference price'),
    Field('currency_id','reference currency'),
    Field('tax_id','reference tax'),
    Field('status', "integer"),
    Field('add_time', 'datetime'))

db.user.email.requires = IS_NOT_IN_DB(db, 'user.email')
db.user.email.requires = IS_NOT_EMPTY()

db.activity.user_id.requires = IS_NOT_EMPTY()
db.activity.new_status.requires = IS_NOT_EMPTY()

db.category.name.requires = IS_NOT_EMPTY()

db.product.name.requires = IS_NOT_EMPTY()
db.product.owner_id.requires = IS_NOT_EMPTY()

db.currency.code.requires = IS_NOT_EMPTY()
db.currency.code.requires = IS_NOT_IN_DB(db, 'currency.code')
db.currency.name.requires = IS_NOT_EMPTY()

db.variation.name.requires = IS_NOT_EMPTY()

db.price.ammount.requires = IS_NOT_EMPTY()
db.price.currency_id.requires = IS_NOT_EMPTY()