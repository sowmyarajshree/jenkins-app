// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BOQ Tender Report"] = {
	"filters": [
		{
			"label": "Project",
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",			
            "get_query": function() {
                var filters = [];
                if (frappe.query_report.get_filter_value("is_open_project") === 1) {
                    filters.push(["status", "=", "Open"]);
                }
                return {filters: filters};
            }

		},		
		{
			"label": "Is Open Project ",
			"fieldname": "is_open_project",
			"fieldtype": "Check"
		},		
		{
			"label": "Project Structure",
			"fieldname": "project_structure",
			"fieldtype": "Link",
			"options": "Project Structure",
			"get_query": ()=>{return{filters:[["project","=",frappe.query_report.get_filter_value("project")]]}}
		},
		{
			"label": "Item Of Work",
			"fieldname": "item_of_work",
			"fieldtype": "Link",
			"options": "Item of Work",
			"get_query": ()=>{return{filters:[["project","=",frappe.query_report.get_filter_value("project")]]}}
		},
		{
			"label": "Work Status",
			"fieldname": "work_status",
			"fieldtype": "Select",
			"options": ["", "Scheduled", "Not Scheduled", "In Progress", "Completed"]
		},
		{
			"label": "Billing Status",
			"fieldname": "billing_status",
			"fieldtype": "Select",
			"options": ["", "To Quotation", "To Order", "Order", "Not Billable"]
		}

	]
};
