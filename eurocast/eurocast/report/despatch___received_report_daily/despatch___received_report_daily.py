# Copyright (c) 2013, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	return [{
		'label': _('Item Code'),
		'fieldtype': 'Link',
		'fieldname': 'item_code',
		'width': 200,
		'options':'Item',
	},
	{
		'label': _('Item Name'),
		'fieldtype': 'Data',
		'fieldname': 'item_name',
		'width': 200,
	},
	{
		'label': _('Source Warehouse'),
		'fieldtype': 'Link',
		'fieldname': 'source_warehouse',
		'options': "Warehouse",
		'width': 200,
	},
	{
		'label': _('A'),
		'fieldtype': 'Float',
		'fieldname': 'shift_a',
		'width': 100,
	},
	{
		'label': _('B'),
		'fieldtype': 'Float',
		'fieldname': 'shift_b',
		'width': 100,
	},
	{
		'label': _('C'),
		'fieldtype': 'Float',
		'fieldname': 'shift_c',
		'width': 100,
	},
	{
		'label': _('Total'),
		'fieldtype': 'Float',
		'fieldname': 'total',
		'width': 100,
	}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql("""
		SELECT
			sum(std.qty) as overall_plan,sum(std.qty)/3 as per_shift_plan,st.posting_date,st.stock_entry_type,
			st.from_warehouse , std.parent as std_parent, std.qty,std.s_warehouse as source_warehouse,std.item_code, std.item_name,
			std.parent as std_parent, st.name as st_name,
			sum(case when (st.posting_time >= "07:30:00" and st.posting_time <= "15:30:00") then std.qty else 0 end) as shift_a,
			sum(case when (st.posting_time >= "15:31:00" and st.posting_time <= "23:30:00") then std.qty else 0 end) as shift_b,
			sum(case when ((st.posting_time >= "00:00:00") and (st.posting_time <= "07:29:00") or (st.posting_time >= "23:31:00")) then std.qty else 0 end) as shift_c,
			sum(case when (st.posting_time >= "7:30:00" and st.posting_time <= "15:30:00") then std.qty else 0 end) +
			sum(case when (st.posting_time >= "15:31:00" and st.posting_time <= "23:30:00") then std.qty else 0 end) +
			sum(case when ((st.posting_time >= "00:00:00") and (st.posting_time <= "07:29:00") or (st.posting_time >= "23:31:00")) then std.qty else 0 end) as total,
			st.shift_date

		FROM
			`tabStock Entry Detail` std,
			`tabStock Entry` st
		WHERE
			st.docstatus = 1 and st.stock_entry_type = "Material Transfer" and
			std.item_group in ("Finished Goods","Semi Finished Goods")
			and st.to_warehouse = "Despatch Store - ECE" and
			std.parent = st.name  %s
		GROUP BY
			std.item_code
		ORDER BY
			std.item_code """% conditions,filters,as_dict=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("item_code"):
		conditions +=" and std.item_code = %(item_code)s"

	if filters.get("date"):
		conditions +=" and st.shift_date = %(date)s"


	if filters.get("warehouse"):
		conditions +=" and st.to_warehouse = %(warehouse)s"


	if filters.get("item_group"):
		conditions +=" and std.item_group = %(item_group)s"

	return conditions
