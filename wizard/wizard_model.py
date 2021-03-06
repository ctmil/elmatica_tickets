from openerp import models, fields, api, _
from openerp.exceptions import except_orm
from openerp.osv import osv
import urllib2, httplib, urlparse, gzip, requests, json
from StringIO import StringIO
import openerp.addons.decimal_precision as dp
import logging
import ast
#Get the logger
_logger = logging.getLogger(__name__)

class ticket_email_customer(models.TransientModel):
	_name = 'ticket.email.customer'

	email_cc = fields.Char(string='Cc')
	subject = fields.Char(string='Subject',required=True)
	body = fields.Text(string='Body',required=True)

	@api.multi
	def send_email(self):
		ticket = self.env['crm.helpdesk'].browse(self.env.context['active_ids'])
		if ticket:
			if ticket.customer_id:
				# Checks for attachments
				attachments = self.env['ir.attachment'].search([('res_model','=','crm.helpdesk'),\
						('res_id','=',ticket.id)])
				ticket.message_post(body=self.body,subtype='mt_comment',partner_ids=[(6,0,[ticket.customer_id.id])])
                                email_to = ticket.customer_id.email
				if email_to:
	                                vals = {
        	                                'body': self.body,
						'email_cc': self.email_cc,
                	                        'body_html': self.body,
                        	                'subject': self.subject,
                                	        'email_to': email_to,
                                        	}
					if attachments:
						vals['attachment_ids'] = [(6,0,attachments.ids)]
	                                msg = self.env['mail.mail'].create(vals)
        	                        if msg:
						msg.send()

		return None

class ticket_email(models.TransientModel):
	_name = 'ticket.email'

	email_cc = fields.Char(string='Cc')
	subject = fields.Char(string='Subject',required=True)
	body = fields.Text(string='Body',required=True)

	@api.multi
	def send_email(self):
		ticket = self.env['crm.helpdesk'].browse(self.env.context['active_ids'])
		if ticket:
			if ticket.supplier_id:
				attachments = self.env['ir.attachment'].search([('res_model','=','crm.helpdesk'),\
						('res_id','=',ticket.id)])
				ticket.message_post(body=self.body,subtype='mt_comment',partner_ids=[(6,0,[ticket.supplier_id.id])])
                                email_to = ticket.supplier_id.email
				if email_to:
	                                vals = {
						'email_cc': self.email_cc,
        	                                'body': self.body,
                	                        'body_html': self.body,
                        	                'subject': self.subject,
                                	        'email_to': email_to
                                        	}
					if attachments:
						vals['attachment_ids'] = [(6,0,attachments.ids)]
	                                msg = self.env['mail.mail'].create(vals)
        	                        if msg:
						msg.send()

		return None

class order_ticket_confirm(models.TransientModel):
	_name = 'order.ticket.confirm'

	query = fields.Char(string='Query')
	notes = fields.Text(string='Notes')

	@api.multi
	def confirm_ticket(self):
		#action_button_confirm
		if self.env.context['active_model'] == 'purchase.order':
			po = self.env['purchase.order'].browse(self.env.context['active_id'])
			attachments = self.env['ir.attachment'].search([('res_model','=','purchase.order'),\
                                                ('res_id','=',po.id)])
			vals_po = {
				'name': self.query,
				'description': self.notes,
				'purchase_id': po.id,
				'sale_order_id': po.sale_order_id.id,
				'partner_id': po.partner_id.id,
				'user_id': self.env.context['uid'],
				}

			return_id = self.env['crm.helpdesk'].create(vals_po)	
			for attachment in attachments:
				new_attachment = attachment.copy({'res_model': 'crm.helpdesk', 'res_id': return_id.id})
			#order.action_button_confirm()			
			return {'type': 'ir.actions.act_window',
        	                'name': 'Create Ticket - ticket',
                	        'res_model': 'crm.helpdesk',
                        	'view_type': 'form',
	                        'view_mode': 'form',
        	                #'view_id': view_id,
                	        'target': 'new',
	                        'nodestroy': True,
				'res_id': return_id.id
                	        }
		else:
			so = self.env['sale.order'].browse(self.env.context['active_id'])
			attachments = self.env['ir.attachment'].search([('res_model','=','sale.order'),\
                                                ('res_id','=',so.id)])
			vals_so = {
				'name': self.query,
				'description': self.notes,
				'sale_order_id': so.id,
				'partner_id': so.partner_id.id,
				'user_id': self.env.context['uid'],
				}
			return_id = self.env['crm.helpdesk'].create(vals_so)	
			for attachment in attachments:
				new_attachment = attachment.copy({'res_model': 'crm.helpdesk', 'res_id': return_id.id})
			#order.action_button_confirm()			
			return None
			"""
			return {'type': 'ir.actions.act_window',
        	                'name': 'Create Ticket - ticket',
                	        'res_model': 'crm.helpdesk',
                        	'view_type': 'form',
	                        'view_mode': 'form',
        	                'view_id': 'elmatica_tickets.view_crm_helpdesk_salepo',
                	        'target': 'new',
	                        'nodestroy': True,
				'res_id': return_id.id
                	        }

			"""

