// Copyright (c) 2020, nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Outward', {
	update: function(frm,doc) {
		if(frm.doc.gate_outward_type === "Purchase Order"){
			//set values to child table from parent
			var child = cur_frm.add_child("go_purchase_order_details");
			frappe.model.set_value(child.doctype, child.name, "document_no", frm.doc.scan_barcode);
			frappe.model.set_value(child.doctype, child.name, "supplier_name", frm.doc.supplier_name);
			//frappe.model.set_value(child.doctype, child.name, "po_date", frm.doc.out_time);
			frappe.model.set_value(child.doctype, child.name, "document_date", frm.doc.out_time);
			cur_frm.refresh_field("go_purchase_order_details");
		}
		/*if(frm.doc.gate_outward_type === "Job Order"){
			//set values to child table from parent
			var child = cur_frm.add_child("go_purchase_order_details");
			frappe.model.set_value(child.doctype, child.name, "document_no", frm.doc.scan_barcode);
			frappe.model.set_value(child.doctype, child.name, "supplier_name", frm.doc.supplier_name);
			//frappe.model.set_value(child.doctype, child.name, "po_date", frm.doc.out_time);
			frappe.model.set_value(child.doctype, child.name, "document_date", frm.doc.out_time);
			cur_frm.refresh_field("go_purchase_order_details");
		}*/
		if(frm.doc.gate_outward_type === "Job Order"){
			//update child table values from purchase order using frappe.call
			frappe.call({
				method: "eurocast.eurocast.stock_entry_euro.update_service_order",
				args: {"docname": frm.doc.name,
				        "scan_barcode": cur_frm.doc.scan_barcode
				},
				freeze: true,
				callback: function(r){
					if(r.message) {
					    var child = cur_frm.add_child("go_send_service");
			            frappe.model.set_value(child.doctype, child.name, "supplier_name", r.message[0]);
			            frappe.model.set_value(child.doctype, child.name, "stock_entry_no", r.message[1]);
			            frappe.model.set_value(child.doctype, child.name, "stock_entry_date", r.message[2]);
			            cur_frm.refresh_field("go_send_service");
			            frm.set_value("scan_barcode",null);
	
					}
				}
			});
		}
		/*if(frm.doc.gate_outward_type === "Invoices"){
			var child = cur_frm.add_child("go_invoices");
			frappe.model.set_value(child.doctype, child.name, "customer_name", frm.doc.customer_name);
			frappe.model.set_value(child.doctype, child.name, "invoice_date", frm.doc.out_time);
			cur_frm.refresh_field("go_invoices");
		}*/
	},
	refresh: function(frm,doc){
		//set filters for child table fields
    	frm.fields_dict.go_purchase_order_details.grid.get_field('supplier_name').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.supplier_name
					}
				};
		};
		if(frm.doc.gate_outward_type == "Purchase Order"){
			frm.fields_dict.go_purchase_order_details.grid.get_field('document_no').get_query = function(doc,cdt,cdn) {
					return {
						filters: [
							["Stock Entry","nx_supplier","=",frm.doc.supplier_name],
							["Stock Entry","stock_entry_status","=","Open"],
							["Stock Entry","stock_entry_type","=","Send to Service"]
						]
					};
			};
		}
		/*if(frm.doc.gate_outward_type == "Job Order"){
			frm.fields_dict.go_purchase_order_details.grid.get_field('document_no').get_query = function(doc,cdt,cdn) {
					return {
						filters: [
							["Stock Entry","supplier","=",frm.doc.supplier_name],
							["Stock Entry","stock_entry_status","=","Open"],
							["Stock Entry","stock_entry_type","=","Send to Subcontractor"]
						]
					};
			};
		}*/
		if(frm.doc.gate_outward_type == "Invoices"){
			frm.fields_dict.go_invoices.grid.get_field('customer_name').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.customer_name
					}
				};
			};
			frm.fields_dict.go_invoices.grid.get_field('invoice_no').get_query = function(doc,cdt,cdn) {
					return {
						filters: [
							["Sales Invoice","customer","=",frm.doc.customer_name],
							["Sales Invoice","sales_invoice_status","=","Open"]
						]
					};
			};
		}
		if(frm.doc.gate_outward_type == "Job Order"){
			frm.fields_dict.go_send_service.grid.get_field('stock_entry_no').get_query = function(doc,cdt,cdn) {
			    var d = locals[cdt][cdn];
				return {
					filters: [
						["Stock Entry","supplier", "=", d.supplier_name]
					]
				};
			};
		}
		if(frm.doc.gate_outward_type == "Other Deliveries"){
			frm.fields_dict.go_other_deliveries.grid.get_field('dc_no').get_query = function(doc,cdt,cdn) {
			    var d = locals[cdt][cdn];
				return {
					filters: [
						["Stock Entry","stock_entry_type", "=", "External Material Issue"],
						["Stock Entry","docstatus", "=", 1]
					]
				};
			};
		}
	},
	gate_outward_type: function(frm,doc){
		//set filters for child table based on outward types
		if(frm.doc.gate_outward_type == "Purchase Order"){
			frm.fields_dict.go_purchase_order_details.grid.get_field('document_no').get_query = function(doc,cdt,cdn) {
					return {
						filters: [
							["Stock Entry","nx_supplier","=",frm.doc.supplier_name],
							["Stock Entry","stock_entry_status","=","Open"],
							["Stock Entry","stock_entry_type","=","Send to Service"]
						]
					};
			};
		}
		/*if(frm.doc.gate_outward_type == "Job Order"){
			frm.fields_dict.go_purchase_order_details.grid.get_field('document_no').get_query = function(doc,cdt,cdn) {
					return {
						filters: [
							["Stock Entry","supplier","=",frm.doc.supplier_name],
							["Stock Entry","stock_entry_status","=","Open"],
							["Stock Entry","stock_entry_type","=","Send to Subcontractor"]
						]
					};
			};
		}*/
		if(frm.doc.gate_outward_type == "Invoices"){
			frm.fields_dict.go_invoices.grid.get_field('customer_name').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.customer_name
					}
				};
			};
			frm.fields_dict.go_invoices.grid.get_field('invoice_no').get_query = function(doc,cdt,cdn) {
					return {
						filters: [
							["Sales Invoice","customer","=",frm.doc.customer_name],
							["Sales Invoice","sales_invoice_status","=","Open"]
						]
					};
			};
		}
		if(frm.doc.gate_outward_type == "Other Deliveries"){
			frm.fields_dict.go_other_deliveries.grid.get_field('dc_no').get_query = function(doc,cdt,cdn) {
			    var d = locals[cdt][cdn];
				return {
					filters: [
						["Stock Entry","stock_entry_type", "=", "External Material Issue"],
						["Stock Entry","docstatus", "=", 1]
					]
				};
			};
		}
		if ((frm.doc.gate_outward_type == "Purchase Order") || (frm.doc.gate_outward_type == "Job Order")){
			frm.set_df_property("supplier_name","reqd",1);
			//frm.set_df_property("scan_barcode","reqd",1);
		}
		else{
			frm.set_df_property("supplier_name","reqd",0);
			//frm.set_df_property("scan_barcode","reqd",0);
		}
		if(frm.doc.gate_outward_type == "Invoices"){
			frm.set_df_property("customer_name","reqd",1);
		}
		else{
			frm.set_df_property("customer_name","reqd",0);
		}
		if(frm.doc.gate_outward_type == "Employees"){
			frm.set_df_property("employee","reqd",1);
			frm.set_df_property("duty_type","reqd",1);
			frm.set_query("employee", function(doc){
	        	return {
	               		 "filters": {
	                    	"status": "Active"
	           			 }
	        	};
    		});
		}
		else{
			frm.set_df_property("employee","reqd",0);
			frm.set_df_property("duty_type","reqd",0);
		}
	},
	duty_type: function(frm,doc){
		//set out time base on duty type
		if(frm.doc.duty_type == "Leave"){
			//frm.set_df_property("in_time","read_only",1);
			frm.set_value("in_time",frm.doc.out_time);
		}
		else{
			//frm.set_df_property("in_time","read_only",0);
			frm.set_value("in_time",null);
		}
	},
	customer_name: function(frm,doc){
		//set values to child table based on outward type
		if(frm.doc.gate_outward_type == "Invoices"){
			var child = cur_frm.add_child("go_invoices");
			frappe.model.set_value(child.doctype, child.name, "customer_name", frm.doc.customer_name);
			cur_frm.refresh_field("go_invoices");
		}
	},
	generate_out_time:function(frm,doc){
		//set in_time value
		cur_frm.set_value("in_time",frappe.datetime.now_datetime());
	},
	ending_km: function(frm,doc){
		//calculate total km 
		var total = frm.doc.ending_km - frm.doc.starting_km;
		frm.set_value("total_km",total);
	},
	ending_km:function(frm,doc) {
		//calculate total km 
		let total_distance = frm.doc.ending_km - frm.doc.starting_km;
		frm.set_value("total_km",total_distance);
	},
	supplier_name:function(frm,doc){
		if(frm.doc.gate_outward_type == "Other Deliveries"){
			frm.fields_dict.go_other_deliveries.grid.get_field('dc_no').get_query = function(doc,cdt,cdn) {
			    var d = locals[cdt][cdn];
				return {
					filters: [
						["Stock Entry","stock_entry_type", "=", "External Material Issue"],
						["Stock Entry","docstatus", "=", 1],
						//["Stock Entry","nx_gate_outward", "=", " "],
						["Stock Entry","nx_supplier", "=", frm.doc.supplier_name]
					]
				};
			};
		}

	},
	customer_name:function(frm,doc){
		if(frm.doc.gate_outward_type == "Other Deliveries"){
			frm.fields_dict.go_other_deliveries.grid.get_field('dc_no').get_query = function(doc,cdt,cdn) {
			    var d = locals[cdt][cdn];
				return {
					filters: [
						["Stock Entry","stock_entry_type", "=", "External Material Issue"],
						["Stock Entry","docstatus", "=", 1],
						//["Stock Entry","nx_gate_outward", "=", " "],
						["Stock Entry","nx_customer_name", "=", frm.doc.customer_name]
					]
				};
			};
		}

	}
});

