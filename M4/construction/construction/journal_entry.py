from __future__ import unicode_literals
import frappe
import json
import pyttsx3
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, add_days, nowdate



#update the muster roll status as Completed on submit
def update_muster_roll_status(self,method):
	for i in self.accounts:
		if i.nx_muster_roll_entry:
			frappe.db.set_value("Muster Roll Entry",i.nx_muster_roll_entry,"status","Completed")
			frappe.db.set_value("Muster Roll Entry",i.nx_muster_roll_entry,"journal_entry",self.name)

#update the muster roll status as To bill on cancel
def update_muster_roll_status_on_cancel(self,method):
	for i in self.accounts:
		if i.nx_muster_roll_entry:
			frappe.db.set_value("Muster Roll Entry",i.nx_muster_roll_entry,"status","To Bill")
			frappe.db.set_value("Muster Roll Entry",i.nx_muster_roll_entry,"journal_entry",self.name)

#update the lpe status as Completed on submit		
def update_lpe_status(self,method):
	for i in self.accounts:
		if i.nx_muster_roll_entry:
			muster_roll_doc = frappe.get_doc("Muster Roll Entry",i.nx_muster_roll_entry)
			for l in muster_roll_doc.labour_progress_details:
				frappe.db.set_value("Working Detail",l.working_details_name,"billed",1)
			billed = []
			for l in muster_roll_doc.labour_progress_details:
				lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
				working_detail_list = frappe.get_list("Working Detail",{"parent":l.labour_progress_entry},["name","muster_roll","billed"])
				billed = []
				for w in working_detail_list:
					if w.billed == 1:
						billed.append(w.idx)
				if len(lpe_doc.working_details) == len(billed):
					frappe.db.set_value("Labour Progress Entry",lpe_doc.name,"status","Completed")

#update the lpe status as To Bill on cancel		
def update_lpe_status_on_cancel(self,method):
	for i in self.accounts:
		if i.nx_muster_roll_entry:
			muster_roll_doc = frappe.get_doc("Muster Roll Entry",i.nx_muster_roll_entry)
			for l in muster_roll_doc.labour_progress_details:
				frappe.db.set_value("Working Detail",l.working_details_name,"billed",0)
				billed = []
			for l in muster_roll_doc.labour_progress_details:
				lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
				working_detail_list = frappe.get_list("Working Detail",{"parent":l.labour_progress_entry},["name","muster_roll","billed"])
				billed = []
				for w in working_detail_list:
					if w.billed == 1:
						billed.append(w.idx)
				if len(lpe_doc.working_details) != len(billed):
					frappe.db.set_value("Labour Progress Entry",lpe_doc.name,"status","To Bill")







# Initialize the recognizer

@frappe.whitelist()
def myvoice(self,method):
	r = sr.Recognizer()
	with sr.Microphone():
		frappe.msgprint("Speak now...")
		audio = r.listen()
		try:
			text = r.recognize_google_cloud(audio, language="en-US")
			process_text(text)
		except sr.UnknownValueError:
			frappe.msgprint("Google Cloud Speech-to-Text could not understand audio")
		except sr.RequestError as e:
			frappe.msgprint(f"Could not request results from Google Cloud Speech-to-Text service; {e}")



@frappe.whitelist()
# handle validation error
def handle_validation_error(exception):
    # convert error message to speech
    engine = pyttsx3.init()
    engine.say("Hi hello M4")
    engine.runAndWait()



