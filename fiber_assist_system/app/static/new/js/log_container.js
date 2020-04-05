var vm = new Vue({
    el: "#log_container",
    data:{
        log_mysql_active: true
    },
    methods:{
        switch_log_tab: function(v){
            if(v==1){
                this.log_mysql_active = true;
            }else{
                this.log_mysql_active = false;
            }

        }
    }
});