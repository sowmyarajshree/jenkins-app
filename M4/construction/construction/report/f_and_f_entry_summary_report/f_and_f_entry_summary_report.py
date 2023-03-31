from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _



def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns=[]
	columns.extend([
		{
		'label'      :_('Project'),
		'fieldtype'  :'Link',
		'fieldname'  :'project',
		'width'      :120,
		'options':'Project'
		},
		{
		'label'      :_('Date'),
		'fieldtype'  :'Date',
		'fieldname'  :'posting_date',
		'width'      :120
		},
		{
		'label'      :_('Subcontractor'),
		'fieldtype'  :'Link',
		'fieldname'  :'subcontractor',
		'width'      :120,
		'options'    :'Supplier'
		},
		{
		'label'      :_('Labour Work Order'),
	    'fieldtype'  :'Link',
	    'fieldname'  :'labour_work_order',
	    'width'      :150,
	    'options'    :'Labour Work Order'
	    },
	    {
	    'label'      :_('Total Hours from LPE'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'total_hours_lpe',
	    'width'      :150
	    },
	    {
	    'label'      :_('Total Hours from Attendance'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'total_hours',
	    'width'      :150
	    },
	    {
	    'label'      :_('Total Amount'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'total_amount',
	    'width'      :150
	    },
	    {
	    'label'      :_('Status'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'status',
	    'width'      :150
	    },
	    {
	    'label'      :_('Work Efficiency'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'work_efficiency',
	    'width'      :150
	    },
	    {
	    'label'      :_('Purchase Invoice'),
	    'fieldtype'  :'Link',
	    'fieldname'  :'purchase_invoice',
	    'width'      :150,
	    'options'    :'Purchase Invoice'
	    }
		])
	return columns
def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		f.project,
		f.subcontractor,
		f.posting_date,
		f.labour_work_order,
		f.purchase_invoice,
		f.work_efficiency,
		f.status,
		f.total_amount,
		f.total_hours,
		f.total_hours_lpe
		FROM
			`tabF and F Entry` f 
		WHERE f.docstatus = 1 %s
		ORDER BY
		f.project
		""" % conditions, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and f.project = %(project)s"
	if filters.get("subcontractor"):
		conditions +=" and f.subcontractor = %(subcontractor)s"
	if filters.get("to_date"):
		conditions +=" and f.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and f.posting_date >= %(from_date)s"
	if filters.get("status"):
		conditions +=" and f.status = %(status)s"
	return conditions
