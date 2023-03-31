// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["F and F Entry Ledger Report"] = {
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
	        "fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"width": 250,
			"options":[" ","To Bill","Completed"]
		}

	]
};
