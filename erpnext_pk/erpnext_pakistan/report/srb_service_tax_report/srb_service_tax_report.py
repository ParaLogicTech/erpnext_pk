# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, today



def execute(filters=None):
	return SRBServiceTaxReport(filters).run()



class SRBServiceTaxReport:
	def __init__(self, filters):
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
		condition = "AND si.customer = %(customer)s" if self.filters.customer else ""

		invoices = frappe.db.sql("""
			SELECT si.name, si.customer, si.posting_date, si.base_net_total,
				c.tax_cnic, c.tax_ntn, address_customer.city
			FROM `tabSales Invoice` si
			LEFT JOIN `tabCustomer` c
				ON c.name = si.customer
			LEFT JOIN `tabAddress` address_customer
				ON address_customer.name = si.customer_address
			WHERE
				si.company = %(company)s AND posting_date BETWEEN %(from_date)s AND %(to_date)s
				AND si.docstatus = 1 AND si.is_return = 0
				AND exists(
					SELECT tax.name from `tabSales Taxes and Charges` tax
					WHERE
						tax.parent = si.name
						AND tax.account_head = %(service_tax_account)s
						AND tax.base_tax_amount_after_discount_amount != 0)
				{0}
			""".format(condition), self.filters, as_dict=1)
		
		for invoice in invoices:
			invoice.buyer_name = invoice.customer
			invoice.buyer_district = invoice.city
			invoice.document_number = invoice.name
			invoice.document_date = invoice.posting_date
			invoice.base_taxable_total = invoice.base_net_total

		self.data = invoices


	def transform_invoices(self):
		pass


	def get_columns(self):
		self.columns = [
			{
				"label": _("NTN"),
				"fieldname": "tax_ntn",
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("CNIC"),
				"fieldname": "tax_cnic",
				"fieldtype": "Data",
				"width": 140
			},
			{
				"label": _("Name of Buyer"),
				"fieldname": "buyer_name",
				"fieldtype": "Data",
				"width": 180
			},
			{
				"label": _("District of Buyer"),
				"fieldname": "buyer_district",
				"fieldtype": "Data",
				"width": 140
			},
			# {
			# 	"label": _("Buyer Type"),
			# 	"fieldname": "buyer_type",
			# 	"fieldtype": "Data",
			# 	"width": 90
			# },
			# {
			# 	"label": _("Document Type"),
			# 	"fieldname": "document_type",
			# 	"fieldtype": "Data",
			# 	"width": 50
			# },
			{
				"label": _("Document Number"),
				"fieldname": "document_number",
				"fieldtype": "Data",
				"width": 180
			},
			{
				"label": _("Document Date"),
				"fieldname": "document_date",
				"fieldtype": "Date",
				"width": 150
			},
			# {
			# 	"label": _("HS Code"),
			# 	"fieldname": "hscode",
			# 	"fieldtype": "Data",
			# 	"width": 80
			# },
			# {
			# 	"label": _("Sale Type"),
			# 	"fieldname": "sale_type",
			# 	"fieldtype": "Data",
			# 	"width": 80
			# },
			# {
			# 	"label": _("Rate"),
			# 	"fieldname": "rate",
			# 	"fieldtype": "Percent",
			# 	"width": 50
			# },
			{
				"label": _("Value of Sales Excluding Sales Tax"),
				"fieldname": "base_taxable_total",
				"fieldtype": "Currency",
				"width": 250
			},
			# {
			# 	"label": _("Sales Tax Involved"),
			# 	"fieldname": "sales_tax_involved",
			# 	"fieldtype": "Currency",
			# 	"width": 110
			# },
			# {
			# 	"label": _("ST Withheld at Source"),
			# 	"fieldname": "sales_tax_withheld",
			# 	"fieldtype": "Currency",
			# 	"width": 110
			# }
		]
