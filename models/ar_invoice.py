# -*- coding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp import models, fields, api, _
import datetime

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    overdue = fields.Integer( string='Overdue', readonly=True, compute='_compute_overdue')
    payment = fields.Char( string='Payments', readonly=True, compute='_compute_payment',store=False)
    description = fields.Char( string='Description', readonly=True, compute='_compute_payment',store=False)
    # ar_report_line_id = fields.Many2one('ar.report.line', string='Ar report line', readonly=True)

    @api.multi
    @api.depends('date_due','invoice_line')
    def _compute_overdue(self):
        today = datetime.datetime.utcnow()
        for account in self:
            account.description = account.invoice_line and account.invoice_line[0].name or ''
            if account.date_due:
                due = (today - datetime.datetime.strptime(account.date_due, '%Y-%m-%d')).days
                if due<0:
                    due = 0
                account.overdue=due

    @api.multi
    def _compute_payment(self):
        for account in self:
            order = self.env['sale.order'].search([('invoice_ids','=',account.id)])
            if len(order)>0 and order[0].payment_term :
                account.payment = order[0].payment_term.name


