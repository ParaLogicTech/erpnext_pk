import frappe
from frappe import _


sales_tax_account_name = "Sales Tax on Goods"
sales_tax_description = "Sales Tax @ 17%"
sales_tax_rate = 17.0

further_tax_account_name = "Further Tax"
further_tax_description = "Further Tax @ 3%"
further_tax_rate = 3.0

sales_tax_template_title = "Sales Tax"
sales_further_tax_template_title = "Sales Tax + Further Tax"


def get_setup_stages(args=None):
	stages = [
		{
			"status": _("Installing Pakistan Workspace Customization"),
			"fail_msg": _("Failed to install Pakistan Workspace Customization"),
			"tasks": [{"fn": stage_install_pakistan_workspace, "args": args,
				"fail_msg": _("Failed to install Pakistan Workspace Customization")}],
		},
	]

	return stages


# This setup wizard method is for new installation
def stage_install_pakistan_workspace(args):
	rename_gst_account_for_pakistan()
	rename_pakistan_tax_template_for_pakistan()

	update_sales_tax_description()

	create_further_tax_accounts_for_pakistan()
	create_tax_templates_for_pakistan()

	update_company_tax_accounts_for_pakistan()


# This installer method is for existing database
def after_install():
	# Do not rename for existing database
	# rename_gst_account_for_pakistan()
	# rename_pakistan_tax_template_for_pakistan()
	# update_sales_tax_description()

	create_further_tax_accounts_for_pakistan()
	create_tax_templates_for_pakistan()

	update_company_tax_accounts_for_pakistan()


def rename_gst_account_for_pakistan():
	companies = frappe.get_all("Company", filters={"country": "Pakistan"})
	for d in companies:
		rename_gst_account(d.name)


def rename_gst_account(company):
	from erpnext.accounts.doctype.account.account import update_account_number

	gst_account = frappe.db.get_value("Account",
		{"account_name": "GST", "account_type": "Tax", "is_group": 0, "company": company})

	if gst_account:
		print('Renaming "GST" account name to "{0}" for Company {1}'.format(sales_tax_account_name, company))

		account_number = frappe.db.get_value("Account", gst_account, "account_number")
		update_account_number(gst_account, sales_tax_account_name, account_number)


def rename_pakistan_tax_template_for_pakistan():
	companies = frappe.get_all("Company", filters={"country": "Pakistan"})
	for d in companies:
		rename_pakistan_tax_template(d.name)


def rename_pakistan_tax_template(company):
	pakistan_tax_template = frappe.db.get_value("Sales Taxes and Charges Template",
		{"title": "Pakistan Tax", "company": company})

	if pakistan_tax_template:
		print('Renaming Sales Taxes and Charges "Pakistan Tax" to "{0}" for Company {1}'.format(sales_tax_template_title,
			company))

		company_abbr = frappe.db.get_value("Company", company, "abbr")
		new_name = "{0} - {1}".format(sales_tax_template_title, company_abbr)
		frappe.rename_doc("Sales Taxes and Charges Template", pakistan_tax_template, new_name)

		# Saving is done to run the triggers to update "Is Default" global default
		frappe.get_doc("Sales Taxes and Charges Template", new_name).save()


def update_sales_tax_description():
	# Change GST % 17.0 Description
	sales_tax_template_rows = frappe.get_all("Sales Taxes and Charges",
		filters={'description': "GST @ 17.0", "parenttype": "Sales Taxes and Charges Template"})

	if sales_tax_template_rows:
		print('Changing "GST @ 17.0" Description to "{0}"'.format(sales_tax_description))

	for d in sales_tax_template_rows:
		frappe.db.set_value("Sales Taxes and Charges", d.name, "description", sales_tax_description)


def create_further_tax_accounts_for_pakistan():
	companies = frappe.get_all("Company", filters={"country": "Pakistan"})
	for d in companies:
		create_further_tax_account(d.name)


