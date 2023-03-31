frappe.query_reports["Journal Entry Summary Report"] = {
	"filters": [
	{
	        "fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": 250,
			"options":"Project"
	},
	{
			"label": "From Date",
			"fieldname": "from_date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
	},
	{
			"label": "To Date",
			"fieldname": "to_date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
	}

	]

};

