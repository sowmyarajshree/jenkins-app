// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Petty Cash"] = {
	"filters": [
		{
			"fieldname":"posting_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname":"account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options": "Account"
		}

	],
	  "formatter": function(value, row, column, data, default_formatter){
	  	value = default_formatter(value, row, column, data);
	  	if (column.fieldname == "total" && data.total <= 0){
	  		value = "<span style ='color:red'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "total" && data.total > 0){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "credit"){
	  		value = "<span style ='color:blue'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "debit"){
	  		value = "<span style ='color:purple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "account"){
	  		value = "<span style ='color:violet'>" + value + "</span>";
	  	}	  
	  	return value;


	  }
};
