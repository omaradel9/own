from odoo import fields, http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)



class WebsiteInherit(WebsiteSale):
    
    @http.route(['/shop/address'], type='http',methods=['GET', 'POST'], auth="public", website=True)
    def address(self, **kw):
        res = super(WebsiteInherit, self).address(**kw)
        
        _logger.info("---------------------------------omar adel omar ------------------------------------")
         
        return res 