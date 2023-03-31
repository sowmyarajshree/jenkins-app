// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Subcontractor Labour Attendance Revision Summary Report"] = {
	"filters": [
	{
    "fieldname": "project",
    "label": "Project",
    "fieldtype": "Link",
    "options": "Project",
    "width": 180,
    "get_query": function() {
        return {
            "filters": [["Project", "status", "=", "Open"]]
        };
    }
	},
	{
		'label': 'From Date',
		'fieldname': 'from_date',
		'fieldtype': 'Date',
		'default': frappe.datetime.get_today()
	},
	{
		'label': 'To Date',
		'fieldname': 'to_date',
		'fieldtype': 'Date',
		'default': frappe.datetime.get_today()
	},
	{
        "fieldname":"subcontractor",
		"label": __("Subcontractor"),
		"fieldtype": "Link",
		"width": 250,
		"options":"Supplier",
		"get_query":function(){
			return{
				"filters":[["nx_is_sub_contractor","=",1]]
			}
		}
	},
	{
    	"label": "Revised Type",
    	"fieldname": "revised_type",
    	"fieldtype": "Select",
    	"options": [' ','Labour In','Labour Out'],
    	"width": 180
	}

	]
};
