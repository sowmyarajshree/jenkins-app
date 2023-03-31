# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.model.document import Document
from datetime import date
import pandas as pd
from dateutil import parser
from frappe.utils import (
    DATE_FORMAT,
    add_days,
    add_to_date,
    cint,
    comma_and,
    date_diff,
    flt,
    getdate,
)

class LabourAttendance(Document):	
	def before_insert(self):
		self.set_balance_hrs()
		self.validate_labourer()
		self.validate_duplicate_attendance_doc0()
		
	def validate(self):
		self.set_balance_hrs()
		self.status_update_lab()
		self.calculate_total_hours_and_amount()
		self.validate_labourer()
		self.validate_duplicate_attendance_doc1()
		
	
	def before_submit(self):
		self.qty_copy_in_no_of_person()

	def before_cancel(self):
		self.status_on_cancel()

	def status_update_lab(self):
		if self.docstatus == 0:
			self.status = "Draft"
		if self.docstatus == 1:
			self.status = "Not Started"

	def set_balance_hrs(self): # removed balance_hrs
		if self.labour_details and self.created_from == "No":
			for i in self.labour_details:
				i.revised_in_time = 0
				i.revised_out_time = 0
				if (i.revised_in_time == 0):
					i.sum_of_working_hrs = i.working_hours
					i.balance_hrs = i.working_hours
				if (i.qty < 0):
					frappe.throw(_("No of person cannot be zero or less than zero"))

		if self.attendance_type == "Muster Roll" and self.created_from == "No":
			for i in self.muster_roll_detail:
				i.total_working_hours = i.working_hours
				i.balance_hours = i.working_hours
	
	def status_on_cancel(self):		
		if self.status == "Not Started":
			self.status = "Cancelled"
		elif self.status == "Completed":
			frappe.throw(("Cannot cancel the completed document"))
		elif self.status == "In Progress":
			frappe.throw(("Cannot cancel the In Progress document"))

	def validate_duplicate_attendance_doc0(self):
		if(self.attendance_type == 'Muster Roll'):
			if(frappe.db.exists('Labour Attendance',{'posting_date':self.posting_date,'project':self.project,'attendance_type':self.attendance_type,'docstatus':0})):
				frappe.throw(('This Muster Roll(NMR) Attendance Already PRESENT'))
		elif(self.attendance_type == 'Subcontractor'):
			if(frappe.db.exists('Labour Attendance',{"posting_date":self.posting_date,'attendance_type':self.attendance_type,'subcontractor':self.subcontractor,"project":self.project,'docstatus':0})):
				frappe.throw(('This Subcontractor Attendance Already PRESENT'))

	def validate_duplicate_attendance_doc1(self):
		if(self.attendance_type == 'Muster Roll'):	
			if(frappe.db.exists('Labour Attendance',{'posting_date':self.posting_date,'project':self.project,'attendance_type':self.attendance_type,'docstatus':1})):
				frappe.throw(('This Muster Roll(NMR) Attendance Already PRESENT'))

		elif(self.attendance_type == 'Subcontractor'):
			if(frappe.db.exists('Labour Attendance',{"posting_date":self.posting_date,'attendance_type':self.attendance_type,'subcontractor':self.subcontractor,"project":self.project,'docstatus':1})):
				frappe.throw(('This Subcontractor Attendance Already PRESENT'))


	# def duplicate_validate(self):
	# 	if(self.attendance_type =='Muster Roll'):
	# 		existing_doc=frappe.get_list("Labour Attendance",filters={"posting_date":self.posting_date,"project":self.project,"attendance_type":self.attendance_type,"docstatus":1})
	# 		if(existing_doc):
	# 			frappe.throw("This Muster Roll Attendance Already Present")
	# 	elif(self.attendance_type == 'Muster Roll'):
	# 		existing_doc=frappe.get_list("Labour Attendance",filters={"docstatus":0,"posting_date":self.posting_date,"project":self.project,"attendance_type":self.attendance_type})
	# 		if(existing_doc):
	# 			frappe.throw("This Muster Roll Attendance Already Present")

	# 	if(self.attendance_type == 'Subcontractor'):
	# 		exist_doc=frappe.get_list("Labour Attendance",filters={"posting_date":self.posting_date,"attendance_type":self.attendance_type,"subcontractor":self.subcontractor,"project":self.project,"docstatus":1})
	# 		if(exist_doc):
	# 			frappe.throw("This Subcontractor Attendance Already Present")
				
	def calculate_total_hours_and_amount(self):
		if(self.attendance_type =='Subcontractor'):
			self.total_working_hours = 0
			self.total_ot_hours = 0
			self.total_hours = 0
			self.total_no_of_persons = 0
			for d in self.labour_details:
				d.no_of_person_from_ot = d.qty
				self.total_working_hours += d.sum_of_working_hrs
				if d.ot_hours != None:
					self.total_ot_hours += d.ot_hours
				self.total_no_of_persons += d.qty
				if d.qty <=0:
					frappe.throw(_("No of person cannot be zero"))				
			self.total_hours = (self.total_working_hours+self.total_ot_hours)

		elif(self.attendance_type == 'Muster Roll'):
			self.total_working_hours = 0
			for i in self.muster_roll_detail:
				self.total_working_hours +=i.total_working_hours
			self.total_no_of_persons = len(self.muster_roll_detail)
							
	def qty_copy_in_no_of_person(self):
		if(self.attendance_type =='Subcontractor'):
			for d in self.labour_details:
				d.no_of_person_from_ot = d.qty

	def validate_labourer(self):
		if (self.attendance_type =='Subcontractor'):
			labourer = []
			for i in self.labour_details:
				if i.labourer not in labourer:
					labourer.append(i.labourer)
				else:
					frappe.throw("Given Labourer is repeated")
		elif (self.attendance_type =='Muster Roll'):
			muster_roll = []
			for i in self.muster_roll_detail:
				if i.muster_roll not in muster_roll:
					muster_roll.append(i.muster_roll)
				else:
					frappe.throw("Given NMR is repeated")
				
	def update_status_in_lab_att(self):
		if self.attendance_type == "Subcontractor":
			lab_doc = frappe.get_doc("Labour Attendance",self.name)
			if self.total_hours == self.total_worked_hrs:
				self.status = "Completed"
			lab_doc.save(ignore_permissions = True)

