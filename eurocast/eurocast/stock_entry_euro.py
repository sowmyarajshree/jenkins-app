from __future__ import unicode_literals
import frappe
import datetime
from frappe import _
from frappe import utils
from frappe.utils import flt,add_days,cint, formatdate, format_time
from erpnext.stock.stock_ledger import get_previous_sle, NegativeStockError, get_valuation_rate
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
import random

#create quality_inspection from button in child table
@frappe.whitelist()
def create_quality_inspection(docname):
	doc = frappe.get_doc("Stock Entry", docname)
	for d in doc.items:
		if d.item_group != "Raw Material":
			docm = frappe.new_doc("Quality Inspection")
			docm.update({
				"item_code": d.item_code,
				"item_name": d.item_name,
				"description": d.description,
				"inspection_type": "In Process",
				"reference_name": doc.name,
				"reference_type": "Stock Entry",
				"stock_completed_qty": doc.fg_completed_qty
			})
			return docm.as_dict()

#update warehouse in parent and child table based stock_entry_type
@frappe.whitelist()
def update_source_warehouse(self,method):
	if self.stock_entry_type == "Send from NC":
		self.from_warehouse =  "NC Store - ECE"
		for d in self.items:
			d.s_warehouse = "NC Store - ECE"

	if self.stock_entry_type == "Send to NC":
		self.to_warehouse =  "NC Store - ECE"
		for d in self.items:
			d.t_warehouse = "NC Store - ECE"

#update warehouse to child table
@frappe.whitelist()
def update_parent_warehouse(self,method):
	for d in self.items:
		if d.idx == 1:
			self.from_warehouse = d.s_warehouse
			self.to_warehouse = d.t_warehouse

#update stock_entry_no to rejection_entry doctype on_submit
@frappe.whitelist()
def update_rejection_entry(self,method):
	if self.stock_entry_type == "Full Rejection":
		doc = frappe.get_doc("Rejection Entry",self.rejection_entry)
		doc.stock_entry = self.name
		doc.save(ignore_permissions=True)

#unlink stock_entry_no from Rejection entry on_cancel
@frappe.whitelist()
def cancel_rejection_entry(self,method):
	if self.stock_entry_type == "Full Rejection":
		doc = frappe.get_doc("Rejection Entry",self.rejection_entry)
		doc.stock_entry = None
		doc.save(ignore_permissions=True)

#validate if an item has inspection_required_before_material_movement = 1
@frappe.whitelist()
def validate_inspection_item(self,method):
	for d in self.items:
		if d.reference_purchase_receipt != None:
			doc = frappe.get_doc("Item",d.item_code)
			if doc.inspection_required_before_material_movement == 1 and d.quality_inspection == None:
				frappe.throw(_("Quality Inspection is required for item {0}").format(d.item_code))
			else:
				pass


#create quality_inspection from child table
@frappe.whitelist()
def create_quality_inspection_child(docname):
	doc = frappe.get_doc("Stock Entry", docname)
	for d in doc.items:
		if d.reference_purchase_receipt != None:
			if d.quality_inspection != None:
				docm = frappe.new_doc("Quality Inspection")
				docm.update({
					"item_code": d.item_code,
					"item_name": d.item_name,
					"description": d.description,
					"reference_name": d.reference_purchase_receipt,
					"reference_type": "Purchase Receipt",
					"stock_entry_ref_no": doc.name,
					"inspection_type": "Material Transfer"
				})
				return docm.as_dict()

#updates quality_inspection no from Quality Inspection to Stock Entry on_submit of Quality Inspection
@frappe.whitelist()
def update_stock_entry(self,method):
	if self.reference_type == "Purchase Receipt" and self.inspection_type == "Material Transfer":
		if self.stock_entry_ref_no:
			doc = frappe.get_doc("Stock Entry",self.stock_entry_ref_no)
			for d in doc.items:
				if d.item_code == self.item_code:
					d.quality_inspection = self.name
					doc.save(ignore_permissions=True)

#updates quality_inspection no from Quality Inspection to Stock Entry on_submit of Quality Inspection
@frappe.whitelist()
def unlink_stock_entry(self,method):
	if self.stock_entry_ref_no:
		doc = frappe.get_doc("Stock Entry",self.stock_entry_ref_no)
		for d in doc.items:
			if d.item_code == self.item_code:
				d.quality_inspection = None
				doc.save(ignore_permissions=True)

