 # Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class LabourAttendanceRevision(Document):
	def validate(self):
		self.validate_for_labour_revision_in()
		self.validate_hours_for_muster_roll()
		
	def before_submit(self):
		self.lab_attendance_in_out_calculation()
		self.set_total_working_hours()
		self.hours_validate()
		self.append_labourer_and_muster_roll()
		self.labour_attendance_creation_from_revision()
		

	def on_submit_after_update(self):
		#self.set_total_working_hours()
		pass

	def before_cancel(self):
		self.lab_attendance_in_out_calculation_cancel()
		self.set_total_working_hours()

#To append labourer and muster roll in the labour revision which is not exist in the child tables of the labour attendance
	def append_labourer_and_muster_roll(self):
		if (self.labour_attendance != None and self.revised_type == "Labour In"):
			labour_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			labourer = []
			muster_roll = []

	#For Subcontractor
			for l in labour_att_doc.labour_details:
				labourer.append(l.labourer)
			for r in self.labour_attendance_revision_item_sub:
				if r.labourer not in labourer:
					labour_att_doc.append("labour_details",{
							"labourer":r.labourer,
							"qty":r.no_of_person,
							"working_hours":r.total_hours,
							"revised_in_time":r.total_hours,
							"doctype":"Labour Detail",
							"sum_of_working_hrs":r.total_hours,
							"balance_hrs":r.total_hours,
							"parenttype":"Labour Attendance",
							"parentfield": "labour_details"
							})
					labour_att_doc.save(ignore_permissions = True)
					frappe.db.set_value("Labour Attendance", labour_att_doc.name, "total_working_hours",labour_att_doc.total_working_hours + r.total_hours)
					frappe.msgprint(_("Labourer Successfully Appended"))
			self.labour_attendance = labour_att_doc.name


	#For Muster Roll
			for l in labour_att_doc.muster_roll_detail:
				muster_roll.append(l.muster_roll)	
			for i in self.labour_attendance_revision_item_muster:							
				if i.muster_roll not in muster_roll:
					labour_att_doc.append("muster_roll_detail",{
							 "muster_roll": i.muster_roll,
				             "working_hours": 0,
				             "revised_in_time": i.total_hours,
				             "total_working_hours": i.total_hours,
				             "balance_hours": i.total_hours,
				             "doctype":"Muster Roll Detail",
				             "parenttype": "Labour Attendance",
							 "parentfield": "muster_roll_detail"
						})
					labour_att_doc.save(ignore_permissions = True)
					frappe.msgprint(_("Muster Roll Successfully Appended"))
			self.labour_attendance = labour_att_doc.name


#Create a new Labour Attendance if the Labour Revision has no Labour Attendance
	def labour_attendance_creation_from_revision(self):

	#For Subcontractor
		if (self.labour_attendance == None and self.attendance_type == "Subcontractor" and self.revised_type == "Labour In"):
					new_lab_att = frappe.new_doc("Labour Attendance")
					new_lab_att.update({
						"project":self.project,
						"attendance_type":self.attendance_type,
						"posting_date":self.posting_date,
						"subcontractor":self.subcontractor,
						"created_from":"Yes"
						})
					for i in self.labour_attendance_revision_item_sub:
						new_lab_att.append("labour_details",{
							"labourer":i.labourer,
							"qty":i.no_of_person,
							"working_hours":8,
							"revised_in_time":i.total_hours,
							"sum_of_working_hrs":i.total_hours,
							"balance_hrs":i.total_hours						
							})
					new_lab_att.save(ignore_permissions = True)
					new_lab_att.submit()
					self.labour_attendance = new_lab_att.name
					frappe.msgprint(_("Labour Attendance is created"))

	#For Muster Roll
		elif (self.labour_attendance == None and self.attendance_type == "Muster Roll" and self.revised_type == "Labour In"):
					new_lab_att = frappe.new_doc("Labour Attendance")
					new_lab_att.update({
						"project":self.project,
						"attendance_type":self.attendance_type,
						"posting_date":self.posting_date,
						"created_from":"Yes"
						})
					for i in self.labour_attendance_revision_item_muster:
						new_lab_att.append("muster_roll_detail",{
							    "muster_roll": i.muster_roll,
					            "working_hours": 0,
					            "revised_in_time": i.total_hours,
					            "total_working_hours": i.total_hours,
					            "balance_hours": i.total_hours,
					            "doctype":"Muster Roll Detail",
					            "parenttype": "Labour Attendance",
								"parentfield": "muster_roll_detail"				
							})

					new_lab_att.save(ignore_permissions = True)
					new_lab_att.submit()
					self.labour_attendance = new_lab_att.name
					frappe.msgprint(_("Labour Attendance is created"))

				
			

