# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


# Custom Field Templates
def get_template_field(args):
	custom_field_templates = {
		'tax_ntn': {"label": "NTN", "fieldname": "tax_ntn", "fieldtype": "Data", "in_standard_filter": 1},
		'tax_strn': {"label": "STRN", "fieldname": "tax_strn", "fieldtype": "Data", "in_standard_filter": 1},
		'tax_nic': {"label": "CNIC", "fieldname": "tax_nic", "fieldtype": "Data", "in_standard_filter": 1},
		'company_tax_ntn': {"label": "Company NTN", "fieldname": "company_tax_ntn", "fieldtype": "Data", "in_standard_filter": 1},
		'company_tax_strn': {"label": "Company STRN", "fieldname": "company_tax_strn", "fieldtype": "Data", "in_standard_filter": 1},
	}
	fieldname = args['fieldname']
	df = custom_field_templates[fieldname].copy()
	df.update(args)
	return df


# Custom Field Definitions
custom_fields = {
	'Company': [
		get_template_field({"fieldname": 'tax_ntn', "insert_after": 'tax_id'}),
		get_template_field({"fieldname": 'tax_strn', 'insert_after': 'tax_ntn'}),
		get_template_field({"fieldname": 'tax_nic', 'insert_after': 'tax_strn'}),

		{"label": "Pakistan Tax Settings", "fieldname": "sec_break_tax", "fieldtype": "Section Break",
			"insert_after": "default_discount_account"},
		{"label": "Sales Tax On Goods Account", "fieldname": "sales_tax_account", "fieldtype": "Link", "options": "Account",
			"insert_after": "sec_break_tax"},
		{"label": "Sales Tax On Services Account", "fieldname": "service_tax_account", "fieldtype": "Link", "options": "Account",
			"insert_after": "sales_tax_account"},
		{"fieldname": "col_break_tax_1", "fieldtype": "Column Break",
			"insert_after": "service_tax_account"},
		{"label": "Further Tax Account", "fieldname": "further_tax_account", "fieldtype": "Link", "options": "Account",
			"insert_after": "col_break_tax_1"},
		{"label": "Extra Tax Account", "fieldname": "extra_tax_account", "fieldtype": "Link", "options": "Account",
			"insert_after": "further_tax_account"},
	],

	'Customer': [
		get_template_field({"fieldname": 'tax_nic', 'insert_after': 'tax_id'}),
		get_template_field({"fieldname": 'tax_ntn', 'insert_after': 'tax_nic'}),
		get_template_field({"fieldname": 'tax_strn', 'insert_after': 'tax_ntn'})
	],

	'Supplier': [
		get_template_field({"fieldname": 'tax_nic', 'insert_after': 'pan'}),
		get_template_field({"fieldname": 'tax_ntn', 'insert_after': 'tax_nic'}),
		get_template_field({"fieldname": 'tax_strn', 'insert_after': 'tax_ntn'})
	],

	'Sales Order': [
		get_template_field({"fieldname": 'tax_nic', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_id', "fetch_from": "customer.tax_nic", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'tax_ntn', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_nic',"fetch_from": "customer.tax_ntn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'tax_strn', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_ntn', "fetch_from": "customer.tax_strn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'company_tax_ntn', "read_only": 1, "hidden": 1,
			"insert_after": 'company', "fetch_from": "company.tax_ntn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'company_tax_strn', "read_only": 1, "hidden": 1,
			"insert_after": 'company_tax_ntn', "fetch_from": "company.tax_strn", "in_standard_filter": 0})
	],

	'Sales Invoice': [
		get_template_field({"fieldname": 'tax_nic', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_id', "fetch_from": "customer.tax_nic", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'tax_ntn', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_nic', "fetch_from": "customer.tax_ntn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'tax_strn', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_ntn', "fetch_from": "customer.tax_strn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'company_tax_ntn', "read_only": 1, "hidden": 1,
			"insert_after": 'company', "fetch_from": "company.tax_ntn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'company_tax_strn', "read_only": 1, "hidden": 1,
			"insert_after": 'company_tax_ntn', "fetch_from": "company.tax_strn", "in_standard_filter": 0})
	],

	'Delivery Note': [
		get_template_field({"fieldname": 'tax_nic', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_id', "fetch_from": "customer.tax_nic", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'tax_ntn', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_nic', "fetch_from": "customer.tax_ntn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'tax_strn', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_ntn', "fetch_from": "customer.tax_strn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'company_tax_ntn', "read_only": 1, "hidden": 1,
			"insert_after": 'company', "fetch_from": "company.tax_ntn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'company_tax_strn', "read_only": 1, "hidden": 1,
			"insert_after": 'company_tax_ntn', "fetch_from": "company.tax_strn", "in_standard_filter": 0})
	],

	'POS Invoice': [
		get_template_field({"fieldname": 'tax_nic', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_id', "fetch_from": "customer.tax_nic", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'tax_ntn', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_nic', "fetch_from": "customer.tax_ntn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'tax_strn', "read_only": 1, "hidden": 1,
			"insert_after": 'tax_ntn', "fetch_from": "customer.tax_strn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'company_tax_ntn', "read_only": 1, "hidden": 1,
			"insert_after": 'company', "fetch_from": "company.tax_ntn", "in_standard_filter": 0}),
		get_template_field({"fieldname": 'company_tax_strn', "read_only": 1, "hidden": 1,
			"insert_after": 'company_tax_ntn', "fetch_from": "company.tax_strn", "in_standard_filter": 0})
	],

	'Employee': [
		{"label": "National ID Card Detail", "fieldname": "sec_nic_details", "fieldtype": "Section Break",
			"insert_after": "health_details", "collapsible": 1},
		get_template_field({"fieldname": 'tax_nic', 'insert_after': 'sec_nic_details'}),
		{"fieldname": "col_break_nic1", "fieldtype": "Column Break",
			"insert_after": "tax_nic"},
		{"label": "CNIC Date of Issue", "fieldname": "nic_date_of_issue", "fieldtype": "Date",
			"insert_after": "col_break_nic1"},
		{"label": "", "fieldname": "col_break_nic2", "fieldtype": "Column Break",
			"insert_after": "nic_date_of_issue"},
		{"label": "CNIC Date of Expiry", "fieldname": "nic_valid_upto", "fieldtype": "Date",
			"insert_after": "col_break_nic2"}
	],
}


