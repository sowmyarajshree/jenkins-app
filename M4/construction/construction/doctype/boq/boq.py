# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, add_days, nowdate
#from construction.construction.doctype.boq.boq import type_converter


class BOQ(Document):
	def validate(self):
		self.material_detail_validation()
		self.labour_detail_validation()
		self.calculate_lifting_amount()
		self.set_status()	
		self.boq_validation()
		self.other_taxes_and_charges_validation()
		self.total_other_taxes_and_charges_add()	
		self.qty_and_rate_convertion()
		self.additional_discount_amount_calculation()
		self.has_uom_valiation()
		self.boq_duplicate_validation_doc1()	

	def before_submit(self):
		self.set_billing_status()
		self.update_structure_level()


	def on_submit(self):
		self.create_labour_boq_ledger()
		self.create_material_boq_ledger()
		
	def before_cancel(self):
		self.set_status_on_cancel()
		self.validate_item()
		self.boq_cancel_variation()

	def on_update_after_submit(self):
		self.update_billing_status()
		self.update_boq_ledger()
		self.update_primary_task_qty()
		self.quotation_qty_after_qty_request()


	def before_insert(self):
		self.boq_duplicate_validation_doc0()

	def on_trash(self):
		self.delete_boq_ledger()
#append structure level name to project structure when the given structure level name is not in project Structure
	def update_structure_level(self):
		if(self.has_level):
			ps_doc = frappe.get_doc('Project Structure', self.project_structure)
			ps_doc.has_level = 1
			sld = []
			for i in ps_doc.structure_level_detail:
				sld.append(i.structure_level_name)
			if self.structure_level_name not in sld:
				ps_doc.append('structure_level_detail', 
					{'structure_level_name':self.structure_level_name}
					)
				ps_doc.save()

	def boq_cancel_variation(self):
		frappe.db.sql(''' update `tabBOQ Ledger` set is_cancelled = 1 where boq=%s''',self.name)
		frappe.db.commit()
		frappe.msgprint("BOQ Ledger is Successfully Cancelled")

		

	#to check the item work if it belongs to the given project
	def boq_duplicate_validation_doc1(self):
		if (self.has_level):
			if (frappe.db.exists("BOQ",{"project":self.project,"project_structure":self.project_structure,"item_of_work":self.item_of_work,"docstatus":1,"boq_type":self.boq_type,"structure_level_name":self.structure_level_name},["name"])):
				frappe.throw(_("Item of work for this Project and Project Structure is already exists"))

		else:
			if (frappe.db.exists("BOQ",{"project":self.project,"project_structure":self.project_structure,"item_of_work":self.item_of_work,"docstatus":1,"boq_type":self.boq_type},["name"])):
				frappe.throw(_("Item of work for this Project and Project Structure is already exists"))

	def boq_duplicate_validation_doc0(self):
		if (self.has_level):
			if (frappe.db.exists("BOQ",{"project":self.project,"project_structure":self.project_structure,"item_of_work":self.item_of_work,"docstatus":0,"boq_type":self.boq_type,"structure_level_name":self.structure_level_name},["name"])):
				frappe.throw(_("Item of work for this Project and Project Structure is already exists"))

		else:
			if (frappe.db.exists("BOQ",{"project":self.project,"project_structure":self.project_structure,"item_of_work":self.item_of_work,"docstatus":0,"boq_type":self.boq_type},["name"])):
				frappe.throw(_("Item of work for this Project and Project Structure is already exists"))
			
	#status related updates
	def set_billing_status(self):
		if (self.boq_type == "Tender"):
			self.billing_status = "To Quotation"
		if (self.boq_type == "Non Tender"):
			self.billing_status = "To Quotation"
		if (self.boq_type == "Non Claimable"):
			self.billing_status = "Not Billable"
		if(self.grand_total == 0):
			frappe.throw('Total Cannot be  zero')


	def set_status(self):
		if (self.docstatus == 0):
			self.status = "Draft"
		elif (self.docstatus == 1):
			self.status = "Submitted"
	def set_status_on_cancel(self):
		if ((self.docstatus == 2) and (self.task == None)):
			self.status = "Cancelled"
		else:
			frappe.throw(_("Cannot Be Cancelled, because for {0} task is created").format(self.name))


	def delete_boq_ledger(self):
		if self.docstatus == 2:
			for l in frappe.get_list("BOQ Ledger",{"boq":self.name},["name"]):
				frappe.delete_doc("BOQ Ledger",l.name)

    #value cannot be Zero calculation with parent field calculation
	def boq_validation(self):
		if (frappe.get_value("Project",{"name":self.project},["status"]) != "Open"):
			frappe.throw(_("Given Project name is Invalid"))
		self.est_total_qty = ((self.estimate_quantity  * self.quantity) + self.excess_quantity ) 
		
		if self.labour_detail:
			if self.has_conversion == 0:
				sum_of_total_work_qty = sum((d.qty_as_stock*self.est_total_qty) for d in self.labour_detail if d.has_measurement_sheet == "Yes")
				self.sum_of_total_work_qty = round(sum_of_total_work_qty,3)
			else:
				sum_of_total_work_qty = sum((l.qty_as_stock * self.converted_qty) for l in self.labour_detail if l.has_measurement_sheet == "Yes")
				self.sum_of_total_work_qty = round(sum_of_total_work_qty,3)

		self.bill_qty = self.est_total_qty
		self.qty_after_request = self.estimate_quantity
		self.total_material_and_labour_cost = self.total_material_cost + self.total_labour_cost
		self.net_total = self.total_material_and_labour_cost
				
		if(self.estimate_quantity == 0):
			frappe.throw('Estimated Qty Cannot be Zero')

		if frappe.db.get_value("Project Structure",self.project_structure,'project') != self.project:
			frappe.throw('Selected Project Structure Not Exists For This Project')

		if frappe.db.get_value("Item of Work",self.item_of_work,'project') != self.project:
			frappe.throw(_("Item of Work does not belongs to this project {0}").format(self.project))

    #duplicate item calculation
	def material_detail_validation(self):
		self.total_no_of_items = len(self.items)
		self.total_material_cost = 0
		l = []
		for d in self.items:
			d.amount = d.qty * d.rate
			self.total_material_cost += d.amount

			if d.item_code not in l:
				l.append(d.item_code)
			else:
				frappe.throw(_("Item Cannot be same in row {0}").format(d.idx))
			if d.rate == 0 or d.qty == 0 or d.amount == 0:
				frappe.throw("Rate or Qty cannot be Zero")
			if (d.uom == d.stock_uom):
				d.uom_conversion_factor = 1
				d.qty_as_per_stock_uom = d.qty * d.uom_conversion_factor

	#duplicate item calculation
	def labour_detail_validation(self):
		if self.labour_detail:
			self.primary_labour_qty = 0
			self.total_labour_cost = 0
			self.total_no_of_labours = 0
			l = []
			for i in self.labour_detail:
				i.amount = i.rate * i.qty
				self.total_labour_cost += i.amount
				self.total_no_of_labours += i.qty

				if i.primary_labour == "Yes":
					self.primary_labour_qty += i.qty
				if i.rate == 0 or i.qty == 0 or (i.rate == 0 and i.qty == 0):
					frappe.throw(_("Rate or Qty cannot be Zero in row {0}").format(i.idx))
				if i.labour not in l:
					l.append(i.labour)
				else:
					frappe.throw(_("Labour cannot be same in row {0}").format(i.idx))

    #to calculation for, if lifting percent is 1
	def calculate_lifting_amount(self):
		if self.lifting_percentage == 1:
			self.lifting_amount = ((self.total_material_and_labour_cost + self.total_other_taxes_and_charges)*(self.lifting_percentage/100))

    #adding the primary labour qty
	def add_primary_labour(self):
		self.primary_labour_qty = 0		
		for i in self.labour_detail:
			if i.primary_labour == "Yes":
				self.primary_labour_qty += i.qty

    #calculation based on amount and rate
	def other_taxes_and_charges_validation(self):
		self.total_other_taxes_and_charges = 0
		self.total_other_taxes_and_charges = 0		
		for d in self.other_taxes_and_charges:
			if d.charges_based_on == "Amount":
				d.total = d.amount
			if d.charges_based_on == "Rate":
				d.total = (self.total_material_and_labour_cost * d.rate)/100
			self.total_other_taxes_and_charges += flt(d.total)

	def total_other_taxes_and_charges_add(self):
		total_taxes_and_other_cost = 0	
		for o in self.other_taxes_and_charges:
			total_taxes_and_other_cost += o.total
		self.total_taxes_and_other_cost = total_taxes_and_other_cost + self.lifting_amount
		self.grand_total = (self.net_total +self.total_taxes_and_other_cost)

    #to create BOQ Ledger for material
	def create_material_boq_ledger(self):
		for m in self.items:
			material_ledger = frappe.new_doc("BOQ Ledger")
			material_ledger.update({
						"project":self.project,
						"project_name":self.project_name,
						"boq":self.name,
						"boq_type":self.boq_type,
						"item_of_work":self.item_of_work,
						"structure_level_name":(self.structure_level_name) if self.has_level == 1 else None,
						"material_name":m.name,
						"ledger_type":"Material",
						"item":m.item_code,
						"item_name":m.item_name,
						"uom":m.uom,
						"stock_uom":m.stock_uom,
						"qty": round(m.qty * self.converted_qty,3) if self.has_conversion == 1 else (m.qty_as_per_stock_uom  * self.est_total_qty),
						"rate":m.rate,
						"amount":(round(m.rate * (m.qty * self.converted_qty)),3) if self.has_conversion == 1 else (m.rate * m.qty_as_per_stock_uom) * self.est_total_qty,
						"qty_as_per_stock_uom":m.qty_as_per_stock_uom,
						"uom_conversion_factor":m.uom_conversion_factor
						})
			material_ledger.save(ignore_permissions = True)

    #to create BOQ Ledger for labour
	def create_labour_boq_ledger(self):
		for l in self.labour_detail:
			labour_ledger = frappe.new_doc("BOQ Ledger")
			labour_ledger.update({
			          "project":self.project,
			          "project_name":self.project_name,
		              "boq":self.name,
		              "boq_type":self.boq_type,
					  "item_of_work":self.item_of_work,
					  "structure_level_name":(self.structure_level_name) if self.has_level == 1 else None,
					  "ledger_type":"Labour",
		              "labour_name":l.name,
			          "labour":l.labour,
			          "primary_labour":l.primary_labour,
			          "has_measurement_sheet":l.has_measurement_sheet,
			          "uom":l.uom,
			          "stock_uom":l.stock_uom,
			          "primary_labour":l.primary_labour,
			          "qty":round((l.qty * self.converted_qty),3) if self.has_conversion == 1 else ((l.qty_as_stock) * self.est_total_qty),
			          "rate":l.rate,
			          "amount":round((l.rate * (l.qty * self.converted_qty)),3) if self.has_conversion == 1 else l.rate * ((l.qty_as_stock) * self.est_total_qty),
			          "qty_as_per_stock_uom":l.qty_as_stock,
			          "uom_conversion_factor":l.uom_con_factor,
			          "balance_qty":round(((l.qty_as_stock * self.quantity) * self.est_total_qty),3)
			          })
			labour_ledger.save(ignore_permissions = True)

	def validate_item(self):
		if frappe.db.exists("Item",{"name":self.name},["name"]):
			frappe.throw(("Cannot cancel because, Item {0} is created for this BOQ").format(self.name))

	#update boq  ledger qty after submit => 'for every quantity requests
	def update_boq_ledger(self):
		ledger_list = frappe.get_list('BOQ Ledger',{'boq':self.name},['name'])
		for d in ledger_list:
			ledger = frappe.get_doc('BOQ Ledger',d.name)
			ledger.update({
				'qty': round((self.converted_qty * ledger.qty_as_per_stock_uom),3) if self.has_conversion == 1 else (self.est_total_qty * ledger.qty_as_per_stock_uom)
				})
			ledger.save(ignore_permissions = True)

	def update_billing_status(self):
		if self.bill_qty == self.billed_qty:
			frappe.db.set_value("BOQ",self.name,"billing_status","To Order")
		else:
			frappe.db.set_value("BOQ",self.name,"billing_status","To Quotation")

	def update_primary_task_qty(self):
		if(self.task):
			task = frappe.get_doc('Task',self.task)
			task.update({
				"nx_qty": round(self.converted_qty,3) if self.has_conversion == 1 else round(self.est_total_qty,3)
				})
			task.save(ignore_permissions= True)

	def qty_and_rate_convertion(self):
		if self.has_conversion == 1:
			if (self.thickness == None and self.width == None):
				converted_qty = type_converter(self.est_total_qty,self.from_uom,self.to_uom,self.thickness,self.thickness_uom,self.width,self.width_uom)  
				self.converted_qty = round(converted_qty,3)
				converted_rate = type_converter(self.grand_total,self.from_uom,self.to_uom,self.thickness,self.thickness_uom,self.width,self.width_uom)   
				self.converted_rate = round(converted_rate,3)

			elif (self.thickness == None and self.width != None):
				converted_qty = type_converter(self.est_total_qty,self.from_uom,self.to_uom,self.thickness,self.thickness_uom,self.width,self.width_uom)  
				self.converted_qty = round(converted_qty,3)
				converted_rate = type_converter(self.grand_total,self.from_uom,self.to_uom,self.thickness,self.thickness_uom,self.width,self.width_uom)   
				self.converted_rate = round(converted_rate,3)


			elif (self.thickness != None and self.width == None):
				converted_qty = type_converter(self.est_total_qty,self.from_uom,self.to_uom,self.thickness,self.thickness_uom,self.width,self.width_uom)  
				self.converted_qty = round(converted_qty,3)
				converted_rate = type_converter(self.grand_total,self.from_uom,self.to_uom,self.thickness,self.thickness_uom,self.width,self.width_uom)   
				self.converted_rate = round(converted_rate,3)
	
			elif (self.thickness != None and self.width != None):
				converted_qty = type_converter(self.est_total_qty,self.from_uom,self.to_uom,self.thickness,self.thickness_uom,self.width,self.width_uom)  
				self.converted_qty = round(converted_qty,3)
				converted_rate = type_converter(self.grand_total,self.from_uom,self.to_uom,self.thickness,self.thickness_uom,self.width,self.width_uom)   
				self.converted_rate = round(converted_rate,3)
		    
	def additional_discount_amount_calculation(self):
		if self.has_conversion == 0 and self.additional_discount_percentage:
			self.additional_discount_amount = self.grand_total * ((self.additional_discount_percentage)/100)
		elif self.has_conversion == 1 and self.additional_discount_percentage:
			self.additional_discount_amount = self.converted_rate * ((self.additional_discount_percentage)/100)

	def has_uom_valiation(self):
		if self.has_conversion == 1:
			self.amount_after_conversion = self.converted_rate - self.additional_discount_amount
			self.rounded_total = self.amount_after_conversion + self.rounding_adjustment

		else:
			self.grand_total_amt = self.grand_total - self.additional_discount_amount
			self.rounded_total = self.grand_total_amt + self.rounding_adjustment

	def quotation_qty_after_qty_request(self):
		if self.billed_qty:
			self.qty_after_request = self.bill_qty - self.billed_qty

	def boq_auto_creation_from_project_structure(self): #additional features
		project_structure = frappe.get_doc("Project Structure",self.project_structure)
		if project_structure.is_master == 1:
			for i in project_structure.project_structure_list:
				boq_copy = frappe.copy_doc(self)
				boq_copy.update({
					"project_structure":i.project_structure,
					})
				boq_copy.save(ignore_permissions = True)
				frappe.msgprint(_("BOQ Successfully Created for Master Project Structure"))
			frappe.db.commit()



