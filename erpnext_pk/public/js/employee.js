frappe.ui.form.on('Employee', {
	validate: function(frm) {
		erpnext_pk.format_cnic(frm, 'tax_cnic');
	},
	tax_cnic: function(frm) {
		erpnext_pk.format_cnic(frm, 'tax_cnic')
	},
});
