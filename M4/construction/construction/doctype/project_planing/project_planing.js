//filters
function item_of_work_filter() {
	cur_frm.set_query("item_of_work", function(doc) {
		return {
			"filters": {
				"project": cur_frm.doc.project,
				'status': 'Active'
			}
		};
	});
}

function project_structure_filter() {
	cur_frm.set_query("project_structure", function(doc) {
		return {
			"filters": {
				"project": cur_frm.doc.project,
			}
		};
	});
}

function project_filter() {
	cur_frm.set_query("project", function(doc) {
		return {
			"filters": {
				"status": 'Open',
			}
		};
	});
}
frappe.ui.form.on('Project Planing', {
	get_boq: function(frm, doc) {
		//if (cur_frm.doc.project !== null && cur_frm.doc.project_structure === null && cur_frm.doc.item_of_work === null){
		const fields = ["boq"];
		frappe.call({
			method: "construction.construction.doctype.project_planing.project_planing.get_boq_entry",
			args: {
				"project": frm.doc.project || '',
				"proj_str": frm.doc.project_structure || "",
				"item_of_work": frm.doc.item_of_work || ""
			},
			freeze: true,
			callback: function(r) {
				if(r.message) {
					$.each(r.message, function(d, i) {
						var boq = frm.add_child("project_plan_details");
						for(let k in i) {
							if(i[k] && in_list(fields, k)) {
								boq[k] = i[k];
							}
						}
					});
				}
				cur_frm.refresh_field("project_plan_details")
			}
		});
		cur_frm.clear_table("project_plan_details")
			//	}
	},
	refresh: function(frm, doc) {
		cur_frm.disable_save()

		function glow() {
			cur_frm.fields_dict['project_plan_details'].$wrapper.css("boxShadow", "#8fd7d2 0px 0px 22px")
		}
		cur_frm.add_custom_button("Create Task", () => {
			let selected_items = []
			cur_frm.doc.project_plan_details.filter(i => {
				if(i.__checked === 1) {
					selected_items.push(i.boq)
				}
			})
			if((cur_frm.doc.project_plan_details === undefined || cur_frm.doc.project_plan_details === '') || cur_frm.doc.project_plan_details.length === 0) {
				frappe.throw("Right Now  'Not Scheduled' BOQs Are Not Available To Creating Tasks For This Project")
			} else if(selected_items.length === 0) {
				frappe.msgprint('To Create a New TASK Select BOQ from Project Plan details')
				setTimeout(glow(), 1000);
				cur_frm.fields_dict['project_plan_details'].$wrapper.css("boxShadow", "none")
			} else {
				frappe.call({
					method: 'construction.construction.doctype.project_planing.project_planing.create_task',
					args: {
						'items': selected_items,
					},
					freeze: true,
					callback: (r) => {
						if(!r.exc) {
							cur_frm.doc.project_plan_details = cur_frm.doc.project_plan_details.filter(i => (i.__checked !== 1));
							cur_frm.doc.project_plan_details.forEach((i, cint = 0) => i.idx = cint + 1);
							cur_frm.refresh_field('project_plan_details');
						}
					}
				});
			}
		});
		//filter for BOQ in project planing
		cur_frm.fields_dict.project_plan_details.grid.get_field("boq").get_query = function() {
			return {
				filters: {
					"project": cur_frm.doc.project,
					"project_structure": cur_frm.doc.project_structure,
					"item_of_work": cur_frm.doc.item_of_work
				}
			}
		}
	}
});
frappe.ui.form.on('Project Planing', {
	project: function(frm, doc) {
		project_structure_filter();
		if(cur_frm.doc.project === undefined || '') {
			cur_frm.set_value('project_name', '');
			cur_frm.set_value('customer_name', '');
			cur_frm.set_value('item_of_work', '');
			cur_frm.set_value('project_structure', '');
			cur_frm.set_value('project_plan_details', '');
		}
	},
	setup: function(frm, doc) {
		item_of_work_filter();
		project_filter();
	}
});