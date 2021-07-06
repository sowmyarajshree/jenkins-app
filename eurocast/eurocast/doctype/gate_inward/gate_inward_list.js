frappe.listview_settings['Gate Inward'] = {
	add_fields: ["status"],
	get_indicator: function (doc) {
		if (doc.status === "Open") {
			return [__("Open"), "orange", "status,=,Open"];
		}else if (doc.status === "Completed") {
			return [__("Completed"), "green", "status,=,Completed"];
		}else if (doc.status === "Billed") {
			return [__("Billed"), "green", "status,=,Billed"];
		}else if (doc.status === "Handed Over") {
			return [__("Handed Over"), "green", "status,=,Handed Over"];
		}else if (doc.status === "Cancelled") {
			return [__("Cancelled"), "red", "status,=,Cancelled"];
		}
	}
};
