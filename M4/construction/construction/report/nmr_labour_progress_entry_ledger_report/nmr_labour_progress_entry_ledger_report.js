// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["NMR Labour Progress Entry Ledger Report"] = {
	"filters": [
		{
		'fieldname':'project',
		'label':'Project',
		'fieldtype':'Link',
		'width':180,
		'options':'Project',
		'get_query': function() {
        	return {
            	"filters": [["Project", "status", "=", "Open"]]
        }
    }
	},
	{
		'fieldname':'project_structure',
		'label':'Project Structure',
		'fieldtype':'Link',
		'width':180,
		'options':'Project Structure',
		'get_query':function(){
			return{
				"filters":[["project","=",frappe.query_report.get_filter_value('project')]]
			}
		}
	},
	{
		'fieldname':'item_of_work',
		'label':'Item of Work',
		'fieldtype':'Link',
		'width':180,
		'options':'Item of Work',
		'get_query':function(){
			return{
				"filters":[["project","=",frappe.query_report.get_filter_value('project')]]
			}
		}
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
		'label':'Status',
		'fieldtype':'Select',
		'fieldname':'status',
		'width'	   :160,
		'options' :[' ','To Prepared and Bill','To Bill','Completed']
	}

	]
};
