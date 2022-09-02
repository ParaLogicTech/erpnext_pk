frappe.ui.form.on('Company', {
	validate: function(frm) {
		erpnext_pk.format_ntn(frm, 'tax_ntn');
		erpnext_pk.format_strn(frm, 'tax_strn');
		erpnext_pk.format_strn(frm, 'tax_cnic');
	},

	tax_ntn: function(frm) {
		erpnext_pk.format_ntn(frm, 'tax_ntn');
	},
	tax_strn: function(frm) {
		erpnext_pk.format_strn(frm, 'tax_strn');
	},
	tax_cnic: function(frm) {
		erpnext_pk.format_strn(frm, 'tax_cnic');
	}
});
