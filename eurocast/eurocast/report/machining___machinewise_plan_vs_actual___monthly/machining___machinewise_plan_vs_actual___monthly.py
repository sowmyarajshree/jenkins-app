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
			"item_code": d.item_code,
			"item_name": d.item_name,
			"one":d.one,
			"two":d.two,
			"three":d.three,
			"four":d.four,
			"five":d.five,
			"six":d.six,
			"seven":d.seven,
			"eight":d.eight,
			"nine":d.nine,
			"ten":d.ten,
			"eleven":d.eleven,
			"twelve":d.twelve,
			"thirteen":d.thirteen,
			"fourteen":d.fourteen,
			"fifteen":d.fifteen,
			"sixteen": d.sixteen,
			"seventeen": d.seventeen,
			"eighteen": d.eighteen,
			"nineteen": d.nineteen,
			"twenty":d.twenty,
			"twenty_one": d.twenty_one,
			"twenty_two": d.twenty_two,
			"twenty_three": d.twenty_three,
			"twenty_four": d.twenty_four,
			"twenty_five": d.twenty_five,
			"twenty_six": d.twenty_six,
			"twenty_seven": d.twenty_seven,
			"twenty_eight": d.twenty_eight,
			"twenty_nine": d.twenty_nine,
			"thirty": d.thirty,
			"thirty_one": d.thirty_one,
			"total": d.total,
			"shots": d.shots
		})

		data.append(row)

	return columns, data

