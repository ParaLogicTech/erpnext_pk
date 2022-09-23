frappe.ui.form.on('Employee', {
	validate: function(frm) {
		erpnext_pk.format_nic(frm, 'tax_nic');
	},
	tax_nic: function(frm) {
		erpnext_pk.format_nic(frm, 'tax_nic')
	},
});
