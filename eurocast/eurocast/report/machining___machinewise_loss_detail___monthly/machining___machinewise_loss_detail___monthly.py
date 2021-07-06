# Copyright (c) 2013, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate,cstr, cint, getdate, flt
from frappe import _,msgprint
from calendar import monthrange

def execute(filters=None):
	filters = frappe._dict(filters or {})
	hours_list = get_hours(filters)
	columns = get_columns(filters)

	if not hours_list:
		msgprint(_("No record found"))
		return columns, hours_list

	data = []
	for d in hours_list:
		row = ({
			"day_of_month": d.day_of_month,
			"item_code": d.item_code,
			"item_name": d.item_name,
			"planned_qty": d.planned_qty,
			"completed_qty": d.completed_qty,
			"rejected_qty": d.rejected_qty,
			"rejection": d.rejection,
			"efficiency": d.efficiency,
			"operation_time": d.operation_time,
			"total_ideal_time": d.total_ideal_time,
			"cum_plan_shots": d.cum_plan_shots,
			"cum_act_shots": d.cum_act_shots,
			"cum_rej_shots": d.cum_rej_shots,
			"cum_down_hrs": d.cum_down_hrs,
			"cum_run_hrs": d.cum_run_hrs
		})

		data.append(row)

	return columns, data

def get_columns(filters):
	columns = [{
		'label': _('Days'),
		'fieldtype': 'Data',
		'fieldname': 'day_of_month',
		'width': 100,
		},
		{
		'label': _('Item Code'),
		'fieldtype': 'Link',
		'fieldname': 'item_code',
		'width': 100,
		'options': 'Item',
		},
		{
		'label': _('Item Name'),
		'fieldtype': 'Data',
		'fieldname': 'item_name',
		'width': 100,
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
			'label': _('Rejection Qty'),
			'fieldtype': 'Float',
			'fieldname': 'rejected_qty',
			'width': 100,
		},
		{
			'label': _('Rejection %'),
			'fieldtype': 'Float',
			'fieldname': 'rejection',
			'width': 100,
		},
		{
			'label': _('Efficiency %'),
			'fieldtype': 'Float',
			'fieldname': 'efficiency',
			'width': 100,
		},
		{
			'label': _('Running Hrs'),
			'fieldtype': 'Float',
			'fieldname': 'operation_time',
			'width': 100,
		},
		{
			'label': _('Downtime Hrs'),
			'fieldtype': 'Float',
			'fieldname': 'total_ideal_time',
			'width': 100,
		},
		{
			'label': _('Cumulative Planned Shots'),
			'fieldtype': 'Float',
			'fieldname': 'cum_plan_shots',
			'width': 100,
		},
		{
			'label': _('Cumulative Actual Shots'),
			'fieldtype': 'Float',
			'fieldname': 'cum_act_shots',
			'width': 100,
		},
		{
			'label': _('Cumulative Rejected Shots'),
			'fieldtype': 'Float',
			'fieldname': 'cum_rej_shots',
			'width': 100,
		},
		{
			'label': _('Cumulative Running Hrs'),
			'fieldtype': 'Float',
			'fieldname': 'cum_run_hrs',
			'width': 100,
		},
		{
			'label': _('Cumulative Downtime Hrs'),
			'fieldtype': 'Float',
			'fieldname': 'cum_down_hrs',
			'width': 100,
		}

	]

	return columns

def get_conditions(filters):
	if not (filters.get("month") and filters.get("year")):
		msgprint(_("Please select month and year"), raise_exception=1)
	filters["total_days_in_month"] = monthrange(cint(filters.year), cint(filters.month))[1]
	conditions = ""
	if filters.get("to_date"):
		conditions +=" and id.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and id.posting_date >= %(from_date)s"
	if filters.get("workstation"):
		conditions +=" and id.workstation >= %(workstation)s"
	conditions = " and month(id.posting_date) = %(month)s and year(id.posting_date) = %(year)s"

	return conditions


