from __future__ import unicode_literals
import frappe
import datetime
from datetime import timedelta
from frappe import _
from frappe import utils
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe.utils import (flt, cint, time_diff_in_hours, get_datetime, getdate,
	get_time, add_to_date, time_diff, add_days, get_datetime_str,now_datetime, ceil)
from erpnext.manufacturing.doctype.manufacturing_settings.manufacturing_settings import get_mins_between_operations


#creates job cards on_submit
@frappe.whitelist()
def create_job_cards(self,method):
	for d in self.operation_details:
		if d.completed_qty != 0:
			operation_id = frappe.db.get_value("Work Order Operation",{"parent":d.work_order},["name"])
			if d.work_order:
				if frappe.db.get_value("Job Card",{"operator_entry":self.name,"idx_no":d.idx},["idx_no"]) != d.idx:
					job_card = frappe.new_doc("Job Card")
					job_card.work_order = d.work_order
					job_card.workstation = self.workstation
					job_card.operation = self.operation
					job_card.for_quantity = d.for_quantity
					job_card.wip_warehouse = d.wip_warehouse
					job_card.posting_date = self.posting_date
					job_card.docstatus = 1
					job_card.employee = d.operator_name
					job_card.operator_entry = self.name
					job_card.idx_no = d.idx
					job_card.total_time_in_mins = d.total_time_
					job_card.operation_id = operation_id
					job_card.append("time_logs",{
							"shift_type": self.shift_type,
		                    "from_time": d.start_time,
		                    "to_time": d.end_time,
		                    "completed_qty": d.completed_qty,
							"time_in_mins": d.total_time_,
							"rejected_qty": d.rejected_qty
					})
					job_card.save(ignore_permissions=True)
					frappe.msgprint(_("Job Card {0} Created").format(job_card.name))
					'''jb = frappe.get_value("Job Card",{"operator_entry":self.name},["name"])
					d.job_card_no = jb
					self.save()'''

#cancels job_card on canceling operator_entry
@frappe.whitelist()
def on_cancel_op(self,method):
	for d in self.operation_details:
		job_card_list = frappe.get_list("Job Card",filters={"work_order":d.work_order,"docstatus":1,"operator_entry":self.name},fields=["name"])
		for j in job_card_list:
			doc = frappe.get_doc("Job Card",j.name)
			doc.docstatus = 2
			doc.save(ignore_permissions=True)
			frappe.msgprint(_("Job card {0} cancelled").format(doc.name))
			frappe.delete_doc("Job Card",doc.name)

#updates the operations child table in work_order based on the values from job_card
@frappe.whitelist()
def update_wo_op(self,method):
	doc = frappe.get_doc("Work Order",self.work_order)
	completed_qty = frappe.db.get_value("Job Card Time Log",{"parent":self.name},["completed_qty"])
	for j in self.time_logs:
		if j.completed_qty:
			doc.operator_entry = self.operator_entry
			for d in doc.operations:
				d.completed_qty += completed_qty
				d.time_in_mins = j.time_in_mins
				d.actual_operation_time = self.total_time_in_mins
				d.planned_start_time = j.from_time
				d.planned_end_time = j.to_time
				d.actual_start_time = j.from_time
				d.actual_end_time = j.to_time
				if d.completed_qty < doc.qty:
					d.status = "Pending"
				if d.completed_qty == doc.qty:
					d.status = "Completed"

#validates job_card entries based on the operator_entry
@frappe.whitelist()
def validate_jb(self,method):
	doc = frappe.db.get_value("Operator Entry",{"name":self.operator_entry},["name"])
	docm = frappe.get_doc("Operator Entry",doc)
	for d in docm.operation_details:
		if frappe.db.count("Job Card",{"operator_entry":docm.name,"idx_no":d.idx}) > 1:
			frappe.throw("Duplicate Job Card Entry")


#updates operations child table in work_order on_cancel of operator_entry
@frappe.whitelist()
def update_wo_ops(self,method):
	doc = frappe.get_doc("Work Order",self.work_order)
	completed_qty = frappe.db.get_value("Job Card Time Log",{"parent":self.name},["completed_qty"])
	for j in self.time_logs:
		if(self.docstatus) == 2:
			for d in doc.operations:
				if self.operation == d.operation:
					#doc.produced_qty -= completed_qty
					d.completed_qty -= completed_qty
					d.status = "Pending"
					doc.save(ignore_permissions=True)


#on deleting operator_entry it removes the operator_entry field value from work_order
@frappe.whitelist()
def on_trash_op(self,method):
	for d in self.operation_details:
		doc = frappe.get_doc("Work Order",d.work_order)
		doc.operator_entry = None
		doc.save(ignore_permissions=True)


#validates completed_qty against for_quantity
@frappe.whitelist()
def val_comp_qty(self,method):
	for d in self.operation_details:
		if d.completed_qty > d.for_quantity:
			frappe.throw("Completed Qty cannot be greater than Qty to manufacture")

#formatting start_time and end_time in operator_entry
@frappe.whitelist()
def time_calculation(self,method):
	self.start_time = self.start_time+":"+"00"
	self.end_time = self.end_time+":"+"00"


