(function(){
    var vm = new Vue({
        el: "#nav-container",
        data:{
            set_active_1: is_show_1,
            set_active_2: is_show_2
        },
        methods:{
            switch_set_tab_1: function(){
                this.set_active_1 = !this.set_active_1;
            },
            switch_set_tab_2: function () {
                this.set_active_2 = !this.set_active_2;
            }
        }
    });
})();
