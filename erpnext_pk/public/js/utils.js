frappe.provide('erpnext_pk');

$.extend(erpnext_pk, {
    format_ntn: function(frm, fieldname) {
		let value = frm.doc[fieldname];
		if (value) {
			value = value.replace(/[^0-9a-zA-Z]+/g, "");
			value = value.toUpperCase();

			//0000000-0
			if (value.length >= 7) {
				value = value.slice(0, 7) + "-" + value.slice(7);
			}

			frm.set_value(fieldname, value);
		}
	},

	format_cnic: function(frm, fieldname) {
		let value = frm.doc[fieldname];
		if (value) {
			value = value.replace(/[^0-9]+/g, "");

			// 00000-0000000-0
			if (value.length >= 12) {
				value = value.slice(0, 12) + "-" + value.slice(12);
			}
			if (value.length >= 5) {
				value = value.slice(0, 5) + "-" + value.slice(5);
			}

			frm.set_value(fieldname, value);
		}
	},

	format_strn: function(frm, fieldname) {
		let value = frm.doc[fieldname];
		if (value) {
			value = value.replace(/[^0-9]+/g, "");

			// 00-00-0000-000-00
			if (value.length >= 11) {
				value = value.slice(0, 11) + "-" + value.slice(11);
			}
			if (value.length >= 8) {
				value = value.slice(0, 8) + "-" + value.slice(8);
			}
			if (value.length >= 4) {
				value = value.slice(0, 4) + "-" + value.slice(4);
			}
			if (value.length >= 2) {
				value = value.slice(0, 2) + "-" + value.slice(2);
			}

			frm.set_value(fieldname, value);
		}
	},
});