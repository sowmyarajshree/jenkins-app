# -*- coding: utf-8 -*-
# Copyright (c) 2020, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import ceil, flt, floor

class OperatorEntry(Document):
	def validate(self):
		self.status = self.get_status()

		self.update_shots_value()
		#self.cal_planned_qty()
		#self.validate_planned_completed()
		self.update_workstation()
		#self.calculate_planned_shots_hrs()
		self.validate_negative_value_reasons()

	def on_submit(self):
		self.validate_workstation_shift()
		self.create_ledger_entries()
		self.validate_planned_completed()
		self.create_assembling_stockentry()

	def before_submit(self):
		self.calculate_avg_value()
		self.total_hour_output_cal()
		self.calculate_avg_total_ideal_time()
		self.calculate_avg_hours_ideal()
		self.validate_operator_name()
		self.validate_pdc_total_hrs_worked()
		self.cal_planned_actual_machining()
		self.validate_pallets_machining()
		self.update_planned_actual_machining()
		self.validate_bom_status()


	def on_cancel(self):
		self.status = self.get_status()
		#self.unlink_operation_ideal_entry()


	def before_save(self):
		self.calculate_production_value()
		self.cal_planned_qty()
		self.update_shots_value()
		self.cal_total_planned_shots()
		self.cal_total_actual_shots()
		#self.cal_planned_actual_machining()
		#self.update_planned_actual_machining()
		#self.validate_planned_completed()
		self.cal_planned_actual_machining_on_save()
		self.calculate_planned_shots_hrs()

#update status based on docstatus
	def get_status(self):
		if self.docstatus == 0:
			status = "Draft"
		elif self.docstatus == 1:
			status = "Submitted"
		elif self.docstatus == 2:
			status = "Cancelled"
		return status

#calculate production_value and value based on with and without operation
	def calculate_production_value(self):
		self.production_value = 0
		for d in self.operation_details:
			if d.completed_qty and self.operation != "PDC":
				d.value = d.completed_qty * d.operation_cost
				self.production_value += d.value
			if d.completed_qty and self.operation == "PDC":
				raw_material_cost = frappe.get_value("BOM",{"name":d.bom_no},["raw_material_cost"])
				operation_cost = frappe.get_value("BOM",{"name":d.bom_no},["operation_cost"])
				cost = raw_material_cost + operation_cost
				d.value = d.completed_qty * cost
				self.production_value += d.value


#validates workstation against shift and posting_date
	def validate_workstation_shift(self):
		if frappe.db.count("Operator Entry",{"posting_date":self.posting_date,"workstation":self.workstation,"shift_type":self.shift_type,"docstatus":1}) > 1:
			frappe.throw("Operator Entry for workstation already exist")
		else:
			pass

#calculate shots values for PDC
	def update_shots_value(self):
		if self.operation == "PDC":
			total_hours = self.total_hours / 60
			for d in self.operation_details:
				if d.production_allocation:
					d.actual_shots = d.completed_qty / d.cavity_value
					d.planned_shots = ceil(((total_hours * int(d.hours_worked))/8) * d.hour_output)
					d.rejected_shots = d.rejected_qty / d.cavity_value

#validate completed_qty against planned_qty
	def validate_planned_completed(self):
		if self.operation == "PDC":
			for d in self.operation_details:
				if d.completed_qty > d.planned_qty:
					frappe.throw(_("Completed Qty {0} cannot be greater than Planned Qty {1} at row {2}").format(d.completed_qty,d.planned_qty,d.idx))
			if self.total_actual_shots > self.total_planned_shots:
				frappe.throw(_("Total Actual Shots {0} cannot be greater than Total Planned Shots {1}").format(self.total_actual_shots,self.total_planned_shots))

		if self.operation == "MACHINING":
			for d in self.operation_details:
				if d.completed_qty > d.planned_qty:
					frappe.throw(_("Completed Qty {0} cannot be greater than Planned Qty {1} at row {2}").format(d.completed_qty,d.planned_qty,d.idx))
			if self.total_actual_qty > self.total_planned_qty:
				frappe.throw(_("Total Actual Qty {0} cannot be greater than Total Planned Qty {1}").format(self.total_actual_qty,self.total_planned_qty))

