# Copyright (c) 2013, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate, flt
from frappe import _,msgprint

def execute(filters=None,additional_query_columns=None):
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
			"workstation": d.workstation,
			"item_code": d.item_code,
			"completed_qty": d.completed_qty,
			"rejected_qty": d.rejected_qty,
			"planned_qty": d.planned_qty,
			"hour_output": d.hour_output,
			"efficiency": d.efficiency,
			"rejection": d.rejection,
			"loss_hours": d.loss_hours
		})
		for h in delay_reasons:
			hours_ideal = flt(hours_map.get(d.workstation, {}).get(h))
			row.update({
					h: hours_ideal
			})

		data.append(row)
	return columns, data

def get_columns(filters,hours_list):
	columns = [{
		'label': _('Machine'),
		'fieldtype': 'Link',
		'fieldname': 'workstation',
		'width': 100,
		'options':'Workstation',
	},
	{
		'label': _('Item'),
		'fieldtype': 'Data',
		'fieldname': 'item_code',
		'width': 200,
	},
	{
		'label': _('Planned Qty'),
		'fieldtype': 'Float',
		'fieldname': 'planned_qty',
		'width': 100,
	},
	{
		'label': _('Actual Qty'),
		'fieldtype': 'Float',
		'fieldname': 'completed_qty',
		'width': 100,
	},
	{
		'label': _('Rejected Qty'),
		'fieldtype': 'Float',
		'fieldname': 'rejected_qty',
		'width': 100,
	},
	{
		'label': _('Efficiency %'),
		'fieldtype': 'Float',
		'fieldname': 'efficiency',
		'width': 100,
	},
	{
		'label': _('Rejection %'),
		'fieldtype': 'Float',
		'fieldname': 'rejection',
		'width': 100,
	},
	{
		'label': _('Loss Hours'),
		'fieldtype': 'Float',
		'fieldname': 'loss_hours',
		'width': 100,
	}
	]

	hours_columns = []
	delay_reasons = []
	if hours_list:
		delay_reasons = frappe.db.sql_list("""select distinct delay_reasons
			from `tabIdeal Details` where operation = "MACHINING" and posting_date in (%s)
			order by delay_reasons""" %
			', '.join(['%s']*len(hours_list)), tuple([id.posting_date for id in hours_list]))


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

def get_hours(filters, additional_query_columns):
	if additional_query_columns:
		additional_query_columns = ', ' + ', '.join(additional_query_columns)

	conditions = get_conditions(filters)

	return frappe.db.sql("""
		select
		    od.workstation,
		    sum(case when od.posting_date = %(posting_date)s then od.planned_qty else 0 end) as planned_qty,
			sum(case when od.posting_date = %(posting_date)s then od.completed_qty else 0 end) as completed_qty,
			sum(case when od.posting_date = %(posting_date)s then od.rejected_qty else 0 end) as rejected_qty,
			group_concat(distinct od.item_name SEPARATOR '|') as item_code,
			sum(case when od.posting_date = %(posting_date)s then od.completed_qty else 0 end)/sum(case when od.posting_date = %(posting_date)s then od.planned_qty else 0 end) * 100 as efficiency,
			sum(case when od.posting_date = %(posting_date)s then od.rejected_qty else 0 end)/sum(case when od.posting_date = %(posting_date)s then od.completed_qty else 0 end) * 100 as rejection,
			sum(case when od.posting_date = %(posting_date)s then od.avg_total_ideal_time else 0 end)/ 60 as loss_hours,
			od.posting_date
		from
			`tabOperation Details` od left join
			`tabOperator Entry` ode on od.parent = ode.name
		where
		  ode.docstatus = 1 and ode.operation = "MACHINING" and od.wip_warehouse = "Machining Store - ECE" and od.posting_date = %(posting_date)s
		group by
		    od.item_code,od.workstation
		""".format(additional_query_columns or ''),{"posting_date":filters.posting_date},as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("posting_date"):
		conditions +=" and od.posting_date = %(posting_date)s"

	return conditions

def get_hours_map(hours_list):

	for w in hours_list:
		ideal_details = frappe.db.sql("""select delay_reasons, format(sum(hours_ideal)/60,2) as hours_ideal,workstation,posting_date, operation
			from `tabIdeal Details` where operation = "MACHINING" and posting_date = %s
			group by delay_reasons,workstation""",w.posting_date,as_dict=1)
	hours_map = {}
	for d in ideal_details:
		hours_map.setdefault(d.workstation, frappe._dict()).setdefault(d.delay_reasons, [])
		hours_map[d.workstation][d.delay_reasons] = flt(d.hours_ideal)

	return hours_map
