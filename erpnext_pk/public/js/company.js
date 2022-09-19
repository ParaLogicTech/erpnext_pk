frappe.ui.form.on('Company', {
	setup: function(frm){
		frm.set_query("sales_tax_account", function(){
			return {filters: {"account_type": "Tax"}}
		});
		frm.set_query("extra_tax_account", function(){
			return {filters: {"account_type": "Tax"}}
		});
		frm.set_query("further_tax_account", function(){
			return {filters: {"account_type": "Tax"}}
		});
		frm.set_query("service_tax_account", function(){
			return {filters: {"account_type": "Tax"}}
		});
		frm.set_query("advance_tax_account", function(){
			return {filters: {"account_type": "Tax"}}
		});
	},
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

