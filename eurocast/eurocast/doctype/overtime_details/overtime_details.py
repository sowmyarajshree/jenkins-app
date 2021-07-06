# -*- coding: utf-8 -*-
# Copyright (c) 2021, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import frappe, re
from frappe.utils import getdate, flt
from datetime import datetime, date
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe import _

class OvertimeDetails(Document):
	def validate(self):
		self.autoname()
		self.validate_is_overtime()
		self.calculate_total_working_days()
		frappe.db.commit()

	def before_save(self):
		frappe.db.commit()

	def before_submit(self):
		self.validate_is_overtime()
		frappe.db.commit()
		#self.calculate_total_working_days()

	def on_submit(self):
		self.calculate_total_working_days()
		frappe.db.commit()

#make autoname based on ot_date and employee_id
	def autoname(self):
		self.name = str(getdate(self.ot_date)) + "-" +str(self.employee_id)

#validate is overtime
	def validate_is_overtime(self):
		if self.employee_id:
			salary_structure = frappe.get_value("Salary Structure Assignment",{"employee":self.employee_id},["salary_structure"])
			is_overtime = frappe.get_value("Salary Structure",{"name":salary_structure},["nx_is_overtime"])
			if is_overtime != "Yes":
				frappe.throw(_("Overtime is not allowed for this employee {0}").format(self.employee_id))
			else:
				pass



#calculate total working days
	def calculate_total_working_days(self):
		if self.ot_date:
			total_days = frappe.db.sql("""select DAY(LAST_DAY(%s)) total from `tabOvertime Details` where name = %s """,(self.ot_date,self.name),as_dict=1)
			holidays = frappe.get_list("Holiday List",{},["name","from_date","to_date"])
			month = getdate(self.ot_date).month
			days = 0
			total_working_days = 0

			for h in holidays:
				if getdate(self.ot_date) >= h.from_date and getdate(self.ot_date) <= h.to_date:
					holiday_list = frappe.get_doc("Holiday List",h.name)
					for k in holiday_list.holidays:
						if getdate(k.holiday_date).month == month:
							days += 1

			for d in total_days:
				total_working_days = d.total - days
			self.total_working_days = total_working_days
			frappe.db.commit()
			if self.employee_id:
				salary_structure = frappe.get_value("Salary Structure Assignment",{"employee":self.employee_id},["salary_structure"])
				salary_structure_assgnmnt = frappe.get_value("Salary Structure Assignment",{"employee":self.employee_id},["name"])
			
			if salary_structure_assgnmnt != None:
				salary_structure_assgnmnt_doc = frappe.get_doc("Salary Structure Assignment",salary_structure_assgnmnt)
				base_rate = salary_structure_assgnmnt_doc.base
				is_active_salary = frappe.get_value("Salary Structure",{"name":salary_structure},["is_active"])
				overtime_based_on = frappe.get_value("Salary Structure",{"name":salary_structure},["nx_overtime_based_on"])
				if is_active_salary == "Yes":
					self.base_rate = base_rate
					frappe.db.commit()
					for k in total_days:
						k_total_working_days = d.total - days
						if k_total_working_days != 0:
							if overtime_based_on == "Daily":
								self.per_hour_rate = base_rate / 8
								frappe.db.commit()
							if overtime_based_on == "Monthly":
								self.per_hour_rate = base_rate / k_total_working_days/ 8
								frappe.db.commit()
					ot_amount = flt(self.authorized_time) * flt(self.per_hour_rate)
					self.db_set('ot_amount', ot_amount)
					self.ot_amount = ot_amount
					frappe.db.commit()

			frappe.db.commit()
						#frappe.db.sql("""update `tabOvertime Details` set ot_amount = %s where name = %s""",(ot_amount,self.name))

