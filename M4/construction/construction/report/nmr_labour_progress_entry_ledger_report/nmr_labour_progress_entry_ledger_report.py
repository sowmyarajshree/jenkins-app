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
	'width':170,
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
	'label':_('Posting Date'),
	'fieldtype':'Date',
	'fieldname':'posting_date',
	'width':140
	},
	{
	'label':_('Labour Type'),
	'fieldtype':'Select',
	'fieldname':'labour_type',
	'width':140,
	'options':['Muster Roll']
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
	'label':_('Grid'),
	'fieldtype':'Link',
	'fieldname':'grid',
	'width':160,
	'options':'Grid'
	},
	{
	'label':_('Description'),
	'fieldtype':'Data',
	'fieldname':'description_of_work',
	'width':150
	},
	{
	'label':_('Total Nos'),
	'fieldtype':'Float',
	'fieldname':'no',
	'width':120
	},
	{
	'label':_('Select Your UOM'),
	'fieldtype':'Link',
	'fieldname':'dimensional_uom',
	'width':140,
	'options':'UOM'
	},
	{
	'label':_('Length'),
	'fieldtype':'Float',
	'fieldname':'length_wise',
	'width':130
	},
	{
	'label':_('Breadth'),
	'fieldtype':'Float',
	'fieldname':'breadth',
	'width':130
	},
	{
	'label':_('Depth & Height'),
	'fieldtype':'Float',
	'fieldname':'depth_height',
	'width':140
	},
	{
	'label':_('Quantity'),
	'fieldtype':'Float',
	'fieldname':'quantity',
	'width':130
	},
	{
	'label':_('UOM'),
	'fieldtype':'Link',
	'fieldname':'uom',
	'width':140,
	'options':'UOM'
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
	'label':'Muster Roll',
	'fieldname':'muster_roll',
	'fieldtype':'Link',
	'width':180,
	'options':'Muster Roll'
	},
	{
	'label':'No Of Person',
	'fieldname':'no_of_person',
	'fieldtype':'Int',
	'width':140
	},
	{
	'label':'Total Working Hours',
	'fieldname':'total_working_hours',
	'fieldtype':'Float',
	'width':140
	},
	{
	'label':'Balance Hours',
	'fieldname':'balance_hours',
	'fieldtype':'Float',
	'width':140
	},
	{
	'label':'Labour Bill Rate',
	'fieldname':'labour_bill_rate',
	'fieldtype':'Float',
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
		lpe.project_name,
		lpe.project_structure,
		lpe.item_of_work,
		lpe.posting_date,
  		lpe.labour_type,
		lpe.labour,
		lpe.is_primary_labour,
		lpe.has_measurement_sheet,
		msd.grid,
		msd.description_of_work,
		msd.no,
		msd.dimensional_uom,
		msd.length_wise,
		msd.breadth,
		msd.depth_height,
		msd.quantity,
		msd.uom,
		lpe.total_qty,
		lpe.ledg_balance_qty,
		lpe.uom,
		wd.muster_roll,
		wd.no_of_person,
		wd.total_working_hours,
		wd.balance_hours,
		wd.labour_bill_rate,
		lpe.lpe_total_hours,
		lpe.status


		FROM 
			`tabLabour Progress Entry` lpe LEFT JOIN
			`tabMeasurement Sheet Detail` msd on msd.parent=lpe.name LEFT JOIN
			`tabWorking Detail` wd on wd.parent=lpe.name
		WHERE lpe.docstatus=1 and lpe.labour_type="Muster Roll" %s


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