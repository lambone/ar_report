# -*- coding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
import datetime
from openerp.exceptions import AccessError, Warning


class ar_report(models.Model):
    _name = 'ar.report'
    _rec_name = 'document_id'

    document_id = fields.Char('Document ID')
    version = fields.Char('Version')
    create_uid = fields.Many2one('res.users', string='issue by', readonly=True)
    create_date = fields.Datetime('first release', readonly=True)
    issue_date = fields.Datetime('Date of issue')
    line_ids = fields.One2many('ar.report.line','report_id')

    def create(self, cr, uid, vals, context=None):
        vals = {'document_id':'AC-AR',
                'version':'1',
                'issue_date':fields.Datetime.now()}
        return super(ar_report, self).create(cr, uid, vals, context)

    @api.multi
    def ar_print_invoice(self):
        context = dict(self._context or {})
        ar_report_id = self.id
        active_ids = context.get('active_ids', []) or []
        if len(active_ids) == 0:
            raise Warning(_("No choice to print content."))


        line = []
        partner_id = 0
        account_invoice_ids = []
        for record in self.env['account.invoice'].search([['id','in',active_ids]],order='partner_id'):
            if partner_id != record.partner_id.id:
                if partner_id >0:
                    self.env['ar.report.line'].create( {'report_id':ar_report_id,
                                                        'partner_id':partner_id,
                                                        'account_invoice_ids':[(6,0,account_invoice_ids)] })
                account_invoice_ids = []
                partner_id = record.partner_id.id
                account_invoice_ids.append(record.id)
            else:
                account_invoice_ids.append(record.id)

        self.env['ar.report.line'].create( {'report_id': ar_report_id,
                                            'partner_id': partner_id,
                                            'account_invoice_ids': [(6,0,account_invoice_ids)] })

        return self.env['report'].get_action(self, 'seidel_ar_report.report_ar_print')

        # return {'type': 'ir.actions.act_window_close'}




class ar_report_line(models.Model):
    _name = 'ar.report.line'

    report_id = fields.Many2one('ar.report','Partner')
    partner_id = fields.Many2one('res.partner','Partner')
    sum_open_amount = fields.Float(string='Sum Open Amount', digits=dp.get_precision('Account'), compute='_compute_amount')
    sum_total_amount = fields.Float(string='Sum Total Amount', digits=dp.get_precision('Account'), compute='_compute_amount')
    account_invoice_ids = fields.Many2many('account.invoice', string='invoice Lines',readonly=True, copy=False)


    @api.multi
    @api.depends('account_invoice_ids')
    def _compute_amount(self):
        for account in self:
            sum_open_amount=0
            sum_total_amount=0
            for invoice in account.account_invoice_ids:
                sum_open_amount+=invoice.residual
                sum_total_amount+=invoice.amount_total
            account.sum_open_amount = sum_open_amount
            account.sum_total_amount = sum_total_amount
