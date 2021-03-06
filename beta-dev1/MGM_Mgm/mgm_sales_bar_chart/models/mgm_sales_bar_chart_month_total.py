import json
from odoo import models, api, _, fields
from datetime import datetime, timedelta, date
import time

order_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
order_months_name = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct','11':'Nov','12':'Dec'}

class SalesBarChart(models.Model):
    _inherit = 'sales.bar.chart'
    
    months_total = fields.Text(compute='_kanban_dashboard_total')
    
    #All
    @api.one
    def _kanban_dashboard_total(self):
        if self.get_sale_bar_chart_months_total():
            self.months_total = json.dumps(self.get_sale_bar_chart_months_total())
        
    @api.multi
    def get_sale_bar_chart_months_total(self):
        data = []
        if self.name == "All":
            to_invoice_records = self.env['sale.order'].search([('state', 'not in', ('draft', 'sent', 'cancel')), ('invoice_status','=','to invoice')])
        elif self.name == "Ferry":
            to_invoice_records = self.env['sale.order'].search([('state', 'not in', ('draft', 'sent', 'cancel')), ('invoice_status','=','to invoice'), ('requisition_id.business_unit.name', '=', 'Ferry')])
        elif self.name == "FLF":
            to_invoice_records = self.env['sale.order'].search([('state', 'not in', ('draft', 'sent', 'cancel')), ('invoice_status','=','to invoice'), ('requisition_id.business_unit.name', '=', 'FLF')])
        elif self.name == "Tug & Barge":
            to_invoice_records = self.env['sale.order'].search([('state', 'not in', ('draft', 'sent', 'cancel')), ('invoice_status','=','to invoice'), ('requisition_id.business_unit.name', '=', 'Tug and Barge')])
        elif self.name == "Stevedoring":
            to_invoice_records = self.env['sale.order'].search([('state', 'not in', ('draft', 'sent', 'cancel')), ('invoice_status','=','to invoice'), ('requisition_id.business_unit.name', '=', 'Stevedoring')])
        elif self.name == "Other Quotation":
            to_invoice_records = self.env['sale.order'].search([('state', 'not in', ('draft', 'sent', 'cancel')), ('invoice_status','=','to invoice'), ('requisition_id.business_unit.name', '=', 'Others')])
        
        january=[];february=[];march=[];april=[];may=[];june=[];
        july=[];august=[];september=[];october=[];november=[];december=[];
        january_total = febuary_total = march_total = april_total = may_total = june_total = july_total = august_total = september_total = october_total = november_total = december_total = 0.0
        
        if to_invoice_records:
            for record in to_invoice_records:
                if record.date_order.split('-')[1] == '01':
                    january.append(record.amount_total)
                elif record.date_order.split('-')[1] == '02':
                    february.append(record.amount_total)
                elif record.date_order.split('-')[1] == '03':
                    march.append(record.amount_total)
                elif record.date_order.split('-')[1] == '04':
                    april.append(record.amount_total)
                elif record.date_order.split('-')[1] == '05':
                    may.append(record.amount_total)
                elif record.date_order.split('-')[1] == '06':
                    june.append(record.amount_total)
                elif record.date_order.split('-')[1] == '07':
                    july.append(record.amount_total)
                elif record.date_order.split('-')[1] == '08':
                    august.append(record.amount_total)
                elif record.date_order.split('-')[1] == '09':
                    september.append(record.amount_total)
                elif record.date_order.split('-')[1] == '10':
                    october.append(record.amount_total)
                elif record.date_order.split('-')[1] == '11':
                    november.append(record.amount_total)
                elif record.date_order.split('-')[1] == '12':
                    december.append(record.amount_total)
        january_total = sum(january)
        febuary_total = sum(february)
        march_total = sum(march)
        april_total = sum(april)
        may_total = sum(may)
        june_total = sum(june)
        july_total = sum(july)
        august_total = sum(august)
        september_total = sum(september)
        october_total = sum(october)
        november_total = sum(november)
        december_total = sum(december)
        return {
            'january_total': float("{0:.2f}".format(january_total)),
            'febuary_total': float("{0:.2f}".format(febuary_total)),
            'march_total': float("{0:.2f}".format(march_total)),
            'april_total': float("{0:.2f}".format(april_total)),
            'may_total': float("{0:.2f}".format(may_total)),
            'june_total': float("{0:.2f}".format(june_total)),
            'july_total': float("{0:.2f}".format(july_total)),
            'august_total': float("{0:.2f}".format(august_total)),
            'september_total': float("{0:.2f}".format(september_total)),
            'october_total': float("{0:.2f}".format(october_total)),
            'november_total': float("{0:.2f}".format(november_total)),
            'december_total': float("{0:.2f}".format(december_total)),
            } 
        