def create_further_tax_account(company):
	parent_account = get_sales_tax_parent_account(company)

	if parent_account:
		try:
			print("Creating Further Tax Account for Company {0}".format(company))

			further_tax_doc = frappe.new_doc("Account")
			further_tax_doc.account_name = further_tax_account_name
			further_tax_doc.account_type = "Tax"
			further_tax_doc.tax_rate = further_tax_rate
			further_tax_doc.company = company
			further_tax_doc.parent_account = parent_account

			further_tax_doc.insert()
		except frappe.DuplicateEntryError:
			print("Further Tax Account already exists")


def create_tax_templates_for_pakistan():
	companies = frappe.get_all("Company", filters={"country": "Pakistan"})
	for d in companies:
		create_tax_templates(d.name)


def create_tax_templates(company):
	sales_tax_account = get_sales_tax_account(company)
	further_tax_account = get_further_tax_account(company)

	if sales_tax_account and further_tax_account:
		print('Creating "{0}" Sales Taxes and Charges Template for Company {1}'.format(sales_further_tax_template_title,
			company))

		try:
			template = frappe.new_doc("Sales Taxes and Charges Template")
			template.title = sales_further_tax_template_title
			template.company = company

			sales_tax_row = template.append('taxes')
			sales_tax_row.charge_type = "On Net Total"
			sales_tax_row.account_head = sales_tax_account
			sales_tax_row.description = sales_tax_description
			sales_tax_row.rate = sales_tax_rate

			further_tax_row = template.append('taxes')
			further_tax_row.charge_type = "On Net Total"
			further_tax_row.account_head = further_tax_account
			further_tax_row.description = further_tax_description
			further_tax_row.rate = further_tax_rate

			template.insert()
		except frappe.DuplicateEntryError:
			print('Sales Taxes and Charges Template "{0}" already exists'.format(sales_further_tax_template_title))


def update_company_tax_accounts_for_pakistan():
	companies = frappe.get_all("Company", filters={"country": "Pakistan"})
	for d in companies:
		update_company_tax_accounts(d.name)


def update_company_tax_accounts(company):
	sales_tax_account = get_sales_tax_account(company)
	further_tax_account = get_further_tax_account(company)

	if sales_tax_account or further_tax_account:
		print("Updating Tax Accounts for Company {0}".format(company))
		company_doc = frappe.get_doc("Company", company)
		company_doc.sales_tax_account = sales_tax_account
		company_doc.further_tax_account = further_tax_account

		company_doc.save()


def get_sales_tax_account(company):
	sales_tax_account = frappe.db.get_value("Account",
		{"account_name": sales_tax_account_name, "account_type": "Tax", "is_group": 0, "company": company})
	if sales_tax_account:
		return sales_tax_account

	sales_tax_account = frappe.db.get_value("Account",
		{"account_name": "GST", "account_type": "Tax", "is_group": 0, "company": company})
	if sales_tax_account:
		return sales_tax_account

	sales_tax_account = frappe.db.get_value("Account",
		{"account_name": "Sales Tax", "account_type": "Tax", "is_group": 0, "company": company})
	if sales_tax_account:
		return sales_tax_account

	sales_tax_account = frappe.db.get_value("Account",
		{"account_name": "Sales Tax on Goods", "account_type": "Tax", "is_group": 0, "company": company})
	if sales_tax_account:
		return sales_tax_account

	return None


def get_further_tax_account(company):
	further_tax_account = frappe.db.get_value("Account",
		{"account_name": further_tax_account_name, "account_type": "Tax", "is_group": 0, "company": company})

	return further_tax_account or None


def get_sales_tax_parent_account(company):
	sales_tax_account = get_sales_tax_account(company)
	if sales_tax_account:
		return frappe.db.get_value("Account", sales_tax_account, "parent_account")

	return frappe.db.get_value("Account", {"account_name": "Duties and Taxes", "is_group": 1, "company": company}) or None
