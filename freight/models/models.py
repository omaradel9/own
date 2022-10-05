# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Test1(models.Model):
    _name = 'test1.test1'
    _description = 'test1.test1'
 
    name = fields.Char()
    mohamedomar = fields.Char()

class Test2(models.Model):
    _name = 'test2.test2'
    _description = 'test2.test2'
    _inherit = 'test1.test1'


class test3(models.Model): 
    _name = "test3.test3"
    _inherits = {'test1.test1': 'test_tmpl_id'} 
    
    test_tmpl_id =  fields.Many2one('test1.test1', 'test1 Template')
    
    cost = fields.Float(
        string='cost',
    )
    
    
class test_exe(models.Model):
    _inherit = 'test2.test2'
    
    cost   = fields.Float('Cost')