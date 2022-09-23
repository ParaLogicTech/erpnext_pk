# Copyright (c) 2022, ParaLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def validate_ntn_cnic_strn_in_document(doc, method):
    validate_ntn_cnic_strn(doc.get('tax_ntn'), doc.get('tax_cnic'), doc.get('tax_strn'))


def validate_ntn_cnic_strn(ntn=None, cnic=None, strn=None):
	import re
	cnic_regex = re.compile(r'^.....-.......-.$')
	ntn_regex = re.compile(r'^.......-.$')
	strn_regex = re.compile(r'^..-..-....-...-..$')

	if ntn and not ntn_regex.match(ntn):
		frappe.throw(_("Invalid NTN. NTN must be in the format #######-#"))
	if cnic and not cnic_regex.match(cnic):
		frappe.throw(_("Invalid CNIC. CNIC must be in the format #####-#######-#"))
	if strn and not strn_regex.match(strn):
		frappe.throw(_("Invalid STRN. STRN must be in the format ##-##-####-###-##"))
