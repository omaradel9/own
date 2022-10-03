# -*- coding: utf-8 -*-

from odoo import models, fields, api
from logging import NullHandler,info
import itertools


# class custom_lot(models.Model):
#     _name = 'custom_lot.custom_lot'
#     _description = 'custom_lot.custom_lot'

# #     name = fields.Char()
# #     value = fields.Integer()
# #     value2 = fields.Float(compute="_value_pc", store=True)
# #     description = fields.Text()
# #
# #     @api.depends('value')
# #     def _value_pc(self):
# #         for record in self:
# #             record.value2 = float(record.value) / 100

class lot(models.Model):
    _inherit = 'stock.move.line'
    qty_done=fields.Float(digits=(12,4))

class lot(models.Model):
    _inherit = 'stock.move'
    

    fixed_qty = fields.Boolean(string='Fixed Quantity')
    number_of_pieces= fields.Integer(string='Number of Pieces')


    seq = fields.Char(
        string='Start serial sequence',
    )
    hide =  fields.Boolean(string='hide',default=True)
    @api.onchange('fixed_qty')
    def confirm(self):
        
    
        if self.fixed_qty == True:
            self.hide = False
        else:
           self.hide = True
           
    @api.constrains('seq')
    def get_serial(self):
            number_line = len(self.move_line_nosuggest_ids )
            if    number_line > 0 :
                self.move_line_nosuggest_ids.unlink()
            def separate(string):
                return ["".join(group) for key, group in itertools.groupby(string, str.isdigit)]
            
            
            sequence2   = separate(self.seq)
            
            first_len   = len(sequence2)-2
            last_len    = len(sequence2)-1
            first_seq   = sequence2[first_len]
            last_seq    = sequence2[last_len]
            
            
            
            number_of_pe = self.number_of_pieces 
            if number_of_pe != 0 :
                seq_num = number_of_pe
            elif number_of_pe == 0 or number_of_pe == "" :
                seq_num = 1
            piece_qty = (self.product_uom_qty) / seq_num
            num_seq = int(last_seq)
            
            
                
            for rec in range(seq_num):
                sequ_str = str(first_seq)
               
               
                sequ = str("%0002d" % num_seq)
                seqy=(sequ_str + sequ)
                self.move_line_nosuggest_ids = [(0, 0, {'product_id': self.product_id.id,
                'lot_name': seqy,
                'move_id' : self.id,
                'picking_id': self.picking_id.id,
                'qty_done': piece_qty,
                'product_uom_id' : self.product_uom.id})]
        
                num_seq+=1
            
            
class productCalc(models.Model):
    _name = 'product.calc'
    _description = 'product calcolation'
    # _rec_name = ''
    
    calc_id = fields.Many2one('stock.production.lot', string='calc_id', required=True, ondelete='cascade', index=True, copy=False)
    Stone_types     = fields.Many2one(string='Type',comodel_name='stones.type')

    item_cat  = fields.Selection([('2', 'Gold Material'),('3', 'Open Stone')], string='Item Category')
    
    karat       = fields.Selection([ ('9', '9k'),
                                     ('12', '12K'),
                                     ('14', '14k'),
                                     ('18', '18k'),
                                     ('21', '21k'),
                                     ('22', '22k')],string="Karat")
    
    stone_type  = fields.Many2one(string='Item Group',comodel_name='product.type')
    item_groups = fields.Many2one('product.product', string='Item Group')
    item_id     = fields.Char('Item Id')
    qty         = fields.Float('Quantity')
    size        = fields.Float('Size')
    golds_price = fields.Float('GoldPrice')
    count       = fields.Integer(string='Count')
    price       = fields.Float('Purch Price')
    sale_price  = fields.Float('Sale Price')
    labor_price = fields.Float('Labor Price')
    consume_qty = fields.Float('Consume Qty')
    
    @api.onchange('count','consume_qty')
    def _onchange_count_qty(self): 
        if self.item_cat == '3':
            if self.consume_qty > 0 and self.count > 0 :
                stone_size = self.consume_qty/self.count
                self.size = stone_size
                
                prod_type  = self.env['product.type'].search([('item_groupss','=', self.item_groups.Stone_type_name.type_name),('sale_categ','=', '3')])
                for rec in prod_type :
                    
                    if stone_size >= rec.size_from and stone_size <= rec.size_to :
                        self.price       = rec.purchase_price
                        self.item_id     = rec.item_name
                        self.sale_price  = rec.sale_price
                        self.labor_price = rec.labor_price
        elif self.item_cat == '2':
            if self.consume_qty > 0 :
                gold_price  = self.env['gold.price'].search([('karat','=', self.item_groups.karat)])
                # self.golds_price = gold_price.fixed_gold_price 
                for rec in gold_price :
                    self.labor_price = rec.labor_gold_price
                    self.golds_price = rec.fixed_gold_price 
                    self.price = (rec.fixed_gold_price + rec.labor_gold_price)* self.consume_qty
                    self.sale_price = (rec.daily_gold_price)* self.consume_qty

   
                    
