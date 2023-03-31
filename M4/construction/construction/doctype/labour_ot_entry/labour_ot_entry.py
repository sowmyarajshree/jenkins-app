# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class LabourOTEntry(Document):
	def validate(self):
		self.validate_no_of_person()
		self.validate_labour_ot_entry()
		self.validate_for_labour_ot_person()
		self.validate_total_no_of_person()
		self.validate_labour_name()

	def before_submit(self):
		self.ot_hours_in_lab_attendance()
		self.set_total_working_hrs()

	def before_cancel(self):
		self.ot_hours_in_lab_attendance_on_cancel()
		self.set_total_working_hrs()

	def validate_for_labour_ot_person(self):
		lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
		labour_list=[]
		for i in lab_att_doc.labour_details:
			labour_list.append(i.labourer)

		for j in self.ot_details:
			if j.labourer not in labour_list:
				pass
				

	# Muster Roll Modification.
	def validate_no_of_person(self):
		lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
		if self.attendance_type == "Subcontractor":
			for l in lab_att_doc.labour_details:
				sum_of_person = 0
				for o in self.ot_details:
					if l.labourer == o.labourer:
						sum_of_person += o.no_of_person
				if sum_of_person > l.qty:
					frappe.throw(_("No Person is greater than the person given in Labour Attendance"))
				if o.ot_hours <= 0:
					frappe.throw(_("OT Hours cannot be Zero or less than Zero"))
				if o.total_ot_hours <= 0:
					frappe.throw(_("OT Hours cannot be Zero or less than Zero"))
		elif self.attendance_type == "Muster Roll":
			self.total_ot_hours = 0
			for i in self.ot_details:
				i.total_ot_hours = i.ot_hours
				self.total_ot_hours += i.total_ot_hours


	def validate_labour_ot_entry(self):
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			if lab_att_doc.status == "Completed":
				frappe.throw(_("Labour Attendance given is Completed"))

			self.project = lab_att_doc.project
			self.posting_date = lab_att_doc.posting_date
			self.attendance_type = lab_att_doc.attendance_type
			if self.subcontractor:
				self.subcontractor = lab_att_doc.subcontractor

			for i in self.ot_details:
				if i.ot_hours <= 0:
					frappe.throw(_("OT Hours cannot be Zero"))

	def ot_hours_in_lab_attendance(self):
		if self.attendance_type == "Subcontractor":
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			for o in self.ot_details:
				lab_att_doc.total_ot_hours = 0
				sum_of_person = 0
				for l in lab_att_doc.labour_details:
					if o.labourer == l.labourer:
						sum_of_person += o.no_of_person
						frappe.db.set_value("Labour Detail",l.name,"ot_hours",((frappe.get_value("Labour Detail",{"parent":self.labour_attendance,"labourer":o.labourer},["ot_hours"])) + o.total_ot_hours))
						
						frappe.db.set_value("Labour Attendance",lab_att_doc.name,"total_ot_hours",((frappe.get_value("Labour Attendance",{"name":self.labour_attendance},["total_ot_hours"])) + o.total_ot_hours))
						
						lab_details = frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["working_hours","ot_hours","f_and_f_hrs","rate_work_hrs","sum_of_working_hrs","total_worked_hours"],as_dict = 1)
						
						frappe.db.set_value("Labour Detail",l.name,"sum_of_working_hrs",(frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["working_hours"]) + frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["ot_hours"]) + frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["revised_in_time"])) + frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["revised_out_time"]))
       
						frappe.db.set_value("Labour Detail",l.name,"balance_hrs",(frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["sum_of_working_hrs"]) - frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["total_worked_hours"])))

						frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_working_hours",frappe.db.get_value("Labour Attendance",{"name":self.labour_attendance},["total_working_hours"]) + frappe.db.get_value("Labour Attendance",{"name":self.labour_attendance},["total_ot_hours"]))
															
		elif self.attendance_type == "Muster Roll":
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			for i in self.ot_details:
				for j in lab_att_doc.muster_roll_detail:
					if i.muster_roll == j.muster_roll:
						frappe.db.set_value("Muster Roll Detail",j.name,"ot_hours",(j.ot_hours + i.total_ot_hours))
						frappe.db.set_value("Muster Roll Detail",j.name,"total_working_hours",(j.working_hours + frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["ot_hours"]) + frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["revised_in_time"])) + frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["revised_out_time"]))
						frappe.db.set_value("Muster Roll Detail",j.name,"balance_hours",(j.working_hours + frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["ot_hours"]) + frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["revised_in_time"])) + frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["revised_out_time"]))
		
	def ot_hours_in_lab_attendance_on_cancel(self):
		if self.attendance_type == "Subcontractor":
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)			
			for o in self.ot_details:
				lab_att_doc.total_ot_hours = 0			
				for l in lab_att_doc.labour_details:
					if o.labourer == l.labourer:
						frappe.db.set_value("Labour Detail",l.name,"ot_hours",((frappe.get_value("Labour Detail",{"parent":self.labour_attendance,"labourer":o.labourer},["ot_hours"])) - o.total_ot_hours))
						
						frappe.db.set_value("Labour Attendance",lab_att_doc.name,"total_ot_hours",((frappe.get_value("Labour Attendance",{"name":self.labour_attendance},["total_ot_hours"])) - o.total_ot_hours))
						
						frappe.db.set_value("Labour Detail",l.name,"no_of_person_from_ot",((frappe.get_value("Labour Detail",{"parent":self.labour_attendance,"labourer":o.labourer},["no_of_person_from_ot"])) + o.no_of_person))
						
						lab_details = frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["working_hours","ot_hours","f_and_f_hrs","rate_work_hrs","sum_of_working_hrs","total_worked_hours"],as_dict = 1)
						
						frappe.db.set_value("Labour Detail",l.name,"sum_of_working_hrs",(frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["sum_of_working_hrs"])) - o.total_ot_hours)
						frappe.db.set_value("Labour Detail",l.name,"balance_hrs",(frappe.db.get_value("Labour Detail",{"parent":self.labour_attendance},["balance_hrs"])) - o.total_ot_hours)
						frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_hours",frappe.db.get_value("Labour Attendance",{"name":self.labour_attendance},["total_working_hours"]) - o.total_ot_hours)

						if ((lab_details.working_hours + lab_details.ot_hours) - (lab_details.f_and_f_hrs + lab_details.rate_work_hrs)) < 0:
							frappe.throw(_("Cannot Cancel this Labour OT Hours"))
					
		elif self.attendance_type == "Muster Roll":
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			for i in self.ot_details:
				for j in lab_att_doc.muster_roll_detail:
					if i.muster_roll == j.muster_roll:
						frappe.db.set_value("Muster Roll Detail",j.name,"ot_hours",(j.ot_hours - i.total_ot_hours))
						frappe.db.set_value("Muster Roll Detail",j.name,"total_working_hours",(j.total_working_hours - i.total_ot_hours))
						frappe.db.set_value("Muster Roll Detail",j.name,"balance_hours",(j.balance_hours - i.total_ot_hours))



	def set_total_working_hrs(self):
		if(self.attendance_type == "Subcontractor"):
			sum_of_working_hrs = frappe.db.sql(''' SELECT sum(sum_of_working_hrs) FROM `tabLabour Detail` ld WHERE ld.parent = %s''',(self.labour_attendance))[0][0]			              
			ot_hours = frappe.db.sql(''' SELECT	 sum(ot_hours) FROM `tabLabour Detail` ld  WHERE ld.parent = %s''',(self.labour_attendance))[0][0]
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_working_hours",sum_of_working_hrs)
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_ot_hours",ot_hours)

		elif(self.attendance_type != "Subcontractor"):
			total_working_hrs = frappe.db.sql(''' SELECT sum(total_working_hours)FROM `tabMuster Roll Detail` mr WHERE mr.parent = %s''',(self.labour_attendance))[0][0]
			ot_hours = frappe.db.sql(''' SELECT sum(ot_hours) ot_hrs FROM `tabMuster Roll Detail` mr WHERE mr.parent = %s''',(self.labour_attendance))[0][0]		
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_working_hours",total_working_hrs)
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_ot_hours",ot_hours)

	def validate_total_no_of_person(self):
		if(self.attendance_type == "Subcontractor"):
			self.total_no_of_person = 0
			for i in self.ot_details:
				self.total_no_of_person += i.no_of_person
		elif(self.attendance_type == "Muster Roll"):
			self.total_no_of_person = len(self.ot_details)

	def validate_labour_name(self):
		lab_att_doc=frappe.get_doc("Labour Attendance",self.labour_attendance)
		if self.attendance_type == "Subcontractor":
			labour_sub=[]
			for i in lab_att_doc.labour_details:
				labour_sub.append(i.labourer)
			for j in self.ot_details:
				if j.labourer not in labour_sub:
					frappe.throw(_("Given Labour Not in Labour Attendance"))
	
# Muster Roll Modification.
@frappe.whitelist()
def update_ot_details(labour_attendance):
	lab_att_doc = frappe.get_doc("Labour Attendance",labour_attendance)
	if lab_att_doc.attendance_type == "Subcontractor":
		ot_details = []
		lab_att_doc = frappe.get_doc("Labour Attendance",labour_attendance)
		if lab_att_doc.status != "Not Started":
			frappe.throw(_("OT can be created for only for Attendance in NOT STARTED status"))
		elif lab_att_doc.status == "Not Started":
			for i in lab_att_doc.labour_details:
				ot_details.append({
					  "labourer":i.labourer,
					  "no_of_person":i.qty
				})
		return ot_details
	elif lab_att_doc.attendance_type == "Muster Roll":
		ot_details = []
		lab_att_doc = frappe.get_doc("Labour Attendance",labour_attendance)
		for i in lab_att_doc.muster_roll_detail:
				ot_details.append({
					  "muster_roll":i.muster_roll,				  
				})
		return ot_details



