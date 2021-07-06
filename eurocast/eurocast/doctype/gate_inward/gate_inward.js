// Copyright (c) 2020, nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Inward', {
	inward_types: function(frm) {
		//filters for child table based on inward types
		if (frm.doc.inward_types === "Purchase Order"){
			frm.fields_dict.gi_po_details.grid.get_field('purchase_order').get_query = function(doc,cdt,cdn) {
			    var d = locals[cdt][cdn];
				return {
					filters: [
						["Purchase Order","status", "in", "To Receive and Bill,To Receive"],
						["Purchase Order","naming_series", "=", "PUR-ORD-.YYYY.-"],
						["Purchase Order","supplier", "=", frm.doc.supplier_name]
					]
				};
			};
			/*frm.set_query("supplier_name", function(doc){
	        	return {
	               		 "filters": [
	                    	["Supplier","supplier_group","!=","Sub Contractor"]
	           			 ]
	        	};
    		});*/
		}
		if (frm.doc.inward_types === "Job Work Order"){
			frm.fields_dict.gi_po_details.grid.get_field('purchase_order').get_query = function(doc,cdt,cdn) {
			    var d = locals[cdt][cdn];
				return {
					filters: [
						["Purchase Order","status", "in", "To Receive and Bill,To Receive"],
						["Purchase Order","naming_series", "=", "JOB-ORD-.YYYY.-"],
						["Purchase Order","supplier", "=", frm.doc.supplier_name]
					]
				};
			};
			frm.set_query("supplier_name", function(doc){
	        	return {
	               		 "filters": {
	                    	"supplier_group": "Sub Contractor"
	           			 }
	        	};
    		});
		}
		if((frm.doc.inward_types === "Purchase Order") || (frm.doc.inward_types === "Job Work Order")) {
			frm.set_df_property("is_company_vehicle","reqd",1);
			frm.set_df_property("supplier_name","reqd",1);
			frm.set_df_property("vehicle_no","reqd",1);
		}
		else{
			frm.set_df_property("is_company_vehicle","reqd",0);
			frm.set_df_property("supplier_name","reqd",0);
			frm.set_df_property("vehicle_no","reqd",0);
		}
		if(frm.doc.inward_types === "Customer Returns"){
			frm.set_df_property("is_company_vehicle","reqd",1);
			frm.set_df_property("customer_name","reqd",1);
			frm.set_df_property("vehicle_no","reqd",1);
		}
		else{
			frm.set_df_property("is_company_vehicle","reqd",0);
			frm.set_df_property("customer_name","reqd",0);
			frm.set_df_property("vehicle_no","reqd",0);
		}
		if(frm.doc.inward_types === "Returnables"){
			frm.set_df_property("is_company_vehicle","reqd",1);
			frm.set_df_property("supplier_name","reqd",1);
			frm.set_df_property("vehicle_no","reqd",1);
		}
		else{
			frm.set_df_property("is_company_vehicle","reqd",0);
			frm.set_df_property("supplier_name","reqd",0);
			frm.set_df_property("vehicle_no","reqd",0);
		}
		if(frm.doc.inward_types === "Couriers"){
			frm.set_df_property("courier_provider","reqd",1);
		}
		else{
			frm.set_df_property("courier_provider","reqd",0);
		}
		if(frm.doc.inward_types === "Visitors Entry"){
			frm.set_df_property("vi_company","reqd",1);
			frm.set_df_property("vi_in_time","reqd",1);
			frm.set_df_property("vi_mobile_no","reqd",1);
			frm.set_df_property("vi_contact_person","reqd",1);
		}
		else{
			frm.set_df_property("vi_company","reqd",0);
			frm.set_df_property("vi_in_time","reqd",0);
			frm.set_df_property("vi_mobile_no","reqd",0);
			frm.set_df_property("vi_contact_person","reqd",0);
		}
		if(frm.doc.inward_types === "Job Work Order"){
			frm.fields_dict.gi_job_work_received_service.grid.get_field('purchase_order').get_query = function(doc,cdt,cdn) {
					return {
						filters: [
							["Purchase Order","status", "in", "To Receive and Bill,To Receive,To Bill"],
							["Purchase Order","naming_series", "in", "SER-ORD-.YYYY.-,JOB-ORD-.YYYY.-"],
							//["Purchase Order","supplier", "=", frm.doc.supplier_name]
						]
					};
			};
		}
	},
	update: function(frm,doc) {
		//update child table items using frappe.call
		if(frm.doc.inward_types === "Purchase Order"){
			const set_fields = ['purchase_order','supplier','pending_qty','document_no','document_date','item_name','po_date','description','item_code','rate','amount','warehouse','cost_center','uom','nx_item_code','conversion_factor','stock_uom','is_subcontracted','supplier_warehouse'];
			frappe.call({
				method: "eurocast.eurocast.doctype.gate_inward.gate_inward.update_po_items",
				args: {"docname": frm.doc.name,
						"supplier_name":frm.doc.supplier_name,
						"document_no":frm.doc.document_no,
						"document_date": frm.doc.document_date,
				        "scan_barcode": cur_frm.doc.scan_barcode
				},
				freeze: true,
				callback: function(r){
					if(r.message) {
					    //frappe.model.set_value('items',[]);
						//var child = cur_frm.add_child("items",{});
					    //cur_frm.clear_table("items");
            			$.each(r.message, function(i, d) {
    						var item = frm.add_child('gi_po_details');
    						for (let key in d) {
    							if (d[key] && in_list(set_fields, key)) {
    								item[key] = d[key];
    							}
						    }
					    });
					}
					frm.set_value("scan_barcode",null);
					frm.set_value("document_no",null);
					frm.set_value("document_date",null);
					frm.set_value("supplier_name",null);
					cur_frm.refresh_field("gi_po_details");
				}
			});

			/*var child = cur_frm.add_child("gi_po_details");
			frappe.model.set_value(child.doctype, child.name, "purchase_order", frm.doc.scan_barcode);
			frappe.model.set_value(child.doctype, child.name, "supplier", frm.doc.supplier_name);
			cur_frm.refresh_field("gi_po_details");
			frm.set_value("scan_barcode",null);*/
		}
		//update values to child table based on parent fields
		if(frm.doc.inward_types === "Job Work Order"){
			var child = cur_frm.add_child("gi_po_details");
			frappe.model.set_value(child.doctype, child.name, "purchase_order", frm.doc.scan_barcode);
			frappe.model.set_value(child.doctype, child.name, "supplier", frm.doc.supplier_name);
			cur_frm.refresh_field("gi_po_details");
		}
		//update child table values using frappe.call
		if(frm.doc.inward_types === "Job Work Order"){
			const set_fields = ['purchase_order','supplier_name','pending_qty','document_no','document_date','item_name','po_date','description','item_code','rate','amount','warehouse','cost_center','uom','bom','nx_item_code','conversion_factor','stock_uom','is_subcontracted','supplier_warehouse'];
			frappe.call({
				method: "eurocast.eurocast.stock_entry_euro.update_received_service",
				args: {"docname": frm.doc.name,
						"supplier_name":frm.doc.supplier_name,
						"document_no":frm.doc.document_no,
						"document_date": frm.doc.document_date,
				        "scan_barcode": cur_frm.doc.scan_barcode
				},
				freeze: true,
				callback: function(r){
					if(r.message) {
						//frappe.model.set_value('items',[]);
						//var child = cur_frm.add_child("items",{});
					    //cur_frm.clear_table("items");
            			$.each(r.message, function(i, d) {
    						var item = frm.add_child('gi_job_work_received_service');
    						for (let key in d) {
    							if (d[key] && in_list(set_fields, key)) {
    								item[key] = d[key];
    							}
						    }
					    });
					}
					frm.set_value("scan_barcode",null);
					frm.set_value("document_no",null);
					frm.set_value("document_date",null);
					frm.set_value("supplier_name",null);
					cur_frm.refresh_field("gi_job_work_received_service");
				}
			});
		}
	},
	refresh: function(frm,doc){
    	/*frm.set_query("courier_provider", function(doc){
        	return {
               		 "filters": {
                    	"nx_is_courier": 1
           			 }
        	};
    	});*/
    	//set filters for fields in child table
    	frm.fields_dict.gi_po_details.grid.get_field('supplier').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.supplier_name
					}
				};
		};
		frm.fields_dict.gi_returnables.grid.get_field('supplier_name').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.supplier_name
					}
				};
		};
		frm.fields_dict.gi_bills.grid.get_field('supplier_name').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.supplier_name
					}
				};
		};
		frm.fields_dict.gi_bills.grid.get_field('issued_to').get_query = function(doc,cdt,cdn) {
				return {
					filters: [
						["Employee","grade","in","STAFF,SUB STAFF"]
					]
				};
		};
		frm.fields_dict.gi_customer_returns.grid.get_field('customer_name').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.customer_name
					}
				};
		};
		if(cur_frm.inward_types === "Job Work Order"){
			frm.set_query("courier_provider", function(doc){
	        	return {
	               		 "filters": {
	                    	"supplier_group": "Sub Contractor"
	           			 }
	        	};
    		});
		}
		frm.fields_dict.gi_supplier_return.grid.get_field('supplier_name').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.supplier_name
					}
				};
		};
		frm.fields_dict.gi_customer_provided.grid.get_field('customer_name').get_query = function(doc,cdt,cdn) {
				return {
					filters: {
						"name": frm.doc.customer_name
					}
				};
		};
		frm.fields_dict.gi_job_work_received_service.grid.get_field('purchase_order').get_query = function(doc,cdt,cdn) {
				return {
					filters: [
						["Purchase Order","status", "in", "To Receive and Bill,To Receive,To Bill"],
						["Purchase Order","naming_series", "in", "SER-ORD-.YYYY.-,JOB-ORD-.YYYY.-"],
						//["Purchase Order","supplier", "=", frm.doc.supplier_name]
					]
				};
		};
	},
	generate_out_time: function(frm,doc){
		//set in time and out time
		frm.set_value("vehicle_out_time",frappe.datetime.now_datetime());
		frm.set_value("vi_out_time",frappe.datetime.now_datetime());
	},
	customer_name: function(frm,doc){
		//uodate values to child table based on parent field values
		if(frm.doc.inward_types == "Customer Returns"){
			var child = cur_frm.add_child("gi_customer_returns");
			frappe.model.set_value(child.doctype, child.name, "customer_name", frm.doc.customer_name);
			cur_frm.refresh_field("gi_customer_returns");
		}
		if(frm.doc.inward_types == "Customer Provided Item"){
			var child = cur_frm.add_child("gi_customer_provided");
			frappe.model.set_value(child.doctype, child.name, "customer_name", frm.doc.customer_name);
			cur_frm.refresh_field("gi_customer_provided");
		}
	},
	supplier_name: function(frm,doc){
		/*if(frm.doc.inward_types === "Purchase Order"){
			var child = cur_frm.add_child("gi_po_details");
			frappe.model.set_value(child.doctype, child.name, "supplier", frm.doc.supplier_name);
			cur_frm.refresh_field("gi_po_details");
		}
		if(frm.doc.inward_types === "Job Work Order"){
			var child = cur_frm.add_child("gi_po_details");
			frappe.model.set_value(child.doctype, child.name, "supplier", frm.doc.supplier_name);
			cur_frm.refresh_field("gi_po_details");
		}*/
		//uodate values to child table based on parent field values
		if(frm.doc.inward_types == "Bills"){
			var child = cur_frm.add_child("gi_bills");
			frappe.model.set_value(child.doctype, child.name, "supplier_name", frm.doc.supplier_name);
			cur_frm.refresh_field("gi_bills");
		}
		if(frm.doc.inward_types == "Returnables"){
			var child = cur_frm.add_child("gi_returnables");
			frappe.model.set_value(child.doctype, child.name, "supplier_name", frm.doc.supplier_name);
			cur_frm.refresh_field("gi_returnables");
		}
		if(frm.doc.inward_types == "Supplier Return"){
			var child = cur_frm.add_child("gi_supplier_return");
			frappe.model.set_value(child.doctype, child.name, "supplier_name", frm.doc.supplier_name);
			cur_frm.refresh_field("gi_supplier_return");
		}
	},
	is_supplier_not_in_list:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		//set field properties
		if(frm.doc.is_supplier_not_in_list == 1){
			var supplier = frappe.meta.get_docfield("GI Bills", "supplier_name", cur_frm.doc.name);
        	supplier.read_only = 1;
			frm.set_df_property("supplier_name","read_only",1);
			frm.set_df_property("supplier_name","reqd",0);
		}
		else{
			frm.set_df_property("supplier_name","read_only",0);
			var supplier = frappe.meta.get_docfield("GI Bills", "supplier_name", cur_frm.doc.name);
        	supplier.read_only = 0;
        	frm.set_df_property("supplier_name","reqd",1);
		}
	}
	//onload: function(frm,cdt,cdn) {
		//frappe.model.add_child(cur_frm.doc, "GI PO Details", "gi_po_details");
	//}
});

