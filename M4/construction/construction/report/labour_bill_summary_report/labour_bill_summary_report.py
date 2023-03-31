import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	if(filters.get("labour_type") == "F and F"):
		data = get_data(filters)
	elif(filters.get("labour_type") == "Muster Roll"):
		data = get_datas(filters)
	elif(filters.get("labour_type") == "Rate Work"):
		data = get_datass(filters)
	else:
		data=[]

	return columns, data

def get_columns(filters):
	columns=[]
	if(filters.get("labour_type") == "Muster Roll"):
		columns += [
		{
		'label'      :_('Muster Roll Entry'),
		'fieldtype'  :'Link',
		'fieldname'  :'name',
		'width'      :120,
		'options':"Muster Roll Entry"
		}]
	if(filters.get("labour_type") == "F and F"):
		columns += [
		{
		'label'      :_('F & F Entry'),
		'fieldtype'  :'Link',
		'fieldname'  :'name',
		'width'      :120,
		'options':"F and F Entry"
		}]
	if(filters.get("labour_type") == "Rate Work"):
		columns += [
		{
		'label'      :_('Rate Work Entry'),
		'fieldtype'  :'Link',
		'fieldname'  :'name',
		'width'      :120,
		'options':"Rate Work Entry"
		}]
	columns.extend([
		{
		'label'      :_('Project'),
		'fieldtype'  :'Link',
		'fieldname'  :'project',
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
	if(filters.get("labour_type") != "Muster Roll"):
		columns += [
		{
		'label' : 'Subcontractor',
		'fieldtype' : 'Data',
		'fieldname' : 'subcontractor',
		'width' : 170,
		'options' : 'Supplier'
		}
		]
	if(filters.get("labour_type") == "Muster Roll"):
			columns += [
			{
			'label' : 'Muster Roll',
			'fieldtype' : 'Data',
			'fieldname' : 'muster_roll',
			"width":170
			}
		]
	columns.extend([
		{
		'label' : _("Accounting Period"),
		'fieldtype' : 'Data',
		'fieldname' : 'accounting_period',
		'width' :260,
		},
		{
		'label':_('Total Amount'),
		'fieldtype':"float",
		'fieldname':'total_amount',
		'width':120
		},
		{
		'label':_('Work Flow'),
		'fieldtype':"Data",
		'fieldname':'workflow_state',
		'width':160
		}
		])
	return columns

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		fe.project,
		fe.name,
		fe.labour_type,
		fe.posting_date,
		fe.accounting_period,
		fe.total_amount,
		fe.workflow_state,
		fe.subcontractor


		FROM
			`tabLabour Progress Detail` lpd left join
    		`tabF and F Entry` fe on fe.name = lpd.parent

		WHERE
		fe.docstatus = 0 %s
		GROUP BY
		fe.project,fe.accounting_period """ % conditions, filters, as_dict=1)

def get_datas(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		mre.project,
		mre.name,
		mre.labour_type,
		mre.posting_date,
		mre.accounting_period,
		mre.total_amount,
		mre.workflow_state,
		mre.muster_roll


		FROM
			`tabMuster Roll Entry` mre left join
    		`tabLabour Progress Detail` lpd on mre.name = lpd.parent

		WHERE
		mre.docstatus = 0 %s
		GROUP BY
		mre.project,mre.accounting_period """ % conditions, filters, as_dict=1)

def get_datass(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		re.project,
		re.name,
		re.labour_type,
		re.posting_date,
		re.accounting_period,
		re.total_amount,
		re.workflow_state,
		re.subcontractor


		FROM
			`tabLabour Progress Work Detail` lpd left join
    		`tabRate Work Entry` re on re.name = lpd.parent

		WHERE
		re.docstatus = 0 %s
		
		GROUP BY
		re.project,re.accounting_period """ % conditions, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("project_name") and filters.get("labour_type") == "Muster Roll":
		conditions +=" and mre.project = %(project_name)s"
	if filters.get("project_name") and filters.get("labour_type") == "Rate Work":
		conditions +=" and re.project = %(project_name)s"
	if filters.get("project_name") and filters.get("labour_type") == "F and F":
		conditions +=" and fe.project = %(project_name)s"
	if filters.get("to_date"):
		conditions +=" and posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and posting_date >= %(from_date)s"
	if filters.get("labour_type"):
		conditions +=" and labour_type >= %(labour_type)s"
	if filters.get("muster_roll") and filters.get("labour_type") == "Muster Roll":
		conditions +=" and mre.muster_roll = %(muster_roll)s"
	if filters.get("subcontractor") and filters.get("labour_type") == "F and F":
		conditions +=" and fe.subcontractor = %(subcontractor)s"
	if filters.get("subcontractor") and filters.get("labour_type") == "Rate Work":
		conditions +=" and re.subcontractor = %(subcontractor)s"
	return conditions


