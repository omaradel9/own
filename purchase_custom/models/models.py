from odoo import models, fields, api
import itertools
from logging import info
from odoo.exceptions import ValidationError,UserError
import itertools
from decimal import Decimal
import logging


class PurchaseOrderOld(models.Model):
    _inherit = 'purchase.order'
    _logger  = logging.getLogger(__name__)

    
    k9          = fields.Float(string='Karat 9k Weight  (G)',compute='_compute_line_weight',store= True)
    k12         = fields.Float(string='Karat 12k Weight (G)',compute='_compute_line_weight',store= True)
    k14         = fields.Float(string='Karat 14k Weight (G)',compute='_compute_line_weight',store= True)
    k18         = fields.Float(string='Karat 18k Weight (G)',compute='_compute_line_weight',store= True)
    k21         = fields.Float(string='Karat 21k Weight (G)',compute='_compute_line_weight',store= True)
    k22         = fields.Float(string='Karat 22k Weight (G)',compute='_compute_line_weight',store= True)
    k24         = fields.Float(string='Karat 24k Weight (G)',compute='_compute_line_weight',store= True)
    c_karat     = fields.Float(string='Converted Karat Weight (G)',compute='_compute_line_weight',store= True)
    sale_categ  = fields.Selection([ ('1', 'Gold Jewelry')
                                    ,('2', 'Gold Material')
                                    ,('3', 'Open Stone')
                                    ,('4', 'Sealed Stone')
                                    ,('5', 'Diamond Jewelry')
                                    ,('6', 'Montrat')
                                    ,('7', 'Scrap')
                                    ,('8', 'Silver')], string='Item Category')
    
    sale_mode   = fields.Selection([('1', 'Fixed'),('2', 'Daily')],string="Sale Base")
    field_invis = fields.Boolean(default=False)
    product_rec = fields.Boolean(default=False)
    vals        = fields.Char('vals',readonly=True)
    

    tesxt = fields.Char(string="tesxt")

    @api.onchange('sale_mode')
    def _onchange_base(self):
        if self.sale_categ == '1' :
            for red in self :
                red.invoice_ids.sale_mode = self.sale_mode
        
        
    
    @api.onchange('partner_id')
    def _onchange_sale_base(self):
        
            self.sale_mode = self.partner_id.sale_mode
        
    @api.depends('order_line')
    def action_create_serial(self):
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.production.lot',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id ref="stock.production.lot.form"': '',
                'target': 'current',
            }
    def _compute_line_weight(self):
      if self.sale_categ in ('1','6','2','7'):
        line_weight9  = 0
        line_weight14 = 0
        line_weight18 = 0
        line_weight21 = 0
        line_weight22 = 0
        line_weight24 = 0
        convert_karat = 0
        karatn        = ""
        for purchase in self:
            for line in purchase.order_line:
                convert_karat = int(line.c_karats)
                karatn        = line.karats
                if line.karats == "9":
                    line_weight9  += line.product_uom_qty
                elif line.karats  == "12":
                    line_weight12 +=  line.product_uom_qty
                elif line.karats  == "14":
                    line_weight1  +=  line.product_uom_qty
                elif line.karats  == "18":
                    line_weight18 +=  line.product_uom_qty
                elif line.karats  == "21":
                    line_weight21 +=  line.product_uom_qty
                elif line.karats  == "22":
                    line_weight22 += line.product_uom_qty
                elif line.karats  == "24":
                    line_weight24 += line.product_uom_qty
                    
            purchase.k9  = line_weight9
            purchase.k12 = line_weight12
            purchase.k14 = line_weight14
            purchase.k18 = line_weight18
            purchase.k21 = line_weight21
            purchase.k22 = line_weight22
            purchase.k24 = line_weight24

            if convert_karat and karatn :
                purchase.c_karat = (((line_weight9 * 9)/convert_karat)
                                   +((line_weight12 * 12)/convert_karat)
                                   +((line_weight14 * 14)/convert_karat)
                                   +((line_weight18 * 18)/convert_karat)
                                   +((line_weight21 * 21)/convert_karat)
                                   +((line_weight22 * 22)/convert_karat)
                                   +((line_weight24 * 24)/convert_karat))

          
    @api.onchange('order_line')
    def serial_uniqe(self):
            self.order_line.update({
                        'sale_sale':  self.sale_mode

                    }) 
        
            
    @api.onchange('sale_categ')
    def onchange_sale_categ(self):
        if self.sale_categ == '1' :
            self.field_invis = True

        elif self.sale_categ == '2' :
            self.field_invis = False
 
    # @api.onchange('partner id')
    # def onchange_partner_id(self):
    #     for rec in self.order_line:
    #         return {'domain': {'product_id': [('partner_id', '=', rec.saller_ids.name)]}}
    def action_set_picking(self):
        self.picking_ids.state = 'done'
        self.picking_ids.date_done = fields.datetime.now()
        self.picking_ids.move_lines.state = 'done'
        self.product_rec = True
        for order_line in self.order_line :
            product_move  = self.env['stock.move'].search([('purchase_line_id', '=', order_line.id)]).move_line_ids
            for move in product_move : 
                product_serial  = self.env['stock.production.lot'].search([('name', '=', order_line.serial)])

                move.lot_name           = order_line.serial
                move.lot_id             = product_serial.id
                # move.product_uom_qty    = 0
                # move.product_qty        = 0
                move.qty_done           = 1
                move.state              = 'done'
        
        
        
