// Copyright (c) 2016, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BOQ Quantity Analysis"] = {
	"filters": [
         {
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Project"
		  },
		  {
			"fieldname":"project_structure",
			"label": __("Project structure"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Project Structure"
		  }
	]
};
