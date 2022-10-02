# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = 'product.template'
    
    karat               = fields.Selection(string='Karat',selection=  [('9', '9K'),('12', '12K'),('14', '14K'),('18', '18K'),('21', '21K'),('22', '22K')],)
    karat_silver        = fields.Selection(string='Silver Karat',selection=  [('999', '999'),('925', '925'),('835', '835'),('800', '800')],)
    has_stones          = fields.Boolean('Stones Weight Included')
    has_stones_price    = fields.Boolean('Stones Price Included')
    product_type_name   = fields.Many2one(string='Product Stone Type',comodel_name='product.type')
    Stone_type_name     = fields.Many2one(string='Product Stone Type',comodel_name='stones.type',editable=False)

    item_cat            = fields.Selection([ ('1', 'Gold Jewelry')
                                            ,('2', 'Gold Material')
                                            ,('3', 'Open Stone')
                                            ,('4', 'Sealed Stone')
                                            ,('5', 'Diamond Jewelry')
                                            ,('6', 'Montrat')
                                            ,('7', 'Scrap')
                                            ,('8', 'Silver')
                                            ], string='Item Category')
    
    @api.onchange('seller_ids')
    def _onchange_(self):
       num_vend = len(self.seller_ids)
       if num_vend > 1 :
            raise ValidationError("Please one Vendor")

    