# Property Setters
property_setters = [
	{"doctype": "Employee", "fieldname": "date_of_issue", "property": "label", "value": "Passport Date of Issue"},
	{"doctype": "Employee", "fieldname": "valid_upto", "property": "label", "value": "Passport Date of Expiry"},
	{"doctype": "Employee", "fieldname": "place_of_issue", "property": "label", "value": "Passport Place of Issue"}
]


# Installer
def before_install():
	check_if_erpnext_installed()


def after_install():
	from erpnext_pk.setup import after_install

	# Installer Process
	make_custom_fields()
	apply_property_setters()

	# Setup Wizard Process
	after_install()


def check_if_erpnext_installed():
	if "erpnext" not in frappe.get_installed_apps():
		frappe.throw("Please install ERPNext app first then install Pakistan Workspace app")


def make_custom_fields():
	print("Creating Custom Fields")

	if not frappe.db.exists("DocType", "Employee"):
		print("Employee DocType does not exists, skipping Employee custom fields")
		custom_fields.pop('Employee')

	create_custom_fields(custom_fields)


def apply_property_setters():
	print("Applying Property Setters")

	employee_doctype_exists = frappe.db.exists("DocType", "Employee")
	for arg in property_setters:
		if arg.get('doctype') == "Employee" and not employee_doctype_exists:
			print("Employee DocType does not exists, skipping Employee property setters")
			continue

		frappe.make_property_setter(arg)
