# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def validate_ntn_nic_strn_in_document(doc, method):
	validate_ntn_nic_strn(doc.get('tax_ntn'), doc.get('tax_nic'), doc.get('tax_strn'))


def validate_ntn_nic_strn(ntn=None, nic=None, strn=None):
	import re
	nic_regex = re.compile(r'^.....-.......-.$')
	ntn_regex = re.compile(r'^.......-.$')
	strn_regex = re.compile(r'^..-..-....-...-..$')

	if ntn and not ntn_regex.match(ntn):
		frappe.throw(_("Invalid NTN. NTN must be in the format #######-#"))
	if nic and not nic_regex.match(nic):
		frappe.throw(_("Invalid NIC. NIC must be in the format #####-#######-#"))
	if strn and not strn_regex.match(strn):
		frappe.throw(_("Invalid STRN. STRN must be in the format ##-##-####-###-##"))