def get_columns(filters):
	columns = [{
		'label': _('Item Code'),
		'fieldtype': 'Data',
		'fieldname': 'item_code',
		'width': 150,
		},
		{
		'label': _('Item Name'),
		'fieldtype': 'Data',
		'fieldname': 'item_name',
		'width': 150,
		},
		{
			'label': _('Qty'),
			'fieldtype': 'Data',
			'fieldname': 'shots',
			'width': 100,
		},
		{
			'label': _('1'),
			'fieldtype': 'Float',
			'fieldname': 'one',
			'width': 100,
		},
		{
			'label': _('2'),
			'fieldtype': 'Float',
			'fieldname': 'two',
			'width': 100,
		},
		{
			'label': _('3'),
			'fieldtype': 'Float',
			'fieldname': 'three',
			'width': 100,
		},
		{
			'label': _('4'),
			'fieldtype': 'Float',
			'fieldname': 'four',
			'width': 100,
		},
		{
			'label': _('5'),
			'fieldtype': 'Float',
			'fieldname': 'five',
			'width': 100,
		},
		{
			'label': _('6'),
			'fieldtype': 'Float',
			'fieldname': 'six',
			'width': 100,
		},
		{
			'label': _('7'),
			'fieldtype': 'Float',
			'fieldname': 'seven',
			'width': 100,
		},
		{
			'label': _('8'),
			'fieldtype': 'Float',
			'fieldname': 'eight',
			'width': 100,
		},
		{
			'label': _('9'),
			'fieldtype': 'Float',
			'fieldname': 'nine',
			'width': 100,
		},
		{
			'label': _('10'),
			'fieldtype': 'Float',
			'fieldname': 'ten',
			'width': 100,
		},
		{
			'label': _('11'),
			'fieldtype': 'Float',
			'fieldname': 'eleven',
			'width': 100,
		},
		{
			'label': _('12'),
			'fieldtype': 'Float',
			'fieldname': 'twelve',
			'width': 100,
		},
		{
			'label': _('13'),
			'fieldtype': 'Float',
			'fieldname': 'thirteen',
			'width': 100,
		},
		{
			'label': _('14'),
			'fieldtype': 'Float',
			'fieldname': 'fourteen',
			'width': 100,
		},
		{
			'label': _('15'),
			'fieldtype': 'Float',
			'fieldname': 'fifteen',
			'width': 100,
		},
		{
			'label': _('16'),
			'fieldtype': 'Float',
			'fieldname': 'sixteen',
			'width': 100,
		},
		{
			'label': _('17'),
			'fieldtype': 'Float',
			'fieldname': 'seventeen',
			'width': 100,
		},
		{
			'label': _('18'),
			'fieldtype': 'Float',
			'fieldname': 'eighteen',
			'width': 100,
		},
		{
			'label': _('19'),
			'fieldtype': 'Float',
			'fieldname': 'nineteen',
			'width': 100,
		},
		{
			'label': _('20'),
			'fieldtype': 'Float',
			'fieldname': 'twenty',
			'width': 100,
		},
		{
			'label': _('21'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_one',
			'width': 100,
		},
		{
			'label': _('22'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_two',
			'width': 100,
		},
		{
			'label': _('23'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_three',
			'width': 100,
		},
		{
			'label': _('24'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_four',
			'width': 100,
		},
		{
			'label': _('25'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_five',
			'width': 100,
		},
		{
			'label': _('26'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_six',
			'width': 100,
		},
		{
			'label': _('27'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_seven',
			'width': 100,
		},
		{
			'label': _('28'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_eight',
			'width': 100,
		},
		{
			'label': _('29'),
			'fieldtype': 'Float',
			'fieldname': 'twenty_nine',
			'width': 100,
		},
		{
			'label': _('30'),
			'fieldtype': 'Float',
			'fieldname': 'thirty',
			'width': 100,
		},
		{
			'label': _('31'),
			'fieldtype': 'Float',
			'fieldname': 'thirty_one',
			'width': 100,
		},
		{
			'label': _('Total'),
			'fieldtype': 'Float',
			'fieldname': 'total',
			'width': 100,
		}

	]

	return columns

def get_conditions(filters):
	conditions = "1=1"
	if filters.get("workstation"): conditions += " and ode.workstation = %(workstation)s"
	if filters.get("month"): conditions += " and month(ode.posting_date) = %(month)s"
	if filters.get("year"): conditions += " and year(ode.posting_date) = %(year)s"
	return conditions


def get_hours(filters):

	conditions = get_conditions(filters)

	return frappe.db.sql("""select ode.item_code as item_code,ode.item_name as item_name,
						sum(case when day(ode.posting_date) = 1 then ode.completed_qty else 0 end) as one,
						sum(case when day(ode.posting_date) = 2 then ode.completed_qty else 0 end) as two,
						sum(case when day(ode.posting_date) = 3 then ode.completed_qty else 0 end) as three,
						sum(case when day(ode.posting_date) = 4 then ode.completed_qty else 0 end) as four,
						sum(case when day(ode.posting_date) = 5 then ode.completed_qty else 0 end) as five,
						sum(case when day(ode.posting_date) = 6 then ode.completed_qty else 0 end) as six,
						sum(case when day(ode.posting_date) = 7 then ode.completed_qty else 0 end) as seven,
						sum(case when day(ode.posting_date) = 8 then ode.completed_qty else 0 end) as eight,
						sum(case when day(ode.posting_date) = 9 then ode.completed_qty else 0 end) as nine,
						sum(case when day(ode.posting_date) = 10 then ode.completed_qty else 0 end) as ten,
						sum(case when day(ode.posting_date) = 11 then ode.completed_qty else 0 end) as eleven,
						sum(case when day(ode.posting_date) = 12 then ode.completed_qty else 0 end) as twelve,
						sum(case when day(ode.posting_date) = 13 then ode.completed_qty else 0 end) as thirteen,
						sum(case when day(ode.posting_date) = 14 then ode.completed_qty else 0 end) as fourteen,
						sum(case when day(ode.posting_date) = 15 then ode.completed_qty else 0 end) as fifteen,
						sum(case when day(ode.posting_date) = 16 then ode.completed_qty else 0 end) as sixteen,
						sum(case when day(ode.posting_date) = 17 then ode.completed_qty else 0 end) as seventeen,
						sum(case when day(ode.posting_date) = 18 then ode.completed_qty else 0 end) as eighteen,
						sum(case when day(ode.posting_date) = 19 then ode.completed_qty else 0 end) as nineteen,
						sum(case when day(ode.posting_date) = 20 then ode.completed_qty else 0 end) as twenty,
						sum(case when day(ode.posting_date) = 21 then ode.completed_qty else 0 end) as twenty_one,
						sum(case when day(ode.posting_date) = 22 then ode.completed_qty else 0 end) as twenty_two,
						sum(case when day(ode.posting_date) = 23 then ode.completed_qty else 0 end) as twenty_three,
						sum(case when day(ode.posting_date) = 24 then ode.completed_qty else 0 end) as twenty_four,
						sum(case when day(ode.posting_date) = 25 then ode.completed_qty else 0 end) as twenty_five,
						sum(case when day(ode.posting_date) = 26 then ode.completed_qty else 0 end) as twenty_six,
						sum(case when day(ode.posting_date) = 27 then ode.completed_qty else 0 end) as twenty_seven,
						sum(case when day(ode.posting_date) = 28 then ode.completed_qty else 0 end) as twenty_eight,
						sum(case when day(ode.posting_date) = 29 then ode.completed_qty else 0 end) as twenty_nine,
						sum(case when day(ode.posting_date) = 30 then ode.completed_qty else 0 end) as thirty,
						sum(case when day(ode.posting_date) = 31 then ode.completed_qty else 0 end) as thirty_one,
						sum(case when day(ode.posting_date) = 1 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 2 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 3 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 4 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 5 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 6 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 7 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 8 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 9 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 10 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 11 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 12 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 13 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 14 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 15 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 16 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 17 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 18 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 19 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 20 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 21 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 22 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 23 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 24 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 25 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 26 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 27 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 28 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 29 then ode.completed_qty else 0 end) +
						sum(case when day(ode.posting_date) = 30 then ode.completed_qty else 0 end)+
						sum(case when day(ode.posting_date) = 31 then ode.completed_qty else 0 end) as total,
	 					case when ode.completed_qty >= 0 then 'PR' else 0 end as shots
	   from         `tabOperation Details` ode
	    where       ode.wip_warehouse = "Machining Store - ECE" and ode.operation = "MACHINING"
		  and day(ode.posting_date) in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
		  ,21,22,23,24,25,26,27,28,29,30,31) and {conditions}
		  group by  ode.item_code
		  union all
					select
					    ode.item_code as item_code,ode.item_name as item_name,
						sum(case when day(ode.posting_date) = 1 then ode.planned_qty else 0 end) as one,
						sum(case when day(ode.posting_date) = 2 then ode.planned_qty else 0 end) as two,
						sum(case when day(ode.posting_date) = 3 then ode.planned_qty else 0 end) as three,
						sum(case when day(ode.posting_date) = 4 then ode.planned_qty else 0 end) as four,
						sum(case when day(ode.posting_date) = 5 then ode.planned_qty else 0 end) as five,
						sum(case when day(ode.posting_date) = 6 then ode.planned_qty else 0 end) as six,
						sum(case when day(ode.posting_date) = 7 then ode.planned_qty else 0 end) as seven,
						sum(case when day(ode.posting_date) = 8 then ode.planned_qty else 0 end) as eight,
						sum(case when day(ode.posting_date) = 9 then ode.planned_qty else 0 end) as nine,
						sum(case when day(ode.posting_date) = 10 then ode.planned_qty else 0 end) as ten,
						sum(case when day(ode.posting_date) = 11 then ode.planned_qty else 0 end) as eleven,
						sum(case when day(ode.posting_date) = 12 then ode.planned_qty else 0 end) as twelve,
						sum(case when day(ode.posting_date) = 13 then ode.planned_qty else 0 end) as thirteen,
						sum(case when day(ode.posting_date) = 14 then ode.planned_qty else 0 end) as fourteen,
						sum(case when day(ode.posting_date) = 15 then ode.planned_qty else 0 end) as fifteen,
						sum(case when day(ode.posting_date) = 16 then ode.planned_qty else 0 end) as sixteen,
						sum(case when day(ode.posting_date) = 17 then ode.planned_qty else 0 end) as seventeen,
						sum(case when day(ode.posting_date) = 18 then ode.planned_qty else 0 end) as eighteen,
						sum(case when day(ode.posting_date) = 19 then ode.planned_qty else 0 end) as nineteen,
						sum(case when day(ode.posting_date) = 20 then ode.planned_qty else 0 end) as twenty,
						sum(case when day(ode.posting_date) = 21 then ode.planned_qty else 0 end) as twenty_one,
						sum(case when day(ode.posting_date) = 22 then ode.planned_qty else 0 end) as twenty_two,
						sum(case when day(ode.posting_date) = 23 then ode.planned_qty else 0 end) as twenty_three,
						sum(case when day(ode.posting_date) = 24 then ode.planned_qty else 0 end) as twenty_four,
						sum(case when day(ode.posting_date) = 25 then ode.planned_qty else 0 end) as twenty_five,
						sum(case when day(ode.posting_date) = 26 then ode.planned_qty else 0 end) as twenty_six,
						sum(case when day(ode.posting_date) = 27 then ode.planned_qty else 0 end) as twenty_seven,
						sum(case when day(ode.posting_date) = 28 then ode.planned_qty else 0 end) as twenty_eight,
						sum(case when day(ode.posting_date) = 29 then ode.planned_qty else 0 end) as twenty_nine,
						sum(case when day(ode.posting_date) = 30 then ode.planned_qty else 0 end) as thirty,
						sum(case when day(ode.posting_date) = 31 then ode.planned_qty else 0 end) as thirty_one,
						sum(case when day(ode.posting_date) = 1 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 2 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 3 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 4 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 5 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 6 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 7 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 8 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 9 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 10 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 11 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 12 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 13 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 14 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 15 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 16 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 17 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 18 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 19 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 20 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 21 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 22 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 23 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 24 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 25 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 26 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 27 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 28 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 29 then ode.planned_qty else 0 end) +
						sum(case when day(ode.posting_date) = 30 then ode.planned_qty else 0 end)+
						sum(case when day(ode.posting_date) = 31 then ode.planned_qty else 0 end) as total,
						case when ode.planned_qty >= 0 then 'P' else 0 end as shots

					from
					    `tabOperation Details` ode
					where
					    ode.wip_warehouse = "Machining Store - ECE"  and ode.operation = "MACHINING"
						  and day(ode.posting_date) in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
						  ,21,22,23,24,25,26,27,28,29,30,31) and {conditions}
					group by
					    ode.item_code

					union all
					select
					    ode.item_code as item_code,ode.item_name as item_name,
					    sum(case when day(ode.posting_date) = 1 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 1 then ode.rejected_qty else 0 end) as one,
						sum(case when day(ode.posting_date) = 2 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 2 then ode.rejected_qty else 0 end)as two,
						sum(case when day(ode.posting_date) = 3 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 3 then ode.rejected_qty else 0 end) as three,
						sum(case when day(ode.posting_date) = 4 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 4 then ode.rejected_qty else 0 end) as four,
						sum(case when day(ode.posting_date) = 5 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 5 then ode.rejected_qty else 0 end) as five,
						sum(case when day(ode.posting_date) = 6 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 6 then ode.rejected_qty else 0 end) as six,
						sum(case when day(ode.posting_date) = 7 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 7 then ode.rejected_qty else 0 end) as seven,
						sum(case when day(ode.posting_date) = 8 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 8 then ode.rejected_qty else 0 end) as eight,
						sum(case when day(ode.posting_date) = 9 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 9 then ode.rejected_qty else 0 end) as nine,
						sum(case when day(ode.posting_date) = 10 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 10 then ode.rejected_qty else 0 end) as ten,
						sum(case when day(ode.posting_date) = 11 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 11 then ode.rejected_qty else 0 end) as eleven,
						sum(case when day(ode.posting_date) = 12 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 12 then ode.rejected_qty else 0 end) as twelve,
						sum(case when day(ode.posting_date) = 13 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 13 then ode.rejected_qty else 0 end) as thirteen,
						sum(case when day(ode.posting_date) = 14 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 14 then ode.rejected_qty else 0 end) as fourteen,
						sum(case when day(ode.posting_date) = 15 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 15 then ode.rejected_qty else 0 end) as fifteen,
						sum(case when day(ode.posting_date) = 16 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 16 then ode.rejected_qty else 0 end) as sixteen,
						sum(case when day(ode.posting_date) = 17 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 17 then ode.rejected_qty else 0 end) as seventeen,
						sum(case when day(ode.posting_date) = 18 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 18 then ode.rejected_qty else 0 end) as eighteen,
						sum(case when day(ode.posting_date) = 19 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 19 then ode.rejected_qty else 0 end) as nineteen,
						sum(case when day(ode.posting_date) = 20 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 20 then ode.rejected_qty else 0 end) as twenty,
						sum(case when day(ode.posting_date) = 21 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 21 then ode.rejected_qty else 0 end) as twenty_one,
						sum(case when day(ode.posting_date) = 22 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 22 then ode.rejected_qty else 0 end) as twenty_two,
						sum(case when day(ode.posting_date) = 23 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 23 then ode.rejected_qty else 0 end) as twenty_three,
						sum(case when day(ode.posting_date) = 24 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 24 then ode.rejected_qty else 0 end) as twenty_four,
						sum(case when day(ode.posting_date) = 25 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 25 then ode.rejected_qty else 0 end) as twenty_five,
						sum(case when day(ode.posting_date) = 26 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 26 then ode.rejected_qty else 0 end) as twenty_six,
						sum(case when day(ode.posting_date) = 27 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 27 then ode.rejected_qty else 0 end) as twenty_seven,
						sum(case when day(ode.posting_date) = 28 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 28 then ode.rejected_qty else 0 end) as twenty_eight,
						sum(case when day(ode.posting_date) = 29 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 29 then ode.rejected_qty else 0 end) as twenty_nine,
						sum(case when day(ode.posting_date) = 30 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 30 then ode.rejected_qty else 0 end) as thirty,
						sum(case when day(ode.posting_date) = 31 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 31 then ode.rejected_qty else 0 end) as thirty_one,
						(sum(case when day(ode.posting_date) = 1 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 1 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 2 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 2 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 3 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 3 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 4 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 4 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 5 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 5 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 6 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 6 then ode.rejected_qty else 0 end))+
						(sum(case when day(ode.posting_date) = 7 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 7 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 8 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 8 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 9 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 9 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 10 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 10 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 11 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 11 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 12 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 12 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 13 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 13 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 14 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 14 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 15 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 15 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 16 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 16 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 17 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 17 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 18 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 18 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 19 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 19 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 20 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 20 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 21 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 21 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 22 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 22 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 23 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 23 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 24 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 24 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 25 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 25 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 26 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 26 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 27 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 27 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 28 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 28 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 29 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 29 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 30 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 30 then ode.rejected_qty else 0 end)) +
						(sum(case when day(ode.posting_date) = 31 then ode.completed_qty else 0 end) - sum(case when day(ode.posting_date) = 31 then ode.rejected_qty else 0 end)) as total,
						case when ode.rejected_qty >= 0 then 'A' else 0 end as shots


					from
					    `tabOperation Details` ode
					where
					    ode.wip_warehouse = "Machining Store - ECE" and ode.operation = "MACHINING"
						  and day(ode.posting_date) in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
						  ,21,22,23,24,25,26,27,28,29,30,31) and {conditions}
					group by
					    ode.item_code """.format(conditions=conditions),filters,as_dict=1)
