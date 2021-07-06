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
			"d1":d.d1,
			"d2":d.d2,
			"d3":d.d3,
			"d4":d.d4,
			"d5":d.d5,
			"d6":d.d6,
			"d7":d.d7,
			"d8":d.d8,
			"d9":d.d9,
			"d10":d.d10,
			"d11":d.d11,
			"d12":d.d12,
			"d13":d.d13,
			"d14":d.d14,
			"d15":d.d15,
			"d16": d.d16,
			"d17": d.d17,
			"d18": d.d18,
			"d19": d.d19,
			"d20":d.d20,
			"d21": d.d21,
			"d22": d.d22,
			"d23": d.d23,
			"d24": d.d24,
			"d25": d.d25,
			"d26": d.d26,
			"d27": d.d27,
			"d28": d.d28,
			"d29": d.d29,
			"d30": d.d30,
			"d31": d.d31,
			"total": d.total,
			"qty": d.qty,
			"customer": d.customer,
			"item_name": d.item_name
		})

		data.append(row)

	return columns, data

def get_columns(filters):
	columns = [{
		'label': _('Customer'),
		'fieldtype': 'Link',
		'fieldname': 'customer',
		'options': 'Customer',
		'width': 150,
		},
		{
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
			'fieldname': 'qty',
			'width': 100,
		},
		{
			'label': _('1'),
			'fieldtype': 'Data',
			'fieldname': 'd1',
			'width': 100,
		},
		{
			'label': _('2'),
			'fieldtype': 'Data',
			'fieldname': 'd2',
			'width': 100,
		},
		{
			'label': _('3'),
			'fieldtype': 'Data',
			'fieldname': 'd3',
			'width': 100,
		},
		{
			'label': _('4'),
			'fieldtype': 'Data',
			'fieldname': 'd4',
			'width': 100,
		},
		{
			'label': _('5'),
			'fieldtype': 'Data',
			'fieldname': 'd5',
			'width': 100,
		},
		{
			'label': _('6'),
			'fieldtype': 'Data',
			'fieldname': 'd6',
			'width': 100,
		},
		{
			'label': _('7'),
			'fieldtype': 'Data',
			'fieldname': 'd7',
			'width': 100,
		},
		{
			'label': _('8'),
			'fieldtype': 'Data',
			'fieldname': 'd8',
			'width': 100,
		},
		{
			'label': _('9'),
			'fieldtype': 'Data',
			'fieldname': 'd9',
			'width': 100,
		},
		{
			'label': _('10'),
			'fieldtype': 'Data',
			'fieldname': 'd10',
			'width': 100,
		},
		{
			'label': _('11'),
			'fieldtype': 'Data',
			'fieldname': 'd11',
			'width': 100,
		},
		{
			'label': _('12'),
			'fieldtype': 'Data',
			'fieldname': 'd12',
			'width': 100,
		},
		{
			'label': _('13'),
			'fieldtype': 'Data',
			'fieldname': 'd13',
			'width': 100,
		},
		{
			'label': _('14'),
			'fieldtype': 'Data',
			'fieldname': 'd14',
			'width': 100,
		},
		{
			'label': _('15'),
			'fieldtype': 'Data',
			'fieldname': 'd15',
			'width': 100,
		},
		{
			'label': _('16'),
			'fieldtype': 'Data',
			'fieldname': 'd16',
			'width': 100,
		},
		{
			'label': _('17'),
			'fieldtype': 'Data',
			'fieldname': 'd17',
			'width': 100,
		},
		{
			'label': _('18'),
			'fieldtype': 'Data',
			'fieldname': 'd18',
			'width': 100,
		},
		{
			'label': _('19'),
			'fieldtype': 'Data',
			'fieldname': 'd19',
			'width': 100,
		},
		{
			'label': _('20'),
			'fieldtype': 'Data',
			'fieldname': 'd20',
			'width': 100,
		},
		{
			'label': _('21'),
			'fieldtype': 'Data',
			'fieldname': 'd21',
			'width': 100,
		},
		{
			'label': _('22'),
			'fieldtype': 'Data',
			'fieldname': 'd22',
			'width': 100,
		},
		{
			'label': _('23'),
			'fieldtype': 'Data',
			'fieldname': 'd23',
			'width': 100,
		},
		{
			'label': _('24'),
			'fieldtype': 'Data',
			'fieldname': 'd24',
			'width': 100,
		},
		{
			'label': _('25'),
			'fieldtype': 'Data',
			'fieldname': 'd25',
			'width': 100,
		},
		{
			'label': _('26'),
			'fieldtype': 'Data',
			'fieldname': 'd26',
			'width': 100,
		},
		{
			'label': _('27'),
			'fieldtype': 'Data',
			'fieldname': 'd27',
			'width': 100,
		},
		{
			'label': _('28'),
			'fieldtype': 'Data',
			'fieldname': 'd28',
			'width': 100,
		},
		{
			'label': _('29'),
			'fieldtype': 'Data',
			'fieldname': 'd29',
			'width': 100,
		},
		{
			'label': _('30'),
			'fieldtype': 'Data',
			'fieldname': 'd30',
			'width': 100,
		},
		{
			'label': _('31'),
			'fieldtype': 'Data',
			'fieldname': 'd31',
			'width': 100,
		}

	]

	return columns

