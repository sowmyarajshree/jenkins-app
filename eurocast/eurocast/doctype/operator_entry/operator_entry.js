// Copyright (c) 2020, nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Operator Entry', {
	after_save: function(frm,doc) {
		//frm.reload_doc();
		frm.refresh();
		//frm.refresh_field('operation_details');
	},
	operation_details: function(frm,doc){
		frm.refresh();
		//frm.reload_doc();
	}
});



