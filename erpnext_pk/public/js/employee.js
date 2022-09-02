frappe.ui.form.on('Employee', {
	validate: function(frm) {
		erpnext_pk.format_cnic(frm, 'cnic');
	},
	cnic: function(frm) {
		erpnext_pk.format_cnic(frm, 'cnic')
	},
});