def get_hours(filters):

	return frappe.db.sql("""with cte as (select day(id.posting_date) as day_of_month,id.posting_date, id.workstation, group_concat(distinct id.item_code) as item_code,group_concat(distinct id.item_name) as item_name,
				sum(case when day(id.posting_date) = 1 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 2 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 3 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 4 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 5 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 6 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 7 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 8 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 9 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 10 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 11 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 12 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 13 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 14 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 15 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 16 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 17 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 18 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 19 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 20 then id.planned_qty else 0 end)+
				sum(case when day(id.posting_date) = 21 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 22 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 23 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 24 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 25 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 26 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 27 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 28 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 29 then id.planned_qty else 0 end) + sum(case when day(id.posting_date) = 30 then id.planned_qty else 0 end) +
				sum(case when day(id.posting_date) = 31 then id.planned_qty else 0 end) as planned_qty,
				sum(case when day(id.posting_date) = 1 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 2 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 3 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 4 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 5 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 6 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 7 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 8 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 9 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 10 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 11 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 12 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 13 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 14 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 15 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 16 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 17 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 18 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 19 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 20 then id.rejected_qty else 0 end)+
				sum(case when day(id.posting_date) = 21 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 22 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 23 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 24 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 25 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 26 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 27 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 28 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 29 then id.rejected_qty else 0 end) + sum(case when day(id.posting_date) = 30 then id.rejected_qty else 0 end) +
				sum(case when day(id.posting_date) = 31 then id.rejected_qty else 0 end) as rejected_qty,
				sum(case when day(id.posting_date) = 1 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 2 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 3 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 4 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 5 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 6 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 7 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 8 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 9 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 10 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 11 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 12 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 13 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 14 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 15 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 16 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 17 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 18 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 19 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 20 then id.completed_qty else 0 end)+
				sum(case when day(id.posting_date) = 21 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 22 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 23 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 24 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 25 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 26 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 27 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 28 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 29 then id.completed_qty else 0 end) + sum(case when day(id.posting_date) = 30 then id.completed_qty else 0 end) +
				sum(case when day(id.posting_date) = 31 then id.completed_qty else 0 end) as completed_qty,
				sum(case when day(id.posting_date) = 1 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 2 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 3 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 4 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 5 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 6 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 7 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 8 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 9 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 10 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 11 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 12 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 13 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 14 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 15 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 16 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 17 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 18 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 19 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 20 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 21 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 22 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 23 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 24 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 25 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 26 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 27 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 28 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 29 then id.avg_consumed_time else 0 end)/60 + sum(case when day(id.posting_date) = 30 then id.avg_consumed_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 31 then id.avg_consumed_time else 0 end) as operation_time,
				sum(case when day(id.posting_date) = 1 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 2 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 3 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 4 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 5 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 6 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 7 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 8 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 9 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 10 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 11 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 12 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 13 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 14 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 15 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 16 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 17 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 18 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 19 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 20 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 21 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 22 then id.avg_total_ideal_time else 0 end)/60  +
				sum(case when day(id.posting_date) = 23 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 24 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 25 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 26 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 27 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 28 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 29 then id.avg_total_ideal_time else 0 end)/60 + sum(case when day(id.posting_date) = 30 then id.avg_total_ideal_time else 0 end)/60 +
				sum(case when day(id.posting_date) = 31 then id.avg_total_ideal_time else 0 end) as total_ideal_time,
				sum(case when day(id.posting_date) = 1 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 2 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 3 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 4 then id.efficiency_others else 0 end)+
				sum(case when day(id.posting_date) = 5 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 6 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 7 then id.efficiency_others else 0 end)+
				sum(case when day(id.posting_date) = 8 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 9 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 10 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 11 then id.efficiency_others else 0 end)+
				sum(case when day(id.posting_date) = 12 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 13 then id.efficiency_others else 0 end)+
				sum(case when day(id.posting_date) = 14 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 15 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 16 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 17 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 18 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 19 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 20 then id.efficiency_others else 0 end)+
				sum(case when day(id.posting_date) = 21 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 22 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 23 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 24 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 25 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 26 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 27 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 28 then id.efficiency_others else 0 end)+
				sum(case when day(id.posting_date) = 29 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 30 then id.efficiency_others else 0 end) +
				sum(case when day(id.posting_date) = 31 then id.efficiency_others else 0 end) as efficiency,
				sum(case when day(id.posting_date) = 1 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 2 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 3 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 4 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 5 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 6 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 7 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 8 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 9 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 10 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 11 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 12 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 13 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 14 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 15 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 16 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 17 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 18 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 19 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 20 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 21 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 22 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 23 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 24 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 25 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 26 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 27 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 28 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 29 then id.rejection_others else 0 end) +
				sum(case when day(id.posting_date) = 30 then id.rejection_others else 0 end)+
				sum(case when day(id.posting_date) = 31 then id.rejection_others else 0 end) as rejection
				from `tabOperation Details` id
				where id.operation = "MACHINING" and id.workstation = %(workstation)s and
					month(id.posting_date) = %(month)s and
					year(id.posting_date) = %(year)s
		 		group by
					id.posting_date)
				select
					day_of_month, item_code,planned_qty, rejected_qty, completed_qty, efficiency, rejection, operation_time, total_ideal_time, item_name,
					sum(planned_qty) over(order by day_of_month) as cum_plan_shots,
					sum(completed_qty) over(order by day_of_month) as cum_act_shots,
					sum(rejected_qty) over(order by day_of_month) as cum_rej_shots,
					sum(operation_time) over(order by day_of_month) as cum_run_hrs,
					sum(total_ideal_time) over(order by day_of_month) as cum_down_hrs
				from cte
				order by
					day_of_month""",{"month":filters.month,"year":filters.year,"workstation":filters.workstation},as_dict=1)
