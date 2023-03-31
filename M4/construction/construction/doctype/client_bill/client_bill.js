frappe.ui.form.on('Client Bill', {
	refresh: function(frm, doc) {
		cur_frm.fields_dict["client_bill_lpe_detail"].grid.get_field('item_of_work').get_query = function() {
				return {
					"filters": {
						"project": cur_frm.doc.project,
					}
				}
			}
			cur_frm.fields_dict["client_bill_lpe_detail"].grid.get_field('project_structure').get_query = function() {
				return {
					"filters": {
						"project": cur_frm.doc.project,
					}
				}
			}
		if(cur_frm.doc.docstatus === 0) {
			cur_frm.add_custom_button(__('Labour Progress Entry'), function() {
				new frappe.ui.form.MultiSelectDialog({
					doctype: "Labour Progress Entry",
					target: cur_frm,
					setters: {
						project_name: cur_frm.doc.project_name
					},
					get_query() {
						return {
							filters: {
								docstatus: ['=', 1],
								client_bill_status: ["!=", "Completed"],
								has_measurement_sheet: ["=", "Yes"],
								is_primary_labour: ["=", "Yes"]
							}
						};
					},
					action(selections) {
						cur_frm.set_value('client_bill_lpe_detail', []);
						var total_lpe_qty = 0;
						for(let b in selections) {
							frappe.db.get_doc("Labour Progress Entry", selections[b]).then(doc => {
								// frappe.db.get_doc("BOQ",doc.boq).then(k => {
								var item = cur_frm.add_child('client_bill_lpe_detail');
								item.item_of_work = doc.item_of_work;
								item.qty = doc.total_qty - doc.previous_client_bill_qty;
								item.boq = doc.boq;
								item.lpe_no = doc.name;
								item.project_structure = doc.project_structure;
								frappe.db.get_doc("BOQ", doc.boq).then(doc1 => {
									item.rate = doc1.rounded_total_rate;
									item.amount = item.rate * doc.total_qty;
									cur_frm.refresh_field("client_bill_lpe_detail");
								});
								total_lpe_qty += item.qty
								console.log(total_lpe_qty)
									//cur_dialog.hide();
								frappe.ui.hide_open_dialog();
								cur_frm.refresh_field("client_bill_lpe_detail");
								cur_frm.set_value("total_lpe_qty", total_lpe_qty)
							});
							//});
						}
						cur_frm.refresh_field("client_bill_lpe_detail");
					}
				});
			}, __("Get Items"));
		}
	},
	get_items: function(frm, doc) {
		cur_frm.set_value('client_bill_detail', null);
		cur_frm.doc.client_bill_lpe_detail.uniqBy(i => i.item_of_work).forEach(j => {
			var row = cur_frm.add_child("client_bill_detail");
			row.item_of_work = j.item_of_work;
			row.boq = j.boq;
			row.project_structure = j.project_structure;
		});
		cur_frm.doc.client_bill_detail.forEach(i => {
			i.qty = cur_frm.doc.client_bill_lpe_detail.filter(j => j.item_of_work == i.item_of_work).reduce((sum, q) => {
				return sum + q.qty
			}, 0);
			i.rate = cur_frm.doc.client_bill_lpe_detail.filter(j => j.item_of_work == i.item_of_work).reduce((sum, q) => {
				return sum + q.rate
			}, 0);
			i.amount = cur_frm.doc.client_bill_lpe_detail.filter(j => j.item_of_work == i.item_of_work).reduce((sum, q) => {
				return sum + q.amount
			}, 0);
		});
		cur_frm.refresh_field('client_bill_detail');
		cur_frm.refresh_field('client_bill_lpe_detail');
		client_bill_items_add()
		highlight();
	},
	total_lpe_qty: function(frm, doc) {
		highlight()
	}
});
frappe.ui.form.on('Client Bill LPE Detail', {
	client_bill_lpe_detail_remove: function(frm, cdt, cdn) {
		lpe_items_add()
	},
	qty: function(frm, cdt, cdn) {
		lpe_items_add()
	}
});

function lpe_items_add(frm) {
	let total_lpe_qty = 0
	cur_frm.doc.client_bill_lpe_detail.forEach(function(i) {
		total_lpe_qty += i.qty;
	});
	cur_frm.set_value("total_lpe_qty", total_lpe_qty);
}

function client_bill_items_add(frm) {
	let total_client_bill_qty = 0
	cur_frm.doc.client_bill_detail.forEach(function(i) {
		total_client_bill_qty += i.qty;
	});
	cur_frm.set_value("total_client_bill_qty", total_client_bill_qty);
}

function highlight(frm) {
	if(cur_frm.doc.total_lpe_qty !== cur_frm.doc.total_client_bill_qty) {
		let $add_cls = $('<span id ="test1" class="spinner-grow spinner-grow-sm"></span>');
		cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default').addClass('btn-danger');
		if($(cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default')).children().length === 0) {
			cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default').append($add_cls);
			frappe.utils.play_sound('alert');
		}
		frappe.show_alert({
			message: __('Update Billing Qty'),
			indicator: 'orange'
		}, 3);
	} else if(cur_frm.doc.total_lpe_qty === cur_frm.doc.total_client_bill_qty) {
		cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default').removeClass('btn-danger');
		if(($(cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default')).children().length !== 0)) {
			document.querySelector('#test1').remove();
		}
		cur_frm.fields_dict.get_items.wrapper.onclick = () => frappe.show_alert({
			message: __('Billing Qty updated'),
			indicator: 'green'
		}, 3, frappe.utils.play_sound('chat-notification'));
	}
}