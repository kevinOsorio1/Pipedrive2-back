db = DAL('mysql://root@localhost:3306/pypedrive2')             #puerto:3306 Chris / puerto:8080 Agustin

from gluon.contrib.appconfig import AppConfig
#from gluon.tools import Auth                                   No conciderar en primera iteracion
from gluon.tools import Crud
#auth = Auth(db)                                                No conciderar en primera iteracion
crud = Crud(db)

db.define_table('user',
    Field('name',type="string", length=255),
    Field('email',type="string", length=255),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime'),
#    Field('passwd'),                                           No conciderar en primera iteracion
    format='%(name)s')

db.define_table('category',
    Field('name',type="string", length=255),
    Field('status', type='integer', default = 1),
    format='%(name)s')

db.define_table('currency',
    Field('code',type="string", length=5),
    Field('name',type="string", length=255),
    Field('symbol',type="string", length=5),
    Field('decimal_points', type='integer', default=0),
    Field('status', type='integer', default = 1),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('product',
    Field('name',type="string", length=255),
    Field('code',type="string", length=255),
    Field('description', type="string", length=255),
    Field('unit',type="string", length=255),
    Field('owner_id','reference user'),
    Field('category_id','reference category'),
    Field('status', type='integer', default = 1),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('variation',
    Field('name',type="string", length=255),
    Field('product_id','reference product'),
    Field('status', type='integer', default = 1),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('price',
    Field('ammount',type='double'),
    Field('currency_id','reference currency'),
    Field('cost',type='double'),
    Field('status', type='integer', default = 1),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('product_price',
    Field('price_id','reference price'),
    Field('product_id','reference product'),
    Field('overhead_cost',type='double'),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime'))

db.define_table('variation_price',
    Field('name',type="string", length=255),
    Field('price_id','reference price'),
    Field('variation_id','reference variation'),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('tax',
    Field('product_id','reference product'),
    Field('name',type="string", length=255),
    Field('ammount',type='double'),
    Field('type', type='integer', default=1),
    Field('status', type='integer', default = 1),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime'),
    format='%(name)s')

db.define_table('activity',
    Field('prev_status', type="integer"),
    Field('new_status', type="integer"),
    Field('activity_time', 'datetime'),
    Field('user_id','reference user'),
    Field('category_id','reference category', requires=IS_EMPTY_OR(IS_IN_DB(db, 'category.id'))),
    Field('product_id','reference product', requires=IS_EMPTY_OR(IS_IN_DB(db, 'product.id'))),
    Field('variation_id','reference variation', requires=IS_EMPTY_OR(IS_IN_DB(db, 'variation.id'))),
    Field('price_id','reference price', requires=IS_EMPTY_OR(IS_IN_DB(db, 'price.id'))),
    Field('currency_id','reference currency', requires=IS_EMPTY_OR(IS_IN_DB(db, 'currency.id'))),
    Field('tax_id','reference tax', requires=IS_EMPTY_OR(IS_IN_DB(db, 'currency.id'))),
    Field('status', type="integer"),
    Field('add_time', 'datetime', default=request.now))

db.user.email.requires = IS_NOT_IN_DB(db, 'user.email')
db.user.email.requires = IS_NOT_EMPTY()
#db.user.passwd.requires = IS_NOT_EMPTY()                                   No conciderar en primera iteracion

db.activity.user_id.requires = IS_NOT_EMPTY()
db.activity.new_status.requires = IS_NOT_EMPTY()

db.category.name.requires = IS_NOT_EMPTY()

db.product.name.requires = IS_NOT_EMPTY()
db.product.owner_id.requires = IS_NOT_EMPTY()

db.currency.code.requires = IS_NOT_EMPTY()
db.currency.code.requires = IS_NOT_IN_DB(db, 'currency.code')
db.currency.name.requires = IS_NOT_EMPTY()

db.variation.name.requires = IS_NOT_EMPTY()
db.variation.product_id.requires = IS_NOT_EMPTY()

db.price.ammount.requires = IS_NOT_EMPTY()
db.price.currency_id.requires = IS_NOT_EMPTY()

db.product_price.price_id.requires = IS_NOT_EMPTY()
db.product_price.product_id.requires = IS_NOT_EMPTY()

db.variation_price.price_id.requires = IS_NOT_EMPTY()
db.variation_price.variation_id.requires = IS_NOT_EMPTY()

db.tax.product_id.requires = IS_NOT_EMPTY()
