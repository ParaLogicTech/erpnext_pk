import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


# Custom Field Templates
def get_template_field(fieldname, insert_after):
	df = custom_field_templates[fieldname].copy()
	df['insert_after'] = insert_after
	return df


custom_field_templates = {
	'tax_ntn': {"label": "NTN", "fieldname": "tax_ntn", "fieldtype": "Data", "in_standard_filter": 1},
	'tax_strn': {"label": "STRN", "fieldname": "tax_strn", "fieldtype": "Data", "in_standard_filter": 1},
	'tax_cnic': {"label": "CNIC", "fieldname": "tax_cnic", "fieldtype": "Data", "in_standard_filter": 1},
}


# Custom Field Definitions
custom_fields = {
	'Company': [
		get_template_field('tax_ntn', insert_after='tax_id'),
		get_template_field('tax_strn', insert_after='tax_ntn'),
		get_template_field('tax_cnic', insert_after='tax_strn'),
	],

	'Customer': [
		get_template_field('tax_cnic', insert_after='tax_id'),
		get_template_field('tax_ntn', insert_after='tax_cnic'),
		get_template_field('tax_strn', insert_after='tax_ntn'),
	],

	'Supplier': [
		get_template_field('tax_cnic', insert_after='pan'),
		get_template_field('tax_ntn', insert_after='tax_cnic'),
		get_template_field('tax_strn', insert_after='tax_ntn'),
	],

	'Employee': [
		{"label": "National ID Card Detail", "fieldname": "sec_nic_details", "fieldtype": "Section Break",
			"insert_after": "health_details", "collapsible": 1},
		get_template_field('tax_cnic', insert_after='sec_nic_details'),
		{"fieldname": "col_break_nic1", "fieldtype": "Column Break", "insert_after": "tax_cnic"},
		{"label": "CNIC Date of Issue", "fieldname": "cnic_date_of_issue", "fieldtype": "Date", "insert_after": "col_break_nic1"},
		{"label": "", "fieldname": "col_break_nic2", "fieldtype": "Column Break", "insert_after": "cnic_date_of_issue"},
		{"label": "CNIC Date of Expiry", "fieldname": "cnic_valid_upto", "fieldtype": "Date", "insert_after": "col_break_nic2"}
	]
}


# Property Setters
property_setters = [
	{"doctype": "Employee", "fieldname": "date_of_issue", "property": "label", "value": "Passport Date of Issue"},
	{"doctype": "Employee", "fieldname": "valid_upto", "property": "label", "value": "Passport Date of Expiry"},
	{"doctype": "Employee", "fieldname": "place_of_issue", "property": "label", "value": "Passport Place of Issue"}
]


# Installer
def after_install():
	make_custom_fields()
	apply_property_setters()


def make_custom_fields():
	if not frappe.db.exists("DocType", "Employee"):
		custom_fields.pop('Employee')

	create_custom_fields(custom_fields)


def apply_property_setters():
	employee_doctype_exists = frappe.db.exists("DocType", "Employee")
	for arg in property_setters:
		if arg.get('doctype') == "Employee" and not employee_doctype_exists:
			continue

		frappe.make_property_setter(arg)
