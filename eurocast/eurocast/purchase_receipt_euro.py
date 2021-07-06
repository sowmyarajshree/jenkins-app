from __future__ import unicode_literals
import frappe
import datetime
from frappe import _
from frappe import utils
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, ceil
from frappe.model.document import Document


#creates Quality Inspection from child table button
@frappe.whitelist()
def create_quality_inspection(docname):
    doc = frappe.get_doc("Purchase Receipt", docname)
    if doc.docstatus == 1:
        for d in doc.items:
            if d.is_inspection == 1:
                docm = frappe.new_doc("Quality Inspection")
                docm.update({
        				"item_code": d.item_code,
        				"item_name": d.item_name,
        				"description": d.description,
        				"inspection_type": "Incoming",
        				"reference_name": doc.name,
        				"reference_type": "Purchase Receipt"
                })
                return docm.as_dict()

#updates is_inspection field in child table from Item table
@frappe.whitelist()
def val_is_inspection(self,method):
    for d in self.items:
        val = frappe.db.get_value("Item",{"item_code":d.item_code},["inspection_required_before_purchase"])
        if val == 1:
            d.is_inspection = 1


#update stock_entry_no in Gate inward child table Gi Returnables
@frappe.whitelist()
def update_gi_st(self,method):
    if self.stock_entry_type == "Service Return":
        if self.gate_inward:
            gi_doc = frappe.get_doc("Gate Inward",self.gate_inward)
            if gi_doc.inward_types == "Returnables":
                for d in gi_doc.gi_returnables:
                    d.stock_entry_no = self.name
                    gi_doc.save(ignore_permissions=True)

#unlink stock_entry_no from Gate inward child table GI Returnables on cancelling Stock Entry
@frappe.whitelist()
def unlink_gi_st(self,method):
    if self.stock_entry_type == "Service Return":
        if self.gate_inward:
            gi_doc = frappe.get_doc("Gate Inward",self.gate_inward)
            if gi_doc.inward_types == "Returnables":
                for d in gi_doc.gi_returnables:
                    d.stock_entry_no = None
                    gi_doc.save(ignore_permissions=True)


#update Purchase Receipt no in Gate Inward from Purchase Receipt on_submit
@frappe.whitelist()
def update_gate_inward(self,method):
    if self.is_return != 1:
        if self.gate_inward:
            doc = frappe.get_doc("Gate Inward",self.gate_inward)
            if doc.inward_types == "Purchase Order":
                for d in doc.gi_po_details:
                    for s in self.items:
                        if d.purchase_order == s.purchase_order and d.supplier == self.supplier and d.item_code == s.item_code:
                            d.purchase_receipt_ref_no = self.name
                doc.save(ignore_permissions=True)
                '''received_count = frappe.db.sql("""select count(purchase_receipt_ref_no) as count from `tabGI PO Details` where purchase_receipt_ref_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
                for k in received_count:
                    received_status = (k.count / doc.total) * 100
                    frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
                    if received_status == 100:
                        frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
                    else:
                        frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
                    doc.reload()
                            #frappe.db.sql("""update `tabGate Inward` set count = count + 1 where name = %s """,doc.name)'''
            if doc.inward_types == "Job Work Order":
                total = 0
                for d in doc.gi_job_work_received_service:
                    for s in self.items:
                        if d.purchase_order == s.purchase_order and d.supplier_name == self.supplier and d.item_code == s.item_code:
                            d.purchase_receipt_no = self.name
                doc.save(ignore_permissions=True)
                '''received_count = frappe.db.sql("""select count(purchase_receipt_no) as count from `tabGI Job Work Received Service` where purchase_receipt_no IS NOT NULL and purchase_type = "Job Work" and parent = %s """,doc.name,as_dict=1)
                so_received_count = frappe.db.sql("""select count(purchase_receipt_no) as count from `tabGI Job Work Received Service` where purchase_receipt_no IS NOT NULL and purchase_type = "Service Order" and parent = %s """,doc.name,as_dict=1)
                for k in received_count:
                    for s in so_received_count:
                        if doc.jo_count != 0 and doc.so_count == 0:
                            received_status = (k.count / doc.jo_count) * 100
                            frappe.db.sql("""update `tabGate Inward` set jo_status = %s where name = %s """,(received_status,doc.name))
                            frappe.db.sql("""update `tabGate Inward` set received_status = jo_status where name = %s """,(doc.name))
                        if doc.so_count != 0 and doc.jo_count == 0:
                            so_status = (s.count / doc.so_count) * 100
                            frappe.db.sql("""update `tabGate Inward` set so_status = %s where name = %s """,(so_status,doc.name))
                            frappe.db.sql("""update `tabGate Inward` set received_status = so_status where name = %s """,(doc.name))
                        if doc.so_count != 0 and doc.jo_count != 0:
                            total = doc.so_count + doc.jo_count
                            so_status_1 = ((s.count / doc.so_count) * 100)
                            jo_status_1 = ((k.count / doc.jo_count) * 100)
                            frappe.db.sql("""update `tabGate Inward` set so_status = %s where name = %s """,(so_status_1,doc.name))
                            frappe.db.sql("""update `tabGate Inward` set jo_status = %s where name = %s """,(jo_status_1,doc.name))
                            frappe.db.sql("""update `tabGate Inward` set received_status = (jo_status+so_status)/2 where name = %s """,(doc.name))
                        status = frappe.db.sql("""select received_status from `tabGate Inward` where name = %s """,doc.name,as_dict=1)
                        for i in status:
                            if i.received_status == 100:
                                frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
                            else:
                                frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
                            doc.reload()'''