class SerialNew(models.Model):
    _inherit = 'stock.production.lot'
    

    calc_ids = fields.One2many('product.calc', 'calc_id', string='Product Calcolation', copy=True, auto_join=True)
    vn = fields.Char('vn')
    product_categ   = fields.Char(string='product_categ')
    sales_price     = fields.Float(string='Sale Stone Price' ,required=True,help="Set Sale Stone price to day")
    purchase_price  = fields.Float(string='Purchase Stone Price' ,required=True,help="Set Purchase Stone price to day")
    stone_qty       = fields.Float(string='Stone Quantity')
    product_qty     = fields.Float(related='stone_qty',store=True)
    weight          = fields.Float(string='Weight',digits=(12,4) )
    cost_price      = fields.Float(string='Cost',compute='_compute_line_price',store= True)
    cost_price_gold = fields.Float(string='Cost With Gold',compute='_compute_line_price',store= True)
    whole_gold      = fields.Float(string='Whole' ,compute='_compute_line_price',store= True)
    whole_w_gold    = fields.Float(string='Whole' ,compute='_compute_line_price',store= True)
    retail_gold     = fields.Float(string='Retail',compute='_compute_line_price',store= True)
    retail_w_gold   = fields.Float(string='Retail',compute='_compute_line_price',store= True)
    stone_type      = fields.Many2one(string='Type',comodel_name='product.type')
    stone_types     = fields.Many2one(string='Type',comodel_name='stones.type')
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
 
    
        
        
        
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.product_categ = self.product_id.item_cat
        number_line = len(self.calc_ids)
        if  number_line > 0 :
            self.calc_ids.unlink()
        self.company_id = self.env.company.id
        if self.product_id :
            bom  = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)])
            for bomn in bom :
                    boms  = self.env['mrp.bom.line'].search([('bom_id', '=', bomn.id)])

                    # self.vn = self.product_id.id
                    
                    for rec in boms :
                            self.calc_ids = [(0, 0, {
                                    'item_cat'      : rec.product_id.item_cat,
                                    'item_groups'   : rec.product_id.id,
                                    'Stone_types'   : rec.product_id.Stone_type_name,
                                    'item_id'       : '',
                                    'qty'           : rec.product_qty,
                                    'size'          : 0,
                                    'count'         : 0,
                                    'price'         : 0,
                                    'sale_price'    : 0,
                                    'labor_price'   : 0

                                    })]
                    

    @api.depends('calc_ids')
    def _compute_line_price(self):
        
        cost_stone          = 0
        cost_gold           = 0 
        sale_price_stone    = 0
        sale_price_gold     = 0

        for line in self.calc_ids :
            if  line.item_cat == "2" :
                cost_gold           += line.price 
                sale_price_gold     += line.sale_price
                
            elif line.item_cat in ('3','4') :
                cost_stone          += line.price + line.labor_price
                sale_price_stone    += line.sale_price
                
            self.cost_price         = cost_stone 
            self.cost_price_gold    = cost_stone + cost_gold
            self.whole_gold         = (sale_price_gold + sale_price_stone) * 2.9
            self.whole_w_gold       = (sale_price_stone) * 2.9
            self.retail_gold        = (sale_price_gold + sale_price_stone) * 3.6
            self.retail_w_gold      = (sale_price_stone) * 3.6
            

    
    
    


