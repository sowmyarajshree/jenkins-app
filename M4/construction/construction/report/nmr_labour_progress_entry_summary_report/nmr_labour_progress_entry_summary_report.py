# Copyright (c) 2023, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns=get_columns(filters)
	data =get_data(filters)
	return columns, data


def get_columns(filters):
	return[
	{
	'label':_('ID'),
	'fieldtype':'Link',
	'fieldname':'name',
	'width':150,
	'options':'Labour Progress Entry'
	},
	{
	'label':_('Project'),
	'fieldtype':'Link',
	'fieldname':'project_name',
	'width':150,
	'options':'Project'
	},
	{
	'label':_('Project Structure'),
	'fieldtype':'Link',
	'fieldname':'project_structure',
	'width':150,
	'options':'Project Structure'
	},
	{
	'fieldname':'item_of_work',
	'label':'Item of Work',
	'fieldtype':'Link',
	'width':180,
	'options':'Item of Work'
	},
	{
	'label':'Task',
	'fieldtype':'Link',
	'fieldname':'task_id',
	'width'	   :160,
	'options' :"Task"
	},
	{
	'label':_('Posting Date'),
	'fieldtype':'Date',
	'fieldname':'posting_date',
	'width':140
	},
	{
	'label':'Muster Roll',
	'fieldname':'muster_roll',
	'fieldtype':'Link',
	'width':180,
	'options':'Muster Roll'
	},
	{
	'label':_('Labour Type'),
	'fieldtype':'Select',
	'fieldname':'labour_type',
	'width':160,
	'options':['Muster Roll']
	},
	{
	'label':_('Accounting Period'),
	'fieldtype':'Link',
	'fieldname':'accounting_period',
	'width':120,
	'options':'Accounting Period'
	},
	{
	'label':_('Labour'),
	'fieldtype':'Link',
	'fieldname':'labour',
	'width':150,
	'options':'Labour'
	},
	{
	'label':_('Is Primary Labour'),
	'fieldtype':'Select',
	'fieldname':'is_primary_labour',
	'width':120,
	'options':['Yes','No']
	},
	{
	'label':_('Has Measurement Sheet'),
	'fieldtype':'Select',
	'fieldname':'has_measurement_sheet',
	'width':120,
	'options':['Yes','No']
	},
	{
	'label':_('Total Qty'),
	'fieldtype':'Float',
	'fieldname':'total_qty',
	'width':120
	},
	{
	'label':_('Balance Qty'),
	'fieldtype':'Float',
	'fieldname':'ledg_balance_qty',
	'width':130
	},
	{
	'label':_('UOM'),
	'fieldtype':'Data',
	'fieldname':'uom',
	'width':140
	},
	{
	'label':_('Worked Hours'),
	'fieldtype':'Float',
	'fieldname':'lpe_total_hours',
	'width':140
	},
	{
	'label':_('Status'),
	'fieldtype':'Select',
	'fieldname':'status',
	'width':160,
	'options':['To Prepared and Bill','To Bill','Completed']
	},
	]


def get_data(filters):
	conditions=get_conditions(filters)
	return frappe.db.sql(""" 
		SELECT
		lpe.name,
		lpe.project_name,
		lpe.project_structure,
		lpe.item_of_work,
		lpe.task_id,
		lpe.posting_date,
		GROUP_CONCAT(wd.muster_roll)AS muster_roll,
  		lpe.labour_type,
		lpe.accounting_period,
		lpe.labour,
		lpe.is_primary_labour,
		lpe.has_measurement_sheet,
		lpe.total_qty,
		lpe.ledg_balance_qty,
		lpe.uom,
		lpe.lpe_total_hours,
		lpe.status


		FROM 
		`tabLabour Progress Entry` lpe INNER JOIN `tabWorking Detail` wd on wd.parent=lpe.name
		WHERE lpe.docstatus=1 and lpe.labour_type="Muster Roll" %s


		GROUP BY
		lpe.name

		ORDER BY
		lpe.project_name,
		lpe.posting_date

		 """ % conditions, filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and lpe.project_name = %(project)s"
	if filters.get("project_structure"):
		conditions +=" and lpe.project_structure = %(project_structure)s"
	if filters.get("item_of_work"):
		conditions +=" and lpe.item_of_work = %(item_of_work)s"
	if filters.get("to_date"):
		conditions +=" and lpe.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and lpe.posting_date >= %(from_date)s"
	if filters.get("status"):
		conditions +=" and lpe.status = %(status)s"
	if filters.get("muster_roll"):
		conditions +=" and wd.muster_roll = %(muster_roll)s"
	return conditions