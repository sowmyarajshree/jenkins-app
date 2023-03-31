/*
#parent filter
1.project
2.project_strucure

#parent function
1.project_filter()
2.create_boq()
3.get_boq_entry()

child filter
1.BOQ(boq_list)
2.project_structure(project_struture_list)

child function
1.boq_filter()
2.project_structure_filter()
3.apply_project_structure_filter()
*/

function project_filter() {
    cur_frm.set_query("project", function() {
        return {
            filters: [
                ["Project", "status", "=", "Open"]
            ]
        }
    })
}

function boq_filter() {
    cur_frm.fields_dict["boq_list"].grid.get_field('boq').get_query = function() {
        return {
            "filters": {
                "project": cur_frm.doc.project,
                'project_structure': cur_frm.doc.project_structure,
            }
        }
    }
}

function project_structure_filter() {
    cur_frm.fields_dict["project_structure_list"].grid.get_field('project_structure').get_query = function() {
        return {
            "filters": {
                "project": cur_frm.doc.project,
            }
        }
    }
}

function create_boq() {
    cur_frm.add_custom_button("Create BOQ", () => {
        let selected_boq = [];
        let selected_proj_str = [];
        cur_frm.doc.boq_list.filter(i => {
            {
                selected_boq.push(i.boq);
            }
        });
        cur_frm.doc.project_structure_list.filter(i => {
            {
                selected_proj_str.push(i.project_structure);
            }
        });
        frappe.call({
            method: 'construction.construction.doctype.boq_generation_tool.boq_generation_tool.create_boq',
            args: {
                "selected_boq": selected_boq,
                "selected_proj_str": selected_proj_str
            },
            freeze: true,
            callback: (r) => {
                if (!r.exc) {
                    cur_frm.doc.boq_list = cur_frm.doc.boq_list.filter(i => (i.__checked !== 1));
                    cur_frm.doc.boq_list.forEach((i, cint = 0) => i.idx = cint + 1);
                    cur_frm.refresh_field("boq_list");
                }
            }
        });
    })
}

function get_boq_entry() {
    const fields = ["boq", "item_of_work", "project_structure"];
    frappe.call({
        method: "construction.construction.doctype.boq_generation_tool.boq_generation_tool.get_boq_entry",
        args: {
            "project": cur_frm.doc.project || '',
            "proj_str": cur_frm.doc.project_structure || ""
        },
        freeze: true,
        callback: function(r) {
            if (r.message) {
                $.each(r.message, function(d, i) {
                    var boq = cur_frm.add_child("boq_list");
                    for (let k in i) {
                        if (i[k] && in_list(fields, k)) {
                            boq[k] = i[k];
                        }
                    }
                });
            }
            cur_frm.refresh_field("boq_list")
        }
    });
    
    cur_frm.clear_table("boq_list")
}

function apply_project_structure_filter() {
    var pro_str = []
    frappe.db.get_doc("Project", cur_frm.doc.project).then(pro_doc => {
        pro_doc.project_structure_detail.forEach(i => {
            pro_str.push(i.project_structure)
        });
        cur_frm.fields_dict["project_structure"].get_query = function(doc) {
            return {
                filters: [
                    ["name", "in", pro_str]
                ]
            }
        }
    })
}
function glow(frm) {
    if (cur_frm.doc.total_amount !== null) {
        cur_frm.fields_dict.get_boq.$input_wrapper.find('.btn-default').addClass('btn-primary');
        frappe.utils.play_sound('chat-notification');
    }
}

frappe.ui.form.on('BOQ Generation Tool', {
    refresh: function(frm, doc) {
        project_filter();
        boq_filter();
        project_structure_filter();
        create_boq();

        cur_frm.$wrapper.find('.btn-sm').remove()
        if (cur_frm.doc.project === "" || cur_frm.doc.project === undefined) {} else if (cur_frm.doc.project !== "" || cur_frm.doc.project !== undefined) {

        }
        cur_frm.fields_dict.get_boq.$input_wrapper.find('.btn-default').addClass('btn-primary');

    },
    get_boq: function(frm, doc) {
        get_boq_entry();
        glow();
    },
    project: function(frm, doc) {
        apply_project_structure_filter();
    }
});