#updates time_in_mins field in child table based on production_allocation and bom_no
@frappe.whitelist()
def get_bom_time(self,method):
	for d in self.operation_details:
		if self.operation == "PDC":
			hour_output = frappe.db.get_value("Production Allocation",{"name":d.production_allocation},["hour_output"])
			d.time_in_mins = round((60 / (d.hour_output * d.cavity_value)),2)
		if self.operation == "MACHINING":
			cycle_time = frappe.db.get_value("Production Allocation",{"name":d.production_allocation},["cycle_time"])
			d.time_in_mins = cycle_time
			if d.pallet == "No Pallet":
				d.planned_qty = ceil(((self.total_hours * flt(d.hours_worked))/8) / d.time_in_mins)
		else:
			operation_time = frappe.db.get_value("BOM Operation",{"parent":d.bom_no},["time_in_mins"])
		d.total_time_ = (flt(d.time_in_mins) * flt(d.completed_qty))/60
		d.total_time_mins = flt(d.time_in_mins) * flt(d.completed_qty)

#this function calculates the consumed_time,difference_time and total_ideal_time in operator_entry
@frappe.whitelist()
def cal_time(self,method):
	if self.operation != "ASSEMBLING":
		self.consumed_time = 0.0
		self.total_ideal_time = 0.0
		self.operation_time = 0.0
		'''for d in self.operation_details:
			self.consumed_time += ceil(d.total_time_mins)
			self.operation_time += d.total_time_mins'''
		if self.operation == "PDC":
			for d in self.operation_details:
				self.operation_time += round((d.actual_shots / d.hour_output) * 60)
		else:
			for d in self.operation_details:
				self.operation_time += round(d.total_time_mins)
		for i in self.ideal_details:
			#self.consumed_time += i.hours_ideal
			self.total_ideal_time += i.hours_ideal
		self.consumed_time = self.operation_time + self.total_ideal_time
		self.difference_time = int(self.total_hours - self.consumed_time)


#this function calculates start time and end time in operation_details table
@frappe.whitelist()
def strt_end_cal(self,method):
	for d in self.operation_details:
		if d.idx == 1:
			d.total_hour = flt(d.start_hour) + flt(d.total_time_)
			d.start_time = self.posting_date +" "+ self.start_time
			t = self.time_ + d.total_hour
			j = t
			hour, minute = divmod(j, 1)
			minute *= 60
			end_time = int(minute)
			hour = int(hour)
			end_t = str(hour) + ":" + str(end_time) + ":" + "00"
			if d.total_hour == None:
				d.total_hour = 0.0
			if hour >= 24:
				d.end_time = add_to_date(self.posting_date,hours= hour, minutes = end_time)
			else:
				d.end_time = self.posting_date +" " + end_t
		if d.idx > 1:
			count = 1
			while count < d.idx :
				if d.idx > 1:
					str_time = frappe.get_value("Operation Details",{"parent":self.name,"idx":count},["total_hour"])
					start_time = frappe.get_value("Operation Details",{"parent":self.name,"idx":count},["end_time"])
					d.start_hour = str_time
					d.total_hour = flt(d.start_hour) + flt(d.total_time_)
					t = self.time_ + d.total_hour
					j = t
					hour, minute = divmod(j, 1)
					minute *= 60
					end_time = int(minute)
					hour = int(hour)
					end_t = str(hour) + ":" + str(end_time) + ":" +"00"
					if d.start_hour == None:
						d.start_hour = 0.0
					d.start_time = start_time
					if d.total_hour == None:
						d.total_hour = 0.0
					#d.end_time = utils.today() +" "+ end_t
					if hour >= 24:
						d.end_time = add_to_date(self.posting_date,hours= hour, minutes = end_time)
					else:
						d.end_time = self.posting_date +" " + end_t
					count += 1


#this function validates consumed_time against total_hours
@frappe.whitelist()
def val_difference_time(self,method):
	if self.operation == "PDC" or self.operation == "MACHINING":
		if self.consumed_time > self.total_hours:
			frappe.throw("Consumed time cannot be greater than total time")
		if (self.total_hours - self.consumed_time) == 0 or (self.total_hours - self.consumed_time) == 1 or (self.total_hours - self.consumed_time) == 2:
			pass
		else:
			frappe.throw("Difference Time is high")

#this function validates Job Card if its linked with operator_entry and throws error on_cancel
@frappe.whitelist()
def val_jb_op(self,method):
	op = frappe.get_doc("Operator Entry",self.operator_entry)
	if op.docstatus != 2:
		frappe.throw(_("Job Card is linked with {0} cannot cancel").format(op.name))


#this function updates the completed_qty in operator_entry child table to work_order produced_qty field
@frappe.whitelist()
def update_produced_qty(self,method):
	for d in self.operations:
		if d.completed_qty:
			self.produced_qty = d.completed_qty


'''@frappe.whitelist()
def update_operator_entry(self,method):
	if self.balance_qty:
		name = frappe.get_value("Operation Details",{"work_order":self.name},["parent"])
		op_doc = frappe.get_doc("Operator Entry",name)
		for d in op_doc.operation_details:
			d.balance_qty = self.balance_qty
			op_doc.save(ignore_permissions=True)'''
