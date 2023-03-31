// Copyright (c) 2016, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BOQ Billing Progress Report"] = {
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
		  },
		  {
			"fieldname":"billing_status",
			"label": __("Billing Status"),
			"fieldtype": "Select",
			"width": "80",
			"options":"\nTo Quotation\nTo Order\nOrdered\nNot Billable"
		  }


	],
	"formatter": function(value, row, column, data, default_formatter){
	  	value = default_formatter(value, row, column, data);
	  	if (column.fieldname == "project" && data.billing_status == "To Quotation"){
	  		value = "<span style ='color:RebeccaPurple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "project_structure" && data.billing_status == "To Quotation"){
	  		value = "<span style ='color:RebeccaPurple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "item_of_work" && data.billing_status == "To Quotation"){
	  		value = "<span style ='color:RebeccaPurple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "billing_status" && data.billing_status == "To Quotation"){
	  		value = "<span style ='color:RebeccaPurple'>" + value + "</span>";
	  	}

	  	if (column.fieldname == "project" && data.billing_status == "To Order"){
	  		value = "<span style ='color:Maroon'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "project_structure" && data.billing_status == "To Order"){
	  		value = "<span style ='color:Maroon'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "item_of_work" && data.billing_status == "To Order"){
	  		value = "<span style ='color:Maroon'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "billing_status" && data.billing_status == "To Order"){
	  		value = "<span style ='color:Maroon'>" + value + "</span>";
	  	}


	  	if (column.fieldname == "project" && data.billing_status == "Not Billable"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "project_structure" && data.billing_status == "Not Billable"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "item_of_work" && data.billing_status == "Not Billable"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "billing_status" && data.billing_status == "Not Billable"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}


	  	if (column.fieldname == "project" && data.billing_status == "Ordered"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "project_structure" && data.billing_status == "Ordered"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "item_of_work" && data.billing_status == "Ordered"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "billing_status" && data.billing_status == "Ordered"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}

	  	return value;
	  }
};
