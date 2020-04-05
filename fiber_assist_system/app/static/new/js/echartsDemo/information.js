/**
 * Created by Zain on 21/3/2018.
 */
// $(function(){
//    var info_container = document.querySelector('.inform_content');
//    var w = info_container.offsetWidth;
//    var ww = $(window).width();
//    var equipment_info = $('.equipment_info');
//    var close_info = $('.close_info');
//    var equipts = $('.equipt');
//    var oMask = $('.mask');
//    equipts.on('click',function(){
//       oMask.show();
//       equipment_info.show();
//    });
//    close_info.on('click',function(){
//       $(this).parent().parent().hide();
//       oMask.hide();
//    });
//    equipment_info.css('left',(ww-780)/2);
//    info_container.style.left = '863px';
//    info_container.style.visibility = 'visible';
//    console.log(w);
//    setInterval(function(){
//       if(parseInt(info_container.style.left) <= -w ){
//           info_container.style.left = '863px';
//       }
//       info_container.style.left = parseInt(info_container.style.left)-2+'px';
//    },1000/60);
// });