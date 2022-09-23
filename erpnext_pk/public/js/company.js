frappe.ui.form.on('Company', {
	setup: function(frm){
		frm.set_query("sales_tax_account", function(){
			return {filters: {"account_type": "Tax", "is_group": 0, "company": frm.doc.name}}
		});
		frm.set_query("extra_tax_account", function(){
			return {filters: {"account_type": "Tax", "is_group": 0, "company": frm.doc.name}}
		});
		frm.set_query("further_tax_account", function(){
			return {filters: {"account_type": "Tax", "is_group": 0, "company": frm.doc.name}}
		});
		frm.set_query("service_tax_account", function(){
			return {filters: {"account_type": "Tax", "is_group": 0, "company": frm.doc.name}}
		});
		frm.set_query("advance_tax_account", function(){
			return {filters: {"account_type": "Tax", "is_group": 0, "company": frm.doc.name}}
		});
	},
	validate: function(frm) {
		erpnext_pk.format_ntn(frm, 'tax_ntn');
		erpnext_pk.format_strn(frm, 'tax_strn');
		erpnext_pk.format_nic(frm, 'tax_nic');
	},

	tax_ntn: function(frm) {
		erpnext_pk.format_ntn(frm, 'tax_ntn');
	},
	tax_strn: function(frm) {
		erpnext_pk.format_strn(frm, 'tax_strn');
	},
	tax_nic: function(frm) {
		erpnext_pk.format_nic(frm, 'tax_nic');
	}
});