#calculate idx_count and avg_value
	def calculate_avg_value(self):
		self.idx_count = 0
		for op in self.operation_details:
			idx_count = frappe.db.count("Operation Details",{"parent":self.name,"idx":op.idx})
			self.idx_count += idx_count
		for d in self.ideal_details:
			if self.idx_count != 0:
				d.avg_value = d.hours_ideal / self.idx_count

#calculate total_hour_output
	def total_hour_output_cal(self):
		self.total_hour_output = 0
		total_hour_output = frappe.db.sql("""select sum(hour_output) as hour_output, parent from `tabOperation Details` where parent = %s """,self.name,as_dict=1)
		for i in total_hour_output:
			self.total_hour_output = i.hour_output

#update workstation in child tables
	def update_workstation(self):
		for d in self.operation_details:
			d.workstation = self.workstation
			d.posting_date = self.posting_date
			d.operation = self.operation
		for i in self.ideal_details:
			i.workstation = self.workstation
			i.posting_date = self.posting_date
			i.operation = self.operation


#update shots value from operation_details child table to ideal_details child table
	def update_ideal_details(self):
		for d in self.operation_details:
			for i in self.ideal_details:
				if i.item == d.item_code:
					idx_count = frappe.db.count("Ideal Details",{"parent":self.name,"item":i.item})
					if frappe.db.count("Ideal Details",{"parent":self.name,"item":i.item}) > 1:
						i.planned_shots = d.planned_shots/flt(idx_count)
						i.actual_shots = d.actual_shots/flt(idx_count)
						i.rejected_shots = d.rejected_shots/flt(idx_count)
						i.hour_output = d.hour_output/flt(idx_count)
					else:
						i.planned_shots = d.planned_shots
						i.actual_shots = d.actual_shots
						i.rejected_shots = d.rejected_shots
						i.hour_output = d.hour_output


#create Operation Details Entry and Ideal Details Entry for PDC
	def create_ledger_entries(self):
		if self.operation == "PDC":
			for d in self.operation_details:
				op_doc = frappe.new_doc("Operation Details Entry")
				op_doc.update({
					"posting_date": d.posting_date,
					"item_code": d.item_code,
					"operation": self.operation,
					"workstation": d.workstation,
					"shift_type": self.shift_type,
					"planned_shots": d.planned_shots,
					"actual_shots": d.actual_shots,
					"rejected_shots": d.rejected_shots,
					"hour_output": d.hour_output,
					"docstatus": 1,
					"status": "Submitted",
					"idx_count": self.idx_count,
					"operator_entry": self.name,
					"item_name": d.item_name,
					"total_ideal_time": d.avg_total_ideal_time,
					"efficiency": d.efficiency,
					"rejection": d.rejection,
					"completed_qty": d.completed_qty,
					"rejected_qty": d.rejected_qty,
					"planned_qty": d.planned_qty,
					"operator_name": d.operator_name,
					"employee_name": d.employee_name,
					"operation_time": d.avg_consumed_time
				})
				op_doc.save(ignore_permissions=True)
			for i in self.ideal_details:
				id_doc = frappe.new_doc("Ideal Details Entry")
				id_doc.update({
					"delay_reasons" : i.delay_reasons,
					"item" :i.item,
					"operation": self.operation,
					"workstation":i.workstation,
					"shift_type":self.shift_type,
					"avg_value":i.avg_value,
					"hours_ideal":i.hours_ideal,
					"posting_date":i.posting_date,
					"docstatus": 1,
					"status":"Submitted",
					"idx_count":self.idx_count,
					"operator_entry": self.name
				})
				id_doc.save(ignore_permissions=True)

