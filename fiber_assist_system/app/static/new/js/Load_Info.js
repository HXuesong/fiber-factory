/**
 * Created by Zain on 27/12/2017.
 */

//  日志信息管理
$(function(){
   var mysql_tab = $('.mysql_tab');
   var hive_tab = $('.hive_tab');
   var mysql_content = $('.mysql_content');
   var hive_content  = $('.hive_content');
   var mysql_timer = null;
   var hive_timer = null;

    // 发送数据请求
   mysql_tab.on('click',function(){
      if(!mysql_timer){
          mysql_timer = setInterval(function(){
              var _data = {};
              $.post(mysql_path,_data,function(data){
                  if(data.status == 200){
                      mysql_content.html("");
                      for(var i = 0 ; i < data.data.length ; i++){
                          mysql_content.append(
                              data.data[i] + '<br>'
                          );
                      }
                  }else{
                      alert(data.status);
                  }
              })
          },5000)
      }
   });
   
     // 发送数据请求
    hive_tab.on('click',function(){
        if(!hive_timer){
            hive_timer = setInterval(function(){
                var _data = {};
                $.post(hive_path,_data,function(data){
                    if(data.status == 200){
                        hive_content.html("");
                        for(var i = 0 ; i < data.data.length ; i++){
                            hive_content.append(
                                data.data[i] + '<br>'
                            );
                        }
                    }else{
                        alert(data.status);
                    }
                })
            },5000)
        }
    });
});