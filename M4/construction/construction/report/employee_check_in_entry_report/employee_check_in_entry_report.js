// Copyright (c) 2016, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Check in Entry Report"] = {
	"filters": [
	      {
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Department"
		  },
		  {
			"fieldname":"time",
			"label": __("Date"),
			"fieldtype": "Date",
			"width":"80",
			"default":frappe.datetime.get_today()

		  }

	  ],
	  "formatter": function(value, row, column, data, default_formatter){
	  	value = default_formatter(value, row, column, data);
	  	if (column.fieldname == "log_type" && data.log_type == "IN"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "employee" && data.log_type == "-"){
	  		value = "<span style ='color:red'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "employee" && data.log_type == "IN"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "check_in_time" && data.log_type == "IN"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "department"){
	  		value = "<span style ='color:purple'>" + value + "</span>";
	  	}
	  
	  	return value;


	  }
};
