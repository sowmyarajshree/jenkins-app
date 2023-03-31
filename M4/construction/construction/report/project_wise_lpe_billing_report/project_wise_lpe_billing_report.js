// Copyright (c) 2016, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Wise LPE Billing Report"] = {
	"filters": [
	     {
			"fieldname":"project_name",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Project"
		  },
		  {
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"width": "80",
			"options":"\nTo Prepared and Bill \nTo Bill \nCompleted"
		  },

	],
	"formatter": function(value, row, column, data, default_formatter){
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "status" && data.status == "To Prepared and Bill"){
			value = "<span style ='color:MidnightBlue'>" + value + "</span>";
		}
		if (column.fieldname == "status" && data.status == "To Bill"){
			value = "<span style ='color:Orange'>" + value + "</span>";
		}
		if (column.fieldname == "status" && data.status == "Completed"){
			value = "<span style ='color:DarkGreen'>" + value + "</span>";
		}
		return value;
	}
};