#update labour attendance according to the labour revision
	def lab_attendance_in_out_calculation(self):
		if (self.labour_attendance != None):
		#For Subcontractor
			lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			if (self.attendance_type == "Subcontractor" and self.revised_type == "Labour Out" ):
				for l in lab_att_doc.labour_details:
					for r in self.labour_attendance_revision_item_sub:
						if l.labourer == r.labourer:
							frappe.db.set_value("Labour Detail",l.name,"revised_out_person",(l.revised_out_person + r.no_of_person))
							frappe.db.set_value("Labour Detail",l.name,"revised_out_time",(frappe.db.get_value("Labour Detail",{"labourer":r.labourer},["revised_out_time"]) - r.total_hours))
							frappe.db.set_value("Labour Detail",l.name,"sum_of_working_hrs",(frappe.db.get_value("Labour Detail",{"labourer":r.labourer},["sum_of_working_hrs"]) - r.total_hours))
							frappe.db.set_value("Labour Detail",l.name,"balance_hrs",(frappe.db.get_value("Labour Detail",{"labourer":r.labourer},["sum_of_working_hrs"])))

			elif (self.attendance_type == "Subcontractor" and self.revised_type == "Labour In" ):
				for l in lab_att_doc.labour_details:				
					for r in self.labour_attendance_revision_item_sub:
						if l.labourer == r.labourer:
							frappe.db.set_value("Labour Detail",l.name,"revised_in_person",(frappe.db.get_value("Labour Detail",{"labourer":r.labourer},["revised_in_person"]) + r.no_of_person))
							frappe.db.set_value("Labour Detail",l.name,"revised_in_time",(frappe.db.get_value("Labour Detail",{"labourer":r.labourer},["revised_in_time"]) + r.total_hours))
							frappe.db.set_value("Labour Detail",l.name,"sum_of_working_hrs",(frappe.db.get_value("Labour Detail",{"labourer":r.labourer},["sum_of_working_hrs"]) + r.total_hours))
							frappe.db.set_value("Labour Detail",l.name,"balance_hrs",(frappe.db.get_value("Labour Detail",{"labourer":r.labourer},["sum_of_working_hrs"])))
										
		#For Muster Roll
			if (self.attendance_type == "Muster Roll" and self.revised_type == "Labour Out" ):
				labour_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
				for m in labour_att_doc.muster_roll_detail:
					for r in self.labour_attendance_revision_item_muster:
						if r.muster_roll == m.muster_roll:
							frappe.db.set_value("Muster Roll Detail",m.name,"revised_out_time",(frappe.db.get_value("Muster Roll Detail",{"muster_roll":r.muster_roll},["revised_out_time"]) - r.total_hours))
							frappe.db.set_value("Muster Roll Detail",m.name,"total_working_hours",(frappe.db.get_value("Muster Roll Detail",{"muster_roll":r.muster_roll},["total_working_hours"]) - r.total_hours))
							frappe.db.set_value("Muster Roll Detail",m.name,"balance_hours",(frappe.db.get_value("Muster Roll Detail",{"muster_roll":r.muster_roll},["total_working_hours"])))

			elif (self.attendance_type == "Muster Roll" and self.revised_type == "Labour In"):
				labour_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
				for m in labour_att_doc.muster_roll_detail:
					for r in self.labour_attendance_revision_item_muster:
						if r.muster_roll == m.muster_roll:
							frappe.db.set_value("Muster Roll Detail",m.name,"revised_in_time",(frappe.db.get_value("Muster Roll Detail",{"muster_roll":r.muster_roll},["revised_in_time"]) + r.total_hours))
							frappe.db.set_value("Muster Roll Detail",m.name,"total_working_hours",(frappe.db.get_value("Muster Roll Detail",{"muster_roll":r.muster_roll},["total_working_hours"]) + r.total_hours))
							frappe.db.set_value("Muster Roll Detail",m.name,"balance_hours",(frappe.db.get_value("Muster Roll Detail",{"muster_roll":r.muster_roll},["total_working_hours"])))

#Set Total Working Hours To The Labour Attendance
	def set_total_working_hours(self):
		if(self.labour_attendance !="" and self.attendance_type =="Subcontractor"):
			#lab_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
			sum_of_working_hrs = frappe.db.sql(''' SELECT sum(sum_of_working_hrs)
					              FROM
					                  `tabLabour Detail` ld
					              WHERE
					                  ld.parent = %s ''',(self.labour_attendance))[0][0]
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_working_hours",sum_of_working_hrs)
		
		elif(self.labour_attendance !="" and self.attendance_type != "Subcontractor"):
			total_working_hrs=frappe.db.sql(''' SELECT sum(total_working_hours)
								  FROM
								  	  `tabMuster Roll Detail` mr
								  WHERE
								  	   mr.parent=%s''',(self.labour_attendance))[0][0]
			frappe.db.set_value("Labour Attendance",self.labour_attendance,"total_working_hours",total_working_hrs)

