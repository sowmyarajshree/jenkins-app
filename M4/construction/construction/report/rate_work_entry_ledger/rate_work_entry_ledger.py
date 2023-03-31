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
		'label'      :_('Labour Progress Entry'),
		'fieldtype'  :'Link',
		'fieldname'  :'labour_progress_entry',
		'width'      :120,
		'options'    :'Labour Progress Entry'
		},
		{
		'label'      :_('Labour Work'),
		'fieldtype'  :'Link',
		'fieldname'  :'labour_work',
		'width'      :120,
		'options'    :'Labour'
		},
		{
		'label'      :_('Lifting Charges'),
		'fieldtype'  :'Data',
		'fieldname'  :'lifting_charges',
		'width'      :120,
		},
		{
		'label'      :_('Rate'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'rate',
	    'width'      :150,
	    },
	    {
	    'label'      :_('Total Amount'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'total_amount',
	    'width'      :150
	    },
	    {
	    'label'      :_('Qty'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'qty',
	    'width'      :150
	    },
	    {
	    'label'      :_('Amount'),
	    'fieldtype'  :'Data',
	    'fieldname'  :'amount',
	    'width'      :150
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
		t.labour_progress_entry,
		t.labour_work,
		t.lifting_type,
		f.total_amount,
		t.lifting_charges,
		t.rate,
		t.qty,
		t.amount
		FROM
			`tabRate Work Entry` f LEFT JOIN `tabLabour Progress Work Detail` t on t.parent = f.name
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
	return conditions
