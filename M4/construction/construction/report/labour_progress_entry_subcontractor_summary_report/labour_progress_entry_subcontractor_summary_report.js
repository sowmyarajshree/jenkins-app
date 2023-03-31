frappe.query_reports["Labour Progress Entry Subcontractor Summary Report"] = {
	"filters": [
	{
	        "fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": 250,
			"options":"Project"
	},
	{
	        "fieldname":"project_structure",
			"label": __("Project Structure"),
			"fieldtype": "Link",
			"get_query": ()=>{return{filters:[["project","=",frappe.query_report.get_filter_value("project")]]}},
			"width": 250,
			"options":"Project Structure"
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
			"options":["","F and F","Rate Work"]
	},
	{
			"fieldname" : "subcontractor",
			"label" : "Subcontractor",
			"fieldtype" : "Link",
			"options" : "Supplier"
	}

	]

};

