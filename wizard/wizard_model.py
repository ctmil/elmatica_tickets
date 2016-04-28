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

class order_ticket_confirm(models.TransientModel):
	_name = 'order.ticket.confirm'

	query = fields.Char(string='Query')
	notes = fields.Text(string='Notes')

	@api.multi
	def confirm_ticket(self):
		#action_button_confirm
		if self.env.context['active_model'] == 'purchase.order':
			po = self.env['purchase.order'].browse(self.env.context['active_id'])
			vals_po = {
				'name': self.query,
				'description': self.notes,
				'purchase_id': po.id,
				'partner_id': po.partner_id.id,
				'user_id': self.env.context['uid'],
				}
			return_id = self.env['crm.helpdesk'].create(vals_po)	
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


