frappe.listview_settings["F and F Entry"] = {
    add_fields:["status"],
    get_indicator:function(doc){
        if (doc.status === "To Bill"){
            return[__("To Bill"),"orange",("status,=,To Bill")];
        }
        if (doc.status === "Completed"){
            return[__("Completed"),"green",("status,=,Completed")];
        }
    },
    refresh:function(doc){
        cur_list.page.fields_dict['project'].get_query =function(doc){
            return{
                filters:[['Project','status','=','Open']]
            }
        }
        cur_list.page.fields_dict['subcontractor'].get_query =function(doc){
            return{
                filters:[['Supplier','nx_is_sub_contractor','=',1]]
            }
        }
    }
};