#unlink operator_entry name from Operation Details Entry and Ideal Details Entry
	def unlink_operation_ideal_entry(self):
		operation_details_entry = frappe.get_list("Operation Details Entry",{"operator_entry": self.name},["name"])
		ideal_details_entry = frappe.get_list("Ideal Details Entry",{"operator_entry": self.name},["name"])
		for d in operation_details_entry:
			op_doc = frappe.get_doc("Operation Details Entry",d.name)
			op_doc.docstatus = 2
			op_doc.operator_entry = None
			op_doc.save(ignore_permissions=True)
			frappe.delete_doc("Operation Details Entry",op_doc.name)
		for i in ideal_details_entry:
			id_doc = frappe.get_doc("Ideal Details Entry",i.name)
			id_doc.docstatus = 2
			id_doc.operator_entry = None
			id_doc.save(ignore_permissions=True)
			frappe.delete_doc("Ideal Details Entry",id_doc.name)

#function for calculating average consumed time, efficiency, rejection in Ideal Details table
	def calculate_avg_total_ideal_time(self):
		self.ideal_idx = 0
		'''self.distinct_idx_count = 0
		idx_count = frappe.db.sql("""select count(distinct item_code) as idx_count, parent from `tabOperation Details` where parent = %s """,self.name,as_dict=1)
		for i in idx_count:
			self.distinct_idx_count = i.idx_count'''
		for i in self.ideal_details:
			ideal_idx = frappe.db.count("Ideal Details",{"parent":self.name,"idx":i.idx})
			self.ideal_idx += ideal_idx
		for d in self.operation_details:
			try:
				#d.avg_total_ideal_time = self.total_ideal_time / self.distinct_idx_count
				d.avg_consumed_time = self.operation_time / self.idx_count
				d.efficiency = (d.actual_shots / d.planned_shots) * 100
				d.rejection = (d.rejected_shots / d.actual_shots) * 100
			except ZeroDivisionError:
				#d.avg_total_ideal_time = 0
				d.avg_consumed_time = 0
				d.efficiency = 0
				d.rejection = 0

#function for calculation average total hours in operation details table
	def calculate_avg_hours_ideal(self):
		idx_count = frappe.db.sql("""select count(distinct item_code) as idx_count, parent from `tabOperation Details` where parent = %s """,self.name,as_dict=1)
		for i in idx_count:
			self.distinct_idx_count = i.idx_count
		for k in self.operation_details:
			k.avg_total_ideal_time = self.total_ideal_time / self.distinct_idx_count
			if k.completed_qty != 0 and k.planned_qty != 0:
				k.efficiency_others = (k.completed_qty / k.planned_qty) * 100
			if k.rejected_qty != 0 and k.completed_qty != 0:
				k.rejection_others = (k.rejected_qty / k.completed_qty) * 100
			if self.operation_time != 0:
				k.avg_consumed_time = self.operation_time / self.idx_count
		for d in self.ideal_details:
			d.avg_hours_ideal = d.hours_ideal / self.distinct_idx_count


#calculating planned shot hours
	def calculate_planned_shots_hrs(self):
		self.planned_shots_hrs = 0.0
		if self.operation == "PDC":
			for d in self.operation_details:
				d.planned_shots_hrs = d.planned_shots / d.hour_output
				self.planned_shots_hrs += d.planned_shots_hrs * 60


	'''def validate_planned_shots_hrs(self):
		if self.operation == "PDC":
			less = self.total_hours - 12.9
			great = self.total_hours + 12.9
			if (self.total_hours - 12.9 < self.planned_shots_hrs < self.total_hours + 12.9):
				pass
			else:
				frappe.throw(_("Planned Shots Hours should be greater than {0} or less than {1}. Change the planned shots accrodingly").format(less,great))'''

#function to calculate planned qty for operation PDC
	def cal_planned_qty(self):
		if self.operation == "PDC":
			for d in self.operation_details:
				d.planned_qty = d.planned_shots * d.cavity_value