#unlink purchase_receipt_no from Gate inward on cancelling Purchase Receipt
@frappe.whitelist()
def unlink_gate_inward(self,method):
    if self.gate_inward:
        doc = frappe.get_doc("Gate Inward",self.gate_inward)
        if doc.inward_types == "Purchase Order":
            for d in doc.gi_po_details:
                for s in self.items:
                    if d.purchase_order == s.purchase_order and d.supplier == self.supplier and d.item_code == s.item_code:
                        d.purchase_receipt_ref_no = None
            doc.save(ignore_permissions=True)
            received_count = frappe.db.sql("""select count(purchase_receipt_ref_no) as count from `tabGI PO Details` where purchase_receipt_ref_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
            for k in received_count:
                received_status = (k.count / doc.total) * 100
                frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
                if received_status == 100:
                    frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
                else:
                    frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
                doc.reload()
                        #frappe.db.sql("""update `tabGate Inward` set count = count + 1 where name = %s """,doc.name)
        if doc.inward_types == "Job Work Order":
            total = 0
            for d in doc.gi_job_work_received_service:
                for s in self.items:
                    if d.purchase_order == s.purchase_order and d.supplier_name == self.supplier and d.item_code == s.item_code:
                        d.purchase_receipt_no = None
            doc.save(ignore_permissions=True)
            received_count = frappe.db.sql("""select count(purchase_receipt_no) as count from `tabGI Job Work Received Service` where purchase_receipt_no IS NOT NULL and purchase_type = "Job Work" and parent = %s """,doc.name,as_dict=1)
            so_received_count = frappe.db.sql("""select count(purchase_receipt_no) as count from `tabGI Job Work Received Service` where purchase_receipt_no IS NOT NULL and purchase_type = "Service Order" and parent = %s """,doc.name,as_dict=1)
            for k in received_count:
                for s in so_received_count:
                    if doc.jo_count != 0 and doc.so_count == 0:
                        received_status = (k.count / doc.jo_count) * 100
                        frappe.db.sql("""update `tabGate Inward` set jo_status = %s where name = %s """,(received_status,doc.name))
                        frappe.db.sql("""update `tabGate Inward` set received_status = jo_status where name = %s """,(doc.name))
                    if doc.so_count != 0 and doc.jo_count == 0:
                        so_status = (s.count / doc.so_count) * 100
                        frappe.db.sql("""update `tabGate Inward` set so_status = %s where name = %s """,(so_status,doc.name))
                        frappe.db.sql("""update `tabGate Inward` set received_status = so_status where name = %s """,(doc.name))
                    if doc.so_count != 0 and doc.jo_count != 0:
                        total = doc.so_count + doc.jo_count
                        so_status_1 = ((s.count / doc.so_count) * 100)
                        jo_status_1 = ((k.count / doc.jo_count) * 100)
                        frappe.db.sql("""update `tabGate Inward` set so_status = %s where name = %s """,(so_status_1,doc.name))
                        frappe.db.sql("""update `tabGate Inward` set jo_status = %s where name = %s """,(jo_status_1,doc.name))
                        frappe.db.sql("""update `tabGate Inward` set received_status = (jo_status+so_status)/2 where name = %s """,(doc.name))
                    status = frappe.db.sql("""select received_status from `tabGate Inward` where name = %s """,doc.name,as_dict=1)
                    for i in status:
                        if i.received_status == 100:
                            frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
                        else:
                            frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
                        doc.reload()


'''@frappe.whitelist()
def unlink_gate_inward_po(self,method):
    if self.gate_inward:
        doc = frappe.get_doc("Gate Inward",self.gate_inward)
        for d in doc.gi_po_details:
            d.purchase_order = None
            doc.save(ignore_permissions=True)


@frappe.whitelist()
def remove_gi_in_childtable(self,method):
    if self.gate_inward == None:
        for d in self.items:
            d.gate_inward = None'''


#updates price_list based on Supplier
@frappe.whitelist()
def update_price_list(docname,supplier):
    price_list = frappe.get_value("Supplier",{"name":supplier},["nx_job_work_price_list"])
    #price = frappe.msgprint(_("Price list is {0}").format(price_list))
    return price_list


#unlink purchase_order number on cancelling purchase_order
@frappe.whitelist()
def unlink_and_cancel_stock_entry(self,method):
    if self.stock_entry_no:
        doc = frappe.get_doc("Stock Entry",self.stock_entry_no)
        doc.nx_sub_purchase_order = None
        doc.docstatus = 2
        doc.save(ignore_permissions=True)
        self.stock_entry_no = None

#updates the rate and price_list_rate in purchase_order item table based on operation
@frappe.whitelist()
def update_price_rate(price_list,item_code,operation):
    price_rate = frappe.get_value("Operation Item Price List",{"operation":operation,"item":item_code,"price_list":price_list},["rate"])
    #msg = frappe.msgprint(_("Price is {0}").format(price_rate))
    return price_rate



#this function assigns null value to gate_inward on_submit of Purchase Receipt
@frappe.whitelist()
def null_gate(self,method):
    if self.status != "To Bill":
        self.gate_inward = None

#validates gate_inward status that is linked in Purchase Receipt
@frappe.whitelist()
def validate_gate_inward_no(self,method):
    if self.is_return == 0:
        if self.gate_inward != None:
            status = frappe.get_value("Gate Inward",{"name":self.gate_inward},["status"])
            if status != "Open":
                frappe.throw(_("Status must be Open for Gate Inward {0}".format(self.gate_inward)))

#throws error if purchase_order no is missing in Purchase Receipt Item table
@frappe.whitelist()
def validate_pr(self,method):
    for d in self.items:
        if d.purchase_order == None:
            frappe.throw("Purchase Order is mandatory")



'''@frappe.whitelist()
def validate_po_gate_inward(self,method):
    if self.gate_inward:
        po_nos =[]
        po_list = frappe.get_list("GI PO Details",filters={"parent":self.gate_inward},fields=["purchase_order"])
        for i in po_list:
            po_nos.append(i.purchase_order)
            frappe.msgprint(_("PO Nos is {0}").format(po_nos))
        for d in self.items:
            if d.purchase_order not in po_nos:
                frappe.throw(_("Purchase Order {0} not found in Gate Inward").format(d.purchase_order))
                #frappe.msgprint(_("Purchase Order no is {0}").format(d.purchase_order))'''



#updates purchase_receipt item table by getting values from Gate Inward child table
@frappe.whitelist()
def update_items(docname,supplier,document_no,document_date,gate_inward):
    items = []
    doc = frappe.get_doc("Gate Inward",gate_inward)
    if doc.inward_types == "Purchase Order":
        for d in doc.gi_po_details:
            if (supplier == d.supplier) and (d.purchase_receipt_ref_no == None):
                items.append({
        			"qty": d.in_qty,
        			"item_name": d.item_name,
        			"description":d.description,
        			"item_code":d.item_code,
                    "uom":d.uom,
                    "stock_uom":d.stock_uom,
                    "received_qty":d.in_qty,
                    "conversion_factor":d.conversion_factor,
                    "purchase_order":d.purchase_order,
                    "rate": d.rate,
                    "amount": d.amount,
                    "warehouse":d.warehouse,
                    "cost_center": d.cost_center,
                    "schedule_date":d.schedule_date,
                    "nx_item_code":d.nx_item_code
                })
        return items
    if doc.inward_types == "Job Work Order":
        for d in doc.gi_job_work_received_service:
            if (supplier == d.supplier_name) and (d.purchase_receipt_no == None):
                uom = frappe.db.get_value("Item",{"item_code":d.item_code},["stock_uom"])
                items.append({
        			"qty": d.in_qty,
        			"item_name": d.item_name,
        			"description":d.description,
        			"item_code":d.item_code,
                    "uom":d.uom,
                    "stock_uom":d.stock_uom,
                    "received_qty":d.in_qty,
                    "conversion_factor":d.conversion_factor,
                    "purchase_order":d.purchase_order,
                    "rate": d.rate,
                    "amount": d.amount,
                    "warehouse":d.warehouse,
                    "cost_center": d.cost_center,
                    "bom":d.bom,
                    "schedule_date":d.schedule_date,
                    "nx_item_code":d.nx_item_code
                })
        return items


#update purchase tax from purchase order
@frappe.whitelist()
def update_purchase_tax(docname,supplier,document_no,document_date,gate_inward):
    doc = frappe.get_doc("Gate Inward",gate_inward)
    if doc.inward_types == "Purchase Order":
        for d in doc.gi_po_details:
            if (supplier == d.supplier) and (d.purchase_receipt_ref_no == None):
                taxes_and_charges = frappe.get_value("Purchase Order",{"name":d.purchase_order},["taxes_and_charges"])
                return taxes_and_charges

    if doc.inward_types == "Job Work Order":
        for d in doc.gi_job_work_received_service:
            if (supplier == d.supplier_name) and (d.purchase_receipt_no == None):
                taxes_and_charges = frappe.get_value("Purchase Order",{"name":d.purchase_order},["taxes_and_charges"])
                return taxes_and_charges


#update received_qty value to purchase_order on on_submit of Purchase Receipt
@frappe.whitelist()
def update_received_qty(self,method):
    per_received = 0
    for d in self.items:
        if d.purchase_order:
            doc = frappe.get_doc("Purchase Order",d.purchase_order)
            for p in doc.items:
                if p.nx_item_code == d.nx_item_code:
                    p.received_qty += d.qty
                    per_received += d.qty
                    #per_received += flt(p.received_qty/doc.total_qty) * 100
            doc.per_received = flt(per_received/doc.total_qty) * 100
            doc.save(ignore_permissions=True)


#substracting received_qty value on_cancel of Purchase Receipt
@frappe.whitelist()
def cancel_received_qty(self,method):
    per_received = 0
    for d in self.items:
        if d.purchase_order:
            doc = frappe.get_doc("Purchase Order",d.purchase_order)
            for p in doc.items:
                if p.nx_item_code == d.nx_item_code:
                    per_received -= d.qty
                    p.received_qty -= d.qty
            doc.per_received = flt(per_received/doc.total_qty) * 100
            doc.save(ignore_permissions=True)


#update returned_qty value to purchase_order on on_submit of Purchase Receipt
@frappe.whitelist()
def update_returned_qty(self,method):
    per_received = 0
    if self.is_return == 1:
        for d in self.items:
            if d.purchase_order:
                doc = frappe.get_doc("Purchase Order",d.purchase_order)
                for p in doc.items:
                    if p.nx_item_code == d.nx_item_code:
                        p.returned_qty += abs(d.qty)
                        per_received += abs(d.qty)
                doc.per_received = flt(per_received/doc.total_qty) * 100
                doc.save(ignore_permissions=True)


#substracting returned_qty value on_cancel of Purchase Receipt
@frappe.whitelist()
def cancel_returned_qty(self,method):
    per_received = 0
    if self.is_return == 1:
        for d in self.items:
            if d.purchase_order:
                doc = frappe.get_doc("Purchase Order",d.purchase_order)
                for p in doc.items:
                    if p.nx_item_code == d.nx_item_code:
                        p.returned_qty -= abs(d.qty)
                        per_received += abs(d.received_qty)
                doc.per_received = flt(per_received/doc.total_qty) * 100
                doc.save(ignore_permissions=True)


#update supplier warehouse field from Purchase Order to Purchase Receipt on clicking on gate_inward field
@frappe.whitelist()
def update_supplier_warehouse(supplier,gate_inward,document_date):
    if gate_inward:
        doc = frappe.get_doc("Gate Inward",gate_inward)
        if doc.inward_types == "Job Work Order":
            for d in doc.gi_job_work_received_service:
                if d.purchase_type == "Job Work" and d.supplier_name == supplier:
                    jo_name = frappe.get_value("GI Job Work Received Service",{"parent":gate_inward,"supplier_name":supplier},["purchase_order"])
                    if jo_name:
                        jo_doc = frappe.get_doc("Purchase Order",jo_name)
                        is_subcontracted = jo_doc.is_subcontracted
                        supplier_warehouse = jo_doc.supplier_warehouse
                        return is_subcontracted, supplier_warehouse


#update supplier warehouse field from Purchase Order to Purchase Receipt on save
@frappe.whitelist()
def update_supplier_warehouse_onsave(self,method):
    if self.gate_inward:
        doc = frappe.get_doc("Gate Inward",self.gate_inward)
        if doc.inward_types == "Job Work Order":
            for d in doc.gi_job_work_received_service:
                if d.purchase_type == "Job Work":
                    jo_name = frappe.get_value("GI Job Work Received Service",{"parent":self.gate_inward,"supplier_name":self.supplier},["purchase_order"])
                    if jo_name != None:
                        jo_doc = frappe.get_doc("Purchase Order",jo_name)
                        self.is_subcontracted = jo_doc.is_subcontracted
                        self.supplier_warehouse = jo_doc.supplier_warehouse

#update bom number on Purchase return
@frappe.whitelist()
def update_bom_onReturn(self,method):
    if self.is_return == 1:
        if self.return_against != None:
            doc = frappe.get_doc("Purchase Receipt",self.return_against)
            self.supplier_warehouse = doc.supplier_warehouse
            for d in doc.items:
                for p in self.items:
                    if p.item_code == d.item_code:
                       p.bom = d.bom


#validate purchase receipt qty based on purchase order qty
@frappe.whitelist()
def validate_po_qty(self,method):
    if self.is_return == 0:
        for i in self.items:
            over_delivery_allowance = frappe.get_value("Item",{"item_code":i.item_code},["over_delivery_receipt_allowance"])
            po_qty = frappe.get_value("Purchase Order Item",{"nx_item_code":i.nx_item_code,"parent":i.purchase_order},["qty"])
            #frappe.msgprint(_("{0}").format(po_qty))
            rec_qty = frappe.get_value("Purchase Order Item",{"nx_item_code":i.nx_item_code,"parent":i.purchase_order},["received_qty"])
            over_delivery_percent = ceil(po_qty + (po_qty * over_delivery_allowance/100)) - rec_qty
            if i.qty > over_delivery_percent:
                frappe.throw(_("Qty is greater than Purchase Order Qty for item {0} at row {1}").format(i.item_code,i.idx))



#update taxes and charges in Purchase receipt from purchase order
@frappe.whitelist()
def update_taxes_purchaseinvoice(self,method):
    for d in self.items:
        taxes_and_charges = frappe.get_value("Purchase Order",{"name":d.purchase_order},["taxes_and_charges"])
        self.taxes_and_charges = taxes_and_charges
