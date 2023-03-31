# Copyright (c) 2013, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate,getdate
from frappe.utils.data import  getdate
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data_list = get_data(filters)
	data = []
	check_in_time = 0
	for i in data_list:
		row = ({
			"employee":i.first_name,
			"department":i.department,
			"log_type":"-",
			"check_in_time":"-"
			

		})
		check_in_time = filters.get("time")
		emp_checkin_entry = frappe.db.sql(""" SELECT ec.employee_name,ec.log_type,ec.time FROM `tabEmployee Checkin` ec WHERE  ec.employee = %s and DATE(ec.time) = %s and ec.log_type = 'OUT'   order by ec.employee_name asc """,(i.name,check_in_time),as_dict = 1)
		for j in emp_checkin_entry:
			if j.log_type != None:
				row.update({				  
				   "log_type":j.log_type,
				   "check_in_time":j.time

				})			
		data.append(row)

	return columns, data

def get_columns(filters):
	return[
	    {
	   'label': _('Employee'),
	   'fieldtype': 'Data',
	   'fieldname': 'employee',
	   'width': 400,

	    },
	    
	    {
	   'label': _('Department'),
	   'fieldtype': 'Data',
	   'fieldname': 'department',
	   'width': 400,
	    },
	    {
	   'label': _('Log In Type'),
	   'fieldtype': 'Data',
	   'fieldname': 'log_type',
	   'width': 400,
	    },
	    {
	   'label': _('Checkin Time'),
	   'fieldtype': 'Data',
	   'fieldname': 'check_in_time',
	   'width': 400,
	    }


	]


def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql("""

       SELECT
              emp.name,
		    emp.first_name,
		    emp.name,
		    emp.department

		FROM
		    `tabEmployee` emp 

		WHERE
		     emp.status = "Active" and emp.department != "Transport - SSC" %s
		ORDER BY
		     emp.first_name asc



		   """ %  conditions,filters, as_dict=1)




def get_conditions(filters):
	conditions = ""
	if filters.get("department"):
		conditions +=" and emp.department = %(department)s"
	
	return conditions






