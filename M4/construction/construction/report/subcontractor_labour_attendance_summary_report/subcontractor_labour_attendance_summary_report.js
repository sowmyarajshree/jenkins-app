frappe.query_reports["Subcontractor Labour Attendance Summary Report"] = {
	"filters": [
	{
		"fieldname": "project",
		"label": "Project",
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
	},
	{
	    "fieldname":"subcontractor",
		"label": __("Subcontractor"),
		"fieldtype": "Link",
		"options":"Supplier"
	}

	]

};