class PurchaseOrderLineOld(models.Model):
    _inherit = 'purchase.order.line'
    _logger  = logging.getLogger(__name__)
    
    
    serial          = fields.Char(string='Serial')
    sale_sale       = fields.Char(string="mode")
    karats          = fields.Char('Karat',readonly=True)
    c_karats        = fields.Char(string='C Karat',store= True)
    making_price    = fields.Float('Cost',digits=(12,4),readonly=True)
    gold_price      = fields.Float('Gold Price',digits=(12,4),readonly=True)
    weight          = fields.Float('Weight',digits=(12,4) ,store= True)
    cost_price_gold = fields.Float(string='Cost')
    available       = fields.Boolean(default=True)
    field_invis     = fields.Boolean(default=False)
    serialso        = fields.Many2one(string='Serial',comodel_name='stock.production.lot')
    stone_type      = fields.Many2one(string='Type',comodel_name='product.type')
    Stone_types     = fields.Many2one(string='Type',comodel_name='stones.type')

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
    
    
    

  
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.order_id.sale_categ == '1' :
            self.field_invis = True
            return {'domain': {'product_id': [('seller_ids.name', '=',self.partner_id.id)]}}
        elif self.order_id.sale_categ == '2' :
            self.field_invis = False
            return {'domain': {'product_id': [('seller_ids.name', '=',self.partner_id.id)]}}
   
           
    @api.onchange('serialso')
    def serial_so(self):
        if self.order_id.sale_categ == '2' :
            for line in self :
                line.product_id  = line.serialso.product_id

    @api.onchange('product_id')
    def serial_soffr(self):
        if self.order_id.sale_categ == '2' :
            for line in self :
                if line.product_id  :
                    line.product_qty =  1
                    
    @api.onchange('product_uom')
    def serial_product_qty(self):
        if self.order_id.sale_categ == '2' :
    
            for line in self :
                if self.order_id.sale_mode == '1' :
                    line.price_unit = line.serialso.whole_gold
                elif self.order_id.sale_mode == '2' :
                    line.price_unit = line.serialso.retail_gold
                    
    @api.onchange('serial','weight')
    def product_change(self):
        
            
            self.field_invis = True

            self.sale_sale  = self.order_id.sale_mode
            gold_p          = self.env['gold.price']
            prod            = self.product_id.id
            product_product = self.env['product.product'].search([('id', '=', prod)]).product_tmpl_id
            karat           = product_product.karat
            making          = product_product.standard_price
            product_serial  = self.env['stock.production.lot'].search([('name', '=', self.serial)])
            weight_gold     = self.weight
            stones_type     = product_product.Stone_type_name

            if prod and self.serial and not product_serial and weight_gold > 0 :
                if self.order_id.sale_categ in ('1','6') :
                        self.env['stock.production.lot'].create({
                            'name'          : self.serial,
                            'product_id'    : prod,
                            'weight'        : weight_gold,
                            'product_categ' : self.order_id.sale_categ,
                            'company_id'    : self.env.company.id,
                        })  
            
            for rec in self:
                    
                        # rec.product_qty = weight_gold
                    rec.karats          = karat
                    latest_price        = gold_p.search([('karat' , '=',rec.karats)], limit=1, order='day desc').gold_price
                    convert_karat       = gold_p.search([('karat' , '=',rec.karats)], limit=1, order='day desc').conversion_karat
                    rec.c_karats        = convert_karat
                    rec.gold_price      = latest_price
                    rec.making_price    = making
                    rec.product_id      = prod 
                    rec.Stone_types     = stones_type
                    serials_qty         = rec.product_qty
                    convert_int         = float(convert_karat)
                    qty_m_karat         = serials_qty * float(karat) 
                    
                    if self.order_id.sale_categ in ('1','2','6') :
                        if rec.sale_sale == "1" :
                            
                            rec.update({
                                    'price_unit' : rec.making_price * rec.weight
                                })
                        elif rec.sale_sale == "2" :
                            rec.update({
                                    'price_unit' :  (rec.making_price + latest_price)* rec.weight
                            })
                    
                
   
            
    @api.onchange('stone_color','stone_config','weight')
    def stone_conf_change(self):
            product_products = self.env['product.product'].search([('id', '=', self.product_id.id)]).product_tmpl_id
            stones_type     = product_products.Stone_type_name
            item_type       = product_products.item_cat
            
            if self.stone_color and self.stone_config and self.weight and item_type == '4' :
                
                line_weight     = self.weight
                product_types = self.env['product.type'].search([ ('stone_config', '=', self.stone_config)
                                                                 ,('stone_color', '=', self.stone_color)
                                                                 ,('item_groupss', '=', self.Stone_types.id)
                                                                 ,('sale_categ', '=', item_type)])
                

            
                for rec in product_types :
                    if rec.size_from <= line_weight and rec.size_to >= line_weight :
                        self.update({
                                    'price_unit' : rec.purchase_price
                                })
                    product_serial  = self.env['stock.production.lot'].search([('name', '=', self.serial)])

                    if self.product_id and self.serial and not product_serial and self.order_id.sale_categ == '4' and self.product_qty > 0 :
                                self.env['stock.production.lot'].create({
                                    'name'          : self.serial,
                                    'product_id'    : self.product_id.id,
                                    'product_categ' : self.order_id.sale_categ,
                                    'stone_qty'     : self.product_qty ,
                                    'company_id'    : self.env.company.id,
                                    'sales_price'   : rec.sale_price  ,
                                    'purchase_price': rec.purchase_price  ,
                                    'stone_types'   : self.Stone_types.id  ,
                                    'stone_size'    : self.stone_size  ,
                                    'stone_color'   : self.stone_color ,
                                    'stone_config'  : self.stone_config,
                                    'stone_style'   : self.stone_style 
                                })
            elif self.weight and item_type == '3' :
                
                line_weight     = self.weight
                product_types = self.env['product.type'].search([ ('item_groupss', '=', self.Stone_types.id)
                                                                 ,('sale_categ', '=', item_type)])
                

            
                for rec in product_types :
                    if rec.size_from <= line_weight and rec.size_to >= line_weight :
                        self.update({
                                    'price_unit' : rec.purchase_price
                                })
            
             