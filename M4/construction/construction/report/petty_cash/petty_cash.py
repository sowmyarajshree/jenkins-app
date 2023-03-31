# Copyright (c) 2013, Nxweb and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe.utils import (formatdate,date_diff)
from frappe import _
from datetime import datetime,date



def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data
def get_columns(filters):
	return [{
		'label': _('Account'),
		'fieldtype': 'Link',
		'fieldname': 'account',
		'width':350,
		"options":"Account"
	},
	{
		'label': _(' Debit'),
		'fieldtype': 'Float',
		'fieldname': 'credit',
		'width': 250
	},
	{
		'label': _('Credit'),
		'fieldtype': 'Float',
		'fieldname': 'debit',
		'width': 250
	},
	{
		'label': _('Balance'),
		'fieldtype': 'Float',
		'fieldname': 'total',
		'width': 250
	}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql("""
		SELECT
			gl.account as account,sum(gl.credit) as credit, sum(gl.debit) as debit, (sum(gl.debit) - sum(gl.credit)) as total
		From
		    `tabGL Entry` gl  left join `tabAccount` a on a.name = gl.account
		where
			gl.docstatus = 1  and gl.is_cancelled != 1 and a.disabled = 0  and a.parent_account = "Cash In Hand - SSC"%s
			
		group by
			gl.account

		""" % conditions, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("posting_date"):
		conditions +=" and gl.posting_date <= %(posting_date)s"
	if filters.get("account"):
		conditions +=" and gl.account = %(account)s"
	return conditions
