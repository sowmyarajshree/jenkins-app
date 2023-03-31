// Copyright (c) 2016, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["LPE Waiting for Billing"] = {
	"filters": [
	     {
			"fieldname":"project_name",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Project"
		  }

	],
	"formatter": function(value, row, column, data, default_formatter){
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "status" && data.status == "To Prepared and Bill"){
			value = "<span style ='color:MidnightBlue'>" + value + "</span>";
		}
		
		return value;
	}
};
