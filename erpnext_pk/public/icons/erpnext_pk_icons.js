$(document).ready(() => {
	var html = frappe.render_template('erpnext_pk_icons');
	$(html).appendTo("body");
});
