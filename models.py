from openerp import api, models, exceptions, fields,  _
import openerp.addons.decimal_precision as dp

import logging
import datetime

_logger = logging.getLogger(__name__)


class crm_helpdesk(models.Model):
	_inherit = 'crm.helpdesk'

	@api.multi
	def email_supplier(self):
		vals = {
			'subject': self.name,
			'body': self.name,
			}
		ticket_email = self.env['ticket.email'].create(vals)
                return {'type': 'ir.actions.act_window',
                        'name': 'e-mail Supplier',
                        'res_model': 'ticket.email',
                        'view_type': 'form',
                        'view_mode': 'form',
                        #'view_id': view_id,
			'res_id': ticket_email.id,
                        'target': 'new',
                        'nodestroy': True,
                        }

	@api.multi
	def email_customer(self):
		vals = {
			'subject': self.name,
			'body': self.name,
			}
		ticket_email_customer = self.env['ticket.email.customer'].create(vals)
                return {'type': 'ir.actions.act_window',
                        'name': 'e-mail Customer',
                        'res_model': 'ticket.email.customer',
                        'view_type': 'form',
                        'view_mode': 'form',
                        #'view_id': view_id,
			'res_id': ticket_email_customer.id,
                        'target': 'new',
                        'nodestroy': True,
                        }
	@api.one
	def _compute_supplier_id(self):
		if self.purchase_id:
			self.supplier_id = self.purchase_id.partner_id.id
		else:
			if self.sale_order_id:
				if self.sale_order_id.purchase_ids:
					self.supplier_id = self.sale_order_id.purchase_ids[0].partner_id.id

	@api.one
	def _compute_customer_id(self):
		self.customer_id = self.sale_order_id.partner_id.id

	supplier_id = fields.Many2one('res.partner',compute=_compute_supplier_id)
	customer_id = fields.Many2one('res.partner',compute=_compute_customer_id)
	purchase_id = fields.Many2one('purchase.order',string='Purchase Order')
	purchase_sale_id = fields.Many2one('sale.order',string='Sale Order related to Purchase Order',related='purchase_id.sale_order_id')
	sale_order_id = fields.Many2one('sale.order',string='Sale Order')



class purchase_order(models.Model):
	_inherit = 'purchase.order'

	@api.multi
	def action_create_ticket(self):
                return {'type': 'ir.actions.act_window',
                        'name': 'Create Ticket',
                        'res_model': 'order.ticket.confirm',
                        'view_type': 'form',
                        'view_mode': 'form',
                        #'view_id': view_id,
                        'target': 'new',
                        'nodestroy': True,
                        }

	ticket_ids = fields.One2many(comodel_name='crm.helpdesk',inverse_name='purchase_id',string='Tickets')

class sale_order(models.Model):
	_inherit = 'sale.order'

	@api.multi
	def action_create_ticket(self):
                return {'type': 'ir.actions.act_window',
                        'name': 'Create Ticket',
                        'res_model': 'order.ticket.confirm',
                        'view_type': 'form',
                        'view_mode': 'form',
                        # 'view_id': 
                        'target': 'new',
                        'nodestroy': True,
                        }

	ticket_ids = fields.One2many(comodel_name='crm.helpdesk',inverse_name='sale_order_id',string='Tickets')
