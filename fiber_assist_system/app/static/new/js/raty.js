/**
 * Created by Zain on 23/1/2018.
 */
$(function(){
    var w = $(window).width();
    var close_score = $('.close_score');
    var BarGraph = $('.BarGraph');
    var ScoreContainer = $('.ScoreContainer');
    var whole_score = $('#whole_score');
    var user_score = $('#user_score');
    ScoreContainer.css('left',(w-500)/2);
    BarGraph.css('left',(w-900)/2);
    BarGraph[0].onmousedown = function(ev){
        var oevent = ev || event;

        var distanceX = oevent.clientX - BarGraph[0].offsetLeft;
        var distanceY = oevent.clientY - BarGraph[0].offsetTop;

        document.onmousemove = function(ev){
            var oevent = ev || event;
            BarGraph[0].style.left = oevent.clientX - distanceX + 'px';
            BarGraph[0].style.top = oevent.clientY - distanceY + 'px';
        };
        document.onmouseup = function(){
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
    //BarGraph[0].onmousedown = function(ev) {
    //    var oEvent = ev || event;
    //    //求出鼠标和box的位置差值
    //    var x = oEvent.clientX - box.offsetLeft;
    //    var y = oEvent.clientY - box.offsetTop;
    //    //鼠标移动的函数
    //    //把事件加在document上，解决因为鼠标移动太快时，
    //    //鼠标超过box后就没有了拖拽的效果的问题
    //    document.onmousemove = function(ev) {
    //        var oEvent = ev || event;
    //        //只能拖动窗口标题才能移动
    //        if(oEvent.target!=tit){
    //            return;
    //        }
    //        //保证拖拽框一直保持在浏览器窗口内部，不能被拖出的浏览器窗口的范围
    //        var l = oEvent.clientX - x;
    //        var t = oEvent.clientY - y;
    //        if(l < 0) {
    //            l = 0;
    //
    //        } else if(l > document.documentElement.clientWidth - box.offsetWidth) {
    //            l = document.documentElement.clientWidth - box.offsetWidth;
    //        }
    //        if(t < 0) {
    //            t = 0;
    //        } else if(t > document.documentElement.clientHeight - box.offsetHeight) {
    //            t = document.documentElement.clientHeight - box.offsetHeight;
    //        }
    //        box.style.left = l + "px";
    //        box.style.top = t + "px";
    //    };
    //    //鼠标抬起的函数
    //    document.onmouseup = function() {
    //        document.onmousemove = null;
    //        document.onmouseup = null;
    //    };
    //    //火狐浏览器在拖拽空div时会出现bug
    //    //return false阻止默认事件，解决火狐的bug
    //    return false;
    //};
    whole_score.raty({
        path: 'static/new/js/img',
        half:true,
        score:0,
        readOnly: true
    });
    user_score.raty({
        path: 'static/new/js/img',
        score:0,
        half:true
    });
    close_score.on('click',function(){
        ScoreContainer.hide();
    });
});