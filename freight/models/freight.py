# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval
import logging

class BaseSales(models.Model):
    _inherit = 'sale.order'
    contract= fields.Boolean('Contract')
    
class Freight(models.Model): 
    _name = "freight.freight"
    _inherits = {'sale.order': 'sale_tmpl_id'} 
    _logger  = logging.getLogger(__name__)

    # _sql_constraints = [
    #     ('sale_tmpl_id', 'unique (sale_tmpl_id)', 'This Sale Order already exists!'),
    # ]
    # sale_tmpl_id =  fields.Many2one('sale.order', 'Sale Order')
    sale_tmpl_id = fields.Many2one('sale.order', string='Sale Order')
    
    cost = fields.Float(string='cost')
    sale = fields.Float(string='Sale')
    text = fields.Char('text')
    @api.onchange('sale_tmpl_id')
    def sale_ser(self):
        # self.sale_tmpl_id.note= "omar adel omar "
        self.sale = self.cost
        sales_order = self.sale_tmpl_id.name
        self.env['sale.order'].search([('name', '=', sales_order)]).write({'contract': True })




    def action_view_task(self):
        self.ensure_one()

        list_view_id = self.env.ref('project.view_task_tree2').id
        form_view_id = self.env.ref('project.view_task_form2').id

        action = {'type': 'ir.actions.act_window_close'}
        task_projects = self.sale_tmpl_id.tasks_ids.mapped('project_id')
        if len(task_projects) == 1 and len(self.sale_tmpl_id.tasks_ids) > 1:  # redirect to task of the project (with kanban stage, ...)
            action = self.with_context(active_id=task_projects.id).env['ir.actions.actions']._for_xml_id(
                'project.act_project_project_2_project_task_all')
            action['domain'] = [('id', 'in', self.sale_tmpl_id.tasks_ids.ids)]
            if action.get('context'):
                eval_context = self.env['ir.actions.actions']._get_eval_context()
                eval_context.update({'active_id': task_projects.id})
                action_context = safe_eval(action['context'], eval_context)
                action_context.update(eval_context)
                action['context'] = action_context
        else:
            action = self.env["ir.actions.actions"]._for_xml_id("project.action_view_task")
            action['context'] = {}  # erase default context to avoid default filter
            if len(self.sale_tmpl_id.tasks_ids) > 1:  # cross project kanban task
                action['views'] = [[False, 'kanban'], [list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'calendar'], [False, 'pivot']]
            elif len(self.sale_tmpl_id.tasks_ids) == 1:  # single task -> form view
                action['views'] = [(form_view_id, 'form')]
                action['res_id'] = self.sale_tmpl_id.tasks_ids.id
        # filter on the task of the current SO
        action.setdefault('context', {})
        action['context'].update({'search_default_sale_order_id': self.id})
        return action
    
    
    def action_view_project_ids(self):
        self.ensure_one()
        view_form_id = self.env.ref('project.edit_project').id
        view_kanban_id = self.env.ref('project.view_project_kanban').id
        action = {
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.sale_tmpl_id.project_ids.ids)],
            'view_mode': 'kanban,form',
            # 'name': _('Projects'),
            'res_model': 'project.project',
        }
        if len(self.sale_tmpl_id.project_ids) == 1:
            action.update({'views': [(view_form_id, 'form')], 'res_id': self.sale_tmpl_id.project_ids.id})
        else:
            action['views'] = [(view_kanban_id, 'kanban'), (view_form_id, 'form')]
        return action

# class FreightTest(models.Model): 
#     _name = "freight.test"
#     # _inherits = {'sale.order': 'sale_tmpl_id'} 
#     _inherit = 'sale.order'
    # sale_tmpl_id =  fields.Many2one('sale.order', 'Sale Order')
    # sale_tmpl_id = fields.Many2one('sale.order', string='Sale Order')
    
    # cost = fields.Float(string='cost')