#Update Labour Attendance After cancelling the related Labour Revision Document
	def lab_attendance_in_out_calculation_cancel(self):

	#For Muster Roll
		labour_att_doc = frappe.get_doc("Labour Attendance",self.labour_attendance)
		if (self.attendance_type == "Muster Roll" and self.labour_attendance !="" and self.revised_type == "Labour In"):
			for i in self.labour_attendance_revision_item_muster:
				muster_roll_detail = frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_in_time","working_hours","total_working_hours","balance_hours","ot_hours","revised_out_time","muster_roll","name"],as_dict=1)														
				#frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"total_working_hours",(muster_roll_detail.working_hours + muster_roll_detail.ot_hours  + frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_out_time"]) + frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_in_time"]) -i.total_hours))
				#frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"balance_hours",(muster_roll_detail.working_hours + muster_roll_detail.ot_hours  + frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_out_time"]) + frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_in_time"]) -i.total_hours - frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["total_worked_hours"])))
				frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"total_working_hours",(frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["total_working_hours"]) - i.total_hours))
				frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"balance_hours",(frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["balance_hours"]) - i.total_hours))
				frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"revised_in_time",(frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_in_time"]) - i.total_hours))
				#self.labour_attendance = None
				
		
		elif (self.attendance_type == "Muster Roll" and self.labour_attendance !="" and self.revised_type == "Labour Out"):
			for i in self.labour_attendance_revision_item_muster:
				muster_roll_detail = frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_in_time","working_hours","total_working_hours","balance_hours","ot_hours","revised_out_time","muster_roll","name"],as_dict=1)														
				#frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"total_working_hours",(muster_roll_detail.working_hours + muster_roll_detail.ot_hours + frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_in_time"]) + frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_out_time"]) + i.total_hours))
				#frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"balance_hours",(muster_roll_detail.working_hours + muster_roll_detail.ot_hours + frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_in_time"]) + frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_out_time"]) + i.total_hours - frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["total_worked_hours"]) ))
				#frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"revised_out_time",(frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_out_time"]) + i.total_hours))
				frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"total_working_hours",(frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["total_working_hours"]) + i.total_hours))
				frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"balance_hours",(frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["balance_hours"]) + i.total_hours))
				frappe.db.set_value("Muster Roll Detail",muster_roll_detail.name,"revised_out_time",(frappe.db.get_value("Muster Roll Detail",{"parent":self.labour_attendance,"muster_roll":i.muster_roll},["revised_out_time"]) + i.total_hours))

	#For Subcontractor
		elif (self.attendance_type == "Subcontractor" and self.labour_attendance !="" and self.revised_type =="Labour In"):
			for j in labour_att_doc.labour_details:
				for i in self.labour_attendance_revision_item_sub:
					if(i.labourer == j.labourer):
						frappe.db.set_value("Labour Detail",j.name,"revised_in_person",(j.revised_in_person - i.no_of_person))
						frappe.db.set_value("Labour Detail",j.name,"revised_in_time",(j.revised_in_time - i.total_hours))
						frappe.db.set_value("Labour Detail",j.name,"sum_of_working_hrs",(j.sum_of_working_hrs - i.total_hours))
						frappe.db.set_value("Labour Detail",j.name,"balance_hrs",frappe.db.get_value("Labour Detail",{"parent":labour_att_doc.name,"name":j.name},["sum_of_working_hrs"]))


		elif (self.attendance_type == "Subcontractor" and self.labour_attendance !="" and self.revised_type == "Labour Out"):
			for j in labour_att_doc.labour_details:
				for i in self.labour_attendance_revision_item_sub:
					if(i.labourer == j.labourer):
						frappe.db.set_value("Labour Detail",j.name,"revised_out_person",(j.revised_out_person - i.no_of_person))
						frappe.db.set_value("Labour Detail",j.name,"revised_out_time",(j.revised_out_time + i.total_hours))
						frappe.db.set_value("Labour Detail",j.name,"sum_of_working_hrs",(j.sum_of_working_hrs + i.total_hours))
						frappe.db.set_value("Labour Detail",j.name,"balance_hrs",frappe.db.get_value("Labour Detail",{"parent":labour_att_doc.name,"name":j.name},["sum_of_working_hrs"]))

#Validation for hours			
	def hours_validate(self):
		for i in self.labour_attendance_revision_item_muster:
			if i.hours == 0:
				frappe.throw(_("Hours field is required"))

#Validation For Labour Attendance Revision In#
	def validate_for_labour_revision_in(self):
		if(self.attendance_type == "Muster Roll" and self.revised_type == "Labour In"):
				lab_list = []
				for d in self.labour_attendance_revision_item_muster:
					if d.muster_roll not in lab_list:
						lab_list.append(d.muster_roll)
					else:
						frappe.throw("The Given Labourer/NMR is repeated")

	def validate_hours_for_muster_roll(self):
		if(self.attendance_type == "Muster Roll" and self.revised_type == "Labour In"):
			for d in self.labour_attendance_revision_item_muster:
				if (d.hours > 8 ):
					frappe.throw("Hour cannot be more than 8")
				elif (d.hours <=0):
					frappe.throw("Hours cannot be 0")

		