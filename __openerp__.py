# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    'name': 'Seidel ar report',
    'version': '0.1',
    'website': '',
    'category': 'Ar report',
    'summary': '',
    'description': """
Organization and management of Acccount
======================================

""",
    'author': 'Shanghai Haiforce',
    'depends': ['base','account' ],
    'data': [
        'views/account_invoice.xml',
        'views/print_ar_report.xml',
        'views/ar_report.xml',
        'security/ar_report_security.xml',
        'security/ir.model.access.csv',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
