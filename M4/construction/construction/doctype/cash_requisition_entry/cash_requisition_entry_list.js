frappe.listview_settings["Cash Requisition Entry"] = {
	refresh: function(frm) {
   cur_list.page.fields_dict['project'].get_query =function(doc){
            return{
                filters:[['Project','status','=','Open']]
            }
        }
    } 
}