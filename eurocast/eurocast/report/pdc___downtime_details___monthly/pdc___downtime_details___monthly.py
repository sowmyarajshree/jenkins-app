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
			"delay_reasons": d.delay_reasons,
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
			"total": d.total
		})

		data.append(row)

	return columns, data

def get_columns(filters):
	columns = [{
		'label': _('Delay Reasons'),
		'fieldtype': 'Data',
		'fieldname': 'delay_reasons',
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
			'fieldtype': 'Data',
			'fieldname': 'thirty',
			'width': 100,
		},
		{
			'label': _('31'),
			'fieldtype': 'Data',
			'fieldname': 'thirty_one',
			'width': 100,
		},
		{
			'label': _('Total'),
			'fieldtype': 'Data',
			'fieldname': 'total',
			'width': 100,
		}

	]

	return columns

def get_conditions(filters):
	conditions = "1=1"
	if filters.get("workstation"): conditions += " and id.workstation = %(workstation)s"
	if filters.get("month"): conditions += " and month(id.posting_date) = %(month)s"
	if filters.get("year"): conditions += " and year(id.posting_date) = %(year)s"
	return conditions


def get_hours(filters):

	conditions = get_conditions(filters)

	return frappe.db.sql("""select day(id.posting_date) as day_of_month, id.delay_reasons,id.posting_date, id.workstation,
				sum(case when day(id.posting_date) = 1 then id.hours_ideal else 0 end)/60 as one,
				sum(case when day(id.posting_date) = 2 then id.hours_ideal else 0 end)/60 as two,
				sum(case when day(id.posting_date) = 3 then id.hours_ideal else 0 end)/60 as three,
				sum(case when day(id.posting_date) = 4 then id.hours_ideal else 0 end)/60 as four,
				sum(case when day(id.posting_date) = 5 then id.hours_ideal else 0 end)/60 as five,
				sum(case when day(id.posting_date) = 6 then id.hours_ideal else 0 end)/60 as six,
				sum(case when day(id.posting_date) = 7 then id.hours_ideal else 0 end)/60 as seven,
				sum(case when day(id.posting_date) = 8 then id.hours_ideal else 0 end)/60 as eight,
				sum(case when day(id.posting_date) = 9 then id.hours_ideal else 0 end)/60 as nine,
				sum(case when day(id.posting_date) = 10 then id.hours_ideal else 0 end)/60 as ten,
				sum(case when day(id.posting_date) = 11 then id.hours_ideal else 0 end)/60 as eleven,
				sum(case when day(id.posting_date) = 12 then id.hours_ideal else 0 end)/60 as twelve,
				sum(case when day(id.posting_date) = 13 then id.hours_ideal else 0 end)/60 as thirteen,
				sum(case when day(id.posting_date) = 14 then id.hours_ideal else 0 end)/60 as fourteen,
				sum(case when day(id.posting_date) = 15 then id.hours_ideal else 0 end)/60 as fifteen,
				sum(case when day(id.posting_date) = 16 then id.hours_ideal else 0 end)/60 as sixteen,
				sum(case when day(id.posting_date) = 17 then id.hours_ideal else 0 end)/60 as seventeen,
				sum(case when day(id.posting_date) = 18 then id.hours_ideal else 0 end)/60 as eighteen,
				sum(case when day(id.posting_date) = 19 then id.hours_ideal else 0 end)/60 as nineteen,
				sum(case when day(id.posting_date) = 20 then id.hours_ideal else 0 end)/60 as twenty,
				sum(case when day(id.posting_date) = 21 then id.hours_ideal else 0 end)/60 as twenty_one,
				sum(case when day(id.posting_date) = 22 then id.hours_ideal else 0 end)/60 as twenty_two,
				sum(case when day(id.posting_date) = 23 then id.hours_ideal else 0 end)/60 as twenty_three,
				sum(case when day(id.posting_date) = 24 then id.hours_ideal else 0 end)/60 as twenty_four,
				sum(case when day(id.posting_date) = 25 then id.hours_ideal else 0 end)/60 as twenty_five,
				sum(case when day(id.posting_date) = 26 then id.hours_ideal else 0 end)/60 as twenty_six,
				sum(case when day(id.posting_date) = 27 then id.hours_ideal else 0 end)/60 as twenty_seven,
				sum(case when day(id.posting_date) = 28 then id.hours_ideal else 0 end)/60 as twenty_eight,
				sum(case when day(id.posting_date) = 29 then id.hours_ideal else 0 end)/60 as twenty_nine,
				sum(case when day(id.posting_date) = 30 then id.hours_ideal else 0 end)/60 as thirty,
				sum(case when day(id.posting_date) = 31 then id.hours_ideal else 0 end)/60 as thirty_one,
				sum(case when day(id.posting_date) = 1 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 2 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 3 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 4 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 5 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 6 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 7 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 8 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 9 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 10 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 11 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 12 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 13 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 14 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 15 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 16 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 17 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 18 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 19 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 20 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 21 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 22 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 23 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 24 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 25 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 26 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 27 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 28 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 29 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 30 then id.hours_ideal else 0 end)/60 +
				sum(case when day(id.posting_date) = 31 then id.hours_ideal else 0 end)/60 as total
				from `tabIdeal Details Entry` id
				where id.operation = "PDC" and
				day(id.posting_date) in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
				  ,21,22,23,24,25,26,27,28,29,30,31) and {conditions}
		 		group by
					id.delay_reasons""".format(conditions=conditions),filters,as_dict=1)
