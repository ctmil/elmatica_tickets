from openerp import api, models, exceptions, fields,  _
import openerp.addons.decimal_precision as dp

import logging
import datetime

_logger = logging.getLogger(__name__)


class crm_helpdesk(models.Model):
	_inherit = 'crm.helpdesk'

	purchase_id = fields.Many2one('purchase.order',string='Purchase Order')

class purchase_order(models.Model):
	_inherit = 'purchase.order'

	@api.multi
	def action_create_ticket(self):
		import pdb;pdb.set_trace()
		res = {}
		return res

	ticket_ids = fields.One2many(comodel_name='crm.helpdesk',inverse_name='purchase_id',string='Tickets')
