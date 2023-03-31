// Copyright (c) 2016, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Material Actual Qty VS Consumption Qty"] = {
	"filters": [
	   {
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default":frappe.datetime.month_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default":frappe.datetime.month_end()
		},
	    {
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Project"
		},
		{
			"fieldname":"project_structure",
			"label": __("Project Structure"),
			"fieldtype": "Link",
			"get_query": ()=>{return{filters:[["project","=",frappe.query_report.get_filter_value("project")]]}},
			"width": "80",
			"options":"Project Structure"
		},
		{
			"fieldname":"item_of_work",
			"label": __("Item of Work"),
			"fieldtype": "Link",
			"get_query": ()=>{return{filters:[["project","=",frappe.query_report.get_filter_value("project")]]}},
			"width": 80,
			"options":"Item of Work"
		}


	]
};