#whitelist function
@frappe.whitelist()
def update_ot_hours(docname):
	lab_att_doc = frappe.get_doc("Labour Attendance",docname)
	lab_ot_entry_doc = frappe.new_doc("Labour OT Entry")
	lab_ot_entry_doc.update({
		"project":lab_att_doc.project,
		"subcontractor":lab_att_doc.subcontractor,
		"posting_date":lab_att_doc.posting_date,
		"attendance_type":lab_att_doc.attendance_type,
		"labour_attendance":lab_att_doc.name
		})
	return lab_ot_entry_doc

@frappe.whitelist()
def create_labour_progress_entry(docname):
	lab_att_doc = frappe.get_doc("Labour Attendance",docname)
	lpe_doc = frappe.new_doc("Labour Progress Entry")
	if lab_att_doc.attendance_type == "Muster Roll":
		lpe_doc.update({
			"project_name":lab_att_doc.project,
			"labour_type":"Muster Roll",
			"posting_date":lab_att_doc.posting_date,
			})
	elif lab_att_doc.attendance_type != "Muster Roll":
		lpe_doc.update({
			"project_name":lab_att_doc.project,
			"labour_type":lab_att_doc.attendance_type,
			"subcontractor":lab_att_doc.subcontractor,
			"posting_date":lab_att_doc.posting_date,
			})
	return lpe_doc

@frappe.whitelist()
def update_labour_att_revision(docname):
	lab_att_doc = frappe.get_doc("Labour Attendance",docname)
	lab_att_revision_doc = frappe.new_doc("Labour Attendance Revision")
	if lab_att_doc.attendance_type == "Muster Roll":
		lab_att_revision_doc.update({
			"project":lab_att_doc.project,
			"attendance_type":lab_att_doc.attendance_type,
			"posting_date":lab_att_doc.posting_date,
			"labour_attendance":lab_att_doc.name,
			"revised_type":"Labour Out"
		})
		for i in lab_att_doc.muster_roll_detail:
			lab_att_revision_doc.append("labour_attendance_revision_item_muster", {
				"muster_roll":i.muster_roll,
				"no_of_person":1
				})
	elif lab_att_doc.attendance_type != "Muster Roll":
		lab_att_revision_doc.update({
			"project":lab_att_doc.project,
			"attendance_type":lab_att_doc.attendance_type,
			"subcontractor":lab_att_doc.subcontractor,
			"posting_date":lab_att_doc.posting_date,
			"labour_attendance":lab_att_doc.name,
			"revised_type":"Labour Out"
		})
		for i in lab_att_doc.labour_details:
			lab_att_revision_doc.append("labour_attendance_revision_item_sub", {
				"labourer":i.labourer,
				"no_of_person":i.qty
				})
	return lab_att_revision_doc
