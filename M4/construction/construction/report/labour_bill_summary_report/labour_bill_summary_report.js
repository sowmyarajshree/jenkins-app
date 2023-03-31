frappe.query_reports["Labour Bill Summary Report"] = {
	"filters": [
	{
	        "fieldname":"project_name",
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
		},
	{
	        "fieldname":"labour_type",
			"label": __("Labour Type"),
			"fieldtype": "Select",
			"width": 250,
			"options":["","Muster Roll","F and F","Rate Work"]
	},
	{
			"fieldname" : "muster_roll",
			"label" : "Muster Roll",
			"fieldtype" : "Link",
			"options" : "Muster Roll"
	},
	{
			"fieldname" : "subcontractor",
			"label" : "Subcontractor",
			"fieldtype" : "Link",
			"options" : "Supplier"
	}

	]
};
