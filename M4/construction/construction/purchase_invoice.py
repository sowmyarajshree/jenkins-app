from __future__ import unicode_literals
import frappe
import datetime
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe import utils






@frappe.whitelist()
def fetch_total_amount_rt(self,method):
    for r in self.items:
        if r.nx_reference_doctype == "Rate Work Entry":
            r_total_amount = frappe.db.get_value("Rate Work Entry",r.nx_reference_name,["total_amount"])
            r.rate = r_total_amount
            r.base_rate = r_total_amount
            r.amount = r_total_amount
            r.base_amount = r_total_amount
        elif r.nx_reference_doctype == "F and F Entry":
            f_total_amount = frappe.db.get_value("F and F Entry",r.nx_reference_name,["total_amount"])
            r.rate = f_total_amount
            r.base_rate = f_total_amount
            r.amount = f_total_amount
            r.base_amount = f_total_amount
def billing_status_update(self,method):
    for item in self.items:
        if item.nx_reference_doctype:
            frappe.db.set_value(item.nx_reference_doctype,item.nx_reference_name,{"status":"Completed","purchase_invoice":self.name})
            ref_doc = frappe.get_doc(item.nx_reference_doctype,item.nx_reference_name)
            if item.nx_reference_doctype == "F and F Entry":
                for l in ref_doc.labour_progress_details:
                    frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"status","Completed")
            elif item.nx_reference_doctype == "Rate Work Entry":
                for l in ref_doc.labour_progress_work_details:
                    frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"status","Completed")





def billing_status_update_on_cancel(self,method):
    for item in self.items:
        if item.nx_reference_doctype:
            frappe.db.set_value(item.nx_reference_doctype,item.nx_reference_name,{"status":"To Bill","purchase_invoice":None})
            ref_doc = frappe.get_doc(item.nx_reference_doctype,item.nx_reference_name)
            if item.nx_reference_doctype == "F and F Entry":
                for l in ref_doc.labour_progress_details:
                    frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"status","To Bill")
            elif item.nx_reference_doctype == "Rate Work Entry":
                for l in ref_doc.labour_progress_work_details:
                    frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"status","To Bill")


def validate_bill(self,method):
    [frappe.throw(_("Bill already created for this row {0}").format(item.idx))  if(frappe.db.exists(item.nx_reference_doctype,{'name':item.nx_reference_name,'status':'Completed'})) else None for item in self.items]


#Set Naming series: if the item_code field in the items table is starts with 'F and F' the purchase invoice naming series is starts with 'FFB-######' 
#if the 'item_code' is starts with Rate Work naming series is starts with 'RWB-######' otherwise its 'PINV-######'
def naming_series(self, method):
    for items in self.items:
        if items.item_code.startswith("F and F") :
            self.naming_series = "PINV-FFB-.#####"
        elif items.item_code.startswith("Rate Work"):
            self.naming_series = "PINV-RWB-.#####"


@frappe.whitelist()
def unlink_purchase_invoice_in_CRE(docname):
    pi_value = frappe.get_value("Cash Requisition Detail",{"document_name":docname},["name"])
    cre_doc = frappe.get_doc("Cash Requisition Detail",pi_value)
    frappe.db.set_value("Cash Requisition Detail",cre_doc.name,"is_cancelled",1)
    frappe.db.set_value("Cash Requisition Detail",cre_doc.name,"cancelled_from",docname)
    frappe.db.set_value("Cash Requisition Detail",cre_doc.name,"document_name",None)
    frappe.msgprint("Unlinked from Cash Requisition")


    





















