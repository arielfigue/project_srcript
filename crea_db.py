import sys
import time
import csv
import odoorpc

# conectarse al server
odoo = odoorpc.ODOO('192.168.56.101', 'jsonrpc', 8069)

# establecer tiempo de espera largo
odoo.config['timeout'] = 6000

database = raw_input('Como quiere llamar a su base de datos? ')
print "Creando la base de datos " + (database)

# crear la base de datos
odoo.db.create('root', database, demo=False, lang='en_US', admin_password='admin')

# loguearse en la base de datos
odoo.login(database, 'admin', 'admin')
print "logueado en la bd"

# instalar idioma
print "Instalando idioma ..."
LangInstall = odoo.env['base.language.install']
idioma = LangInstall.create({'lang':'es_MX'})
LangInstall.lang_install([idioma])
print "Idioma instalado"

# instalar modulos
print "iniciando instalacion de modulos ..."
module = odoo.env['ir.module.module']
for linea in csv.reader(open('modulos.csv')):
    module_id = module.search([('name', '=', linea)])
    module.button_immediate_install(module_id)
    print "modulo instalado " + linea[0]

# configurar modulo stock
print "iniciando configuracion de modulo stock ..."
cfg_stock = odoo.env['stock.config.settings']
cfg_stock_val = cfg_stock.create({
    'group_stock_production_lot' : 1,
    'module_product_expiry' : 0,
    'group_stock_tracking_lot' : 1,
    'group_stock_tracking_owner' : 1,
    'module_stock_barcode' : True,
    'module_stock_landed_costs' : 1,
    'group_stock_inventory_valuation' : 1,
    'module_delivery_dhl' : False,
    'module_delivery_fedex' : False,
    'module_delivery_temando' : False,
    'module_delivery_dhl' : False,
    'module_delivery_ups' : False,
    'module_delivery_usps' : False,
    'module_procurement_jit' : 1,
    'warehouse_and_location_usage_level' : 2,
    'group_stock_adv_location' : 0,
    'decimal_precision' : 0,
    'module_stock_dropshipping' : 0,
    'module_stock_picking_wave' : 0,
    'module_stock_calendar' : 0,
    'group_warning_stock' : 1,
    'group_uom' : 1,
    'group_product_variant' : 1,
    'group_stock_packaging' : 0,
    })
cfg_stock.execute(cfg_stock_val)
print "modulo stock configurado"
