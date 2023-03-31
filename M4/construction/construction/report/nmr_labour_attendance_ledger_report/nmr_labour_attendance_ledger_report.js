// Copyright (c) 2023, Nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["NMR Labour Attendance Ledger Report"] = {
	"filters": [
		{
		'fieldname':'project',
		'label':'Project',
		'fieldtype':'Link',
		'width':180,
		'options':'Project'
	},
	{
		'label':'Muster Roll',
		'fieldtype':'Link',
		'fieldname':'muster_roll',
		'width'	   :160,
		'options' :"Muster Roll"
	},
	{
		"label": "From Date",
		"fieldname": "from_date",
		"fieldtype": "Date",
		"default": frappe.datetime.get_today()
	},
	{
		"label": "To Date",
		"fieldname": "to_date",
		"fieldtype": "Date",
		"default": frappe.datetime.get_today()
	}

	]
};
