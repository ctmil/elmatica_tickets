from openerp import api, models, exceptions, fields,  _
import openerp.addons.decimal_precision as dp

import logging
import datetime

_logger = logging.getLogger(__name__)


class crm_helpdesk(models.Model):
	_inherit = 'crm.helpdesk'

	@api.multi
	def email_supplier(self):
		title_window = self._context.get('title_window', _('Comment'))

		#template = self.env.ref(template_name, False)
		#assert template, 'Unable to find %s' % template_name
		assert len(self) == 1, 'This option should only be used for a single id at a time.'

		compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
		#if self.supplier_id:
		#	vals_message = {
		#		'res_id': self.id,
		#		'res_model': 'crm.helpdesk',
		#		'partner_ids': (6,0,[self.supplier_id.id])
		#		}
		#	message_id = self.env['mail.compose.message'].create(vals_message)
		if self.supplier_id.email:
			ctx = dict(
				default_model='crm.helpdesk',
				default_res_id=self.id,
				default_email_to=self.supplier_id.email,
				default_partner_ids=[self.supplier_id.id],
				#default_use_template=bool(template),
				#default_template_id=template.id,
				default_composition_mode='comment',
				#mark_invoice_as_sent=False,
				#default_is_log=True,
				#is_log=True,
				#internal_partners_only=True,
			       )	
		return {
	        	    'name': title_window,
	        	    'type': 'ir.actions.act_window',
		            'view_type': 'form',
        		    'view_mode': 'form',
		            #'res_model': 'elmatica_invoice.mail.compose.message', # 'compose.message', # 'mail.compose.message',
			    #'res_id': message_id.id,
        		    'res_model': 'mail.compose.message',
	        	    'views': [(compose_form.id, 'form')],
	        	    'view_id': compose_form.id,
		            'target': 'new',
        		    'context': ctx,
		        }

		#vals = {
		#	'subject': self.name,
		#	'body': self.name,
		#	}
		#ticket_email = self.env['ticket.email'].create(vals)
                #return {'type': 'ir.actions.act_window',
                        #'name': 'e-mail Supplier',
                        #'res_model': 'ticket.email',
                        #'view_type': 'form',
                        #'view_mode': 'form',
                        ##'view_id': view_id,
			#'res_id': ticket_email.id,
                        #'target': 'new',
                        #'nodestroy': True,
                        #}

	@api.multi
	def email_customer(self):
		title_window = self._context.get('title_window', _('Comment'))

		assert len(self) == 1, 'This option should only be used for a single id at a time.'

		compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
		#if self.supplier_id:
		#	vals_message = {
		#		'res_id': self.id,
		#		'res_model': 'crm.helpdesk',
		#		'partner_ids': (6,0,[self.supplier_id.id])
		#		}
		#	message_id = self.env['mail.compose.message'].create(vals_message)
		if self.customer_id.email:
			ctx = dict(
				default_model='crm.helpdesk',
				default_res_id=self.id,
				default_email_to=self.customer_id.email,
				default_partner_ids=[self.customer_id.id],
				#default_use_template=bool(template),
				#default_template_id=template.id,
				default_composition_mode='comment',
				#mark_invoice_as_sent=False,
				#default_is_log=True,
				#is_log=True,
				#internal_partners_only=True,
			       )	
		return {
	        	    'name': title_window,
	        	    'type': 'ir.actions.act_window',
		            'view_type': 'form',
        		    'view_mode': 'form',
		            #'res_model': 'elmatica_invoice.mail.compose.message', # 'compose.message', # 'mail.compose.message',
			    #'res_id': message_id.id,
        		    'res_model': 'mail.compose.message',
	        	    'views': [(compose_form.id, 'form')],
	        	    'view_id': compose_form.id,
		            'target': 'new',
        		    'context': ctx,
		        }

		#vals = {
		#	'subject': self.name,
		#	'body': self.name,
		#	}
		#ticket_email_customer = self.env['ticket.email.customer'].create(vals)
                #return {'type': 'ir.actions.act_window',
                #        'name': 'e-mail Customer',
                #        'res_model': 'ticket.email.customer',
                #        'view_type': 'form',
                #        'view_mode': 'form',
                #        #'view_id': view_id,
		#	'res_id': ticket_email_customer.id,
                #        'target': 'new',
                #        'nodestroy': True,
                #        }
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
