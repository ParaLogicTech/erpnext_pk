frappe.ui.form.on('Customer', {
	validate: function(frm) {
		erpnext_pk.format_ntn(frm, 'tax_ntn');
		erpnext_pk.format_nic(frm, 'tax_nic');
		erpnext_pk.format_strn(frm, 'tax_strn');
	},

	tax_ntn: function(frm) {
		erpnext_pk.format_ntn(frm, 'tax_ntn');
	},
	tax_nic: function(frm) {
		erpnext_pk.format_nic(frm, 'tax_nic')
	},
	tax_strn: function(frm) {
		erpnext_pk.format_strn(frm, 'tax_strn')
	}
});
