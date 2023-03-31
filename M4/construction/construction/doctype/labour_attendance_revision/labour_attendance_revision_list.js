frappe.listview_settings["Labour Attendance Revision"] = {
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

}
