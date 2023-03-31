# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe import utils
from frappe.utils import getdate
import datetime
import json


class LabourProgressEntry(Document):
	def validate(self):
		self.calculate_quantity()
		self.labour_attendance_validate()
		self.validate_working_details()
		self.copy_conversion_type_in_steel_reinforcement()
		self.calculation_for_total_dia()
		self.bbs_validation()
		self.has_conversion_calculation()	
		self.validate_boq_data()
		self.set_labour_attendance_name()
		#self.validate_for_late_lpe()

	
	def before_submit(self):
		self.status_validate()
		self.update_actual_qty_in_boq_ledg()
		self.update_actual_qty_in_task()
		self.total_hours_in_lab_attendance()
		self.validate_no_of_person()
		self.update_status_in_lab_attendance()
		#self.validate_for_late_lpe()
		self.set_total_working_hrs()

	def before_cancel(self):
		self.update_actual_qty_in_boq_ledg_on_cancel()
		self.update_actual_qty_in_task_on_cancel()
		self.status_validate_on_cancel()
		self.total_hours_in_lab_attendance_on_cancel()
		self.update_status_in_lab_attendance_cancel()
		self.unlink_labour_attendance()
		self.set_total_working_hrs()


	#validate cancel labour attendance 
	def unlink_labour_attendance(self):
		if self.labour_attendance != None:
			self.labour_attendance = None


	#Validation For Conversion Type
	def copy_conversion_type_in_steel_reinforcement(self):
		if(self.conversion_type == "Meter"):
			for i in self.bbs_details:
				i.conversion_type = "Meter"
		else:
			for j in self.bbs_details:
				j.conversion_type = "Feet"


	def calculation_for_total_dia(self):
		for i in self.bbs_details:
			if (i.conversion_type == "Feet"):
				i.total_dia = i.member * i.nos * i.cutting_length
				i.total_dia = (i.total_dia)/3.28
			elif (i.conversion_type == "Meter"):
				i.total_dia = i.member * i.nos * i.cutting_length

		self.total_quantity = 0;
		for j in self.bbs_abstract:
			self.total_quantity += j.weight

	

   #get abstract error through in LPE
	def bbs_validation(self):
		if self.steel_reinforcement == 1:
			if sum(round(i.total_dia,3) for i in self.bbs_details) != sum(round(j.length,3) for j in self.bbs_abstract):
				frappe.throw(title='Calculation Error',msg='''BBS Details & abstract length are different,Kindly click The "Get Abstract" Button to update new value or Conversion Type is not same as given''')
	
    #has conversion calculation in LPE
	def has_conversion_calculation(self):
		if self.steel_reinforcement == 1:
			if self.has_conversion == 1:
				self.total_qty = self.total_quantity / 1000
			else:
				self.total_qty = self.total_quantity


    #status related updates
	def status_validate(self):
		if self.docstatus == 0:
			self.status = "Draft"
		if self.docstatus == 1:
			self.status = "To Prepared and Bill"

	def status_validate_on_cancel(self):
		if self.docstatus == 2:
			self.status = "Cancelled"

	def validate_working_details(self):
		if self.labour_type != "Muster Roll":
			for i in self.working_details:
				if i.no_of_person <= 0:
					frappe.throw(_("No Person Cannot be Zero or lesser"))
				if i.total_working_hours <= 0:
					frappe.throw(_("Working Hours Cannot be Zero or lesser"))

    #for task calculation to update actual qty and balance qty(it update in task)
	def update_actual_qty_in_task(self):
		if self.task_id and self.is_primary_labour == "Yes":
			task_doc = frappe.get_doc("Task",self.task_id)
			task_doc.actual_qty = round((task_doc.actual_qty + self.total_qty),3)
			task_doc.nx_actual_qty = round((task_doc.actual_qty / task_doc.nx_primary_labour_qty),3)
			task_doc.balance_qty = round((task_doc.qty - task_doc.actual_qty),3)
			task_doc.actual_qty_uom = self.uom
			task_doc.pl_act_qty_uom = self.uom
			task_doc.balance_qty_uom =self.uom
			task_doc.pl_bal_qty_uom = self.uom
			task_doc.save(ignore_permissions = True)

    #for task calculation to remove or reduce actual qty and balance qty(it update in task on cancel)
	def update_actual_qty_in_task_on_cancel(self):
		if self.task_id and self.is_primary_labour == "Yes":
			task_doc = frappe.get_doc("Task",self.task_id)
			task_doc.actual_qty -= round(self.total_qty,3)
			task_doc.nx_actual_qty = round((task_doc.actual_qty / task_doc.nx_primary_labour_qty),3)
			task_doc.balance_qty = round((task_doc.qty - task_doc.actual_qty),3)
			task_doc.save(ignore_permissions = True)

    #for boq ledger calculation to update actual qty and balance qty(it update in boq ledger)
	def update_actual_qty_in_boq_ledg(self):
		boq_ledger  = frappe.get_doc("BOQ Ledger",{"boq":self.boq,"labour":self.labour,"ledger_type":"Labour"})
		if (boq_ledger.has_measurement_sheet == "No" and self.total_qty == 0):
			if boq_ledger.actual_qty == 0:
				boq_ledger.actual_qty = 1
		boq_ledger.actual_qty = boq_ledger.actual_qty + self.total_qty
		boq_ledger.save(ignore_permissions = True)

    #for boq ledger calculation to remove or reduce actual qty and balance qty(it update in boq ledger)
	def update_actual_qty_in_boq_ledg_on_cancel(self):
		boq_ledger = frappe.get_doc("BOQ Ledger",{"boq":self.boq,"labour":self.labour,"ledger_type":"Labour"})
		boq_ledger.actual_qty -= self.total_qty
		boq_ledger.save(ignore_permissions = True)

    #validate the given boq data
	def validate_boq_data(self):
		if frappe.db.get_value("BOQ Ledger",{"boq":self.boq,"labour":self.labour},['has_measurement_sheet']) == "Yes":
			if self.total_qty < 0:
				frappe.throw(_("Total Qty cannot be lesser than Zero"))
		if self.total_qty > self.ledg_balance_qty:
			frappe.throw(_("Total Qty cannot be Greater than Balance Qty"))

		if self.labour_type == "F and F" and self.lpe_total_hours <= 0:
			frappe.throw(_("Worked Hours cannot be Zero or less than Zero"))
		
		boq_doc = frappe.get_doc("BOQ",self.boq)
		if boq_doc.project != self.project_name:
			frappe.throw(_("The given project is not related given BOQ"))
		if boq_doc.project_structure != self.project_structure:
			frappe.throw(_("The given project structure is not related given BOQ"))
		if boq_doc.item_of_work != self.item_of_work:
			frappe.throw(_("The given item of work is not related given BOQ"))
		if boq_doc.task != self.task_id:
			frappe.throw(_("The given task is not related given BOQ"))

    #validate child table values
	def calculate_quantity(self):
		if (self.measurement_sheet_detail == "Yes" and self.steel_reinforcement == 0):
			for m in self.measurement_sheet_detail:
				if (m.no <= 0 or m.length_wise <= 0 or m.breadth <= 0 or m.depth_height <= 0 or m.quantity <= 0):
					frappe.throw(_("Nos or Length or Breadth or Depth cannot be Zero"))
				else:
					m.quantity = m.no * m.breadth * m.length_wise * m.depth_height
			self.total_qty = round(sum(i.quantity for i in self.measurement_sheet_detail),3)
		
		if (self.has_measurement_sheet == "Yes" and self.steel_reinforcement == 0 and self.total_qty <= 0):
			frappe.throw(_("Total quantity cannot be Zero"))				
		self.lpe_total_hours = sum(i.total_working_hours for i in self.working_details)
		
		if(self.lpe_total_hours <= 0):
			frappe.throw(_("Worked hours cannot be Zero"))	
		if (self.working_details):
			for w in self.working_details:
				w.total_working_hours = w.no_of_person * w.working_hours
				if w.total_working_hours <= 0:
 					frappe.throw(_("In Working Details Total Working Hours Cannot be Zero"))

	def validate_no_of_person(self):
		if (self.working_details and self.labour_type != "Muster Roll"):
			for i in self.working_details:
				lpe_person = frappe.db.sql(""" SELECT sum(no_of_person) FROM `tabWorking Detail` WHERE `tabWorking Detail`.parent = %s and `tabWorking Detail`.labourer = %s """,(self.name,i.labourer))[0][0]			
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor"},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
				for j in lab_att_doc.labour_details:
					lab_att_person = frappe.db.sql("""SELECT ((qty + revised_in_time) - revised_out_time) as lab_att_person FROM `tabLabour Detail`  WHERE `tabLabour Detail`.parent = %s and `tabLabour Detail`.labourer = %s """,(lab_att_doc.name,i.labourer))[0][0]
					if lpe_person > lab_att_person:
						frappe.throw(_("No of Person Cannot be added more than given in Labour Attendance"))

	def set_labour_attendance_name(self):
		if (self.labour_type == "Muster Roll"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"attendance_type":"Muster Roll","docstatus":1},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
				self.labour_attendance = lab_att_doc.name

		if (self.labour_type == "F and F"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor","docstatus":1},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
				self.labour_attendance = lab_att_doc.name
				for l in lab_att_doc.labour_details:
					if i.labourer == l.labourer:
						if i.no_of_person > l.qty:
							frappe.throw(_("No of person Cannot be added more than given in Labour Attendance"))
						if i.total_working_hours > i.balance_hours:
							frappe.throw(_("No of Working Hours Cannot be added more than given in Labour Attendance"))

		if (self.labour_type == "Rate Work"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor","docstatus":1},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
				self.labour_attendance = lab_att_doc.name
				for l in lab_att_doc.labour_details:
					if i.labourer == l.labourer:
						if i.no_of_person > l.qty:
							frappe.throw(_("No of person Cannot be added more than given in Labour Attendance"))
						if i.total_working_hours > i.balance_hours:
							frappe.throw(_("No of Working Hours Cannot be added more than given in Labour Attendance"))

	def total_hours_in_lab_attendance(self):
		if (self.labour_type == "Muster Roll"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"attendance_type":"Muster Roll","docstatus":1},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
				self.labour_attendance = lab_att_doc.name
				for j in lab_att_doc.muster_roll_detail:
					if j.muster_roll == i.muster_roll:
						frappe.db.set_value("Muster Roll Detail",j.name,"total_worked_hours",frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name,"muster_roll":i.muster_roll},["total_worked_hours"]) + i.total_working_hours)
						muster_roll_det = frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["total_working_hours","total_worked_hours","balance_hours"],as_dict=1)
						frappe.db.set_value("Muster Roll Detail",j.name,"balance_hours",(muster_roll_det.total_working_hours - muster_roll_det.total_worked_hours))

						if (muster_roll_det.total_working_hours - muster_roll_det.total_worked_hours) < 0:
							frappe.throw(_("Working hours for the labourer is Exceeded"))
										
						elif frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["balance_hours"]) == 0:
							frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Completed")
						elif frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["total_worked_hours"]) != 0 and frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name,"muster_roll":i.muster_roll},["balance_hours"]) != 0:
							frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","In Progress")
						elif frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["total_worked_hours"]) == 0:
							frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Not Started")

		if (self.working_details and self.labour_type == "F and F"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor","docstatus":1},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
				self.labour_attendance = lab_att_doc.name
				lab_att_doc.total_worked_hrs = 0
				for j in lab_att_doc.labour_details:
					if i.labourer == j.labourer:
						frappe.db.set_value("Labour Attendance",lab_att_doc.name,"total_worked_hrs",(frappe.db.get_value("Labour Attendance",{"name":lab_att_doc.name},["total_worked_hrs"]) + i.total_working_hours))
						frappe.db.set_value("Labour Detail",j.name,"f_and_f_hrs",(frappe.db.get_value("Labour Detail",{"parent":lab_att_doc.name,"labourer":i.labourer},["f_and_f_hrs"]) + i.total_working_hours))
						lab_details = frappe.db.get_value("Labour Detail",{"parent":lab_att_doc.name},["working_hours","ot_hours","f_and_f_hrs","rate_work_hrs","sum_of_working_hrs","total_worked_hours"],as_dict = 1)
						frappe.db.set_value("Labour Detail",j.name,"total_worked_hours",(lab_details.f_and_f_hrs + lab_details.rate_work_hrs))
						frappe.db.set_value("Labour Detail",j.name,"balance_hrs",(lab_details.sum_of_working_hrs - (lab_details.f_and_f_hrs + lab_details.rate_work_hrs)))	
						if ((lab_details.sum_of_working_hrs) - (lab_details.f_and_f_hrs + lab_details.rate_work_hrs)) < 0:
							frappe.throw(_("Working hours for the labourer is Exceeded"))
						else:
							pass
				
		if (self.working_details and self.labour_type == "Rate Work"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor","docstatus":1},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
				self.labour_attendance = lab_att_doc.name
				lab_att_doc.total_worked_hrs = 0
				for j in lab_att_doc.labour_details:
					if i.labourer == j.labourer:
						frappe.db.set_value("Labour Attendance",lab_att_doc.name,"total_worked_hrs",(frappe.get_value("Labour Attendance",{"name":lab_att_doc.name},["total_worked_hrs"]) + i.total_working_hours))
						frappe.db.set_value("Labour Detail",j.name,"rate_work_hrs",(frappe.get_value("Labour Detail",{"parent":lab_att_doc.name,"labourer":i.labourer},["rate_work_hrs"]) + i.total_working_hours))
						lab_details = frappe.db.get_value("Labour Detail",{"parent":lab_att_doc.name},["working_hours","ot_hours","f_and_f_hrs","rate_work_hrs","sum_of_working_hrs","total_worked_hours"],as_dict = 1)
						frappe.db.set_value("Labour Detail",j.name,"total_worked_hours",(lab_details.f_and_f_hrs + lab_details.rate_work_hrs))
						frappe.db.set_value("Labour Detail",j.name,"balance_hrs",(lab_details.sum_of_working_hrs - (lab_details.f_and_f_hrs + lab_details.rate_work_hrs)))				
						if ((lab_details.sum_of_working_hrs) - (lab_details.f_and_f_hrs + lab_details.rate_work_hrs)) < 0:
							frappe.throw(_("Working hours for the labourer is Exceeded"))
						else:
							pass

	def total_hours_in_lab_attendance_on_cancel(self):
		if (self.labour_type == "Muster Roll"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"attendance_type":"Muster Roll"},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
				self.labour_attendance = lab_att_doc.name
				for j in lab_att_doc.muster_roll_detail:
					if j.muster_roll == i.muster_roll:
						frappe.db.set_value("Muster Roll Detail",j.name,"total_worked_hours",frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name,"muster_roll":i.muster_roll},["total_worked_hours"]) - i.total_working_hours)
						muster_roll_det = frappe.db.get_value("Muster Roll Detail",{"parent":lab_att_doc.name},["total_working_hours","total_worked_hours","balance_hours"],as_dict=1)
						frappe.db.set_value("Muster Roll Detail",j.name,"balance_hours",(muster_roll_det.total_working_hours - muster_roll_det.total_worked_hours))					
			
		if (self.working_details and self.labour_type == "F and F"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor"},["name"])
				lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
				lab_att_doc.total_worked_hrs = 0
				for j in lab_att_doc.labour_details:
					if i.labourer == j.labourer:
						frappe.db.set_value("Labour Detail",j.name,"f_and_f_hrs",(frappe.get_value("Labour Detail",{"parent":lab_att_doc.name,"labourer":i.labourer},["f_and_f_hrs"]) - i.total_working_hours))						
						frappe.db.set_value("Labour Attendance",lab_att_doc.name,"total_worked_hrs",(frappe.get_value("Labour Attendance",{"name":lab_att_doc.name},["total_worked_hrs"]) - i.total_working_hours))
						lab_details = frappe.db.get_value("Labour Detail",{"parent":lab_att_doc.name},["working_hours","ot_hours","f_and_f_hrs","rate_work_hrs","sum_of_working_hrs","total_worked_hours"],as_dict = 1)
						frappe.db.set_value("Labour Detail",j.name,"total_worked_hours",(lab_details.f_and_f_hrs + lab_details.rate_work_hrs))						
						frappe.db.set_value("Labour Detail",j.name,"balance_hrs",(lab_details.sum_of_working_hrs - (lab_details.f_and_f_hrs + lab_details.rate_work_hrs)))				
						
		if (self.working_details and self.labour_type == "Rate Work"):
			for i in self.working_details:
				lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor"},["name"])				
				lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)				
				lab_att_doc.total_worked_hrs = 0
				for j in lab_att_doc.labour_details:
					if i.labourer == j.labourer:
						frappe.db.set_value("Labour Detail",j.name,"rate_work_hrs",(frappe.get_value("Labour Detail",{"parent":lab_att_doc.name,"labourer":i.labourer},["rate_work_hrs"]) - i.total_working_hours))					
						frappe.db.set_value("Labour Attendance",lab_att_doc.name,"total_worked_hrs",(frappe.get_value("Labour Attendance",{"name":lab_att_doc.name},["total_worked_hrs"]) - i.total_working_hours))						
						lab_details = frappe.db.get_value("Labour Detail",{"parent":lab_att_doc.name},["working_hours","ot_hours","f_and_f_hrs","rate_work_hrs","sum_of_working_hrs","total_worked_hours"],as_dict = 1)	
						frappe.db.set_value("Labour Detail",j.name,"total_worked_hours",(lab_details.f_and_f_hrs + lab_details.rate_work_hrs))						
						frappe.db.set_value("Labour Detail",j.name,"balance_hrs",(lab_details.sum_of_working_hrs - (lab_details.f_and_f_hrs + lab_details.rate_work_hrs)))				
				
	def update_status_in_lab_attendance(self):
		if self.labour_type != "Muster Roll":
			lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor","docstatus":1},["name"])			
			lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)			
			if lab_att_doc.labour_details:
				balance_hours = 0
				ot_hours = 0
				f_and_f_hrs = 0
				rate_work_hrs = 0
				for i in lab_att_doc.labour_details:
					balance_hours += i.balance_hrs
					ot_hours += i.ot_hours
					f_and_f_hrs += i.f_and_f_hrs
					rate_work_hrs += i.rate_work_hrs
				if  f_and_f_hrs == 0 and rate_work_hrs == 0:
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Not Started")
				elif balance_hours == 0:
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Completed")
				elif ((f_and_f_hrs + rate_work_hrs) != 0 and (f_and_f_hrs + rate_work_hrs) < lab_att_doc.total_working_hours):
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","In Progress")

		if self.labour_type == "Muster Roll":
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			if lab_att_doc.muster_roll_detail:
				balance_hours = 0
				total_worked_hours = 0
				for m in lab_att_doc.muster_roll_detail:
					balance_hours += m.balance_hours
					total_worked_hours += m.total_worked_hours
				if m.total_worked_hours == 0:
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Not Started")
				elif balance_hours == 0:
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Completed")
				elif (total_worked_hours != 0 and balance_hours != 0 and total_worked_hours < balance_hours):
						frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","In Progress")

	def update_status_in_lab_attendance_cancel(self):
		if self.labour_type != "Muster Roll":
			lab_att_name = frappe.get_value("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"subcontractor":self.subcontractor,"attendance_type":"Subcontractor"},["name"])
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			if lab_att_doc.labour_details:
				balance_hours = 0
				ot_hours = 0
				f_and_f_hrs = 0
				rate_work_hrs = 0
				for i in lab_att_doc.labour_details:
					balance_hours += i.balance_hrs
					ot_hours += i.ot_hours
					f_and_f_hrs += i.f_and_f_hrs
					rate_work_hrs += i.rate_work_hrs
				if  f_and_f_hrs == 0 and rate_work_hrs == 0:
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Not Started")
				if balance_hours == 0:
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Completed")
				if ((f_and_f_hrs + rate_work_hrs) != 0 and (f_and_f_hrs + rate_work_hrs) < lab_att_doc.total_working_hours):
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","In Progress")

		if self.labour_type == "Muster Roll":
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			if lab_att_doc.muster_roll_detail:
				balance_hours = 0
				total_worked_hours = 0
				for m in lab_att_doc.muster_roll_detail:
					balance_hours += m.balance_hours
					total_worked_hours += m.total_worked_hours
				if total_worked_hours == 0:
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Not Started")
				elif balance_hours == 0:
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","Completed")
				elif (total_worked_hours != 0):
					frappe.db.set_value("Labour Attendance",lab_att_doc.name,"status","In Progress")

	def labour_attendance_validate(self):
		if self.labour_type == "F and F":
			if not frappe.db.exists("Labour Attendance",{"project":self.project_name,"subcontractor":self.subcontractor,"posting_date":self.posting_date,"docstatus":1}):
				frappe.throw(_("Labour Attendance is NOT PRESENT in the given Date"))
		elif self.labour_type == "Rate Work":
			if not frappe.db.exists("Labour Attendance",{"project":self.project_name,"subcontractor":self.subcontractor,"posting_date":self.posting_date,"docstatus":1}):
				frappe.throw(_("Labour Attendance is NOT PRESENT in the given Date"))
		elif self.labour_type == "Muster Roll":
			if not frappe.db.exists("Labour Attendance",{"project":self.project_name,"posting_date":self.posting_date,"docstatus":1}):
				frappe.throw(_("Labour Attendance is NOT PRESENT in the given Date"))

	#Restriction For Labour Progress Entry
	def validate_for_late_lpe(self):
		noon = datetime.time(10,0,0)
		posting_date = datetime.datetime.strptime(str(self.posting_date), '%Y-%m-%d').date()
		cur_date = datetime.datetime.now().date()
		cur_time = datetime.datetime.now().time()
		if(self.is_late_lpe_entry != 1) and (posting_date !=  cur_date and cur_time >= noon):
			frappe.throw("Mark the entry as late,then try submitting.")

	def set_total_working_hrs(self):
		if(self.labour_type != "Muster Roll"):
			sum_of_working_hrs = frappe.db.sql(''' SELECT sum(sum_of_working_hrs) FROM `tabLabour Detail` ld WHERE ld.parent = %s''',(self.labour_attendance))[0][0]			              
			ot_hours = frappe.db.sql(''' SELECT	 sum(ot_hours) FROM `tabLabour Detail` ld  WHERE ld.parent = %s''',(self.labour_attendance))[0][0]
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_working_hours",sum_of_working_hrs)
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_ot_hours",ot_hours)

		elif(self.labour_type == "Muster Roll"):
			total_working_hrs = frappe.db.sql(''' SELECT sum(total_working_hours)FROM `tabMuster Roll Detail` mr WHERE mr.parent = %s''',(self.labour_attendance))[0][0]
			ot_hours = frappe.db.sql(''' SELECT sum(ot_hours) ot_hrs FROM `tabMuster Roll Detail` mr WHERE mr.parent = %s''',(self.labour_attendance))[0][0]		
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_working_hours",total_working_hrs)
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_ot_hours",ot_hours)


#create muster roll entry
@frappe.whitelist()
def create_muster_role_entry(docname):
	mre_doc = frappe.new_doc("Muster Roll Entry")
	lpe_entry = frappe.get_doc("Labour Progress Entry",docname)
	mre_doc.update({
		"project":lpe_entry.project_name,
		"labour_type":lpe_entry.labour_type,
		"reference_doctype":"Labour Progress Entry",
		"reference_name":lpe_entry.name,
		"total_lpe_hours":lpe_entry.lpe_total_hours
		})

	mre_doc.append("labour_progress_details",{
		"labour_progress_entry":docname,
		"is_primary_labour":lpe_entry.is_primary_labour,
		"dates":lpe_entry.posting_date,
		"item_code":lpe_entry.labour,
		"project":lpe_entry.project_name,
		"project_structure":lpe_entry.project_structure,
		"total_hrs":lpe_entry.lpe_total_hours
		})
	return mre_doc

#create f and f entry
@frappe.whitelist()
def create_f_and_f_entry(docname):
	ff_doc = frappe.new_doc("F and F Entry")
	lpe_doc = frappe.get_doc("Labour Progress Entry",docname)
	lwo_name = frappe.get_value("Labour Work Order",{"labour_type":lpe_doc.labour_type,"subcontractor":lpe_doc.subcontractor},["name"])
	lwo_price_list = frappe.get_value("Labour Work Order",{"labour_type":lpe_doc.labour_type,"subcontractor":lpe_doc.subcontractor},["price_list"])

	ff_doc.update({
		"project":lpe_doc.project_name,
		"labour_type":lpe_doc.labour_type,
		"subcontractor":lpe_doc.subcontractor,
		"reference_doctype":"Labour Progress Entry",
		"reference_name":lpe_doc.name,
		"labour_work_order":lwo_name,
		"price_list":lwo_price_list,
		"total_hours_lpe":lpe_doc.lpe_total_hours

	})
	for i in lpe_doc.working_details:
		ff_doc.append("labour_progress_details",{
			"labour_progress_entry":docname,
			"is_primary_labour":lpe_doc.is_primary_labour,
			"dates":lpe_doc.posting_date,
			"project":lpe_doc.project_name,
			"project_structure":lpe_doc.project_structure,
			"total_hrs":i.total_working_hours,
			"no_of_person":i.no_of_person,
			"labourer":i.labourer,
			"working_details_name":i.name

	})
	return ff_doc

@frappe.whitelist()
def create_rate_work_entry(docname):
	rwe_doc = frappe.new_doc("Rate Work Entry")
	lpe_doc = frappe.get_doc("Labour Progress Entry",docname)
	lwo_name = frappe.get_value("Labour Work Order",{"labour_type":lpe_doc.labour_type,"subcontractor":lpe_doc.subcontractor},["name"])
	lwo_price_list = frappe.get_value("Labour Work Order",{"labour_type":lpe_doc.labour_type,"subcontractor":lpe_doc.subcontractor},["price_list"])
	rwe_doc.update({
		"labour_type":lpe_doc.labour_type,
		"project":lpe_doc.project_name,
		"subcontractor":lpe_doc.subcontractor,
		"reference_doctype":"Rate Work Entry",
		"reference_name":lpe_doc.name,
		"labour_work_order":lwo_name,
		"price_list":lwo_price_list,
		})
	rwe_doc.append("labour_progress_work_details",{
		"labour_progress_entry":lpe_doc.name,
		"is_primary_labour":lpe_doc.is_primary_labour,
		"labour_work":lpe_doc.labour,
		"qty":lpe_doc.total_qty
		})
	return rwe_doc

@frappe.whitelist()
def get_labourer_details(project,posting_date,subcontractor,labour_type):
	if labour_type != "Muster Roll":
		lab_att_name = frappe.get_value("Labour Attendance",{"project":project,"posting_date":posting_date,"subcontractor":subcontractor,"attendance_type":"Subcontractor","docstatus":1,"status":["!=","Completed"]},["name"])
		if lab_att_name:
			lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
			lab_detail = []
			for l in lab_att_doc.labour_details:
				lab_detail.append({
					"labourer":l.labourer,
					"no_of_person":l.qty,
					"balance_hours":l.balance_hrs
					})
		else:
			frappe.throw(_("Attendance is NOT PRESENT for given posting date"))
		return lab_detail

	if labour_type == "Muster Roll":
		lab_att_name = frappe.get_value("Labour Attendance",{"project":project,"posting_date":posting_date,"attendance_type":"Muster Roll","docstatus":1},["name"])
		if lab_att_name:
			lab_att_doc = frappe.get_doc("Labour Attendance",lab_att_name)
			lab_detail = []
			for l in lab_att_doc.muster_roll_detail:
				lab_detail.append({
					"muster_roll":l.muster_roll,
					"working_hours":l.working_hours,
					"no_of_person":1,
					"balance_hours":l.balance_hours
					})
		else:
			frappe.throw(_("Attendance is NOT PRESENT for given posting date"))
		return lab_detail

@frappe.whitelist()
def make_grids(items,boq_detail):
	boq_detail = eval(boq_detail)
	item = json.loads(items).get("items")	
	for g in item:
		for i in boq_detail:
			grid_doc = frappe.new_doc("Grid")
			grid_doc.update({
			   "project":boq_detail["project"],
			   "grid_name":g["grid_name"]
		       })
		grid_doc.save(ignore_permissions = True)
	frappe.msgprint("Grid is Created Successfully")
@frappe.whitelist()
def get_uom(category):
	return frappe.db.get_list("UOM Conversion Factor",{'category':category},['to_uom'], pluck = 'to_uom' )

