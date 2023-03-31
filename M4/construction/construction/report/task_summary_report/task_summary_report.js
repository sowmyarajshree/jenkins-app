frappe.query_reports["Task Summary Report"] = {
	"filters": [
	{
	        "fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": 250,
			"options":"Project"
	},
	{
	        "fieldname":"nx_project_structure",
			"label": __("Project Structure"),
			"fieldtype": "Link",
			"get_query": ()=>{return{filters:[["project","=",frappe.query_report.get_filter_value("project")]]}},
			"width": 250,
			"options":"Project Structure"
	},
	{
	        "fieldname":"nx_item_of_work",
			"label": __("Item of Work"),
			"fieldtype": "Link",
			"get_query": ()=>{return{filters:[["project","=",frappe.query_report.get_filter_value("project")]]}},
			"width": 250,
			"options":"Item of Work"
	},
	{
	
			"fieldname":"progress_status",
			"label": __("Status"),
			"fieldtype": "Select",
			"width": 250,
			"options":["Open","In Progress"]
	}

	]

};

