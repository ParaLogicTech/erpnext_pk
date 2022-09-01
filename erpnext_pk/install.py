import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields



custom_fields = {
	# Doctype Company Mods
	'Company': [
		# NTN field
		{"label": "NTN", "fieldname": "tax_ntn", "fieldtype": "Data", "insert_after": "tax_id"},
		# STRN field
		{"label": "STRN", "fieldname": "tax_strn", "fieldtype": "Data", "insert_after": "tax_ntn"}
	],

	# Doctype Customer Mods
	'Customer': [
		# NTN field
		{"label": "NTN", "fieldname": "tax_ntn", "fieldtype": "Data", "insert_after": "tax_category"},
		# CNIC field
		{"label": "CNIC", "fieldname": "tax_cnic", "fieldtype": "Data", "insert_after": "tax_ntn"},
		# STRN field
		{"label": "STRN", "fieldname": "tax_strn", "fieldtype": "Data", "insert_after": "tax_cnic"}
	],

	# Doctype Supplier Mods
	'Supplier': [
		# NTN field
		{"label": "NTN", "fieldname": "tax_ntn", "fieldtype": "Data", "insert_after": "pan"},
		# CNIC field
		{"label": "CNIC", "fieldname": "tax_cnic", "fieldtype": "Data", "insert_after": "tax_ntn"},
		# STRN field
		{"label": "STRN", "fieldname": "tax_strn", "fieldtype": "Data", "insert_after": "tax_cnic"}
	],

	# Doctype Employee Mods
	'Employee': [
		# CNIC field
		{"label": "CNIC", "fieldname": "cnic", "fieldtype": "Data", "description": "Format: xxxxx-xxxxxxx-x" ,"insert_after": "date_of_joining"},
		# CNIC Issue Date field
		{"label": "CNIC Issue Date", "fieldname": "cnic_issue_date", "fieldtype": "Date", "insert_after": "cnic"},
		# CNIC Expiry Datefield
		{"label": "CNIC Expiry Date", "fieldname": "cnic_expiry_date", "fieldtype": "Date", "insert_after": "cnic_issue_date"}
	]
}

def after_install():
	make_custom_fields()

def make_custom_fields():
	create_custom_fields(custom_fields)

