// Copyright (c) 2016, nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Sales Plan Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "sales_plan_frequency",
			"label": __("Frequency"),
			"fieldtype": "Select",
			"options": ["Daily","Weekly","Monthly"],
			"reqd": 1
		},
		{
			"fieldname": "item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "group_by_item",
			"label": __("Group By Item"),
			"fieldtype": "Check"
		}

	]
};
