from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.document import Document



def validate_project_sturcture(self,method):
	ps_list = [d.project_structure for d in self.project_structure_detail]
	if(len(set(ps_list)) != len(ps_list)): 
		frappe.throw('Same Project Structure Exists Multiple Times in Structure Detail')
