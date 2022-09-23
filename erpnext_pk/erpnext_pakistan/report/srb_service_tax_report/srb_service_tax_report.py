# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, today, flt


def execute(filters=None):
	return SRBServiceTaxReport(filters).run()


class SRBServiceTaxReport:
	def __init__(self, filters=None):
		self.data = []
		self.invoices_map = {}
		self.filters = frappe._dict(filters or dict())
		self.filters.from_date = getdate(filters.from_date or today())
		self.filters.to_date = getdate(filters.to_date or today())
		self.filters.company = filters.company or frappe.db.get_single_value('Global Defaults', 'default_company')
		self.filters.service_tax_account = frappe.get_cached_value('Company', self.filters.company, "service_tax_account")	
		if not self.filters.service_tax_account:
			frappe.throw(_("Please set Service Tax Account in Company {0}".format(self.filters.company)))
		if self.filters.from_date > self.filters.to_date:
			frappe.throw(_("Date Range is incorrect"))

	def run(self):
		self.get_columns()
		self.get_invoices()
		self.transform_invoices()
		return self.columns, self.data

	def get_invoices(self):
		condition = "AND invoice.customer = %(customer)s" if self.filters.customer else ""
		invoices = frappe.db.sql("""
			SELECT
				invoice.name as document_number,
				invoice.customer as buyer_name,
				invoice.posting_date as document_date,
				invoice.base_net_total as sale_total_excluding_tax,
				invoice.tax_nic,
				invoice.tax_ntn,
				address.city as buyer_district
			FROM
				`tabSales Invoice` invoice
			LEFT JOIN
				`tabAddress` address
				ON address.name = invoice.customer_address
			WHERE
				invoice.company = %(company)s
				AND invoice.posting_date BETWEEN %(from_date)s AND %(to_date)s
				AND invoice.docstatus = 1
				AND invoice.is_return = 0
				AND exists(
					SELECT
						tax.name
					FROM
						`tabSales Taxes and Charges` tax
					WHERE
						tax.parent = invoice.name
						AND tax.account_head = %(service_tax_account)s
						AND tax.base_tax_amount_after_discount_amount != 0)
				{0}
			""".format(condition), self.filters, as_dict=1)
		for invoice in invoices:
			invoice.buyer_type = "End_Consumer"
			invoice.document_type = "SI"
			invoice.sale_type = "Services"
			self.invoices_map[invoice.document_number] = frappe._dict({
				'invoice':invoice
			})
			invoice_names = list(self.invoices_map.keys())
			invoice_taxes = frappe.db.sql("""
				SELECT
					rate, parent as invoice,
					base_tax_amount_after_discount_amount as sales_tax
				FROM
					`tabSales Taxes and Charges`
				WHERE
					parent IN({0})
					AND account_head = %(service_tax_account)s
			""".format(",".join([frappe.db.escape(d) for d in invoice_names])),
			self.filters, as_dict=1)
			for tax in invoice_taxes:
				self.invoices_map[tax.invoice]['tax'] = tax

	def transform_invoices(self):
		for invoice in self.invoices_map.values():
			row_fill = invoice.get("invoice")
			row_fill.rate = flt(invoice.get("tax").get("rate"))
			row_fill.sales_tax = flt(invoice.get("tax").get("sales_tax"))
			self.data.append(row_fill)


	def get_columns(self):
		self.columns = [
			{
				"label": _("NTN"),
				"fieldname": "tax_ntn",
				"fieldtype": "Data",
				"width": 110
			},
			{
				"label": _("CNIC"),
				"fieldname": "tax_nic",
				"fieldtype": "Data",
				"width": 140
			},
			{
				"label": _("Name of Buyer"),
				"fieldname": "buyer_name",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 130
			},
			{
				"label": _("District of Buyer"),
				"fieldname": "buyer_district",
				"fieldtype": "Data",
				"width": 80
			},
			{
				"label": _("Buyer Type"),
				"fieldname": "buyer_type",
				"fieldtype": "Data",
				"width": 90,
				"hide_for_view": 1
			},
			{
				"label": _("Document Type"),
				"fieldname": "document_type",
				"fieldtype": "Data",
				"width": 50,
				"hide_for_view": 1
			},
			{
				"label": _("Document Number"),
				"fieldname": "document_number",
				"fieldtype": "Link",
				"options": "Sales Invoice",
				"width": 170
			},
			{
				"label": _("Document Date"),
				"fieldname": "document_date",
				"fieldtype": "Data",
				"width": 140
			},
			{
				"label": _("HS Code"),
				"fieldname": "hscode",
				"fieldtype": "Data",
				"width": 80
			},
			{
				"label": _("Sale Type"),
				"fieldname": "sale_type",
				"fieldtype": "Data",
				"width": 80,
				"hide_for_view": 1
			},
			{
				"label": _("Rate"),
				"fieldname": "rate",
				"fieldtype": "Percent",
				"width": 70
			},
			{
				"label": _("Value of Sales Excluding Sales Tax"),
				"fieldname": "sale_total_excluding_tax",
				"fieldtype": "Currency",
				"width": 190
			},
			{
				"label": _("Sales Tax Involved"),
				"fieldname": "sales_tax",
				"fieldtype": "Currency",
				"width": 100
			},
			{
				"label": _("ST Withheld at Source"),
				"fieldname": "sales_tax_withheld",
				"fieldtype": "Data",
				"width": 80,
				"hide_for_view": 1
			},
		]

		if not self.filters.for_export:
			self.columns =  list(filter(lambda d: not d.get("hide_for_view"), self.columns))
