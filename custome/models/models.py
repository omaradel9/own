# -*- coding: utf-8 -*-
from odoo import models, fields, api
import itertools
from logging import info
from odoo.exceptions import ValidationError,UserError
import itertools
from decimal import Decimal



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    

    sale_mode   = fields.Selection([('1', 'Fixed'),('2', 'Daily')],string="Sale Base")
    k9          = fields.Float(string='Karat 9k Weight  (G)',compute='_compute_line_weight',store= True)
    k12         = fields.Float(string='Karat 12k Weight (G)',compute='_compute_line_weight',store= True)
    k14         = fields.Float(string='Karat 14k Weight (G)',compute='_compute_line_weight',store= True)
    k18         = fields.Float(string='Karat 18k Weight (G)',compute='_compute_line_weight',store= True)
    k21         = fields.Float(string='Karat 21k Weight (G)',compute='_compute_line_weight',store= True)
    k22         = fields.Float(string='Karat 22k Weight (G)',compute='_compute_line_weight',store= True)
    k24         = fields.Float(string='Karat 24k Weight (G)',compute='_compute_line_weight',store= True)
    c_karat     = fields.Float(string='Converted Karat Weight (G)',compute='_compute_line_weight',store= True)
    tesxt = fields.Char(string="tesxt")
    pricelist_id = fields.Many2one(required=False)
    sale_categ  = fields.Selection([ ('1', 'Gold Jewelry')
                                    ,('2', 'Gold Material')
                                    ,('3', 'Open Stone')
                                    ,('4', 'Sealed Stone')
                                    ,('5', 'Diamond Jewelry')
                                    ,('6', 'Montrat')
                                    ,('7', 'Scrap')
                                    ,('8', 'Silver')], string='Item Category')
    field_invis     = fields.Boolean(default=False)
    @api.onchange('sale_mode')
    def _onchange_base(self):
        for red in self :
            red.invoice_ids.sale_mode = self.sale_mode
    
    
    @api.constrains('partner_invoice_id')
    def _check_partner_invoice_id(self):
        self.pricelist_id = 1
            
    
    
    @api.onchange('partner_id')
    def sale_base(self):
       self.sale_mode =  self.partner_id.sale_mode
   
    @api.onchange('partner_invoice_id')
    def price_list(self):
        if self.pricelist_id :
            self.pricelist_id = False
        
    @api.depends('order_line')
    def _compute_line_weight(self):
      
        line_weight9  = 0
        line_weight12 = 0
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
                    line_weight9  += line.weight
                elif line.karats  == "12":
                    line_weight12 +=  line.weight
                elif line.karats  == "14":
                    line_weight14 +=  line.weight
                elif line.karats  == "18":
                    line_weight18 +=  line.weight
                elif line.karats  == "21":
                    line_weight21 +=  line.weight
                elif line.karats  == "22":
                    line_weight22 += line.weight
                elif line.karats  == "24":
                    line_weight24 += line.weight
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
        
        self.pricelist_id = False
        exist_product_list = []
        for sale in self:
            for line in sale.order_line:

                if line.serial.id in exist_product_list:
                    raise ValidationError('Serial should be one per line.')
                exist_product_list.append(line.serial.id)
    
    

    # @api.model
    # def _action_cancel(self):

    #     info("-----------------------------oooooooooooooooooooooooooo--------------------")
    #     return super(SaleOrder, self)._action_cancel()
        # Your code goes here
        # info("-----------------------------oooooooooooooooooooooooooo--------------------")
        # def separate(string):
        #         return ["".join(group) for key, group in itertools.groupby(string, str.isdigit)]
        # seq_id = self.env['sale.order'].search([])[0].name
        # sequence2   = separate(seq_id)
            
        # first_len   = len(sequence2)-2
        # last_len    = len(sequence2)-1
        # first_seq   = sequence2[first_len]
        # last_seq    = sequence2[last_len]
        # num_seq = int(last_seq)+1
        # sequ_str = str(first_seq)
        # sequ = str(num_seq).zfill(5)
        # seqy=(sequ_str + sequ)
        # self.tesxt = seqy
        # return super(SaleOrder, self).create_invoices()
        # self.env['account.move'].search([('karat' , '=',rec.karats)])
        
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    sale_sale       = fields.Char(string="mode")
    serial          = fields.Many2one(string='Serial',comodel_name='stock.production.lot')
    available       = fields.Boolean(default=True)
    net_weight      = fields.Float('Weight',digits=(12,4) )
    making_price    = fields.Float('Cost',digits=(12,4),readonly=True)
    gold_price      = fields.Float('Gold Price',digits=(12,4),readonly=True)
    karats          = fields.Char('Karat',readonly=True)
    weight          = fields.Float('Weight',digits=(12,4) )
    c_karats        = fields.Char(string='C Karat',store= True)
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
    
    
    
    @api.onchange('serial')
    def onchange_sale_product(self):
        if self.order_id.sale_categ in ('1','6') :
        
            serials         = self.env['stock.production.lot'].search([('id', '=', self.serial.id)])
            
            self.invoice_lines.weight = 45698

            self.sale_sale      = self.order_id.sale_mode
            gold_p              = self.env['gold.price'].search([('karat' , '=',serials.product_id.karat)], limit=1, order='day desc')
            prod                = serials.product_id.id
            karat               = serials.product_id.product_tmpl_id.karat
            # making             = serials.product_id.product_tmpl_id.standard_price
            self.karats         = karat
            latest_price        = gold_p.gold_price
            convert_karat       = gold_p.conversion_karat
            self.c_karats       = convert_karat
            self.gold_price     = latest_price
            self.making_price   = gold_p.labor_gold_price
            self.product_id     = prod 
            self.weight         = serials.weight
            if self.sale_sale == "1" :
                        self.update({
                                'price_unit' : self.making_price * rec.weight
                            })
            elif self.sale_sale == "2" :
                        self.update({
                                'price_unit' :  (self.making_price + latest_price)* self.weight
                        })
    
        elif self.order_id.sale_categ == '5' :
            for line in self :
                line.product_id  = line.serial.product_id
                line.product_uom_qty =  1
                if self.order_id.sale_mode == '1' :
                    line.price_unit = line.serial.whole_gold
                elif self.order_id.sale_mode == '2' :
                    line.price_unit = line.serial.retail_gold
                    
        elif self.order_id.sale_categ == '4' :
            
            self.product_id  = self.serial.product_id
            self.product_uom_qty =  1
            if self.order_id.sale_mode == '1' :
                self.price_unit = self.serial.whole_gold
            elif self.order_id.sale_mode == '2' :
                self.price_unit = self.serial.retail_gold




