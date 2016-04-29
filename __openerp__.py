{
    'name': 'Elmatica - Tickets',
    'category': 'Sales',
    'version': '0.1',
    'depends': ['purchase','crm_helpdesk','portal'],
    'data': [
	'ticket_view.xml',
	'wizard/wizard_view.xml',
	'security/ir.model.access.csv'
    ],
    'demo': [
    ],
    'qweb': [],
    # 'css': ['static/src/css/styles.css',],
    'installable': True,
}
