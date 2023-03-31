# Copyright (c) 2013, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data_details = get_data(filters)
	data = []
	for i in data_details:
		row = ({
			"name":i.name,
			"company":i.company,
			"project":i.project,
			"description":i.description,
			"document_date":i.document_date
		})
		emp_name = frappe.db.get_value("Employee",{"name":i.handing_over},["first_name"])
		row.update({
			"emp_name":emp_name
			})
		data.append(row)


	return columns, data

def get_columns(filters):
	return[
	   {
	   'label': _('Bill Number'),
	   'fieldtype': 'Link',
	   'fieldname': 'name',
	   'width': 200,
	   'options':'Lettering Inward',
	   },
	   {
	   'label': _('Supplier'),
	   'fieldtype': 'Link',
	   'fieldname': 'company',
	   'width': 200,
	   'options':'Supplier',
	   },
	   {
	   'label': _('Site Name'),
	   'fieldtype': 'Link',
	   'fieldname': 'project',
	   'width': 200,
	   'options':'Project',
	   },
	   {
	   'label': _('Subject'),
	   'fieldtype': 'Data',
	   'fieldname': 'description',
	   'width': 200
	   },
	   {
	   'label': _('Date'),
	   'fieldtype': 'Date',
	   'fieldname': 'document_date',
	   'width': 210
	   },
	   {
	   'label': _('Signature'),
	   'fieldtype': 'Data',
	   'fieldname': 'emp_name',
	   'width': 220
	   }
	   ]


def get_data(filters):
	#conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql("""
		SELECT
		   li.name,
		   li.project,
		   li.description,
		   li.document_date,
		   li.company,
		   li.handing_over
              

		FROM
		    `tabLettering Inward` li




		WHERE
		    li.docstatus = 0  """,  as_dict=1)






'''def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions +=" and bo.from_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions +=" and bo.from_date <= %(to_date)s"
	if filters.get("item_code"):
		conditions +=" and boi.item_code = %(item_code)s"
	return conditions'''