@frappe.whitelist()
def get_item_details(item):
	if item != None:
		return frappe.get_doc("Item",item,as_dict=1)

@frappe.whitelist()
def get_labour_details(labour):
	return frappe.get_doc("Labour",labour,as_dict=1)

@frappe.whitelist()
def uom_conversion_factor(uom,stock_uom):
	if uom == stock_uom:
		return 1
	else:
		return frappe.get_value("UOM Conversion Factor",{"from_uom":uom,"to_uom":stock_uom},["value"])

@frappe.whitelist()
def update_task(boq_name):
	boq_doc = frappe.get_doc("BOQ",boq_name)
	task_doc = frappe.new_doc("Task")
	task_doc.update({
		"nx_boq_id":boq_doc.name,
		"project":boq_doc.project,
		"subject":boq_doc.project_name,
		"nx_project_structure":boq_doc.project_structure,
		"nx_item_of_work":boq_doc.item_of_work,
		"nx_primary_labour_qty":boq_doc.primary_labour_qty,
		"nx_qty":boq_doc.converted_qty if boq_doc.has_conversion == 1 else boq_doc.est_total_qty,
	})
	return task_doc.as_dict()

@frappe.whitelist()
def create_quotation(boq_name):
	boq_doc = frappe.get_doc("BOQ",boq_name)
	qt_doc = frappe.new_doc("Quotation")
	qt_doc.update({
		"project":boq_doc.project
		})

	qt_doc.append("items",{
		"item_code":boq_doc.name,
		"item_name":boq_doc.project_structure +"-"+ boq_doc.item_of_work.split("-")[1],
		"description":boq_doc.project_structure +"-"+ boq_doc.item_of_work.split("-")[1],
		"uom":boq_doc.from_uom if boq_doc.has_conversion == 1 else boq_doc.to_uom,
		"qty":boq_doc.qty_after_request,
		"rate":boq_doc.converted_rate if  boq_doc.converted_rate != 0 else boq_doc.rounded_total,
		"amount":boq_doc.est_total_qty * boq_doc.converted_rate if boq_doc.converted_rate != 0 else boq_doc.est_total_qty * boq_doc.rounded_total,
		"nx_boq":boq_doc.name
	})

	return qt_doc