#uplink quality_inspection no in Stock Entry on_cancel of Quality Inspection
@frappe.whitelist()
def unlink_quality_inspection(self,method):
	for d in self.items:
		if d.quality_inspection:
			doc = frappe.get_doc("Quality Inspection",d.quality_inspection)
			if doc.item_code == d.item_code:
				doc.stock_entry_ref_no = None
				doc.save(ignore_permissions=True)

#update stock_entry_no to purchase_order doctype
@frappe.whitelist()
def update_purchase_order(self,method):
	if self.stock_entry_type == "Send to Service":
		if self.nx_sub_purchase_order:
			doc = frappe.get_doc("Purchase Order",self.nx_sub_purchase_order)
			doc.stock_entry_no = self.name
			doc.save(ignore_permissions=True)

#calculatees total_rejection_value and weight in stock entry child table
@frappe.whitelist()
def calculate_total_rejection_value_and_weight(self,method):
	self.total_rejection_value = 0
	self.total_rejection_weight = 0
	for d in self.items:
		self.total_rejection_value += flt(d.item_value)
		self.total_rejection_weight += flt(d.item_weight)

#update items from Rejection Entry
@frappe.whitelist()
def update_items(docname,source_item,qty):
	if source_item:
		source_item_doc = frappe.get_doc("Item",source_item)
		items = []
		stock_uom = frappe.get_value("Item",{"item_code":source_item},["stock_uom"])
		uom = frappe.get_value("UOM Conversion Detail",{"parent":source_item},["uom"])
		conversion_factor = frappe.get_value("UOM Conversion Detail",{"parent":source_item},["conversion_factor"])
		default_bom = frappe.get_value("Item",{"item_code":source_item},["default_bom"])
		items.append({
						"item_code": source_item,
						"stock_uom": stock_uom,
						"uom": uom,
						"conversion_factor": conversion_factor,
						"default_bom": default_bom,
						"transfer_qty": qty,
						"qty": qty
						})
	return items


#update only raw_material items in child table based on bom
@frappe.whitelist()
def update_items_bom(docname,rejection_entry,nx_target_warehouse):
	items = []
	if rejection_entry:
		rejection_entry_doc = frappe.get_doc("Rejection Entry",rejection_entry)
		for d in rejection_entry_doc.rejection_detail:
			qty = frappe.db.sql("""select sum(qty) as qty, item_code as item_code, parent, sum(item_value) as item_value, sum(item_weight) as item_weight
					from `tabRejection Detail`
					where parent = %s group by item_code""",(rejection_entry_doc.name),as_dict=1)
		for q in qty:
			source_item_doc = frappe.get_doc("Item",q.item_code)
			if source_item_doc.default_bom != None:
				bom_doc = frappe.get_doc("BOM",source_item_doc.default_bom)
				stock_uom = frappe.get_value("Item",{"item_code":source_item_doc.item_code},["stock_uom"])
				uom = frappe.get_value("UOM Conversion Detail",{"parent":source_item_doc.item_code},["uom"])
				conversion_factor = frappe.get_value("UOM Conversion Detail",{"parent":source_item_doc.item_code},["conversion_factor"])
				default_bom = frappe.get_value("Item",{"item_code":source_item_doc.item_code},["default_bom"])
				for k in bom_doc.exploded_items:
					item_code = k.item_code
					transfer_qty = k.stock_qty * float(q.qty)
					qty = k.stock_qty * float(q.qty)
					stock_uom = frappe.get_value("Item",{"item_code":k.item_code},["stock_uom"])
					items.append({
						"item_code": k.item_code,
						"transfer_qty": transfer_qty,
						"qty": qty,
						"default_bom": default_bom,
						"stock_uom": stock_uom,
						"uom": stock_uom,
						"conversion_factor": 1,
						"source_or_raw_material_": "Raw Material",
						"t_warehouse":nx_target_warehouse,
						"source_item": bom_doc.item
					})
	return items


#this function assigns posting_date based on the shift time
@frappe.whitelist()
def validate_shift(self,method):
	if(self.posting_time >= "00:00:00") and (self.posting_time <= "07:30:00") or (self.posting_time >= "23:31:00"):
		self.shift_date = add_days(self.posting_date, -1)
	else:
		self.shift_date = self.posting_date