class Serial(models.Model):
    _inherit = 'stock.production.lot'
    gross_weight =fields.Float(
    'Gross Weight',
    digits=(12,4) )
    net_weight =fields.Float(
    'Net Weight',
    digits=(12,4) )
    # diamond_ids = fields.One2many('product.product', 'product_id', string='Diamond Calcolation')    




class Karat(models.Model):
    _inherit = 'purchase.order.line'
    gold_price =fields.Float('Gold Price',digits=(12,4),readonly=True,store = True)
    karats = fields.Char('Karat',store = True)

    # @api.depends('product_id')
    # @api.onchange('product_id')
    # def product_id_change(self):
    #     for rec in self:
    #         rec.price_subtotal = 565
            
# class SaleAdvance(models.TransientModel):
#     _inherit = 'sale.advance.payment.inv'
#     karats = fields.Char('Karat')

#     @api.model
#     def create_invoices(self):
       
#         self.karats = "omar adel omar mohamed"
#         return super(SaleAdvance, self).create_invoices()
    
class SaleAdvanced(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    karats = fields.Char('Karat')
    def create_invoices(self):
            """ Override method from sale/wizard/sale_make_invoice_advance.py

                When the user want to invoice the timesheets to the SO
                up to a specific period then we need to recompute the
                qty_to_invoice for each product_id in sale.order.line,
                before creating the invoice.
            """
            sale_order = self.env['sale.order'].browse(
                self._context.get('active_id')
            )

            if self.karats == 'delivered':
                # return {'type': 'ir.actions.act_window_close'}
                # sok =  self.env['sale.order'].search([('id','=',sale_order.id)]).sale_mode
                # sok =  self.env['sale.order'].search([('id','=',sale_order.id)]).sale_mode
                cok = self.env['account.move'].search([('invoice_origin','=',sale_order.name)]).invoice_origin
                self.env['sale.order'].search([('id','=',sale_order.id)]).write({'tesxt':cok})
                # self.env['gold.price'].create({'gold_price': sok})
            return super(SaleAdvanced, self).create_invoices()
    