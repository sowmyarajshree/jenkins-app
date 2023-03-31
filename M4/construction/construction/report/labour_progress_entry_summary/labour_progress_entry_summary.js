// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Labour Progress Entry Summary"] = {
	"filters": [
	        {   
				'fieldname':'project_name',
	            'label': __('Project'),
	            'fieldtype': 'Link',            
	            'width': "80",
	            'options': "Project"
	        },
	        {
				"fieldname":"from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"width": "80",
				"default": frappe.datetime.month_start()
			},
			{
				"fieldname":"to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"width": "80",
				"default": frappe.datetime.month_end()
			},
			{   
				'fieldname':'labour_type',
	            'label': __('Labour Type'),
	            'fieldtype': 'Select',            
	            'options': [" ","F and F","Rate Work","Muster Roll"]
	        },
	        {   
				'fieldname':'item_of_work',
	            'label': __('Item of Work'),
	            'fieldtype': 'Link',            
	            'width': "80",
	            'options': "Item of Work"
	        },
			


	]
};
