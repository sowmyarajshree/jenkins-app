// Copyright (c) 2016, nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Dispatch Details Report"] = {
	"filters": [
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"reqd": 1 ,
			"options": [
				{ "value": "Jan", "label": __("Jan") },
				{ "value": "Feb", "label": __("Feb") },
				{ "value": "Mar", "label": __("Mar") },
				{ "value": "Apr", "label": __("Apr") },
				{ "value": "May", "label": __("May") },
				{ "value": "June", "label": __("June") },
				{ "value": "July", "label": __("July") },
				{ "value": "Aug", "label": __("Aug") },
				{ "value": "Sep", "label": __("Sep") },
				{ "value": "Oct", "label": __("Oct") },
				{ "value": "Nov", "label": __("Nov") },
				{ "value": "Dec", "label": __("Dec") },
			],
			"default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1
		},
		{
				"fieldname": "year",
				"label": __("Year"),
				"fieldtype": "Link",
				"options": "Fiscal Year",
				"default": frappe.defaults.get_user_default("fiscal_year"),
				"reqd": 1
		},
	]
};
