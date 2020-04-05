var vm = new Vue({
    el: "#team_manage_container",
    data:{
        content_active: true
    },
    methods:{
        switch_log_tab: function(v){
            if(v==1){
                this.content_active = true;
            }else{
                this.content_active = false;
            }

        }
    }
});