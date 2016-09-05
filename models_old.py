from openerp.osv import fields, osv
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
from openerp import tools

# main mako-like expression pattern

class mail_compose_message(osv.TransientModel):
    """ Generic message composition wizard. You may inherit from this wizard
        at model and view levels to provide specific features.

        The behavior of the wizard depends on the composition_mode field:
        - 'comment': post on a record. The wizard is pre-populated via ``get_record_data``
        - 'mass_mail': wizard in mass mailing mode where the mail details can
            contain template placeholders that will be merged with actual data
            before being sent to each recipient.
    """
    _inherit = 'mail.compose.message'

    def get_record_data(self, cr, uid, values, context=None):
        """ Returns a defaults-like dict with initial values for the composition
        wizard when sending an email related a previous email (parent_id) or
        a document (model, res_id). This is based on previously computed default
        values. """
        if context is None:
            context = {}
        result, subject = {}, False
        if values.get('parent_id'):
            parent = self.pool.get('mail.message').browse(cr, uid, values.get('parent_id'), context=context)
            result['record_name'] = parent.record_name,
            subject = tools.ustr(parent.subject or parent.record_name or '')
            if not values.get('model'):
                result['model'] = parent.model
            if not values.get('res_id'):
                result['res_id'] = parent.res_id
            partner_ids = values.get('partner_ids', list()) + [partner.id for partner in parent.partner_ids]
            if context.get('is_private') and parent.author_id:  # check message is private then add author also in partner list.
                partner_ids += [parent.author_id.id]
            result['partner_ids'] = partner_ids
        elif values.get('model') and values.get('res_id'):
            doc_name_get = self.pool[values.get('model')].name_get(cr, uid, [values.get('res_id')], context=context)
            result['record_name'] = doc_name_get and doc_name_get[0][1] or ''
            subject = tools.ustr(result['record_name'])

        re_prefix = _('Re:')
        if subject and not (subject.startswith('Re:') or subject.startswith(re_prefix)):
            subject = "%s %s" % (re_prefix, subject)
        result['subject'] = subject
	if context.has_key('default_model') and context.has_key('elmatica_tickets'):
		if context['default_model'] == 'crm.helpdesk' and context['elmatica_tickets'] == True:
			result['attachment_ids'] = None
        return result

mail_compose_message()