@frappe.whitelist()
def fetch_basic_rate(item,project):
	if item != None:
		rate = frappe.db.get_value("Basic Rate",{"project":project,"item_code":item},["rate"])
		return rate



@frappe.whitelist()
def convert(value,from_uom,to_uom):
	value = float(value)
	if from_uom == to_uom:
		return value

	exact_match = frappe.db.get_value("UOM Conversion Factor", {"to_uom": to_uom, "from_uom": from_uom}, ["value"],as_dict=1)

	if exact_match:
		return round((exact_match.value * value),5)

	inverse_match = frappe.db.get_value("UOM Conversion Factor", {"to_uom": from_uom, "from_uom": to_uom}, ["value"],as_dict=1)

	if inverse_match:
		return (round((1 / inverse_match.value),5) * value)

	else:
		frappe.throw('Conversion Error')

@frappe.whitelist()
def type_converter(value,from_uom,to_uom,tk_value,tk_uom,w_value,w_uom):
	value  =  float(value)
	tk_value = float(tk_value)
	w_value = float(w_value)
	fm_uom = from_uom.split(" ")
	t_uom = to_uom.split(" ")

	#Both FROM and TO UOM are Same
	if(from_uom == to_uom):
		return convert(value,from_uom,to_uom)

	#Both FROM and TO UOM are Single(1D) Dimension
	elif(('Square' not in t_uom and 'Cubic' not in t_uom) and ('Square' not in fm_uom and 'Cubic' not in fm_uom)):
		return convert(value,from_uom,to_uom)

	elif(('Square' in t_uom and 'Square'  in fm_uom) or ("Cubic" in t_uom and "Cubic" in fm_uom)):
		return convert(value,from_uom,to_uom)


	elif(('Square' in fm_uom and "Cubic" in t_uom) or ('Square' in t_uom and "Cubic" in fm_uom)):
		if('Square' in fm_uom):
			t_convert = convert(tk_value,tk_uom,fm_uom[1])
			to_value = value * t_convert
			to_value = convert(to_value,(t_uom[0]+' '+fm_uom[1]),to_uom)
			return to_value

		elif('Cubic' in fm_uom):
			t_convert = convert(tk_value,tk_uom,fm_uom[1])
			to_value = value / t_convert
			to_value = convert(to_value,(t_uom[0]+' '+fm_uom[1]),to_uom)
			return to_value

	#Any On of the UOM is SINGLE Dimension and Other UOM is TWO or THREE Dimension
	elif(('Square' not in t_uom or 'Cubic' not in t_uom ) and ('Square' in fm_uom or 'Cubic' in fm_uom)):
		# TO UOM IS SINGLE DIMENSION AND FROM UOM IS 2ND OR 3RD DIMENSION
		if('Square' in fm_uom):
			w_convert = convert(w_value,w_uom,fm_uom[1])
			to_value = round((value/w_convert),5)
			return convert(to_value,fm_uom[1],to_uom)

		elif('Cubic' in fm_uom):
			w_convert = convert(w_value,w_uom,fm_uom[1])
			t_convert = convert(tk_value,tk_uom,fm_uom[1])
			to_value = value/(w_convert*t_convert)
			return convert(to_value,fm_uom[1],to_uom)
		else:
			return frappe.throw(_('Enter valid Dimension'))

	elif(('Square' not in fm_uom or 'Cubic' not in fm_uom ) and ('Square' in t_uom or 'Cubic' in t_uom)):
		# FROM UOM IS SINGLE DIMENSION AND TO UOM IS 2ND OR 3RD DIMENSION
		if('Square' in t_uom):
			w_convert = convert(w_value,w_uom,t_uom[1])
			to_value = convert(value,from_uom,t_uom[1])
			to_value = round((to_value*w_convert),5)
			return to_value


		elif('Cubic' in t_uom):
			w_convert = convert(w_value,w_uom,t_uom[1])
			t_convert = convert(tk_value,tk_uom,t_uom[1])
			to_value = convert(value,from_uom,t_uom[1])*w_convert*t_convert
			return convert(to_value,to_uom,to_uom)
		else:
			return frappe.throw(_('Enter valid Dimension'))