def get_conditions(filters):
	conditions = "1=1"
	if filters.get("month"): conditions += " and month(ode.posting_date) = %(month)s"
	if filters.get("year"): conditions += " and year(ode.posting_date) = %(year)s"
	return conditions


def get_hours(filters):

	conditions = get_conditions(filters)
	return frappe.db.sql("""with cte as (SELECT
									t1.customer AS customer,
								    t1.item_code AS item_code,
								    t1.item_name AS item_name,
									"Actual Qty" AS qty,
									0 AS d1,
									0 AS d2,
									0 AS d3,
									0 AS d4,
									0 AS d5,
									0 AS d6,
									0 AS d7,
									0 AS d8,
									0 AS d9,
									0 AS d10,
									0 AS d11,
									0 AS d12,
									0 AS d13,
									0 AS d14,
									0 AS d15,
									0 AS d16,
									0 AS d17,
									0 AS d18,
									0 AS d19,
									0 AS d20,
									0 AS d21,
									0 AS d22,
									0 AS d23,
									0 AS d24,
									0 AS d25,
									0 AS d26,
									0 AS d27,
									0 AS d28,
									0 AS d29,
									0 AS d30,
									0 AS d31
								FROM
								(
									SELECT
										ode.customer AS customer,
										ode.item_code AS item_code,
										ode.item_name AS item_name
									FROM
										`tabSales Invoice Item` ode
									WHERE
										{conditions}
									GROUP BY
										ode.item_code

									UNION

									SELECT
										ode.customer AS customer,
										ode.item_code AS item_code,
										ode.item_name AS item_name
									FROM
										`tabSales Plan Ledger Entry` ode
									WHERE
										{conditions}
									GROUP BY
										ode.item_code
								) t1
								GROUP BY
									t1.item_code

								UNION

								SELECT
									t1.customer AS customer,
								    t1.item_code AS item_code,
								    t1.item_name AS item_code,
									"Plan Qty" AS qty,
									0 AS d1,
									0 AS d2,
									0 AS d3,
									0 AS d4,
									0 AS d5,
									0 AS d6,
									0 AS d7,
									0 AS d8,
									0 AS d9,
									0 AS d10,
									0 AS d11,
									0 AS d12,
									0 AS d13,
									0 AS d14,
									0 AS d15,
									0 AS d16,
									0 AS d17,
									0 AS d18,
									0 AS d19,
									0 AS d20,
									0 AS d21,
									0 AS d22,
									0 AS d23,
									0 AS d24,
									0 AS d25,
									0 AS d26,
									0 AS d27,
									0 AS d28,
									0 AS d29,
									0 AS d30,
									0 AS d31
								FROM
								(
									SELECT
										ode.customer AS customer,
										ode.item_code AS item_code,
										ode.item_name AS item_name
									FROM
										`tabSales Invoice Item` ode
									WHERE
										{conditions}
									GROUP BY
										ode.item_code

									UNION

									SELECT
										ode.customer AS customer,
										ode.item_code AS item_code,
										ode.item_name AS item_name
									FROM
										`tabSales Plan Ledger Entry` ode
									WHERE
										{conditions}
									GROUP BY
										ode.item_code
								) t1
								GROUP BY
									t1.item_code
								UNION

								select ode.item_code as item_code, ode.customer, ode.item_name,
													sum(case when day(ode.posting_date) = 1 then ode.qty else 0 end) as d1,
													sum(case when day(ode.posting_date) = 2 then ode.qty else 0 end) as d2,
													sum(case when day(ode.posting_date) = 3 then ode.qty else 0 end) as d3,
													sum(case when day(ode.posting_date) = 4 then ode.qty else 0 end) as d4,
													sum(case when day(ode.posting_date) = 5 then ode.qty else 0 end) as d5,
													sum(case when day(ode.posting_date) = 6 then ode.qty else 0 end) as d6,
													sum(case when day(ode.posting_date) = 7 then ode.qty else 0 end) as d7,
													sum(case when day(ode.posting_date) = 8 then ode.qty else 0 end) as d8,
													sum(case when day(ode.posting_date) = 9 then ode.qty else 0 end) as d9,
													sum(case when day(ode.posting_date) = 10 then ode.qty else 0 end) as d10,
													sum(case when day(ode.posting_date) = 11 then ode.qty else 0 end) as d11,
													sum(case when day(ode.posting_date) = 12 then ode.qty else 0 end) as d12,
													sum(case when day(ode.posting_date) = 13 then ode.qty else 0 end) as d13,
													sum(case when day(ode.posting_date) = 14 then ode.qty else 0 end) as d14,
													sum(case when day(ode.posting_date) = 15 then ode.qty else 0 end) as d15,
													sum(case when day(ode.posting_date) = 16 then ode.qty else 0 end) as d16,
													sum(case when day(ode.posting_date) = 17 then ode.qty else 0 end) as d17,
													sum(case when day(ode.posting_date) = 18 then ode.qty else 0 end) as d18,
													sum(case when day(ode.posting_date) = 19 then ode.qty else 0 end) as d19,
													sum(case when day(ode.posting_date) = 20 then ode.qty else 0 end) as d20,
													sum(case when day(ode.posting_date) = 21 then ode.qty else 0 end) as d21,
													sum(case when day(ode.posting_date) = 22 then ode.qty else 0 end) as d22,
													sum(case when day(ode.posting_date) = 23 then ode.qty else 0 end) as d23,
													sum(case when day(ode.posting_date) = 24 then ode.qty else 0 end) as d24,
													sum(case when day(ode.posting_date) = 25 then ode.qty else 0 end) as d25,
													sum(case when day(ode.posting_date) = 26 then ode.qty else 0 end) as d26,
													sum(case when day(ode.posting_date) = 27 then ode.qty else 0 end) as d27,
													sum(case when day(ode.posting_date) = 28 then ode.qty else 0 end) as d28,
													sum(case when day(ode.posting_date) = 29 then ode.qty else 0 end) as d29,
													sum(case when day(ode.posting_date) = 30 then ode.qty else 0 end) as d30,
													sum(case when day(ode.posting_date) = 31 then ode.qty else 0 end) as d31,
								 					'Planned Qty' as qty
								   from         `tabSales Plan Ledger Entry` ode
								    where
									  day(ode.posting_date) in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
									  ,21,22,23,24,25,26,27,28,29,30,31) and {conditions}
									  group by  ode.item_code
									  union all
												select
												    ode.nx_item_code as item_code,ode.customer,ode.item_name,
													sum(case when day(ode.posting_date) = 1 then ode.qty else 0 end) as d1,
													sum(case when day(ode.posting_date) = 2 then ode.qty else 0 end) as d2,
													sum(case when day(ode.posting_date) = 3 then ode.qty else 0 end) as d3,
													sum(case when day(ode.posting_date) = 4 then ode.qty else 0 end) as d4,
													sum(case when day(ode.posting_date) = 5 then ode.qty else 0 end) as d5,
													sum(case when day(ode.posting_date) = 6 then ode.qty else 0 end) as d6,
													sum(case when day(ode.posting_date) = 7 then ode.qty else 0 end) as d7,
													sum(case when day(ode.posting_date) = 8 then ode.qty else 0 end) as d8,
													sum(case when day(ode.posting_date) = 9 then ode.qty else 0 end) as d9,
													sum(case when day(ode.posting_date) = 10 then ode.qty else 0 end) as d10,
													sum(case when day(ode.posting_date) = 11 then ode.qty else 0 end) as d11,
													sum(case when day(ode.posting_date) = 12 then ode.qty else 0 end) as d12,
													sum(case when day(ode.posting_date) = 13 then ode.qty else 0 end) as d13,
													sum(case when day(ode.posting_date) = 14 then ode.qty else 0 end) as d14,
													sum(case when day(ode.posting_date) = 15 then ode.qty else 0 end) as d15,
													sum(case when day(ode.posting_date) = 16 then ode.qty else 0 end) as d16,
													sum(case when day(ode.posting_date) = 17 then ode.qty else 0 end) as d17,
													sum(case when day(ode.posting_date) = 18 then ode.qty else 0 end) as d18,
													sum(case when day(ode.posting_date) = 19 then ode.qty else 0 end) as d19,
													sum(case when day(ode.posting_date) = 20 then ode.qty else 0 end) as d20,
													sum(case when day(ode.posting_date) = 21 then ode.qty else 0 end) as d21,
													sum(case when day(ode.posting_date) = 22 then ode.qty else 0 end) as d22,
													sum(case when day(ode.posting_date) = 23 then ode.qty else 0 end) as d23,
													sum(case when day(ode.posting_date) = 24 then ode.qty else 0 end) as d24,
													sum(case when day(ode.posting_date) = 25 then ode.qty else 0 end) as d25,
													sum(case when day(ode.posting_date) = 26 then ode.qty else 0 end) as d26,
													sum(case when day(ode.posting_date) = 27 then ode.qty else 0 end) as d27,
													sum(case when day(ode.posting_date) = 28 then ode.qty else 0 end) as d28,
													sum(case when day(ode.posting_date) = 29 then ode.qty else 0 end) as d29,
													sum(case when day(ode.posting_date) = 30 then ode.qty else 0 end) as d30,
													sum(case when day(ode.posting_date) = 31 then ode.qty else 0 end) as d31,
													'Actual Qty' as qty

												from
												    `tabSales Invoice Item` ode
												where
													  day(ode.posting_date) in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
													  ,21,22,23,24,25,26,27,28,29,30,31) and {conditions}
												group by
												    ode.item_code)
													select customer, group_concat(qty), item_code, item_name, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10,
													d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21,d22, d23, d24, d25, d26, d27, d28,
													d29, d30, d31

													from cte
													group by item_code,qty
								 """.format(conditions=conditions),filters,as_dict=1)
