// Copyright (c) 2021, Nxweb and contributors
// For license information, please see license.txt
frappe.ui.form.on('Item of Work', {
	refresh: function(frm, doc) {
		cur_frm.set_query("project", function() {
			return {
				"filters": [
					["Project", "status", "=", "Open"]
				]
			};
		});
		frm.add_custom_button(__('New'), function() {
			frappe.route_options = {
				"project": cur_frm.doc.project
			};
			frappe.new_doc("Item of Work");
		})
        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === "BOQ") {
            let boq_doc = frappe.model.get_doc("BOQ", frappe.get_prev_route()[2])
            cur_frm.set_value("project", boq_doc.project)
        }
        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === "Rate Work Entry") {
            let rwe_doc = frappe.model.get_doc("Rate Work Entry", frappe.get_prev_route()[2])
            cur_frm.set_value("project", rwe_doc.project)
        }
        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === "Labour Progress Entry") {
            let boq_doc = frappe.model.get_doc("Labour Progress Entry", frappe.get_prev_route()[2])
            cur_frm.set_value("project", boq_doc.project_name)
        }
	}
});
