# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, today, flt


def execute(filters=None):
	return FBRSalesTaxReport(filters).run()


class FBRSalesTaxReport:
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or dict())
		self.filters.from_date = getdate(filters.from_date or today())
		self.filters.to_date = getdate(filters.to_date or today())
		self.filters.company = filters.company or frappe.db.get_single_value('Global Defaults', 'default_company')

		self.filters.sales_tax_account = frappe.get_cached_value('Company', self.filters.company, "sales_tax_account")
		self.filters.further_tax_account = frappe.get_cached_value('Company', self.filters.company, "further_tax_account")
		self.filters.extra_tax_account = frappe.get_cached_value('Company', self.filters.company, "extra_tax_account")
		
		self.filters.tax_accounts = [
			self.filters.sales_tax_account,
			self.filters.further_tax_account,
			self.filters.extra_tax_account
		]
		self.filters.tax_accounts = [d for d in self.filters.tax_accounts if d]

		if not self.filters.sales_tax_account:
			frappe.throw(_("Please set Sales Tax Account in Company {0}".format(self.filters.company)))

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
				c.tax_cnic, c.tax_ntn, c.tax_strn,
				address_customer.state as destination_province,
				address_company.state as supplier_province
			FROM `tabSales Invoice` si
			LEFT JOIN `tabCustomer` c
				ON c.name = si.customer
			LEFT JOIN `tabAddress` address_customer
				ON address_customer.name = si.customer_address
			LEFT JOIN `tabAddress` address_company 
				ON address_company.name = si.company_address
			WHERE
				si.company = %(company)s AND posting_date BETWEEN %(from_date)s AND %(to_date)s
				AND si.docstatus = 1 AND si.is_return = 0
				AND exists(
					SELECT tax.name from `tabSales Taxes and Charges` tax
					WHERE
						tax.parent = si.name
						AND tax.account_head IN({0})
						AND tax.base_tax_amount_after_discount_amount != 0)
				{1}
			""".format(",".join([frappe.db.escape(x) for x in self.filters.tax_accounts]), condition),
			self.filters, as_dict=1)

		self.invoices_map = {}
		for invoice in invoices:
			invoice.registration_no = invoice.tax_ntn or invoice.tax_cnic
			invoice.buyer_type = "Registered" if invoice.tax_strn else "Unregistered"
			# fixed values
			invoice.sale_type = " Goods at standard rate (default)"
			invoice.document_type = "Sales Invoice"
			invoice.uom = "Numbers, pieces, units"


			self.invoices_map[invoice.name] = frappe._dict({
				'invoice': invoice,
				'items': [],
				'taxes': [],
			})

		invoice_names = list(self.invoices_map.keys())

		if invoice_names:
			invoice_items = frappe.db.sql("""
				SELECT parent as invoice, qty as item_quantity
				FROM `tabSales Invoice Item`
				WHERE parent in %s
			""", [invoice_names], as_dict=1)

			for item in invoice_items:
				invoice = self.invoices_map.get(item.invoice)
				if invoice:
					invoice['items'].append(item)

			invoice_taxes = frappe.db.sql("""
				SELECT parent as invoice, rate, account_head,
					base_tax_amount_after_discount_amount as tax_amount
				FROM `tabSales Taxes and Charges`
				WHERE parent in %s
			""", [invoice_names], as_dict=1)

			for tax in invoice_taxes:
				invoice = self.invoices_map.get(tax.invoice)
				if invoice:
					invoice.get('taxes').append(tax)


	def transform_invoices(self):
		self.data = []
		for invoice in self.invoices_map.values():
			sales_tax = [tax for tax in invoice['taxes'] if tax.account_head == self.filters.sales_tax_account]
			sales_tax = sales_tax[0] if sales_tax else frappe._dict()

			further_tax = [tax for tax in invoice['taxes'] if tax.account_head == self.filters.further_tax_account]
			further_tax = further_tax[0] if further_tax else frappe._dict()

			extra_tax = [tax for tax in invoice['taxes'] if tax.account_head == self.filters.extra_tax_account]
			extra_tax = extra_tax[0] if extra_tax else frappe._dict()

			row_fill = invoice.get("invoice")
			row_fill.buyer_name = row_fill.customer
			row_fill.document_number = row_fill.name
			row_fill.document_date = row_fill.posting_date
			row_fill.base_taxable_amount = row_fill.base_net_total
			row_fill.quantity = sum([item.item_quantity for item in invoice.get('items')])
			row_fill.rate = flt(sales_tax.rate)
			row_fill.sales_tax = flt(sales_tax.tax_amount)
			row_fill.extra_tax = flt(extra_tax.tax_amount)
			row_fill.further_tax = flt(further_tax.tax_amount)
			self.data.append(row_fill)


	def get_columns(self):
		self.columns = [
			{
				"label": _("Registration No"),
				"fieldname": "registration_no",
				"fieldtype": "Data",
				"width": 140
			},
			{
				"label": _("Buyer Name"),
				"fieldname": "buyer_name",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 110
			},
			{
				"label": _("Buyer Type"),
				"fieldname": "buyer_type",
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Sale Origination Province of Supplier"),
				"fieldname": "supplier_province",
				"fieldtype": "Data",
				"width": 105
			},
			{
				"label": _("Destination of Supply"),
				"fieldname": "destination_province",
				"fieldtype": "Data",
				"width": 110
			},
			{
				"label": _("Document Type"),
				"fieldname": "document_type",
				"fieldtype": "Data",
				"width": 170,
				"hide_for_export": 1
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
				"fieldtype": "Date",
				"width": 120
			},
			{
				"label": _("HS Code Description"),
				"fieldname": "hs_code_description",
				"fieldtype": "Date",
				"width": 130,
				"hide_for_export": 1
			},
			{
				"label": _("Sale Type"),
				"fieldname": "sale_type",
				"fieldtype": "Data",
				"width": 130,
				"hide_for_export": 1
			},
			{
				"label": _("Rate"),
				"fieldname": "rate",
				"fieldtype": "Percent",
				"width": 60
			},
			{
				"label": _("Quantity"),
				"fieldname": "quantity",
				"fieldtype": "Float",
				"width": 80
			},
			{
				"label": _("UoM"),
				"fieldname": "uom",
				"fieldtype": "Data",
				"width": 90,
				"hide_for_export": 1
			},
			{
				"label": _("Value of Sales Excluding Sales Tax"),
				"fieldname": "base_taxable_amount",
				"fieldtype": "Currency",
				"width": 240
			},
			{
				"label": _("Sales Tax/ FED in ST Mode"),
				"fieldname": "sales_tax",
				"fieldtype": "Currency",
				"width": 130
			},
			{
				"label": _("Fixed / notified value or Retail Price"),
				"fieldname": "retail_price",
				"fieldtype": "Currency",
				"width": 140,
				"hide_for_export": 1
			},
			{
				"label": _("Extra Tax"),
				"fieldname": "extra_tax",
				"fieldtype": "Currency",
				"width": 100
			},
			{
				"label": _("Further Tax"),
				"fieldname": "further_tax",
				"fieldtype": "Currency",
				"width": 100
			},
			{
				"label": _("Total Value of Sales (In case of PFAD only"),
				"fieldname": "sales_total_PFAD",
				"fieldtype": "Currency",
				"width": 110,
				"hide_for_export": 1
			},
			{
				"label": _("ST Withheld at Source"),
				"fieldname": "sales_tax_withheld",
				"fieldtype": "Currency",
				"width": 110,
				"hide_for_export": 1
			},
			{
				"label": _("SRO No./ Schedule No."),
				"fieldname": "sro_no",
				"fieldtype": "Data",
				"width": 110,
				"hide_for_export": 1
			},
			{
				"label": _("Item S. No."),
				"fieldname": "item_no",
				"fieldtype": "Data",
				"width": 110,
				"hide_for_export": 1
			}
		]
		if not self.filters.for_export:
			self.columns =  list(filter(lambda d: not d.get("hide_for_export"), self.columns))
