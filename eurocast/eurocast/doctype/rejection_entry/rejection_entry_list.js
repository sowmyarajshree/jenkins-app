frappe.listview_settings['Rejection Entry'] = {
	add_fields: ["status"],
	get_indicator: function (doc) {
		if (doc.status === "Submitted") {
			return [__("Submitted"), "orange", "status,=,Submitted"];
		}else if (doc.status === "Completed") {
			return [__("Completed"), "green", "status,=,Completed"];
		}else if (doc.status === "Cancelled") {
			return [__("Cancelled"), "red", "status,=,Cancelled"];
		}
	}
};