#update update planned qty based on pallet hours for operation machining
	def cal_planned_actual_machining(self):
		if self.operation == "MACHINING":
			total_pallet_hrs = 0
			total_pallet_hrs2 = 0
			total_pallet_hrs3 = 0
			total_pallet_hrs4 = 0
			for d in self.operation_details:
				pallet_1 = frappe.get_value("Operation Details",{"parent":self.name,"idx":d.pallet},["pallet"])
				wrked_hrs = frappe.get_value("Operation Details",{"parent":self.name,"idx":d.pallet},["hours_worked"])
				sum_palletset1 = frappe.db.sql("""select sum(time_in_mins) as time_in_mins_set1 from `tabOperation Details` where parent = %s and pallet in (2,1)""",(self.name),as_dict=1)
				sum_palletset2 = frappe.db.sql("""select sum(time_in_mins) as time_in_mins_set2 from `tabOperation Details` where parent = %s and pallet in (3,4)""",(self.name),as_dict=1)
				sum_palletset3 = frappe.db.sql("""select sum(time_in_mins) as time_in_mins_set3 from `tabOperation Details` where parent = %s and pallet in (3,1)""",(self.name),as_dict=1)
				sum_palletset4 = frappe.db.sql("""select sum(time_in_mins) as time_in_mins_set4 from `tabOperation Details` where parent = %s and pallet in (2,4)""",(self.name),as_dict=1)
				pallet1 = frappe.get_value("Operation Details",{"parent":self.name,"pallet":1},["pallet"])
				pallet2 = frappe.get_value("Operation Details",{"parent":self.name,"pallet":2},["pallet"])
				pallet3 = frappe.get_value("Operation Details",{"parent":self.name,"pallet":3},["pallet"])
				pallet4 = frappe.get_value("Operation Details",{"parent":self.name,"pallet":4},["pallet"])
				for p in sum_palletset1:
					#frappe.msgprint(_("Total pallet hrs sql {0}").format(p.time_in_mins_set1))
					total_pallet_hrs = p.time_in_mins_set1
				for q in sum_palletset2:
					#frappe.msgprint(_("Total pallet hrs sql {0}").format(q.time_in_mins_set2))
					total_pallet_hrs2 = q.time_in_mins_set2
				for i in sum_palletset3:
					#frappe.msgprint(_("Total pallet hrs sql {0}").format(i.time_in_mins_set3))
					total_pallet_hrs3 = i.time_in_mins_set3
				for s in sum_palletset4:
					#frappe.msgprint(_("Total pallet hrs sql {0}").format(s.time_in_mins_set4))
					total_pallet_hrs4 = s.time_in_mins_set4

				if d.pallet == "No Pallet":
					d.planned_qty = ceil(((flt(self.total_hours) * flt(d.hours_worked))/8) / flt(d.time_in_mins))
				#elif ( (int(d.pallet) != d.idx) and (d.idx == int(pallet_1)) ):
				elif (((d.pallet == pallet1) and (d.idx == 3))  or ((d.pallet == pallet3) and (d.idx == 1))):
					#if int(d.hours_worked) == int(wrked_hrs):
					frappe.msgprint(_("Total pallet hrs {0}").format(total_pallet_hrs3))
					frappe.msgprint(_("Total hrs {0}").format(self.total_hours))
					d.planned_qty = ceil(((self.total_hours * flt(d.hours_worked)/8)) / flt(total_pallet_hrs3))
					frappe.msgprint(_("Planned Qty {0} at row {1}").format(d.planned_qty,d.idx))

				elif (((d.pallet == pallet1) and (d.idx == 2)) or ((d.pallet == pallet2) and (d.idx == 1))):
					frappe.msgprint(_("Total pallet hrs {0}").format(total_pallet_hrs))
					frappe.msgprint(_("Total hrs {0}").format(self.total_hours))
					d.planned_qty = ceil(((self.total_hours * flt(d.hours_worked)/8)) / flt(total_pallet_hrs))
					frappe.msgprint(_("Planned Qty {0} at row {1}").format(d.planned_qty,d.idx))

				elif (((d.pallet == pallet2) and (d.idx == 4)) or ((d.pallet == pallet4) and (d.idx == 2))):
					frappe.msgprint(_("Total pallet hrs {0}").format(total_pallet_hrs4))
					frappe.msgprint(_("Total hrs {0}").format(self.total_hours))
					d.planned_qty = ceil(((self.total_hours * flt(d.hours_worked)/8)) / flt(total_pallet_hrs4))
					frappe.msgprint(_("Planned Qty {0} at row {1}").format(d.planned_qty,d.idx))

				elif (((d.pallet == pallet3) and (d.idx == 4)) or ((d.pallet == pallet4) and (d.idx == 3))):
					frappe.msgprint(_("Total pallet hrs {0}").format(total_pallet_hrs2))
					frappe.msgprint(_("Total hrs {0}").format(self.total_hours))
					d.planned_qty = ceil(((self.total_hours * flt(d.hours_worked)/8)) / flt(total_pallet_hrs2))
					frappe.msgprint(_("Planned Qty {0} at row {1}").format(d.planned_qty,d.idx))

			frappe.msgprint("Completed one loop")


