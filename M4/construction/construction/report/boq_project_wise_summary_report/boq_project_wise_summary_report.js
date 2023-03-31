// Copyright (c) 2016, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BOQ Project Wise Summary Report"] = {
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
			"get_query": ()=>{return{filters:[["project","=",frappe.query_report.get_filter_value("project")]]}},
			"width": "80",
			"options":"Project Structure"
		  },
		   {
			"fieldname":"work_status",
			"label": __("Work status"),
			"fieldtype": "Select",
			"width": "80",
			"options":"\nNot Scheduled\nScheduled\nIn Progress\nCompleted"
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
	  	if (column.fieldname == "project" && data.work_status == "Not Scheduled"){
	  		value = "<span style ='color:DeepPink'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "project_structure" && data.work_status == "Not Scheduled"){
	  		value = "<span style ='color:DeepPink'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "item_of_work" && data.work_status == "Not Scheduled"){
	  		value = "<span style ='color:DeepPink'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "billing_status" && data.work_status == "Not Scheduled"){
	  		value = "<span style ='color:DeepPink'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "work_status" && data.work_status == "Not Scheduled"){
	  		value = "<span style ='color:DeepPink'>" + value + "</span>";
	  	}



	  	if (column.fieldname == "project" && data.work_status == "In Progress"){
	  		value = "<span style ='color:MediumSeaGreen'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "project_structure" && data.work_status == "In Progress"){
	  		value = "<span style ='color:MediumSeaGreen'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "item_of_work" && data.work_status == "In Progress"){
	  		value = "<span style ='color:MediumSeaGreen'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "billing_status" && data.work_status == "In Progress"){
	  		value = "<span style ='color:MediumSeaGreen'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "work_status" && data.work_status == "In Progress"){
	  		value = "<span style ='color:MediumSeaGreen'>" + value + "</span>";
	  	}


	  	if (column.fieldname == "project" && data.work_status == "Scheduled"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "project_structure" && data.work_status == "Scheduled"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "item_of_work" && data.work_status == "Scheduled"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "billing_status" && data.work_status == "Scheduled"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "work_status" && data.work_status == "Scheduled"){
	  		value = "<span style ='color:Purple'>" + value + "</span>";
	  	}


	  	if (column.fieldname == "project" && data.work_status == "Completed"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "project_structure" && data.work_status == "Completed"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "item_of_work" && data.work_status == "Completed"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "billing_status" && data.work_status == "Completed"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
	  	if (column.fieldname == "work_status" && data.work_status == "Completed"){
	  		value = "<span style ='color:green'>" + value + "</span>";
	  	}
  
	  	return value;
	  }
};
