from __future__ import unicode_literals
import frappe, json
from frappe import msgprint, _
from frappe.model.document import Document
from frappe import utils

#update status in attendance based on nx_output_code
@frappe.whitelist()
def update_attendance(self,method):
    if(self.nx_output_code == "XL"):
        self.status = "Half Day"
    elif(self.nx_output_code == "XE"):
	    self.status = "Present"
    elif(self.nx_output_code == "WW"):
	    self.status = "Present"
    elif(self.nx_output_code == "XA"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "XF"):
	    self.status ="Present"
    elif(self.nx_output_code == "XO"):
	    self.status = "Present"
    elif(self.nx_output_code == "XC"):
	    self.status = "Present"
    elif(self.nx_output_code == "LX"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "OO"):
	    self.status = "Present"
    elif(self.nx_output_code == "OX"):
        self.status = "Present"
    elif(self.nx_output_code == "OA"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "HH"):
	    self.status = "Present"
    elif(self.nx_output_code == "CA"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "EE"):
	    self.status = "Present"
    elif(self.nx_output_code == "EX"):
        self.status = "Present"
    elif(self.nx_output_code == "EA"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "LL"):
	    self.status = "Absent"
    elif(self.nx_output_code == "FF"):
	    self.status = "Present"
    elif(self.nx_output_code == "FX"):
	    self.status = "Present"
    elif(self.nx_output_code == "FA"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "CC"):
	    self.status = "Present"
    elif(self.nx_output_code == "CX"):
	    self.status = "Present"
    elif(self.nx_output_code == "AX"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "AE"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "AF"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "AO"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "XX"):
	    self.status = "Present"
    elif(self.nx_output_code == "AA"):
	    self.status = "Absent"
    elif(self.nx_output_code == "WX"):
	    self.status = "Present"
    elif(self.nx_output_code == "WY"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "HX"):
	    self.status = "Present"
    elif(self.nx_output_code == "HY"):
	    self.status = "Present"
    elif(self.nx_output_code == "WH"):
	    self.status = "Present"
    elif(self.nx_output_code == "LC"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "CL"):
	    self.status = "Half Day"
    elif(self.nx_output_code == "EC"):
	    self.status = "Present"
    elif(self.nx_output_code == "CE"):
	    self.status = "Present"
    elif(self.nx_output_code == "CO"):
	    self.status = "Present"
