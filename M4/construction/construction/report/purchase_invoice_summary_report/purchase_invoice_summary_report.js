// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Invoice Summary Report"] = {
	"filters": [
	{
		"fieldname":"supplier",
		"label":__("Supplier"),
		"fieldtype":"Link",
        "options":"Supplier"
	},
	{
		"label":__("From Date"),
		"fieldname": "from_date",
		"fieldtype": "Date",
		"default": frappe.datetime.get_today()
	},
	{
		"label":__("To Date"),
		"fieldname": "to_date",
		"fieldtype": "Date",
		"default": frappe.datetime.get_today()
	},
	{
		"label":__("Project"),
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project"
	}
	]
};