/*frappe.ui.form.on('Gate Inward', {
	user: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];
		if(d.user){
			var acknowledgement = frappe.meta.get_docfield("GI Bills", "acknowledgement", cur_frm.doc.name);
        	acknowledgement.read_only = 1;
        	var user = frappe.meta.get_docfield("GI Bills", "user", cur_frm.doc.name);
        	user.read_only = 1;
        	//d.user.read_only = 1;
		}
		else{
			var acknowledgement = frappe.meta.get_docfield("GI Bills", "acknowledgement", cur_frm.doc.name);
        	acknowledgement.read_only = 0;
        	var user = frappe.meta.get_docfield("GI Bills", "user", cur_frm.doc.name);
        	user.read_only = 0;
        	//d.user.read_only = 0;
		}
	}
});


frappe.ui.form.on('GI Courier Details', {
	form_render: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];
		if(d.acknowledgement){
			var acknowledgement = frappe.meta.get_docfield("GI Courier Details", "acknowledgement", cur_frm.doc.name);
        	acknowledgement.read_only = 1;
        	var user = frappe.meta.get_docfield("GI Courier Details", "issued_to", cur_frm.doc.name);
        	user.read_only = 1;
        	//d.user.read_only = 1;
		}
		else{
			var acknowledgement = frappe.meta.get_docfield("GI Courier Details", "acknowledgement", cur_frm.doc.name);
        	acknowledgement.read_only = 0;
        	var user = frappe.meta.get_docfield("GI Courier Details", "issued_to", cur_frm.doc.name);
        	user.read_only = 0;
        	//d.user.read_only = 0;
		}
	}
});*/