/**
 * Created by Zain on 12/12/2017.
 */
// 在当前网页装载完毕后执行init()方法
window.onload = init();

function init(){
    var pwd_confirm = document.querySelector('#user_confirm_pwd');
    var pwd_input = document.querySelector('#user_pwd');
    var confirm_tip = document.querySelector('.confirm_tip');
    var ghost_mask = document.querySelectorAll('.selector_box > .ghost_mask');
    var selections = document.querySelectorAll('.selector_box > .selections');
    var selectors = document.querySelectorAll('.selector_box > .selections > li');
    var to_login = document.querySelector(".to_login");

    // 身份创建管理
    for(var i = 0 ; i < selectors.length ; i++){
        selectors[i].onclick = function(e){
            var evt = e ? e : window.event;
            if (evt.stopPropagation) {
                evt.stopPropagation();
            }
            else {
                evt.cancelBubble = true;
            }
            this.parentNode.parentNode.querySelector('.user_input').value = this.innerHTML;
            this.parentNode.parentNode.querySelector('.user_input').setAttribute('value',this.innerHTML);
            if(this.innerHTML == '团队创建者'){
                var mask = this.parentNode.parentNode.nextElementSibling.querySelector('.ghost_mask');
                mask.style.display = 'none';
                this.parentNode.parentNode.nextElementSibling.querySelector('.user_input').value = '创建团队';
                this.parentNode.parentNode.nextElementSibling.querySelector('.user_input').setAttribute('value','创建团队')
            }else if(this.innerHTML == '普通成员'){
                var mask = this.parentNode.parentNode.nextElementSibling.querySelector('.ghost_mask');
                mask.style.display = 'block';
                this.parentNode.parentNode.nextElementSibling.querySelector('.user_input').value = '加入团队';
                this.parentNode.parentNode.nextElementSibling.querySelector('.user_input').setAttribute('value','加入团队')
            }
            this.parentNode.style.display = 'none';
        }
    }

    // 创建/加入团队管理
    for(var i = 0 ; i < ghost_mask.length ; i++){
        ghost_mask[i].onclick = function(e){
            var evt = e ? e : window.event;
            if (evt.stopPropagation) {
                evt.stopPropagation();
            }
            else {
                evt.cancelBubble = true;
            }
            if(!this.nextElementSibling.style.display || this.nextElementSibling.style.display == 'none'){
                if(this.parentNode.nextElementSibling.querySelector('.selections')){
                    this.parentNode.nextElementSibling.querySelector('.selections').style.display = 'none';
                }else{
                    this.parentNode.previousElementSibling.querySelector('.selections').style.display = 'none';
                }
                this.nextElementSibling.style.display = 'block';
            }else{
                this.nextElementSibling.style.display = 'none';
            }
        };
    }
    document.onclick = function(){
        for(var i = 0 ; i < selections.length ; i++){
            selections[i].style.display = 'none';
        }
    };

    // 在对象失去焦点时发生
    pwd_confirm.onblur = function(){
        if(pwd_confirm.value == pwd_input.value && pwd_confirm.value){
            confirm_tip.style.backgroundImage = "url('/static/new/imgs/login/tick.png')";
        }else{
            confirm_tip.style.backgroundImage = "url('/static/new/imgs/login/cross.png')";
        }
    };
    pwd_input.onblur = function(){
        if(pwd_confirm.value == pwd_input.value && pwd_confirm.value){
            confirm_tip.style.backgroundImage = "url('/static/new/imgs/login/tick.png')";
        }else{
            confirm_tip.style.backgroundImage = "url('/static/new/imgs/login/cross.png')";
        }
    };
    pwd_confirm.onfocus = function(){
        confirm_tip.style.display = 'block';
    };
    to_login.onclick = function() {
        
    }
}