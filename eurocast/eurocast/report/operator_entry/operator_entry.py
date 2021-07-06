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
		'label': _('Operator Entry'),
		'fieldtype': 'Link',
		'fieldname': 'name',
		'width': 100,
		'options':'Operator Entry',
	},
	{
		'label': _('Operation'),
		'fieldtype': 'Link',
		'fieldname': 'operation',
		'width': 100,
		'options':'Operation',
	},
	{
		'label': _('Workstation'),
		'fieldtype': 'Link',
		'fieldname': 'workstation',
		'width': 100,
		'options':'Workstation',
	},
	{
		'label': _('Operator Name'),
		'fieldtype': 'Link',
		'fieldname': 'operator_name',
		'width': 100,
		'options':'Employee',
	},
	{
		'label': _('Posting Date'),
		'fieldtype': 'Data',
		'fieldname': 'posting_date',
		'width': 100,
	},
	{
		'label': _('Shift Type'),
		'fieldtype': 'Link',
		'fieldname': 'shift_type',
		'width': 100,
		'options':'Shift Type',
	},
	{
		'label': _('Shift Start Time'),
		'fieldtype': 'Data',
		'fieldname': 'shift_start_time',
	},
	{
		'label': _('Shift End Time'),
		'fieldtype': 'Data',
		'fieldname': 'shift_end_time',
		'width': 100,
	},
	{
		'label': _('Total Time'),
		'fieldtype': 'Data',
		'fieldname': 'total_hours',
		'width': 100,
	},
	{
		'label': _('Total Time'),
		'fieldtype': 'Data',
		'fieldname': 'total_hours',
		'width': 100,
	},
	{
		'label': _('Total Time'),
		'fieldtype': 'Data',
		'fieldname': 'total_hours',
		'width': 100,
	},
	{
		'label': _('Item'),
		'fieldtype': 'Link',
		'fieldname': 'item_code',
		'width': 100,
		'options':'Item',
	},
	{
		'label': _('Work Order'),
		'fieldtype': 'Link',
		'fieldname': 'work_order',
		'width': 100,
		'options':'Work Order',
	},
	{
		'label': _('BOM'),
		'fieldtype': 'Link',
		'fieldname': 'bom_no',
		'width': 100,
		'options':'BOM',
	},
	{
		'label': _('For  Quantity'),
		'fieldtype': 'Data',
		'fieldname': 'for_quantity',
		'width': 100,
	},
	{
		'label': _('Completed Qty'),
		'fieldtype': 'Data',
		'fieldname': 'completed_qty',
		'width': 100,
	},
	{
		'label': _('Rejected Qty'),
		'fieldtype': 'Data',
		'fieldname': 'rejected_qty',
		'width': 100,
	},
	{
		'label': _('Operation Time'),
		'fieldtype': 'Data',
		'fieldname': 'time_in_mins',
		'width': 100,
	},
	{
		'label': _('Total Time In Minutes'),
		'fieldtype': 'Data',
		'fieldname': 'total_time_mins',
		'width': 100,
	},
	{
		'label': _('Total Time In Hours'),
		'fieldtype': 'Data',
		'fieldname': 'total_time_',
		'width': 100,
	},
	{
		'label': _('Start Time'),
		'fieldtype': 'Data',
		'fieldname': 'start_time',
		'width': 100,
	},
	{
		'label': _('End Time'),
		'fieldtype': 'Data',
		'fieldname': 'end_time',
		'width': 100,
	},
	{
		'label': _('WIP Warehouse'),
		'fieldtype': 'Link',
		'fieldname': 'wip_warehouse',
		'width': 100,
		'options': 'Warehouse'
	},
	{
		'label': _('Start Hour'),
		'fieldtype': 'Data',
		'fieldname': 'start_hour',
		'width': 100,
	},
	{
		'label': _('Total Hour'),
		'fieldtype': 'Data',
		'fieldname': 'total_hour',
		'width': 100,
	},
	{
		'label': _('Delay Reasons'),
		'fieldtype': 'Link',
		'fieldname': 'delay_reasons',
		'width': 100,
		'options': 'Delay Reasons'
	},
	{
		'label': _('Hours Ideal'),
		'fieldtype': 'Data',
		'fieldname': 'hours_ideal',
		'width': 100,
	},
	{
		'label': _('Consumed Time'),
		'fieldtype': 'Data',
		'fieldname': 'consumed_time',
		'width': 100,
	},
	{
		'label': _('Difference Time'),
		'fieldtype': 'Data',
		'fieldname': 'difference_time',
		'width': 100,
	}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql("""
		SELECT
			op.name,op.operation, op.workstation, op.operator_name, op.posting_date, op.shift_type, op.start_time as shift_start_time, op.end_time as
			shift_end_time, op.total_hours, op.consumed_time, op.difference_time, od.item_code, od.work_order, od.completed_qty, od.rejected_qty,
			od.time_in_mins, od.total_time_mins, od.total_time_, od.bom_no, od.for_quantity, od.start_time, od.end_time, od.wip_warehouse, od.start_hour,
			od.total_hour, id.delay_reasons, id.hours_ideal
		FROM
			`tabOperator Entry` op, `tabOperation Details` od, `tabIdeal Details` id
		WHERE
			od.parent = op.name and id.parent = op.name and op.docstatus = 1 %s """ % conditions, filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("item_code"):
		conditions +=" and od.item_code = %(item_code)s"
	if filters.get("wip_warehouse"):
		conditions +=" and od.wip_warehouse = %(wip_warehouse)s"
	if filters.get("to_date"):
		conditions +=" and posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and posting_date >= %(from_date)s"

	return conditions