#update planned_qty value on save for operation Machining
	def cal_planned_actual_machining_on_save(self):
		if self.operation == "MACHINING":
			for d in self.operation_details:
				if d.pallet == "No Pallet":
					pass
				else:
					d.planned_qty = 0

#update planned_qty,actual_qty value for operation Machining
	def update_planned_actual_machining(self):
		if self.operation == "MACHINING":
			total_planned_qty = 0
			total_actual_qty = 0
			for d in self.operation_details:
				total_planned_qty += d.planned_qty
				total_actual_qty += d.completed_qty
			self.total_planned_qty = round(total_planned_qty)
			self.total_actual_qty = round(total_actual_qty)


#calculate planned_shots  for operation PDC
	def cal_total_planned_shots(self):
		if self.operation == "PDC":
			total_planned_by_shots = 0
			for d in self.operation_details:
				total_planned_by_shots += d.planned_shots
			self.total_planned_shots = total_planned_by_shots

#calculate total_actual_shots  for operation PDC
	def cal_total_actual_shots(self):
		if self.operation == "PDC":
			total_actual_by_actual_shots = 0
			for d in self.operation_details:
				total_actual_by_actual_shots += d.actual_shots
			self.total_actual_shots = total_actual_by_actual_shots


#validate if operator name is present or not
	def validate_operator_name(self):
		if self.operation == "PDC" or self.operation == "MACHINING":
			if self.operation_time > 0.0:
				for d in self.operation_details:
					if d.operator_name == None:
						frappe.throw("Operator Name is Required")
					else:
						pass

#validate hours ideal is negative or not
	def validate_negative_value_reasons(self):
		for d in self.ideal_details:
			if d.hours_ideal < 0:
				frappe.throw("Value cannot be negative")

#validate total_hrs worked for operation PDC
	def validate_pdc_total_hrs_worked(self):
		if self.operation == "PDC":
			total_hrs = 0
			for d in self.operation_details:
				total_hrs += int(d.hours_worked)
			if total_hrs > 8:
				frappe.throw("Total Hrs worked cannot be greater than 8")
			if total_hrs < 8:
				frappe.throw("Total Hrs worked cannot be lesser than 8")

