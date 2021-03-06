# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape

import json


class FinancialReportController(http.Controller):

    @http.route('/enterprise_accounting_report/<string:output_format>/<string:report_name>/<string:report_id>/'
        '<string:aging_filter_cmp>/<string:aging_due_filter_cmp>/<string:filter_local_currency>/'
        '<string:filter_original_currency>', type='http', auth='user')
    def report(self, output_format, report_name, token, report_id=None, aging_filter_cmp=False,
        aging_due_filter_cmp=False, filter_local_currency=False, filter_original_currency=False, **kw):

        aging_filter_cmp = eval(aging_filter_cmp.capitalize())
        aging_due_filter_cmp = eval(aging_due_filter_cmp.capitalize())
        filter_local_currency = eval(filter_local_currency.capitalize())
        filter_original_currency = eval(filter_original_currency.capitalize())

        uid = request.session.uid
        domain = [('create_uid', '=', uid)]
        report_model = request.env['account.report.context.common'].get_full_report_name_by_report_name(report_name)
        report_obj = request.env[report_model].sudo(uid)
        if report_name == 'financial_report':
            report_id = int(report_id)
            domain.append(('report_id', '=', report_id))
            report_obj = report_obj.browse(report_id)
        context_obj = request.env['account.report.context.common'].get_context_by_report_name(report_name)
        context_id = context_obj.sudo(uid).search(domain, limit=1)
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', 'attachment; filename=' + report_obj.get_name() + '.xlsx;')
                    ]
                )
                context_id.with_context(aging_filter_cmp=aging_filter_cmp, aging_due_filter_cmp=aging_due_filter_cmp,
                    filter_local_currency=filter_local_currency, filter_original_currency=filter_original_currency).get_xlsx(response)
                response.set_cookie('fileToken', token)
                return response
            if output_format == 'pdf':
                response = request.make_response(
                    context_id.with_context(aging_filter_cmp=aging_filter_cmp, aging_due_filter_cmp=aging_due_filter_cmp,
                        filter_local_currency=filter_local_currency, filter_original_currency=filter_original_currency).get_pdf(),
                    headers=[
                        ('Content-Type', 'application/pdf'),
                        ('Content-Disposition', 'attachment; filename=' + report_obj.get_name() + '.pdf;')
                    ]
                )
                response.set_cookie('fileToken', token)
                return response
            if output_format == 'xml':
                content = context_id.with_context(aging_filter_cmp=aging_filter_cmp, aging_due_filter_cmp=aging_due_filter_cmp,
                    filter_local_currency=filter_local_currency, filter_original_currency=filter_original_currency).get_xml()
                response = request.make_response(
                    content,
                    headers=[
                        ('Content-Type', 'application/vnd.sun.xml.writer'),
                        ('Content-Disposition', 'attachment; filename=' + report_obj.get_name() + '.xml;'),
                        ('Content-Length', len(content))
                    ]
                )
                response.set_cookie('fileToken', token)
                return response
        except Exception, e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
        else:
            return request.not_found()

    @http.route('/enterprise_accounting_report/followup_report/<string:partners>/', type='http', auth='user')
    def followup(self, partners, token, **kw):
        uid = request.session.uid
        try:
            context_obj = request.env['account.report.context.followup']
            partners = request.env['res.partner'].browse([int(i) for i in partners.split(',')])
            context_ids = context_obj.search([('partner_id', 'in', partners.ids), ('create_uid', '=', uid)])
            response = request.make_response(
                context_ids.with_context(public=True).get_pdf(log=True),
                headers=[
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', 'attachment; filename=payment_reminder.pdf;')
                ]
            )
            response.set_cookie('fileToken', token)
            return response
        except Exception, e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))

