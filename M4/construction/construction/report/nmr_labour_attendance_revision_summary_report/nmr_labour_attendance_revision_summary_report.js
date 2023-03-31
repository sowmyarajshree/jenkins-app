// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["NMR Labour Attendance Revision Summary Report"] = {
	"filters": [
	{
    "fieldname": "project",
    "label": "Project",
    "fieldtype": "Link",
    "options": "Project",
    "width": 180,
    "get_query": function() {
        return {
            "filters": [["Project", "status", "=", "Open"]]
        };
    }
	},
	{
		'label': 'From Date',
		'fieldname': 'from_date',
		'fieldtype': 'Date',
		'default': frappe.datetime.get_today()
	},
	{
		'label': 'To Date',
		'fieldname': 'to_date',
		'fieldtype': 'Date',
		'default': frappe.datetime.get_today()
	},
	{
		'label':'Muster Roll',
		'fieldtype':'Link',
		'fieldname':'muster_roll',
		'width'	   :160,
		'options' :"Muster Roll",
		'get_query':function(){
			return{
				'filters':[['Muster Roll','status','=','Active']]
			}
		}
	},
	{
    	"label": "Revised Type",
    	"fieldname": "revised_type",
    	"fieldtype": "Select",
    	"options": [' ','Labour In','Labour Out'],
    	"width": 180
	}
	]
};
