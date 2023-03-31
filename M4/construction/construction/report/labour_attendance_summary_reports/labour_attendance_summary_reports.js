// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Labour Attendance Summary Report"] = {
	"filters": [
		{
			"label": "Project",
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"label": "Attendance Type",
			"fieldname": "attendance_type",
			"fieldtype": "Select",
			"options": ["", "Muster Roll", "Subcontractor"]
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
			"label": "Subcontractor",
			"fieldname": "subcontractor",
			"get_query": ()=>{return{filters:[["nx_is_sub_contractor","=",1]]}},
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
			"label": "Muster Roll",
			"fieldname": "muster_roll",
			"fieldtype": "Link",
			"options": "Muster Roll",
			"get_query":()=>{return{filters:[["status","=","Active"]]}}
		}
	]
}