#this function reloads the document
'''@frappe.whitelist()
def reload_cur_doc(self,method):
	frappe.reload_doc("Stock Entry","doctype",self.name)



@frappe.whitelist()
def create_repack_entry(self,method):
	if self.stock_entry_type == "Full Rejection":
		for d in self.items:
			doc = frappe.new_doc("Stock Entry")
			doc.update({
				"stock_entry_type": "Repack",
				"source_item": d.item_code,
				"qty": d.qty,
				"docstatus": 0
			})
			doc.append("items",{
				"item_code": d.item_code,
				"transfer_qty": d.transfer_qty,
				"qty": d.qty,
				"stock_uom": d.stock_uom,
				"uom": d.uom,
				"conversion_factor": d.conversion_factor
			})
			doc.save(ignore_permissions=True)
			doc_last = frappe.get_doc("Stock Entry",doc.name)
			source_item_doc = frappe.get_doc("Item",doc_last.source_item)
			bom_doc = frappe.get_doc("BOM",source_item_doc.default_bom)
			stock_uom = frappe.get_value("Item",{"item_code":source_item},["stock_uom"])
			uom = frappe.get_value("UOM Conversion Detail",{"parent":source_item},["uom"])
			conversion_factor = frappe.get_value("UOM Conversion Detail",{"parent":source_item},["conversion_factor"])
			default_bom = frappe.get_value("Item",{"item_code":source_item},["default_bom"])
			for q in bom_doc.exploded_items:
				item_code = q.item_code
				transfer_qty = q.stock_qty * float(qty)
				qty = q.stock_qty * float(qty)
				doc_last.update({
					"docstatus": 1
				})
				doc_last.append("items",{
					"item_code": q.item_code,
					"transfer_qty": transfer_qty,
					"qty": qty,
					"stock_uom": stock_uom,
					"uom": uom,
					"conversion_factor": conversion_factor
				})
				doc_last.save(ignore_permissions=True)'''


#updates the stock_entry_ref_no with a random number
@frappe.whitelist()
def update_stock_entry_no(self,method):
    n = 8
    range_start = 10**(n-1)
    range_end = (10**n)-1
    self.stock_entry_ref_no = random.randint(range_start, range_end)

#updates the barcode field
@frappe.whitelist()
def update_stock_entry_barcode(self,method):
    self.nx_barcode_id = self.stock_entry_ref_no

#this function reloads the document
@frappe.whitelist()
def reload_entry(self,method):
    self.reload()


#update stock entry number to Gate Inward
@frappe.whitelist()
def update_supplier_gi(self,method):
	if self.stock_entry_type == "Supplier Return":
		if self.gate_inward:
			doc = frappe.get_doc("Gate Inward",self.gate_inward)
			for d in doc.gi_supplier_return:
				if d.document_no == self.document_no:
					d.stock_entry_no = self.name
					doc.save(ignore_permissions=True)
					received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabGI Supplier Return` where stock_entry_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
					for k in received_count:
						received_status = (k.count / doc.total) * 100
						frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
						if received_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
						doc.reload()


#unlink stock_entry number from Gate Inward
@frappe.whitelist()
def cancel_supplier_gi(self,method):
	if self.stock_entry_type == "Supplier Return":
		if self.gate_inward:
			doc = frappe.get_doc("Gate Inward",self.gate_inward)
			for d in doc.gi_supplier_return:
				if d.document_no == self.document_no:
					d.stock_entry_no = None
					doc.save(ignore_permissions=True)
					received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabGI Supplier Return` where stock_entry_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
					for k in received_count:
						received_status = (k.count / doc.total) * 100
						frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
						if received_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
						doc.reload()


#link stock_entry_no to Gate Inward
@frappe.whitelist()
def update_customer_gi(self,method):
	if self.stock_entry_type == "Customer Provided Item":
		if self.gate_inward:
			doc = frappe.get_doc("Gate Inward",self.gate_inward)
			for d in doc.gi_customer_provided:
				if d.document_number == self.document_no:
					d.stock_entry_no = self.name
					doc.save(ignore_permissions=True)
					received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabGI Customer Provided` where stock_entry_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
					for k in received_count:
						received_status = (k.count / doc.total) * 100
						frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
						if received_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
						doc.reload()


#unlink stock_entry_no to Gate Inward
@frappe.whitelist()
def cancel_customer_gi(self,method):
	if self.stock_entry_type == "Customer Provided Item":
		if self.gate_inward:
			doc = frappe.get_doc("Gate Inward",self.gate_inward)
			for d in doc.gi_customer_provided:
				if d.document_number == self.document_no:
					d.stock_entry_no = None
					doc.save(ignore_permissions=True)
					received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabGI Customer Provided` where stock_entry_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
					for k in received_count:
						received_status = (k.count / doc.total) * 100
						frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
						if received_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
						doc.reload()


