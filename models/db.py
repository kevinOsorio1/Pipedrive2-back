db = DAL('mysql://user1:user1@localhost:3306/pipedrive2')

from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from gluon.tools import Crud
auth = Auth(db)
auth.define_tables()
crud = Crud(db)

db.define_table('user',
    Field('name'),
    Field('email'),
    Field('passwd'),
    format='%(name)s')

db.define_table('category',
    Field('name'),
    format='%(name)s')

db.define_table('item',
    Field('name',),
    Field('code'),
    Field('description', type="string", length=256),
    Field('unit'),
    Field('tax',type='double'),
    Field('owner_id','reference user'),
    Field('category_id','reference category'),
    Field('enabled', type='boolean'),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime', default=request.now),
    format='%(name)s')

db.define_table('currency',
    Field('code'),
    Field('name'),
    Field('symbol'),
    Field('decimal_points',type='integer', default=0),
    Field('status',type='integer', default=1),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime', default=request.now),
    format='%(name)s')

db.define_table('variation',
    Field('name'),
    Field('item_id','reference item'),
    Field('enabled', type='boolean'),
    Field('description'),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime', default=request.now),
    format='%(name)s')

db.define_table('price',
    Field('price',type='double'),
    Field('reference_id'),
    Field('is_variation', type='boolean', default=False),
    Field('currency_id','reference currency'),
    Field('cost',type='double'),
    Field('overhead_cost',type='double'),
    Field('comment', type="string", length=256),
    Field('add_time', 'datetime', default=request.now),
    Field('update_time', 'datetime', default=request.now),
    format='%(name)s')

db.user.email.requires = IS_NOT_IN_DB(db, 'user.email')
db.user.email.requires = IS_NOT_EMPTY()
db.user.passwd.requires = IS_NOT_EMPTY()

db.category.name.requires = IS_NOT_EMPTY()

db.item.name.requires = IS_NOT_EMPTY()
db.item.owner_id.requires = IS_NOT_EMPTY()
db.item.add_time.readable = db.item.add_time.writable = False
db.item.update_time.readable = db.item.update_time.writable = False

db.currency.code.requires = IS_NOT_IN_DB(db, 'currency.code')
db.currency.code.requires = IS_NOT_EMPTY()
db.currency.name.requires = IS_NOT_EMPTY()
db.currency.add_time.readable = db.currency.add_time.writable = False
db.currency.update_time.readable = db.currency.update_time.writable = False

db.variation.name.requires = IS_NOT_EMPTY()
db.variation.item_id.requires = IS_NOT_EMPTY()
db.variation.add_time.readable = db.variation.add_time.writable = False
db.variation.update_time.readable = db.variation.update_time.writable = False

db.price.price.requires = IS_NOT_EMPTY()
db.price.reference_id.requires = IS_NOT_EMPTY()
db.price.currency_id.requires = IS_NOT_EMPTY()
db.price.add_time.readable = db.price.add_time.writable = False
db.price.update_time.readable = db.price.update_time.writable = False