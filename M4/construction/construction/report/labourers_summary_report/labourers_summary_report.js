// Copyright (c) 2022, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Labourers Summary Report"] = {
	"filters": [
	    {
			"fieldname":"subcontractor",
			"label": __("Subcontractor"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Supplier"
		},
		{


			"fieldname":"posting_date",
			"label": __("Posting Date"),
			"fieldtype": "Date",
			"width": "80",
			"default":frappe.datetime.get_today()
			


			
	   },

	]
};