#link stock_entry_no to Gate Inward
@frappe.whitelist()
def update_received_gi(self,method):
	if self.stock_entry_type == "Received from Service":
		if self.gate_inward:
			doc = frappe.get_doc("Gate Inward",self.gate_inward)
			for d in doc.gi_job_work_received_service:
				if d.purchase_order == self.nx_sub_purchase_order and d.document_no == self.document_no:
					d.stock_entry_no = self.name
					doc.save(ignore_permissions=True)
					received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabGI Job Work Received Service` where stock_entry_no IS NOT NULL and purchase_type = "Service Order" and parent = %s """,doc.name,as_dict=1)
					for k in received_count:
						received_status = (k.count / doc.so_count) * 100
						frappe.db.sql("""update `tabGate Inward` set so_status = %s where name = %s """,(received_status,doc.name))
						if doc.jo_count == 0 and doc.so_count != 0:
							received_status_so = received_status
							frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status_so,doc.name))
						if doc.jo_count != 0 and doc.so_count != 0:
							received_status_so = received_status/2
							frappe.db.sql("""update `tabGate Inward` set received_status = jo_status+so_status where name = %s """,(doc.name))
						status = frappe.db.sql("""select received_status from `tabGate Inward` where name = %s """,doc.name,as_dict=1)
						for i in status:
							if i.received_status == 100:
								frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
							else:
								frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
						doc.reload()

#unlink stock_entry_no to Gate Inward
@frappe.whitelist()
def cancel_received_gi(self,method):
	if self.stock_entry_type == "Received from Service":
		if self.gate_inward:
			doc = frappe.get_doc("Gate Inward",self.gate_inward)
			for d in doc.gi_job_work_received_service:
				if d.purchase_order == self.nx_sub_purchase_order and d.document_no == self.document_no:
					d.stock_entry_no = None
					doc.save(ignore_permissions=True)
					received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabGI Job Work Received Service` where stock_entry_no IS NOT NULL and purchase_type = "Service Order" and parent = %s """,doc.name,as_dict=1)
					for k in received_count:
						received_status = (k.count / doc.so_count) * 100
						frappe.db.sql("""update `tabGate Inward` set so_status = %s where name = %s """,(received_status,doc.name))
						if doc.jo_count == 0 and doc.so_count != 0:
							received_status_so = received_status
							frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status_so,doc.name))
						if doc.jo_count != 0 and doc.so_count != 0:
							received_status_so = received_status/2
							frappe.db.sql("""update `tabGate Inward` set received_status = jo_status+so_status where name = %s """,(doc.name))
						status = frappe.db.sql("""select received_status from `tabGate Inward` where name = %s """,doc.name,as_dict=1)
						for i in status:
							if i.received_status == 100:
								frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
							else:
								frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
						doc.reload()


#updates the items from Purchase Order to Gate Inward using update button
@frappe.whitelist()
def update_received_service(docname,supplier_name,document_no,document_date,scan_barcode):
	pending_qty = 0
	doc = frappe.get_doc("Purchase Order",scan_barcode)
	if doc.purchase_type == "Job Work":
		items = []
		for d in doc.items:
			pending_qty = (d.qty + round(d.qty * 5/100)) - d.received_qty
			items.append({
				"purchase_order":scan_barcode,
				"supplier_name": doc.supplier,
				"document_no": document_no,
				"document_date":document_date,
				"in_qty": d.qty,
				"pending_qty": pending_qty,
				"item_name": d.item_name,
				"po_date":doc.transaction_date,
				"description":d.description,
				"item_code":d.item_code,
				"uom":d.uom,
				"rate":d.rate,
				"amount":d.amount,
				"warehouse":d.warehouse,
				"cost_center":d.cost_center,
				"bom":d.bom,
				"nx_item_code":d.nx_item_code,
				"conversion_factor":d.conversion_factor,
				"stock_uom":d.stock_uom,
				"is_subcontracted": doc.is_subcontracted,
				"supplier_warehouse": doc.supplier_warehouse
			})
		return items
	if doc.purchase_type == "Service Order":
		items = []
		for d in doc.items:
			pending_qty = (d.qty + round(d.qty * 5/100)) - d.received_qty
			items.append({
				"purchase_order":scan_barcode,
				"supplier_name": doc.supplier,
				"document_no":document_no,
				"document_date":document_date,
				"in_qty": d.qty,
				"pending_qty": pending_qty,
				"item_name": d.item_name,
				"po_date":doc.transaction_date,
				"description":d.description,
				"item_code":d.item_code,
				"uom":d.uom,
				"rate":d.rate,
				"amount":d.amount,
				"warehouse":d.warehouse,
				"cost_center":d.cost_center,
				"conversion_factor":d.conversion_factor,
				"stock_uom":d.stock_uom
			})
		return items
	if doc.purchase_type not in["Job Work","Service Order"]:
		frappe.throw("Purchase Order type should be Service Order or Job Work")


#updates the details from Stock entry to gate inward
@frappe.whitelist()
def update_service_order(docname,scan_barcode):
	#scan_doc = frappe.get_value("Stock Entry",{"nx_stock_entry_ref_no":scan_barcode},["name"])
	doc = frappe.get_doc("Stock Entry",scan_barcode)
	if doc.stock_entry_type == "Send to Subcontractor":
		supplier_name = doc.supplier
		stock_entry_no = doc.name
		stock_entry_date = doc.posting_date
		return supplier_name, stock_entry_no, stock_entry_date
	if doc.stock_entry_type == "Send to Service":
		supplier_name = doc.nx_supplier
		stock_entry_no = doc.name
		stock_entry_date = doc.posting_date
		return supplier_name, stock_entry_no, stock_entry_date
	if doc.stock_entry_type not in["Send to Service","Send to Subcontractor"]:
		frappe.throw("Stock entry type should be Send to Subcontractor or Send to Service")



#return the value of warehouse from Purchase Order
@frappe.whitelist()
def update_warehouse(docname,purchase_order):
	doc = frappe.get_doc("Purchase Order",purchase_order)
	from_warehouse = doc.source_warehouse
	to_warehouse = doc.set_warehouse
	return from_warehouse,to_warehouse

#update the from_warehouse value from Purchase Order
@frappe.whitelist()
def update_warehouse_received(docname,purchase_order):
	doc = frappe.get_doc("Purchase Order",purchase_order)
	from_warehouse = doc.set_warehouse
	return from_warehouse

#copies purchase_order value and assi' to purchase_order field
@frappe.whitelist()
def copy_purchase_order(self,method):
	if self.stock_entry_type == "Received from Service":
		self.purchase_order = self.nx_sub_purchase_order

#validates if Repack entry for this stock entry already exist or not
@frappe.whitelist()
def validate_repack_entry(self,method):
	if (self.stock_entry_type == "Full Rejection") or (self.stock_entry_type == "Repack"):
		if frappe.db.count("Stock Entry",{"rejection_entry":self.rejection_entry,"docstatus":1,"stock_entry_type":"Full Rejection"},["name"]) > 1:
			frappe.throw(_("Stock Entry for Full Rejection for {0} already exist").format(self.rejection_entry))
		if frappe.db.count("Stock Entry",{"rejection_entry":self.rejection_entry,"docstatus":1,"stock_entry_type":"Repack"},["name"]) > 1:
			frappe.throw(_("Stock Entry for Repack for {0} already exist").format(self.rejection_entry))


#returns the box_no value
@frappe.whitelist()
def update_packing_box_items(docname,scan_barcode):
	if scan_barcode:
		item_code = frappe.get_value("Packing Box Label Item",{"box_no":scan_barcode},["item_code"])
		qty = frappe.get_value("Packing Box Label Item",{"box_no":scan_barcode},["quantity"])
		box_no = scan_barcode
		return item_code,qty,box_no

#validates if any Duplicate box nos is present
@frappe.whitelist()
def validate_duplicate_box_nos(self,method):
	if self.stock_entry_type == "Transfer to Safety Stock":
		for d in self.items:
			if frappe.db.count("Stock Entry Detail",{"nx_box_no":d.nx_box_no}) > 1:
				frappe.throw(_("Duplicate Box no in row {0}").format(d.idx))


#validates the warehouse based on stock_entry_type
@frappe.whitelist()
def validate_warehouse_fg_stock(self,method):
	if self.stock_entry_type == "Transfer to Safety Stock":
		self.to_warehouse == "Safety Stock Store - ECE"
		from_warehouse = ["Final Store - ECE","Machining Store - ECE","Incoming Store - ECE"]
		if self.from_warehouse not in from_warehouse:
			frappe.throw("Warehouse must be in Final Store - ECE,Machining Store - ECE,Incoming Store - ECE ")



#stock validation on save
@frappe.whitelist()
def set_actual_qty(self,method):
	if self.stock_entry_type in["Material Transfer","Transfer to Safety Stock","Full Rejection","Material Issue","External Material Transfer","Send to Subcontractor"]:
		allow_negative_stock = cint(frappe.db.get_value("Stock Settings", None, "allow_negative_stock"))

		for d in self.get('items'):
			previous_sle = get_previous_sle({
				"item_code": d.item_code,
				"warehouse": d.s_warehouse or d.t_warehouse,
				"posting_date": self.posting_date,
				"posting_time": self.posting_time
			})

			# get actual stock at source warehouse
			d.actual_qty = previous_sle.get("qty_after_transaction") or 0


			# validate qty during save
			if d.s_warehouse and not allow_negative_stock and flt(d.actual_qty, d.precision("actual_qty")) < flt(d.transfer_qty, d.precision("actual_qty")):
				frappe.throw(_("Row {0}: Quantity not available for {4} in warehouse {1} at posting time of the entry ({2} {3})").format(d.idx,
					frappe.bold(d.s_warehouse), formatdate(self.posting_date),
					format_time(self.posting_time), frappe.bold(d.item_code))
					+ '<br><br>' + _("Available quantity is {0}, you need {1}").format(frappe.bold(d.actual_qty),
					frappe.bold(d.transfer_qty)),
					NegativeStockError, title=_('Insufficient Stock'))


#update stock entry no to Gate inward
@frappe.whitelist()
def update_others_gi(self,method):
	if self.stock_entry_type == "External Material Receipt":
		if self.gate_inward:
			doc = frappe.get_doc("Gate Inward",self.gate_inward)
			for d in doc.other_deliveries:
				if (d.dc_date == self.document_date):
					d.stock_entry_no = self.name
					doc.save(ignore_permissions=True)
					received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabOther Deliveries` where stock_entry_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
					for k in received_count:
						received_status = (k.count / doc.total) * 100
						frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
						if received_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
						doc.reload()


#remove stock entry no to Gate inward
@frappe.whitelist()
def cancel_others_gi(self,method):
	if self.stock_entry_type == "External Material Receipt":
		if self.gate_inward:
			doc = frappe.get_doc("Gate Inward",self.gate_inward)
			for d in doc.other_deliveries:
				if (d.dc_date == self.document_date):
					d.stock_entry_no = None
					doc.save(ignore_permissions=True)
					received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabOther Deliveries` where stock_entry_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
					for k in received_count:
						received_status = (k.count / doc.total) * 100
						frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
						if received_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
						doc.reload()


#validate if both customer name and supplier
@frappe.whitelist()
def validate_supplier_warehouse(self,method):
	'''if self.stock_entry_type == "External Material Issue":
		if self.nx_supplier != None:
			supplier_warehouse = frappe.get_value("Supplier",{"name":self.nx_supplier},["nx_supplier_warehouse"])
			self.nx_target_warehouse = supplier_warehouse
		if self.nx_customer != None:
			customer_warehouse = frappe.get_value("Customer",{"name":self.nx_customer},["customer_warehouse"])
			self.nx_target_warehouse = customer_warehouse
	if self.stock_entry_type == "External Material Receipt":
		if self.nx_supplier != None:
			supplier_warehouse = frappe.get_value("Supplier",{"name":self.nx_supplier},["nx_supplier_warehouse"])
			self.from_warehouse = supplier_warehouse
		if self.nx_customer != None:
			customer_warehouse = frappe.get_value("Customer",{"name":self.nx_customer},["customer_warehouse"])
			self.from_warehouse = customer_warehouse'''
	if self.nx_customer_name != None and self.nx_supplier != None:
		frappe.throw("Cannot select both supplier and customer")

#return supplier warehouse
@frappe.whitelist()
def get_supplier_warehouse(docname,supplier,stock_entry_type):
	supplier_warehouse = frappe.get_value("Supplier",{"name":supplier},["nx_supplier_warehouse"])
	return supplier_warehouse


#return customer warehouse
@frappe.whitelist()
def get_customer_warehouse(docname,customer,stock_entry_type):
	customer_warehouse = frappe.get_value("Customer",{"name":customer},["customer_warehouse"])
	return customer_warehouse
	
