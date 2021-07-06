from __future__ import unicode_literals
import frappe, json
from frappe import msgprint, _
from frappe.model.document import Document
from frappe import utils

#throws error if bom in child table is not matched with operation
@frappe.whitelist()
def validate_bom(self,method):
    if(self.purchase_type=="Job Work"):
        for d in self.items:
            bom = frappe.get_value("BOM",{"item":d.item_code,"nx_operation":d.operation},["name"])
            if d.bom != bom:
                frappe.throw(_("BOM is not matched with operation at row {0}").format(d.idx))


#validates if same item is added more than once
@frappe.whitelist()
def validate_same_item(self,method):
    if(self.purchase_type=="Job Work"):
        for d in self.items:
            if frappe.db.count("Purchase Order Item",{"item_code":d.item_code,"parent":self.name}) > 1:
                frappe.throw("Cannot add same item more than once")


#Validates Items having same raw materials
@frappe.whitelist()
def validate_raw_material(self,method):
    raw_material = []
    if self.purchase_type == "Job Work":
        for d in self.items:
            if d.bom:
                bom_doc_list = frappe.get_list("BOM Item",filters={"parent":d.bom},fields=["item_code"])
                for b in bom_doc_list:
                    raw_material.append(b.item_code)
        if(len(raw_material)) != len(set(raw_material)):
            frappe.throw("Items having same raw materials cannot be added")

#validates if raw_material is added as an item
@frappe.whitelist()
def validate_raw_material_as_item(self,method):
    raw_material = []
    if self.purchase_type == "Job Work":
        for d in self.items:
            if d.bom:
                bom_doc_list = frappe.get_list("BOM Item",filters={"parent":d.bom},fields=["item_code"])
                for b in bom_doc_list:
                    raw_material.append({
                        "item_code":b.item_code
                    })
                if d.idx == (d.idx + 1):
                    for r in raw_material:
                        if r["item_code"] == d.item_code:
                            frappe.throw(_("Raw material cannot be added as a Item at row {0}").format(d.idx))


            '''for a in self.items:
                if d.bom:
                    bom_doc_list = frappe.get_list("BOM Item",filters={"parent":d.bom},fields=["item_code"])
                    for b in bom_doc_list:
                        raw_material.append({
                            "item_code":b.item_code
                        })
                    if d.idx != a.idx:
                        for r in raw_material:
                            if r["item_code"] == d.item_code:
                                frappe.throw(_("Raw material cannot be added as a Item at row {0}").format(d.idx))'''

                                

#update naming_series series in Employee based status of employee
@frappe.whitelist()
def update_employee_series(docname,naming_series,status):
    doc = frappe.get_last_doc("Employee",filters = {"naming_series":naming_series,"status":('in',['Active','Left'])})
    d = doc.name
        #d=frappe.db.get_value("Employee",{"naming_series":naming_series,"status":('in',['Active','Left'])},["name"])
    return d


#copy document no and document date
@frappe.whitelist()
def copy_billno_billdate(self,method):
    self.bill_no = self.document_no
    self.bill_date = self.document_date


#create unique item code
@frappe.whitelist()
def create_nx_item_code(self,method):
    for d in self.items:
        nx_item_code = str(d.item_code) + str(d.idx)
        d.nx_item_code = nx_item_code