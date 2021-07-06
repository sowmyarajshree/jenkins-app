// Copyright (c) 2020, nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Packing Box Labels', {
	item: function(frm,doc) {
		//update items to child table using frapp.call
		const set_fields = ['item_code','part_no','part_name','weight','drawing_no','material','quantity'];
	    frappe.call({
				method: "eurocast.eurocast.doctype.packing_box_labels.packing_box_labels.update_items",
				args: {"docname": frm.doc.name,
				        "item": cur_frm.doc.item
				},
				freeze: true,
				callback: function(r){
					if(r.message) {
					    frm.set_value('packing_box_label_item', []);
						var child = cur_frm.add_child("packing_box_label_item");
						cur_frm.clear_table("packing_box_label_item");
            			$.each(r.message, function(i, d) {
    						var item = frm.add_child('packing_box_label_item');
    						for (let key in d) {
    							if (d[key] && in_list(set_fields, key)) {
    								item[key] = d[key];
    							}
						    }
					    });
					}
					refresh_field('packing_box_label_item');
				}
			});

	},
	no_of_boxes: function(frm,doc) {
		//update no of boxes available to child table
		const set_fields = ['item_code','part_no','part_name','weight','drawing_no','material','quantity'];
	    frappe.call({
				method: "eurocast.eurocast.doctype.packing_box_labels.packing_box_labels.update_items_nos",
				args: {"docname": frm.doc.name,
				        "item": cur_frm.doc.item,
				        "no_of_boxes": cur_frm.doc.no_of_boxes
				},
				freeze: true,
				callback: function(r){
					if(r.message) {
					    frm.set_value('packing_box_label_item', []);
						var child = cur_frm.add_child("packing_box_label_item");
						cur_frm.clear_table("packing_box_label_item");
            			$.each(r.message, function(i, d) {
    						var item = frm.add_child('packing_box_label_item');
    						for (let key in d) {
    							if (d[key] && in_list(set_fields, key)) {
    								item[key] = d[key];
    							}
						    }
					    });
					}
					refresh_field('packing_box_label_item');
				}
			});

	},
	refresh:function(frm){
		frm.set_query("item", function(doc){
			//set filters for item
	        return {
	                "filters": {
	                    "item_group": "Finished Goods"
	            }
	        };
    	});
	}
});
