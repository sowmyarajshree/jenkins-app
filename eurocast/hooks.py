# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "eurocast"
app_title = "Eurocast"
app_publisher = "nxweb"
app_description = "Development for Eurocast"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@nxweb.in"
app_license = "MIT"

fixtures = ["Custom Field","Print Format","Custom Script"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/eurocast/css/eurocast.css"
# app_include_js = "/assets/eurocast/js/eurocast.js"

# include js, css files in header of web template
# web_include_css = "/assets/eurocast/css/eurocast.css"
# web_include_js = "/assets/eurocast/js/eurocast.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "eurocast.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "eurocast.install.before_install"
# after_install = "eurocast.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "eurocast.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
"Work Order": {
    "before_save":"eurocast.eurocast.work_order.warehouse",
    "on_submit": "eurocast.eurocast.work_order.warehouse"
    #"before_update_after_submit": ["eurocast.eurocast.operation.update_produced_qty"]
},
"Production Plan": {
    "on_submit":"eurocast.eurocast.production.prod_plan_item",
    "before_save":"eurocast.eurocast.production.prod_plan_item"
},
"Job Card": {
    "on_submit": "eurocast.eurocast.operation.update_wo_op",
    #"on_cancel": ["eurocast.eurocast.operation.update_wo_ops","eurocast.eurocast.operation.val_jb_op","eurocast.eurocast.doctype.operator_entry.operator_entry.cancel_stock_entry"]
    #"validate": "eurocast.eurocast.operation.validate_jb"
},
"Operator Entry": {
	#"after_insert":"eurocast.eurocast.operation.create_job_cards",
	"after_delete": "eurocast.eurocast.operation.on_cancel_op",
    "on_trash": "eurocast.eurocast.operation.on_trash_op",
    "validate": "eurocast.eurocast.operation.val_comp_qty",
    "before_save":["eurocast.eurocast.operation.get_bom_time","eurocast.eurocast.operation.cal_time","eurocast.eurocast.operation.strt_end_cal"],
    "on_update": ["eurocast.eurocast.operation.get_bom_time","eurocast.eurocast.operation.cal_time","eurocast.eurocast.operation.strt_end_cal"],
    "on_submit": ["eurocast.eurocast.operation.val_difference_time", "eurocast.eurocast.operation.create_job_cards", "eurocast.eurocast.doctype.operator_entry.operator_entry.create_finish_entry"],
    "on_cancel": "eurocast.eurocast.operation.on_cancel_op"
},
"Purchase Receipt": {
    "before_save": "eurocast.eurocast.purchase_receipt_euro.val_is_inspection",
    "on_submit": ["eurocast.eurocast.purchase_receipt_euro.update_gate_inward","eurocast.eurocast.purchase_receipt_euro.null_gate","eurocast.eurocast.purchase_receipt_euro.update_received_qty","eurocast.eurocast.purchase_receipt_euro.update_returned_qty"],
    "on_cancel": ["eurocast.eurocast.purchase_receipt_euro.unlink_gate_inward","eurocast.eurocast.purchase_receipt_euro.cancel_received_qty","eurocast.eurocast.purchase_receipt_euro.cancel_returned_qty"],
    "validate": ["eurocast.eurocast.purchase_receipt_euro.validate_gate_inward_no","eurocast.eurocast.purchase_receipt_euro.validate_pr","eurocast.eurocast.purchase_receipt_euro.update_supplier_warehouse_onsave","eurocast.eurocast.purchase_receipt_euro.update_bom_onReturn","eurocast.eurocast.purchase_order.copy_billno_billdate"],
    "before_submit":"eurocast.eurocast.purchase_receipt_euro.validate_po_qty"
    #"before_submit":"eurocast.eurocast.purchase_receipt_euro.update_supplier_warehouse_onsave"
    #"before_submit":"eurocast.eurocast.purchase_receipt_euro.validate_po_gate_inward"
},
"Material Request": {
    "before_save": "eurocast.eurocast.material_req.update_warehouse"
},
"Stock Entry": {
    "before_save": ["eurocast.eurocast.stock_entry_euro.update_source_warehouse","eurocast.eurocast.stock_entry_euro.update_parent_warehouse","eurocast.eurocast.stock_entry_euro.validate_shift","eurocast.eurocast.stock_entry_euro.update_stock_entry_no","eurocast.eurocast.stock_entry_euro.copy_purchase_order"],
    "on_update": ["eurocast.eurocast.stock_entry_euro.update_source_warehouse","eurocast.eurocast.stock_entry_euro.calculate_total_rejection_value_and_weight"],
    "on_submit": ["eurocast.eurocast.purchase_receipt_euro.update_gi_st","eurocast.eurocast.stock_entry_euro.update_rejection_entry","eurocast.eurocast.stock_entry_euro.validate_inspection_item","eurocast.eurocast.stock_entry_euro.update_purchase_order","eurocast.eurocast.stock_entry_euro.reload_entry",
                    "eurocast.eurocast.stock_entry_euro.update_supplier_gi","eurocast.eurocast.stock_entry_euro.update_customer_gi","eurocast.eurocast.stock_entry_euro.update_received_gi","eurocast.eurocast.stock_entry_euro.validate_repack_entry","eurocast.eurocast.stock_entry_euro.update_others_gi"],
    "before_submit":["eurocast.eurocast.stock_entry_euro.validate_shift","eurocast.eurocast.stock_entry_euro.validate_duplicate_box_nos"],
    "on_cancel": ["eurocast.eurocast.purchase_receipt_euro.unlink_gi_st","eurocast.eurocast.stock_entry_euro.cancel_rejection_entry","eurocast.eurocast.stock_entry_euro.unlink_quality_inspection",
                    "eurocast.eurocast.stock_entry_euro.cancel_supplier_gi","eurocast.eurocast.stock_entry_euro.cancel_received_gi","eurocast.eurocast.stock_entry_euro.cancel_customer_gi","eurocast.eurocast.stock_entry_euro.cancel_others_gi"],
    "validate":["eurocast.eurocast.stock_entry_euro.update_stock_entry_barcode","eurocast.eurocast.stock_entry_euro.validate_warehouse_fg_stock","eurocast.eurocast.stock_entry_euro.set_actual_qty","eurocast.eurocast.stock_entry_euro.validate_supplier_warehouse"]
},
"Sales Invoice": {
    "on_submit": ["eurocast.eurocast.sales_inv_euro.update_gate_inward","eurocast.eurocast.sales_inv_euro.create_stock_entry"],
    "before_submit": "eurocast.eurocast.sales_inv_euro.calculate_bin_qty",
    "on_cancel": ["eurocast.eurocast.sales_inv_euro.cancel_gate_inward_link","eurocast.eurocast.sales_inv_euro.unlink_stock_entry"],
    "validate": "eurocast.eurocast.sales_inv_euro.update_cus_date"
},
"Purchase Order": {
    "on_cancel": "eurocast.eurocast.purchase_receipt_euro.unlink_and_cancel_stock_entry",
    "before_submit": ["eurocast.eurocast.purchase_order.validate_same_item","eurocast.eurocast.purchase_order.validate_raw_material_as_item","eurocast.eurocast.purchase_order.create_nx_item_code"]
    #"before_update_after_submit": "eurocast.eurocast.purchase_receipt_euro.remove_gi_in_childtable"
},
"Quality Inspection": {
    "on_submit": "eurocast.eurocast.stock_entry_euro.update_stock_entry",
    "on_cancel": "eurocast.eurocast.stock_entry_euro.unlink_stock_entry"
},
"Delivery Trip":{
    "on_submit": ["eurocast.eurocast.delivery_trip.update_stock_entry","eurocast.eurocast.delivery_trip.update_sv_st"],
    #"before_submit": "eurocast.eurocast.delivery_trip.update_address",
    "on_cancel": ["eurocast.eurocast.delivery_trip.unlink_stock_entry","eurocast.eurocast.delivery_trip.unlink_sv_st"],
    "before_update_after_submit": "eurocast.eurocast.delivery_trip.update_delivery_status"
},
"Attendance":{
    "validate":["eurocast.eurocast.attendance.update_attendance"],
    "before_update_after_submit": ["eurocast.eurocast.attendance.update_attendance"],
    "on_update_after_submit": ["eurocast.eurocast.attendance.update_attendance"]

},
"Employee":{
    "validate":"eurocast.eurocast.employee.validate_doj"
},
"Purchase Invoice":{
    "validate":"eurocast.eurocast.purchase_receipt_euro.update_taxes_purchaseinvoice"
}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"eurocast.tasks.all"
# 	],
# 	"daily": [
# 		"eurocast.tasks.daily"
# 	],
# 	"hourly": [
# 		"eurocast.tasks.hourly"
# 	],
# 	"weekly": [
# 		"eurocast.tasks.weekly"
# 	]
# 	"monthly": [
# 		"eurocast.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "eurocast.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "eurocast.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "eurocast.task.get_dashboard_data"
# }
