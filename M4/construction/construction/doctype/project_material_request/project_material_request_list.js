frappe.listview_settings["Project Material Request"] = {
	refresh:function(doc){
        cur_list.page.fields_dict['project'].get_query =function(doc){
            return{
                filters:[['Project','status','=','Open']]
            }
        }
        cur_list.page.fields_dict['warehouse'].get_query = function(doc){
        	return{
        		filters:[['Warehouse','disabled','=','0']]
        	}
        }
    }
}