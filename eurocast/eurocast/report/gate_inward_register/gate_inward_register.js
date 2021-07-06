frappe.query_reports["Gate Inward Register"] = {
	"filters": [
		{
				"fieldname":"from_date",
				"label": __("From Date"),
				"fieldtype": "Datetime",
				"width": "80",
				"default": frappe.datetime.month_start()
			},
			{
				"fieldname":"to_date",
				"label": __("To Date"),
				"fieldtype": "Datetime",
				"width": "80",
				"default": frappe.datetime.month_end()
			}
		]
};
