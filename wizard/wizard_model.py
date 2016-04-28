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

class purchase_order_ticket_confirm(models.TransientModel):
	_name = 'purchase.order.ticket.confirm'

	notes = fields.Text(string='Notes')

	@api.multi
	def confirm_po_ticket(self):
		#action_button_confirm
		import pdb;pdb.set_trace()
			#order.action_button_confirm()			
		print "Hola mundo"
		return None

