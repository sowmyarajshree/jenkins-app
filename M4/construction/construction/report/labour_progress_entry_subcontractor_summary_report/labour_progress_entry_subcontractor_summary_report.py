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
		'fieldname'  :'project_name',
		'width'      :120,
		"options":"Project"
		},
		{
		'label'      :_('Date'),
		'fieldtype'  :'Date',
		'fieldname'  :'posting_date',
		'width'      :120
		},
		{
		'label'      :_('Labour Type'),
		'fieldtype'  :'Data',
		'fieldname'  :'labour_type',
		'width'      :120
		}])
	columns.extend([
	{
	'label'      :_('Posting Date'),
	'fieldtype'  :'Date',
	'fieldname'  :'posting_date',
	'width'      :150
	},
	{
	'label'      :_('Project Structure'),
	'fieldtype'  :'Link',
	'fieldname'  :'project_structure',
	'width'      :150,
	"options":"Project Structure"
	},
	{
	'label'      :_('Labour'),
	'fieldtype'  :'Link',
	'fieldname'  :'labour',
	'width'      :150,
	"options": "Labour"
	},
	{
	'label'      :_('UOM'),
	'fieldtype'  :'Data',
	'fieldname'  :'uom',
	'width'      :150
	},
	{
	'label'      :_('Is Primary Labour'),
	'fieldtype'  :'Select',
	'fieldname'  :'is_primary_labour',
	'width'      :150,
	'options' : ['','Yes','No']
	},
	{
	'label'      :_('Has Measurement Sheet'),
	'fieldtype'  :'Select',
	'fieldname'  :'has_measurement_sheet',
	'width'      :150,
	'options' : ['','Yes','No']
	},
	{
	'label'      :_('Total Worked Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'total_lpe_hours',
	'width'      :150
	}
		])
	return columns

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		lpe.project_name,
		lpe.project_structure,
		lpe.posting_date,
		lpe.labour,
		lpe.labour_type,
		lpe.uom,
		lpe.is_primary_labour,
		lpe.has_measurement_sheet,
		lpe.total_qty,
		lpe.lpe_total_hours
		FROM
			`tabLabour Progress Entry` lpe 
		WHERE lpe.docstatus = 1 %s
		ORDER BY
		lpe.project_name
		""" % conditions, filters, as_dict=1)




def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and lpe.project_name = %(project)s"
	if filters.get("project structure"):
		conditions +=" and lpe.project_structure = %(project_structure)s"
	if filters.get("to_date"):
		conditions +=" and lpe.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and lpe.posting_date >= %(from_date)s"
	if filters.get("labour_type"):
		conditions +=" and labour_type = %(labour_type)s"
	if filters.get("subcontractor") and filters.get("labour_type") == "F and F":
		conditions +=" and fe.subcontractor = %(subcontractor)s"
	if filters.get("subcontractor") and filters.get("labour_type") == "Rate Work":
		conditions +=" and re.subcontractor = %(subcontractor)s"
	return conditions

