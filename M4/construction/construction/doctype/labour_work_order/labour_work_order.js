/*
#Parent Filter
1.project

#Parent Function
1.apply_project_filter()

#Child Filter

#Child function
*/
function apply_project_filter() {
    cur_frm.set_query("project", function() {
        return {
            filters: [
                [
                    "Project", "status", "=", "Open"
                ]
            ]
        }

    })
}

function apply_subcontractor_filter() {
    cur_frm.set_query("subcontractor", function() {
        return {
            filters: [
                ["Supplier", "nx_is_sub_contractor", "=", 1]
            ]
        }
    })
}

function apply_price_list_filter() {
    cur_frm.set_query("price_list", function() {
        return {
            filters: [
                ["Price List", "buying", "=", 1]
            ]
        }

    })
}

function get_labour_list() {
    frappe.xcall('construction.construction.doctype.labour_work_order.labour_work_order.get_labour_list', {
        'project_name': cur_frm.doc.project,
        'labour_type': cur_frm.doc.labour_type,
        'subcontractor': cur_frm.doc.subcontractor
    }).then(i =>

        cur_frm.fields_dict.labour_rate_details.grid.get_field('labour_item').get_query = function() {
            return {
                filters: [
                    ['Labour', 'name', 'in', i],
                    ['Labour','is_disabled','=',0]
                ]
            }
        })
}

function update_labour_attendance_details() {
    let last_doc = frappe.socketio.last_doc;
    if (last_doc !== undefined) {
        if (last_doc[0] === 'Labour Attendance' || last_doc[0] === 'Rate Work Entry' || last_doc[0] === 'F and F Entry') {
            try {
                let lst_doc = frappe.get_doc(last_doc[0], last_doc[1]);
                cur_frm.set_value(lst_doc);
            } 
            
            catch (error) {
                console.error(error);

            }
        }
    }
}

frappe.ui.form.on('Labour Work Order', {
    refresh: function(frm, doc) {
        apply_project_filter();
        apply_subcontractor_filter();
        apply_price_list_filter();
        update_labour_attendance_details();
        get_labour_list();

        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === "F and F Entry") {
            let fnf_doc = frappe.model.get_doc("F and F Entry", frappe.get_prev_route()[2])
            cur_frm.set_value("project", fnf_doc.project)
        }
    },

    subcontractor: function(frm, doc) {
        if (cur_frm.doc.labour_type === "Rate Work" && cur_frm.doc.subcontractor){
            get_labour_list();
        }
    },

    labour_type: function(frm, doc) {
        if (cur_frm.doc.labour_type === "Rate Work" && cur_frm.doc.subcontractor){
           get_labour_list();
        }
    }
});