@frappe.whitelist()
def rate_converter(value,from_uom,to_uom,tk_value,tk_uom,w_value,w_uom):
	value  =  float(value)
	tk_value = float(tk_value)
	w_value = float(w_value)
	fm_uom = from_uom.split(" ")
	t_uom = to_uom.split(" ")

	#Both FROM and TO UOM are Same
	if(from_uom == to_uom):
		return convert(value,from_uom,to_uom)

	#Both FROM and TO UOM are Single(1D) Dimension
	elif(('Square' not in t_uom and 'Cubic' not in t_uom) and ('Square' not in fm_uom and 'Cubic' not in fm_uom)):
		return convert(value,from_uom,to_uom)

	elif(('Square' in t_uom and 'Square'  in fm_uom) or ("Cubic" in t_uom and "Cubic" in fm_uom)):
		return convert(value,from_uom,to_uom)


	elif(('Square' in fm_uom and "Cubic" in t_uom) or ('Square' in t_uom and "Cubic" in fm_uom)):
		if('Square' in fm_uom):
			t_convert = convert(tk_value,tk_uom,fm_uom[1])
			to_value = value / t_convert
			to_value = convert(to_value,(t_uom[0]+' '+fm_uom[1]),to_uom)
			return to_value

		elif('Cubic' in fm_uom):
			t_convert = convert(tk_value,tk_uom,fm_uom[1])
			to_value = value * t_convert
			to_value = convert(to_value,(t_uom[0]+' '+fm_uom[1]),to_uom)
			return to_value

	#Any On of the UOM is SINGLE Dimension and Other UOM is TWO or THREE Dimension
	elif(('Square' not in t_uom or 'Cubic' not in t_uom ) and ('Square' in fm_uom or 'Cubic' in fm_uom)):
		# TO UOM IS SINGLE DIMENSION AND FROM UOM IS 2ND OR 3RD DIMENSION
		if('Square' in fm_uom):
			w_convert = convert(w_value,w_uom,fm_uom[1])
			to_value = round((value*w_convert),5)
			return convert(to_value,fm_uom[1],to_uom)

		elif('Cubic' in fm_uom):
			w_convert = convert(w_value,w_uom,fm_uom[1])
			t_convert = convert(tk_value,tk_uom,fm_uom[1])
			to_value = value*(w_convert/t_convert)
			return convert(to_value,fm_uom[1],to_uom)
		else:
			return frappe.throw(_('Enter valid Dimension'))

	elif(('Square' not in fm_uom or 'Cubic' not in fm_uom ) and ('Square' in t_uom or 'Cubic' in t_uom)):
		# FROM UOM IS SINGLE DIMENSION AND TO UOM IS 2ND OR 3RD DIMENSION
		if('Square' in t_uom):
			w_convert = convert(w_value,w_uom,t_uom[1])
			to_value = convert(value,from_uom,t_uom[1])
			to_value = round((to_value/w_convert),5)
			return to_value
		
		elif('Cubic' in t_uom):
			w_convert = convert(w_value,w_uom,t_uom[1])
			t_convert = convert(tk_value,tk_uom,t_uom[1])
			to_value = convert(value,from_uom,t_uom[1])/w_convert/t_convert
			return convert(to_value,to_uom,to_uom)
		else:
			return frappe.throw(_('Enter valid Dimension'))

@frappe.whitelist()
def create_grid(boq_name):
	boq_doc = frappe.get_doc("BOQ",boq_name)
	grid_doc = frappe.new_doc("Grid")
	grid_doc.update({
		"project":boq_doc.project,
		"project_structure":boq_doc.project_structure,
		"item_of_work":boq_doc.item_of_work,
		"boq":boq_doc.name
		})
	return grid_doc

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
