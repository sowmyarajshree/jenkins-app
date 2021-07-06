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
			"customer": d.customer,
			"item_code": d.item_code,
			"scheduled_qty": d.scheduled_qty,
			"planned_qty": d.planned_qty,
			"actual_qty": d.actual_qty,
			"cum_plan_qty": d.cum_plan_qty,
			"cum_actual_qty": d.cum_actual_qty
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
		'label': _('Customer'),
		'fieldtype': 'Link',
		'fieldname': 'customer',
		'width': 100,
		'options': 'Customer',
		},
		{
		'label': _('Item Code'),
		'fieldtype': 'Link',
		'fieldname': 'item_code',
		'width': 100,
		'options': 'Item',
		},
		{
			'label': _('Scheduled Qty'),
			'fieldtype': 'Float',
			'fieldname': 'scheduled_qty',
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
			'fieldname': 'actual_qty',
			'width': 100,
		},
		{
			'label': _('Cumulative Planned Qty'),
			'fieldtype': 'Float',
			'fieldname': 'cum_plan_qty',
			'width': 100,
		},
		{
			'label': _('Cumulative Actual Qty'),
			'fieldtype': 'Float',
			'fieldname': 'cum_actual_qty',
			'width': 100,
		}

	]

	return columns


def get_hours(filters):

	return frappe.db.sql("""with cte as (select day(id.posting_date) as day_of_month,id.posting_date, id.item_code as item_code,
				id.customer as customer,id.month as month, id.year as year,
				sum(case when day(id.posting_date) = 1 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 2 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 3 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 4 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 5 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 6 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 7 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 8 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 9 then id.scheduled_qty else 0 end)+ sum(case when day(id.posting_date) = 10 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 11 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 12 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 13 then id.scheduled_qty else 0 end)+ sum(case when day(id.posting_date) = 14 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 15 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 16 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 17 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 18 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 19 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 20 then id.scheduled_qty else 0 end)+
				sum(case when day(id.posting_date) = 21 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 22 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 23 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 24 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 25 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 26 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 27 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 28 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 29 then id.scheduled_qty else 0 end) + sum(case when day(id.posting_date) = 30 then id.scheduled_qty else 0 end) +
				sum(case when day(id.posting_date) = 31 then id.scheduled_qty else 0 end) as scheduled_qty,
				sum(case when day(id.posting_date) = 1 then id.qty else 0 end) + sum(case when day(id.posting_date) = 2 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 3 then id.qty else 0 end) + sum(case when day(id.posting_date) = 4 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 5 then id.qty else 0 end) + sum(case when day(id.posting_date) = 6 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 7 then id.qty else 0 end) + sum(case when day(id.posting_date) = 8 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 9 then id.qty else 0 end)+ sum(case when day(id.posting_date) = 10 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 11 then id.qty else 0 end) + sum(case when day(id.posting_date) = 12 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 13 then id.qty else 0 end)+ sum(case when day(id.posting_date) = 14 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 15 then id.qty else 0 end) + sum(case when day(id.posting_date) = 16 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 17 then id.qty else 0 end) + sum(case when day(id.posting_date) = 18 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 19 then id.qty else 0 end) + sum(case when day(id.posting_date) = 20 then id.qty else 0 end)+
				sum(case when day(id.posting_date) = 21 then id.qty else 0 end) + sum(case when day(id.posting_date) = 22 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 23 then id.qty else 0 end) + sum(case when day(id.posting_date) = 24 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 25 then id.qty else 0 end) + sum(case when day(id.posting_date) = 26 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 27 then id.qty else 0 end) + sum(case when day(id.posting_date) = 28 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 29 then id.qty else 0 end) + sum(case when day(id.posting_date) = 30 then id.qty else 0 end) +
				sum(case when day(id.posting_date) = 31 then id.qty else 0 end) as planned_qty,
				sum(case when day(si.posting_date) = 1 then si.qty else 0 end) + sum(case when day(si.posting_date) = 2 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 3 then si.qty else 0 end) + sum(case when day(si.posting_date) = 4 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 5 then si.qty else 0 end) + sum(case when day(si.posting_date) = 6 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 7 then si.qty else 0 end) + sum(case when day(si.posting_date) = 8 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 9 then si.qty else 0 end)+ sum(case when day(si.posting_date) = 10 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 11 then si.qty else 0 end) + sum(case when day(si.posting_date) = 12 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 13 then si.qty else 0 end)+ sum(case when day(si.posting_date) = 14 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 15 then si.qty else 0 end) + sum(case when day(si.posting_date) = 16 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 17 then si.qty else 0 end) + sum(case when day(si.posting_date) = 18 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 19 then si.qty else 0 end) + sum(case when day(si.posting_date) = 20 then si.qty else 0 end)+
				sum(case when day(si.posting_date) = 21 then si.qty else 0 end) + sum(case when day(si.posting_date) = 22 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 23 then si.qty else 0 end) + sum(case when day(si.posting_date) = 24 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 25 then si.qty else 0 end) + sum(case when day(si.posting_date) = 26 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 27 then si.qty else 0 end) + sum(case when day(si.posting_date) = 28 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 29 then si.qty else 0 end) + sum(case when day(si.posting_date) = 30 then si.qty else 0 end) +
				sum(case when day(si.posting_date) = 31 then si.qty else 0 end) as actual_qty
				from
					`tabSales Plan Ledger Entry` id left join
					`tabSales Invoice Item` si
					on id.item_code = si.item_code
				where
				 	id.month =  %(month)s and id.year = %(year)s
					and id.customer = si.customer
					and id.posting_date = si.posting_date
		 		group by
					id.item_code, id.posting_date)
				select
					day_of_month, item_code, scheduled_qty, planned_qty,customer, actual_qty,
					sum(planned_qty) over(order by day_of_month) as cum_plan_qty,
					sum(actual_qty) over(order by day_of_month) as cum_actual_qty
				from cte
				order by
					day_of_month""",{"month":filters.month,"year":filters.year},as_dict=1)
