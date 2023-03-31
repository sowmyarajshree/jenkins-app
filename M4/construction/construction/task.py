from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.document import Document



#task status update
def task_status_update(self,method):
    if (self.nx_bal_qty == 0):
        self.progress_status = "Completed"
    elif (self.nx_actual_qty > 0):
        self.progress_status = "In Progress"
    elif (self.nx_actual_qty == 0):
        self.progress_status = "Open"
    
def update_progess_percent(self,method):
    if self.actual_qty:
        self.progress = round(((self.actual_qty/self.qty)*100),3)

#validation for boq status in Not Scheduled
@frappe.whitelist()
def validate_boq(self,method):
    if (frappe.db.exists("BOQ",{"name":self.nx_boq_id,"work_status":"Not Scheduled"},["name"]) == False):
        frappe.throw(_("Enter the Valid Boq"))

#duplicate_task_validation
@frappe.whitelist()
def duplicate_task_validation(self,method):
    if (frappe.db.exists("Task",{"nx_boq_id":self.nx_boq_id})):
        frappe.throw(_("Task is already present {0} for this BOQ").format(frappe.get_value("Task",{"nx_boq_id":self.nx_boq_id},["name"])))

@frappe.whitelist()
def calculate_balance_qty(self,method):
    boq_doc = frappe.get_doc("BOQ",self.nx_boq_id)
    if boq_doc.has_conversion == 1:
        self.qty = round((boq_doc.converted_qty * self.nx_primary_labour_qty),3) 
    else:
        self.qty = round((self.nx_qty * self.nx_primary_labour_qty),3)
    self.nx_bal_qty = round((self.nx_qty - self.nx_actual_qty),3)
    self.balance_qty = round((self.qty - self.actual_qty),3)

def validate_qty(self,method):
    if(self.balance_qty < 0):
       frappe.throw(_("Total Qty is greater than Estimated Qty"))

#remove task name to boq on cancel
@frappe.whitelist()
def update_task_and_work_status_in_boq(self,method):
    if self.nx_boq_id != None:
        frappe.db.set_value("BOQ",self.nx_boq_id,{"task":None,"work_status":"Not Scheduled"})

def update_task_in_boq(self,method):
     if self.nx_boq_id != None:
        frappe.db.set_value("BOQ",self.nx_boq_id,{"task":self.name,"work_status":"Scheduled"})

#to create measurement sheet
@frappe.whitelist()
def make_measurement_sheet(docname,project,project_name,project_structure,item_of_work,boq):
    ms_doc = frappe.new_doc("Labour Progress Entry")
    ms_doc.update({
        "project_name":project,
        "project":project_name,
        "project_structure":project_structure,
        "item_of_work":item_of_work,
        "task_id":docname,
        "boq":boq
        })
    return ms_doc.as_dict()

#for make stock entry
@frappe.whitelist()
def get_material_items(docname):
    item = []
    boq_doc = frappe.get_doc("BOQ",docname)
    for i in boq_doc.items:
        item.append({
            "item_code":i.item_code,
            "qty":i.qty,
            "material_entry_name":i.name
            })
    return item

@frappe.whitelist()
def make_stock_entry(items):
    items = json.loads(items).get("items")
    ste_doc = frappe.new_doc("Stock Entry")
    ste_doc.update({
        "stock_entry_type":"Material Issue",
        "docstatus":0
        })
    for i in items:
        ste_doc.append("items",{
                "item_code":i["item_code"],
                "qty":i["qty"] * i["stock_qty"],
                "nx_material_entry_name":i["material_entry_name"],
                "s_warehouse":"Stores - SSC"
            })
    ste_doc.save(ignore_permissions = True)
    ste_link = frappe.utils.get_link_to_form("Stock Entry",ste_doc.name)
    frappe.msgprint(_("Stock Entry {0} is created").format(ste_link))
    

