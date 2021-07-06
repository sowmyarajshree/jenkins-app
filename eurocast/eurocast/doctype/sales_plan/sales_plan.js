// Copyright (c) 2020, nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Plan', {
//filters for item code in child table
	refresh: function(frm) {
		frm.fields_dict.sales_plan_detail.grid.get_field('item_code').get_query = function(doc,cdt,cdn) {
		    var d = locals[cdt][cdn];
			return {
				filters: {
					"is_sales_item": 1,
					"item_code": frm.doc.item_code
				}
			};
		};
		frm.set_query("item_code", function(doc){
        	return {
               		 "filters": {
                    	"item_group": "Finished Goods"
           			 }
        	};
    	});
	},
	sales_plan_frequency: function(frm){
		//set mandatory for fields based on frequency
		if(cur_frm.doc.sales_plan_frequency == "Daily"){
			frm.set_df_property("start_date","reqd",1);
			frm.set_df_property("end_date","reqd",1);
			frm.set_df_property("per_day_qty","reqd",1);
		}
		else{
			frm.set_df_property("start_date","reqd",0);
			frm.set_df_property("end_date","reqd",0);
			frm.set_df_property("per_day_qty","reqd",0);
		}
	},
	is_holiday_list_included:function(frm){
		//set mandatory based on holiday included or not
		if(cur_frm.doc.is_holiday_list_included === 1){
			frm.set_df_property("holiday_list","reqd",1);
		}
		else{
			frm.set_df_property("holiday_list","reqd",0);
		}
	},
	item_code: function(frm){
		//update items to child table using frappe.call
		if(cur_frm.doc.sales_plan_frequency == "Daily"){
			const set_fields = ['date','item_code','frequency_planned_qty'];
		    frappe.call({
					method: "eurocast.eurocast.doctype.sales_plan.sales_plan.update_items",
					args: {"docname": frm.doc.name,
					        "item_code": cur_frm.doc.item_code,
					         "per_day_qty": cur_frm.doc.per_day_qty,
					         "start_date": cur_frm.doc.start_date,
					         "end_date": cur_frm.doc.end_date
					},
					freeze: true,
					callback: function(r){
						if(r.message) {
						    frm.set_value('sales_plan_detail', []);
							var child = cur_frm.add_child("sales_plan_detail");
							cur_frm.clear_table("sales_plan_detail");
	            			$.each(r.message, function(i, d) {
	    						var item = frm.add_child('sales_plan_detail');
	    						for (let key in d) {
	    							if (d[key] && in_list(set_fields, key)) {
	    								item[key] = d[key];
	    							}
							    }
						    });
						}
						refresh_field('sales_plan_detail');
					}
			});
		}
		else{	
			var child = cur_frm.add_child("sales_plan_detail");
			frappe.model.set_value(child.doctype, child.name, "item_code", frm.doc.item_code);
			cur_frm.refresh_field("sales_plan_detail");
		}
	},
	holiday_list: function(frm){
		//update items to child table if holiday is included
		const set_fields = ['date','item_code','frequency_planned_qty'];
		    frappe.call({
					method: "eurocast.eurocast.doctype.sales_plan.sales_plan.update_holidays",
					args: {"docname": frm.doc.name,
					        "item_code": cur_frm.doc.item_code,
					         "per_day_qty": cur_frm.doc.per_day_qty,
					         "start_date": cur_frm.doc.start_date,
					         "end_date": cur_frm.doc.end_date,
					         "holiday_list": cur_frm.doc.holiday_list
					},
					freeze: true,
					callback: function(r){
						if(r.message) {
						    frm.set_value('sales_plan_detail', []);
							var child = cur_frm.add_child("sales_plan_detail");
							cur_frm.clear_table("sales_plan_detail");
	            			$.each(r.message, function(i, d) {
	    						var item = frm.add_child('sales_plan_detail');
	    						for (let key in d) {
	    							if (d[key] && in_list(set_fields, key)) {
	    								item[key] = d[key];
	    							}
							    }
						    });
						}
						refresh_field('sales_plan_detail');
					}
			});
	},
	onload: function(frm){
		//set default fiscal year on loading the document
		frm.set_value('year',frappe.defaults.get_user_default("fiscal_year"));
		//frm.set_df_property("month","options",frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1);
		//frm.refresh_field('month');
       
        frm.ignore_doctypes_on_cancel_all = ["Sales Plan Ledger Entry"];
	},
	month: function(frm){
		//update dates based on month
		frappe.call({
					method: "eurocast.eurocast.doctype.sales_plan.sales_plan.update_dates",
					args: {"docname": frm.doc.name,
					        "month": cur_frm.doc.month,
					        "year": cur_frm.doc.year
					},
					freeze: true,
					callback: function(r){
						if(r.message) {
							frm.set_value("start_date",r.message[0]);
							//frm.set_value("end_date",frappe.datetime.month_end(r.message));
							frm.set_value("end_date",r.message[1]);
						}
					}
			});
	}
});
