
// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cash Requisition Report"] = {
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
			"label": "Accounting Period",
			"fieldname": "accounting_period",
			"fieldtype": "Link",
			"options": "Accounting Period"
		},
		{
			"label": "Workflow State",
			"fieldname": "workflow_state",
			"fieldtype": "Select",
			"options": ["", "Pending", "Waiting for Approval", "Approved"]
		}
	]
}






