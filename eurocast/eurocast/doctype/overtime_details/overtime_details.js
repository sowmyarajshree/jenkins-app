// Copyright (c) 2021, nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Details', {
	timeline_refresh: function(frm,doc) {
		var ot_amount = parseFloat(frm.doc.authorized_time) * parseFloat(frm.doc.per_hour_rate);
		frm.set_value("ot_amount",ot_amount);

	}
});
