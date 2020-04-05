(function(){
    var vm = new Vue({
        el: "#user_info_container",
        data:{
            set_head: false,
            //    所有的头像
            head_icons:[
                "1.jpg",
                "2.jpg",
                "3.jpg",
                "4.jpg",
                "5.jpg",
                "6.jpg",
                "7.jpg",
                "8.jpg",
                "9.jpg",
                "10.jpg",
                "11.jpg",
                "12.jpg"
            ],
            head_flags: [false, false, false, false, false, false, false, false, false, false, false, false],
            current_head_index: -1
        },
        methods:{
            init: function(){
                for(var i=0; i < 12; i++){
                    if(this.head_icons[i] == current_src){
                        this.$set(this.head_flags, i, true);
                        this.current_head_index = i;
                    }
                }
            },
            open_set_head: function(){
                this.set_head = true;
            },
            close_set_head: function () {
                this.set_head = false;
            },
            switch_head: function (index) {
                if(this.current_head_index != index){
                    if(this.current_head_index != -1){
                        this.$set(this.head_flags, this.current_head_index, false);
                    }
                    this.$set(this.head_flags, index, true);
                    this.current_head_index = index;
                }
            },
            submit_head: function () {
                if(this.current_head_index==-1) return;
                //接口
                this.$http.post('/head', {src: this.head_icons[this.current_head_index]}).then(function(res){
                    if(res.ok != 200){
                        alert("数据出错， 请稍后重试");
                        return;
                    }

                    var data = res.json();

                    if(data.status == 'ok'){
                        alert("修改成功！！");
                        window.location.reload();
                    }

                }).catch(function(){
                    alert("数据出错， 请稍后重试");
                });
            }
        }
    });

    vm.init();
})();

