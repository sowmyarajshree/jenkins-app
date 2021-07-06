// Copyright (c) 2016, nxweb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MACHINING - Delivery Report Daily"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Select",
			"options": ["Finished Goods","Semi Finished Goods"],
			"hidden": 1
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
			"hidden": 1
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
			"hidden": 1
		},

	]
};
