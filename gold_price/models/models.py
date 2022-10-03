# -*- coding: utf-8 -*-
from email.policy import default
import string
from odoo import models, fields, api
import logging
from odoo.exceptions import ValidationError
from twilio.rest import Client
# import fbchat
# from getpass import getpass
class goldPrice(models.Model):
    _name = 'gold.price'
    _description = 'gold price'
    _logger  = logging.getLogger(__name__)

    
    
    daily_gold_price    = fields.Float(string='Sale Gold Price' ,required=True,help="set Daily gold price to day")
    fixed_gold_price    = fields.Float(string='Purchase Gold Price' ,required=True,help="set Fixed gold price to day")
    labor_gold_price    = fields.Float(string='Labor Gold Price' ,required=True,help="set Labor gold price to day")
    gold_price          = fields.Float(string='Gold Price' ,required=True,help="set gold price to day")
    day                 = fields.Datetime(string="Active From Date",required=True , default = lambda self : fields.datetime.now()   )
    active              = fields.Boolean(string="Active")
    text                = fields.Char(string='TEXT')
    whats               = fields.Char(string='whats')
    usernames           = fields.Char(string='usernames')
    password            = fields.Char(string='password')
    mesg                = fields.Char(string='Message')
    
    karat               = fields.Selection(selection = [('9', '9K'),('12', '12K'),('14', '14K'),('18', '18K'),('21', '21K'),('22', '22K'),('24', '24K')],string="Karat",required=False)
    conversion_karat    = fields.Selection(selection = [('9', '9K'),('12', '12K'),('14', '14K'),('18', '18K'),('21', '21K'),('22', '22K'),('24', '24K')],string="Conversion Karat",required=False)
    
    

    @api.constrains('day')
    def val_date(self):
        date = self.day
        if date.date() < fields.datetime.now().date():
            raise ValidationError("Please select now or future date")
        else :
            self.env['gold.price'].search([('karat','=',self.karat),('id' ,'!=',self.id)]).write({'active': False })
        
    
    # def whatsapp(self):
    #     self.whats = "omar adel omar mohamed"
    #     account_sid ='AC6af293e8ebb9c14cddfd79c04d7b1f8b'
    #     auth_token ='ec46e85e9a42903b147a708764660cc4'
    #     client = Client (account_sid , auth_token)
    #     from_whatsapp_number = 'whatsapp:+14155238886'
    #     to_whatsapp_number = 'whatsapp:+201117206477'

    #     client.messages.create(
    #         body="صبح صبح ياعم الحج" , 
    #         from_= from_whatsapp_number ,
    #         to= to_whatsapp_number
               
        
    #     )
        
