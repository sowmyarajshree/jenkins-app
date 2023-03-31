// Copyright (c) 2022, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Labourers Summary"] = {
	"filters": [
	    {
			"fieldname":"subcontractor",
			"label": __("Subcontractor"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Supplier"
		},

	]
};