#validate pallets for operation machining
	def validate_pallets_machining(self):
		if self.operation == "MACHINING":
			total_hrs = 0
			for d in self.operation_details:
				pallet_1 = frappe.get_value("Operation Details",{"parent":self.name,"idx":d.pallet},["pallet"])
				wrked_hrs = frappe.get_value("Operation Details",{"parent":self.name,"idx":d.pallet},["hours_worked"])
				if (d.pallet == "No Pallet"):
					total_hrs += flt(d.hours_worked)
					frappe.msgprint(_("All ok at row {0}").format(d.idx))
				elif( (int(d.pallet) != d.idx) and (d.idx == int(pallet_1)) ):
					if int(d.hours_worked) == int(wrked_hrs):
						total_hrs += flt(d.hours_worked)/ 2
					else:
						frappe.throw(_("Pallet is not ok at row {0}").format(d.idx))
				else:
					frappe.throw(_("Wrong pallet mentioned at row {0}").format(d.idx))
			if total_hrs != 8:
				frappe.throw("Total Hrs must be 8")


#validate whether the bom status is active or not
	def validate_bom_status(self):
		for d in self.operation_details:
			if d.bom_no:
				is_active = frappe.get_value("BOM",{"name":d.bom_no},["is_active"])
				is_default = frappe.get_value("BOM",{"name":d.bom_no},["is_default"])
				if is_default == 0 and is_active == 0:
					frappe.throw(_("BOM is Not Active at row {0}").format(d.idx))

#Create stock entry on submit of operator entry for Assembling operation
	def create_assembling_stockentry(self):
		if self.operation == "ASSEMBLING":
			for d in self.assembling_detail:
				doc = frappe.new_doc("Stock Entry")
				doc.stock_entry_type = "Assembling Transfer"
				doc.from_bom = 1
				doc.bom_no = d.bom
				doc.fg_completed_qty = d.qty
				doc.to_warehouse = d.target_warehouse
				doc.docstatus = 1
				doc.operator_entry = self.name
				bom_doc = frappe.get_doc("BOM",d.bom)
				for k in bom_doc.items:
					doc.append("items",{
									"item_code": k.item_code,
									"s_warehouse": d.source_warehouse,
									"qty": k.qty * d.qty
					})
				doc.append("items",{
								"item_code": d.item_code,
								"t_warehouse": d.target_warehouse,
								"qty": d.qty
				})
				doc.save(ignore_permissions=True)
				frappe.msgprint(_("Stock Entry {0} Created").format(doc.name))


#create finish entry(stock entry) from work order 
@frappe.whitelist()
def create_finish_entry(self,method):
	op_doc = frappe.get_doc("Operator Entry",self.name)
	for d in op_doc.operation_details:
		if d.work_order and d.completed_qty != 0:
			work_order = frappe.get_doc("Work Order",d.work_order)
			stock_entry = frappe.new_doc("Stock Entry")
			stock_entry.work_order = d.work_order
			stock_entry.stock_entry_type = "Manufacture"
			stock_entry.from_bom = 1
			stock_entry.bom_no = d.bom_no
			stock_entry.fg_completed_qty = d.completed_qty
			stock_entry.to_warehouse = work_order.fg_warehouse
			stock_entry.docstatus = 1
			stock_entry.operator_entry = op_doc.name
			bom_doc = frappe.get_doc("BOM",d.bom_no)
			#for i in work_order.required_items:
			for k in bom_doc.items:
				stock_entry.append("items",{
								"item_code": k.item_code,
								"s_warehouse": work_order.wip_warehouse,
								"qty": k.qty * d.completed_qty
				})
			stock_entry.append("items",{
							"item_code": work_order.production_item,
							"t_warehouse": work_order.fg_warehouse,
							"qty": d.completed_qty
			})
			stock_entry.save(ignore_permissions=True)
			frappe.msgprint(_("Finish Entry {0} Created").format(stock_entry.name))



#Cancel and delete stock entries created against operator entry
@frappe.whitelist()
def cancel_stock_entry(self,method):
	stock_entry_list = frappe.get_list("Stock Entry",filters={"operator_entry":self.operator_entry},fields=["name"])
	for d in stock_entry_list:
		doc = frappe.get_doc("Stock Entry",d.name)
		doc.docstatus = 2
		doc.save(ignore_permissions=True)
		frappe.delete_doc("Stock Entry",doc.name)
		frappe.msgprint(_("Stock Entry {0} cancelled").format(doc.name))
