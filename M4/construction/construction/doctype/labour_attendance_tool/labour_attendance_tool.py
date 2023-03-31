# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LabourAttendanceTool(Document):
	pass

@frappe.whitelist()
def create_labour_attendance(project,muster_roll_details):
	#frappe.throw(_("muster_role_details {0}").format(muster_role_details))
	muster_role = eval(muster_roll_details)
	#labourer_list = json.loads(muster_role_details).get("muster_role_details")

	for i in muster_role:
		lab_att_doc = frappe.new_doc("Labour Attendance")
		lab_att_doc.update({
			"project":project,
			#"posting_date":posting_date,
			"attendance_type":"Muster Roll",
			"muster_roll":i["muster_roll"],
			"working_hours":8,
			"total_hours":8		
			})
		lab_att_doc.submit()
		frappe.db.commit()
	frappe.msgprint("Today's Attendance for Muster Role is created")


	