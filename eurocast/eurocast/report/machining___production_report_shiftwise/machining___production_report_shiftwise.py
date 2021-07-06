# Copyright (c) 2013, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate, flt
from frappe import msgprint,_

def execute(filters=None, additional_query_columns=None):
	filters = frappe._dict(filters or {})
	hours_list = get_hours(filters, additional_query_columns)
	columns, delay_reasons = get_columns(filters,hours_list)

	if not hours_list:
		msgprint(_("No record found"))
		return columns, hours_list
	hours_map = get_hours_map(hours_list)
	data = []
	for d in hours_list:
		row = ({
			"name": d.name,
			"workstation": d.workstation,
			"employee_name": d.employee_name,
			"shift_type": d.shift_type,
			"item_name": d.item_name,
			"completed_qty": d.completed_qty,
			"rejected_qty": d.rejected_qty,
			"planned_qty": d.planned_qty,
			"efficiency": d.efficiency,
			"rejection": d.rejection,
			"loss_hours": d.loss_hours
		})
		for h in delay_reasons:
			hours_ideal = flt(hours_map.get(d.name, {}).get(h))
			row.update({
					h: hours_ideal
			})

		if additional_query_columns:
			for col in additional_query_columns:
				row.update({
					col: d.get(col)
				})
		data.append(row)
	return columns, data

def get_columns(filters, hours_list):
	columns = [{
		'label': _('Operator Entry'),
		'fieldtype': 'Link',
		'fieldname': 'name',
		'width': 100,
		'options':'Operator Entry',
	},
	{
		'label': _('Machine'),
		'fieldtype': 'Link',
		'fieldname': 'workstation',
		'width': 100,
		'options':'Workstation',
	},
	{
		'label': _('Operator Name'),
		'fieldtype': 'Link',
		'fieldname': 'employee_name',
		'width': 100,
		'options':'Employee',
	},
	{
		'label': _('Component Name'),
		'fieldtype': 'Data',
		'fieldname': 'item_name',
		'width': 100,
	},
	{
		'label': _('Planned Qty'),
		'fieldtype': 'Float',
		'fieldname': 'planned_qty',
		'width': 75,
	},
	{
		'label': _('Completed Qty'),
		'fieldtype': 'Float',
		'fieldname': 'completed_qty',
		'width': 75,
	},
	{
		'label': _('Rejected Qty'),
		'fieldtype': 'Float',
		'fieldname': 'rejected_qty',
		'width': 75,
	},
		{
		'label': _('Loss Hours'),
		'fieldtype': 'Float',
		'fieldname': 'loss_hours',
		'width': 75,
	},
	{
		'label': _('Efficiency %'),
		'fieldtype': 'Data',
		'fieldname': 'efficiency',
		'width': 75,
	},
	{
		'label': _('Rejection %'),
		'fieldtype': 'Data',
		'fieldname': 'rejection',
		'width': 75,
	}
	]

	hours_columns = []
	delay_reasons = []
	if hours_list:
		delay_reasons = frappe.db.sql_list("""select distinct delay_reasons
			from `tabIdeal Details` where parent in (%s) order by delay_reasons""" %
			', '.join(['%s']*len(hours_list)), tuple([id.name for id in hours_list]))

	for ide in delay_reasons:
		if ide in delay_reasons:
			hours_columns.append({
				"label": ide,
				"fieldname": ide,
				"fieldtype": "Data",
				"width": 120
			})

	columns = columns + hours_columns
	return columns, delay_reasons


def get_conditions(filters):
	conditions = ""
	#if filters.get("from_date"): conditions += " and op.posting_date >= %(from_date)s"
	if filters.get("posting_date"): conditions += " and op.posting_date = %(posting_date)s"
	if filters.get("shift_type"): conditions += " and op.shift_type = %(shift_type)s"
	return conditions

def get_hours(filters, additional_query_columns):
	if additional_query_columns:
		additional_query_columns = ', ' + ', '.join(additional_query_columns)

	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
			op.name , op.posting_date, op.workstation,op.shift_type,op.operator_name,od.item_code, sum(od.completed_qty) as completed_qty, sum(od.rejected_qty) as rejected_qty, sum(od.planned_qty) as planned_qty,
			op.operation, format((sum(od.completed_qty)/sum(od.planned_qty) * 100),2) as efficiency, format((sum(od.rejected_qty) /sum(od.completed_qty) * 100),2) as rejection,
			od.avg_total_ideal_time/60 as loss_hours, group_concat(distinct od.employee_name) as employee_name, od.item_name
		FROM
			`tabOperator Entry` op, `tabOperation Details` od
		WHERE
			od.parent = op.name and op.docstatus = 1 and op.operation = "MACHINING" %s
		GROUP BY
			op.name,od.item_code""".format(additional_query_columns or '') %
		conditions, filters, as_dict=1)

def get_hours_map(hours_list):
	ideal_details = frappe.db.sql("""select parent, delay_reasons, format(sum(hours_ideal/ 60),2) as hours_ideal, item,
		format(sum(avg_hours_ideal/ 60),2) as avg_hours_ideal
		from `tabIdeal Details` where parent in (%s) group by parent, item,delay_reasons"""%
		', '.join(['%s']*len(hours_list)), tuple([id.name for id in hours_list]), as_dict=1)

	hours_map = {}
	for d in ideal_details:
		hours_map.setdefault(d.parent, frappe._dict()).setdefault(d.delay_reasons, [])
		hours_map[d.parent][d.delay_reasons] = flt(d.avg_hours_ideal)

	return hours_map
