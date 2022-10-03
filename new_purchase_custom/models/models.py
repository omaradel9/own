from odoo import models, fields, api
import itertools
from logging import info
from odoo.exceptions import ValidationError,UserError
import itertools
from decimal import Decimal
 



class productType(models.Model):
    _name = 'product.type'
    _description = 'productType'
    _rec_name = 'item_group'
    # product_type_name = fields.Char(string='Name')
    item_group      = fields.Selection([('RD', 'RD')], string='Item Group')
    item_groupss     = fields.Many2one(string='Item Group',comodel_name='stones.type')

    item_name       = fields.Char('Item Name')
    size_from       = fields.Float('Size From')
    size_to         = fields.Float('Size To')
    sale_price      = fields.Float('Sale Price')
    purchase_price  = fields.Float('Purchase Price')
    labor_price     = fields.Float('Labor Price')
    date            = fields.Datetime('Date')
    active          = fields.Boolean(string="Active")
    sale_categ      = fields.Selection([ ('3', 'Open Stone'),('4', 'Sealed Stone')], string='Item Category')
    stone_size      = fields.Selection([ ('D','D')
                                        ,('D-F','D-F')
                                        ,('E','E')
                                        ,('F','F')
                                        ,('F-I-Y','F-I-Y')
                                        ,('G','G')
                                        ,('G-H','G-H')
                                        ,('H','H')
                                        ,('I','I')
                                        ,('I-J','I-J')
                                        ,('J','J')
                                        ,('K','K')
                                        ,('K-L','K-L')
                                        ,('L','L')
                                        ,('M','M')
                                        ,('M-N','M-N')],string="Size")
    
    stone_color     = fields.Selection([ ('I1','I1')
                                        ,('I2','I2')
                                        ,('I3','I3')
                                        ,('IF','IF')
                                        ,('IF-VVS','IF-VVS')
                                        ,('LC','LC')
                                        ,('SI1','SI1')
                                        ,('SI2','SI2')
                                        ,('SI3','SI3')
                                        ,('VS','VS')
                                        ,('VS1','VS1')
                                        ,('VS2','VS2')
                                        ,('VVS1','VVS1')
                                        ,('VVS2','VVS2')],string="Color")
    
    stone_config    = fields.Selection([ ('EXCELLENT', 'EXCELLENT')
                                        ,('FAIR', 'FAIR')
                                        ,('GOOD', 'GOOD')
                                        ,('STD', 'STD')
                                        ,('Triple', 'Triple')
                                        ,('VeryGood', 'Very Good')],string="Configration")
    
    stone_style     = fields.Selection([ ('EXCELLENT', 'EXCELLENT')
                                        ,('FAIR', 'FAIR')
                                        ,('GOOD', 'GOOD')
                                        ,('STD', 'STD')
                                        ,('Triple', 'Triple')
                                        ,('VeryGood', 'Very Good')],string="Style")
          
class stonesType(models.Model):
    _name = 'stones.type'
    _description = 'stoneType'
    _rec_name = 'type_name'
    # product_type_name = fields.Char(string='Name')
    
    type_name       = fields.Char('Type Name')
    