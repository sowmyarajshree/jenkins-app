from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime,time,date

def validate_location(self,method):
	if not (self.location):
		frappe.throw('Select Your Location')
	if not (self.device_id):
		frappe.throw('Your Current Location/Device Id is not set by Administrator, Contact Your Admin')
	if not (self.nx_location):
		frappe.throw('Set Valid Location')
	if(self.nx_location):
		nx_location = self.nx_location.split('+')
		location = self.device_id.split('+')
		if(nx_location[0] != location[0]):
			frappe.throw('Out Of Attendance Zone')




def duplicate_validation(self,method):
	pass
	'''date = self.time.split(" ")[0]
	if frappe.db.exists("Employee Checkin",{"employee":self.employee,"log_type":self.log_type,"nx_date":self.nx_date},["name"]):
		emp_check_doc = frappe.get_value("Employee Checkin",{"employee":self.employee,"log_type":self.log_type,"nx_date":self.nx_date},["name"])
		frappe.throw(_("Employee Checkin is already present {0} in the date {1}").format(emp_check_doc,self.nx_date))'''






def to_show_msgprint(self,method):
	if self.log_type == "IN":
		frappe.msgprint(_("Employee Checkin is Saved Successfully"))

def create_attendance_from_checkin(self,method):
	time = (self.time).date()
	if self.log_type == "IN":
		attendance_doc = frappe.new_doc("Attendance")
		attendance_doc.update({
			"employee":self.employee,
			"attendance_date":self.time,
			"company":"Sri Sasthaa Constructions",
			"docstatus":0
			})
		attendance_doc.save(ignore_permissions = True)
		frappe.db.commit()

	if frappe.db.exists("Attendance", {"employee_name":self.employee_name},{"attendance_date":time}) and self.log_type == "OUT":
		attendance_doc_one = frappe.get_doc("Attendance",{"employee_name":self.employee_name},{"attendance_date":time})
		attendance_doc_one.docstatus = 1
		attendance_doc_one.save(ignore_permissions = True)
		frappe.db.commit()






































