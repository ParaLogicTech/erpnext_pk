frappe.ui.form.on('Supplier', {
	validate: function(frm) {
		erpnext_pk.format_ntn(frm, 'tax_ntn');
		erpnext_pk.format_cnic(frm, 'tax_cnic');
		erpnext_pk.format_strn(frm, 'tax_strn');
	},

	tax_ntn: function(frm) {
		erpnext_pk.format_ntn(frm, 'tax_ntn');
	},
	tax_cnic: function(frm) {
		erpnext_pk.format_cnic(frm, 'tax_cnic')
	},
	tax_strn: function(frm) {
		erpnext_pk.format_strn(frm, 'tax_strn')
	}
});
