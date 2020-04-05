// $(document).ready(function(){
//   var stageselectLabel=$('#stageselectPart label'),
//       stagesmenu=$('#stagesmenu'),
//       featuresmenu=$('#featuresmenu'),
//       multiplemenu=$('#multiplemenu'),
//       iconRight=$('.iconRight'),
//       submitattr=$('#submitattr');
//   var featureContainer = $('#featuresDetail');
//   var tip_info = $('.tip_info');
//   var data_={
//         'VAD塔线':{
//           '1':'E',
//           '2':'G',
//           '3':'H',
//           '4':'D',
//           '5':'F',
//           '6':'C'
//         },
//         'VAD烧结塔线':{
//           '1':'E',
//           '2':'G',
//           '3':'H',
//           '4':'D',
//           '5':'F',
//           '6':'C'
//         },
//         '拉伸塔线': {
//           '1':'B'
//         },
//         'OVD塔线': {
//           '1':'C',
//           '2':'D',
//           '3':'E'
//         }
//   };
//    // 二级联动选择
//   $('#stageselect').on('DOMNodeInserted',function(){
//     if(this.innerText==0){
//       $('#multipleDetail').empty();
//     }else{
//       for(key in data_){
//         if(key == this.innerText){
//           $('#multipleDetail').empty();
//           $('#multiple').empty();
//           var temps = '';
//           for(var index in data_[this.innerText]){
//             // 渲染数据
//             temps+='<label>'+data_[this.innerText][index]+'</label>'
//           }
//           ($(temps)).appendTo($('#multipleDetail'));
//           //点击选中，多选
//           var multipleLabel=$('#multiplePart label')
//           var multiplevalue="";
//           multipleLabel.click(function(){
//             $('#features').empty();
//             if($(this).attr('class')=='active'){
//               $(this).removeClass('active');
//                 multiplevalue = multiplevalue.replace($(this).html()+',',"");
//                 $('#multiple').html(multiplevalue);
//                 $('#multiple').siblings('.form').attr('value',multiplevalue);
//             }else{
//               $(this).addClass('active');
//               multiplevalue=multiplevalue+$(this).html()+',';
//               $('#multiple').html(multiplevalue);
//               $('#multiple').siblings('.form').attr('value',multiplevalue);
//             }
//           });
//         }
//       }
//     }
//   });
//   // 点击显示和隐藏
//   stagesmenu.click(function(){
//     	if($(this).siblings('#stageselectDetail').is(':hidden')){
//     		$('#stagesmenu .iconRight').addClass('active');
//         // 先隐藏其他的下拉菜单
//         $(this).parent().parent().find('.detail').hide();
//     		$(this).siblings('#stageselectDetail').show();
//     	}else{
//     		$('#stagesmenu .iconRight').removeClass('active');
//     		$(this).siblings('#stageselectDetail').hide();
//     	}
//   });
//   //阻止冒泡
//   $('#stageselectPart').on('click',function(e){
//      e.stopPropagation();
//   });
//   $('#multiplePart').on('click',function(e){
//     e.stopPropagation();
//   });
//   $('#featuresPart').on('click',function(e){
//     e.stopPropagation();
//   });
//   // 点击选中，单选
//   stageselectLabel.click(function(){
//    	   $(this).addClass('active');
//    	   $(this).siblings('label').removeClass('active');
//    	   var value=$(this).html();
//    	   $('#stageselect').html(value);
//        $('#stageselect').siblings('.form').attr('value',value);
//    });
//   // 点击显示和隐藏
//   multiplemenu.click(function(){
//     	if($(this).siblings('#multipleDetail').is(':hidden')){
//     		$('#multiplemenu .iconRight').addClass('active');
//          // 先隐藏其他的下拉菜单
//         $(this).parent().parent().find('.detail').hide();
//     		$(this).siblings('#multipleDetail').show();
//     	}else{
//     		$('#multiplemenu .iconRight').removeClass('active');
//     		$(this).siblings('#multipleDetail').hide();
//     	}
//     });
//   // 点击显示和隐藏
//   featuresmenu.click(function(){
//       if($(this).siblings('#featuresDetail').is(':hidden')){
//             var _data = {};
//             var temps="";
//             _data.label = PredictingTarget;
//             _data.step_name = $('#stageselect').html();
//             _data.equip_list = $('#multiple').html().split(',');
//             _data.equip_list.pop();
//             console.log(_data.equip_list);
//               for(index in _data){
//                   if(_data[index]==null || _data[index].length ==0){
//                       alert('请选择正确的阶段和设备再选择特征');
//                       return false;
//                   }
//               }
//             if(oldStep){
//                 console.log(oldStep);
//                 if(_data.step_name == oldStep[0] && _data.equip_list.toString() == oldStep[1].toString()){
//                     $('#featuresmenu .iconRight').addClass('active');
//                     $(this).parent().parent().find('.detail').hide();
//                     $(this).siblings('#featuresDetail').show();
//                 }else{
//                     var features = ['特征1','特征2','特征3','特征4'];
//                     //////////////////////////////////////////////////////////////////////////////////////
//                     $.post(featuresLink,_data,function(data){
//                       if(data.status == 200){
//                           featureContainer.html("");
//                           $('#features').html("");
//                           var labels = "";
//                           for(var i = 0 ; i < data.features.length ; i++){
//                               labels += '<label>' + data.features[i] + '</label>';
//                           }
//                           featureContainer.append(labels);
//                           oldStep = [];
//                           oldStep.push(_data.step_name);
//                           oldStep.push(_data.equip_list);
//                           var featuresLabel=$('#featuresPart label');
//                           var featuresvalue="";
//                           featuresLabel.click(function(){
//                               if($(this).attr('class')=='active'){
//                                   $(this).removeClass('active');
//                                   featuresvalue = featuresvalue.replace($(this).html()+',',"");
//                                   $('#features').html(featuresvalue);
//                                   $('#features').siblings('.form').attr('value',featuresvalue);
//                               }else{
//                                   $(this).addClass('active');
//                                   featuresvalue=featuresvalue+$(this).html()+',';
//                                   $('#features').html(featuresvalue);
//                                   $('#features').siblings('.form').attr('value',featuresvalue);
//                               }
//                           });
//                           $('#featuresmenu .iconRight').addClass('active');
//                           $(this).parent().parent().find('.detail').hide();
//                           $(this).siblings('#featuresDetail').show();
//                       }else{
//                           alert(data.status);
//                       }
//                     });
//                     ///////////////////////////////////////////////////////////////////////////////////////////////////
//                     //我虚拟的数据测试用
//                     // featureContainer.html("");
//                     // $('#features').html("");
//                     // var labels = "";
//                     // for(var i = 0 ; i < features.length ; i++){
//                     //     labels += '<label>' + features[i] + '</label>';
//                     // }
//                     // featureContainer.append(labels);
//                     // oldStep = [];
//                     // oldStep.push(_data.step_name);
//                     // oldStep.push(_data.equip_list);
//                     // var featuresLabel=$('#featuresPart label');
//                     // var featuresvalue="";
//                     // featuresLabel.click(function(){
//                     //     if($(this).attr('class')=='active'){
//                     //         $(this).removeClass('active');
//                     //         featuresvalue = featuresvalue.replace($(this).html()+',',"");
//                     //         $('#features').html(featuresvalue);
//                     //         console.log($('#features').siblings('.form'));
//                     //         $('#features').siblings('.form').attr('value',featuresvalue);
//                     //     }else{
//                     //         $(this).addClass('active');
//                     //         featuresvalue=featuresvalue+$(this).html()+',';
//                     //         $('#features').html(featuresvalue);
//                     //         $('#features').siblings('.form').attr('value',featuresvalue);
//                     //     }
//                     // });
//                     // featuresLabel.on('mouseover',function(event){
//                     //     tip_info.html($(this).html());
//                     //     tip_info.show();
//                     //     $(this).on('mousemove',function(event){
//                     //         tip_info.css({'left':event.pageX,'top':event.pageY-15})
//                     //     });
//                     // });
//                     // featuresLabel.on('mouseout',function(){
//                     //    $(this).off('mousemove');
//                     //    tip_info.hide();
//                     // });
//                     // $('#featuresmenu .iconRight').addClass('active');
//                     // $(this).parent().parent().find('.detail').hide();
//                     // $(this).siblings('#featuresDetail').show();
//                     //对上接口把这些删了或者注释了就行了.
//                     //////////////////////////////////////////////////////
//                 }
//             }else{
//                 oldStep = [];
//                 oldStep.push(_data.step_name);
//                 oldStep.push(_data.equip_list);
//                 var features = ['特征1','特征233333333333333','特征3','特征4'];
//                 ///////////////////////////////////////////////////////////////////////////////////////////////////
//                 $.post(featuresLink,_data,function(data){
//                    if(data.status == 200){
//                        featureContainer.html("");
//                        $('#features').html("");
//                        var labels = "";
//                        for(var i = 0 ; i < data.features.length ; i++){
//                            labels += '<label>' + data.features[i] + '</label>';
//                        }
//                        featureContainer.append(labels);
//                        oldStep = [];
//                        oldStep.push(_data.step_name);
//                        oldStep.push(_data.equip_list);
//                        var featuresLabel=$('#featuresPart label');
//                        var featuresvalue="";
//                        featuresLabel.click(function(){
//                            if($(this).attr('class')=='active'){
//                                $(this).removeClass('active');
//                                featuresvalue = featuresvalue.replace($(this).html()+',',"");
//                                $('#features').html(featuresvalue);
//                                $('#features').siblings('.form').attr('value',featuresvalue);
//                            }else{
//                                $(this).addClass('active');
//                                featuresvalue=featuresvalue+$(this).html()+',';
//                                $('#features').html(featuresvalue);
//                                $('#features').siblings('.form').attr('value',featuresvalue);
//                            }
//                        });
//                        $('#featuresmenu .iconRight').addClass('active');
//                        $(this).parent().parent().find('.detail').hide();
//                        $(this).siblings('#featuresDetail').show();
//                    }else{
//                        alert(data.status);
//                    }
//                 });
//                 ///////////////////////////////////////////////////////////////////////////////////////////////////
//                 //和上面同理
//                 // ///////////////////////////////////////////////////////////////////////////////////////////////////
//                 // featureContainer.html("");
//                 // var labels = "";
//                 // for(var i = 0 ; i < features.length ; i++){
//                 //     labels += '<label>' + features[i] + '</label>';
//                 // }
//                 // featureContainer.append(labels);
//                 // var featuresLabel=$('#featuresPart label');
//                 // var featuresvalue="";
//                 // featuresLabel.click(function(){
//                 //     if($(this).attr('class')=='active'){
//                 //         $(this).removeClass('active');
//                 //         featuresvalue = featuresvalue.replace($(this).html()+',',"");
//                 //         $('#features').html(featuresvalue);
//                 //         $('#features').siblings('.form').attr('value',featuresvalue);
//                 //     }else{
//                 //         $(this).addClass('active');
//                 //         featuresvalue=featuresvalue+$(this).html()+',';
//                 //         $('#features').html(featuresvalue);
//                 //         $('#features').siblings('.form').attr('value',featuresvalue);
//                 //     }
//                 // });
//                 // featuresLabel.on('mouseover',function(event){
//                 //     tip_info.html($(this).html());
//                 //     tip_info.show();
//                 //     $(this).on('mousemove',function(event){
//                 //         tip_info.css({'left':event.pageX,'top':event.pageY-15})
//                 //     });
//                 // });
//                 // featuresLabel.on('mouseout',function(){
//                 //     $(this).off('mousemove');
//                 //     tip_info.hide();
//                 // });
//                 // $('#featuresmenu .iconRight').addClass('active');
//                 // $(this).parent().parent().find('.detail').hide();
//                 // $(this).siblings('#featuresDetail').show();
//                 ///////////////////////////////////////////////////////////////////////////////////////////////////
//             }
//       }else{
//         $('#featuresmenu .iconRight').removeClass('active');
//         $(this).siblings('#featuresDetail').hide();
//       }
//     });
//   $(document).bind('click',function(e){
//     var target=$(e.target);
//     if(!target.is('.detail')){
//       if($('.detail').is(':visible')){
//           $('.detail').hide();
//       }
//       //e.stopPropagation();
//     }
//   });
//   // 点击提交按钮
//   submitattr.click(function(){
//       var stage = $('#stageselect').html();
//       var multi = $('#multiple').html().split(",");
//       var featureselected = $('#features').html().split(",");
//       multi = multi.splice(0,multi.length-1);
//       featureselected = featureselected.splice(0,featureselected.length-1);
//       console.log(stage);
//       console.log(multi);
//       console.log(featureselected);
//   });
// });


$(document).ready(function(){
  var stageselectLabel=$('#stageselectPart label'),
      stagesmenu=$('#stagesmenu'),
      featuresmenu=$('#featuresmenu'),
      multiplemenu=$('#multiplemenu'),
      iconRight=$('.iconRight'),
      submitattr=$('#submitattr');
  var featureContainer = $('#featuresDetail');
  var tip_info = $('.tip_info');
  var tablediv = $('#tablediv');
  var data_={
        'VAD塔线':{
          '1':'E',
          '2':'G',
          '3':'H',
          '4':'D',
          '5':'F',
          '6':'C'
        },
        'VAD烧结塔线':{
          '1':'E',
          '2':'G',
          '3':'H',
          '4':'D',
          '5':'F',
          '6':'C'
        },
        '拉伸塔线': {
          '1':'B'
        },
        'OVD塔线': {
          '1':'C',
          '2':'D',
          '3':'E'
        }
  };
   // 二级联动选择
    featureContainer.scrollBar({
        position: "y",
        barWidth: 8
    });
    tablediv.scrollBar({
        position: "y",
        barWidth: 8
    });
  if(oldStep != null){
      var multipleLabel = $('#multiplePart label');
      var multiplevalue = $('#multiple').html();
      multipleLabel.click(function(){
          $('#features').empty();
          if($(this).attr('class')=='active'){
              $(this).removeClass('active');
              multiplevalue = multiplevalue.replace($(this).html()+',',"");
              $('#multiple').html(multiplevalue);
              $('#multiple').siblings('.form').attr('value',multiplevalue);
          }else{
              $(this).addClass('active');
              multiplevalue=multiplevalue+$(this).html()+',';
              $('#multiple').html(multiplevalue);
              $('#multiple').siblings('.form').attr('value',multiplevalue);
          }
      });
      var featuresLabel = $('#featuresPart label');
      var featuresvalue = $('#features').html();
      featuresLabel.click(function(){
          if($(this).attr('class') == 'active'){
              $(this).removeClass('active');
              featuresvalue = featuresvalue.replace($(this).html()+',',"");
              $('#features').html(featuresvalue);
              $('#features').siblings('.form').attr('value',featuresvalue);
          }else{
              $(this).addClass('active');
              featuresvalue=featuresvalue+$(this).html()+',';
              $('#features').html(featuresvalue);
              $('#features').siblings('.form').attr('value',featuresvalue);
          }
      });
      featuresLabel.on('mouseover',function(event){
          tip_info.html($(this).html());
          tip_info.show();
          $(this).on('mousemove',function(event){
              tip_info.css({'left':event.pageX,'top':event.pageY-15})
          });
      });
      featuresLabel.on('mouseout',function(){
          $(this).off('mousemove');
          tip_info.hide();
      });
  }
  $('#stageselect').on('DOMNodeInserted',function(){
    if(this.innerText==0){
      $('#multipleDetail').empty();
    }else{
      for(key in data_){
        if(key == this.innerText){
          $('#multipleDetail').empty();
          $('#multiple').empty();
          var temps = '';
          for(var index in data_[this.innerText]){
            // 渲染数据
            temps+='<label>'+data_[this.innerText][index]+'</label>'
          }
          ($(temps)).appendTo($('#multipleDetail'));
          //点击选中，多选
          var multipleLabel=$('#multiplePart label');
          var multiplevalue="";
          multipleLabel.click(function(){
            $('#features').empty();
            if($(this).attr('class')=='active'){
              $(this).removeClass('active');
                multiplevalue = multiplevalue.replace($(this).html()+',',"");
                $('#multiple').html(multiplevalue);
                $('#multiple').siblings('.form').attr('value',multiplevalue);
            }else{
              $(this).addClass('active');
              multiplevalue=multiplevalue+$(this).html()+',';
              $('#multiple').html(multiplevalue);
              $('#multiple').siblings('.form').attr('value',multiplevalue);
            }
          });
        }
      }
    }
  });
  // 点击显示和隐藏
  stagesmenu.click(function(){
    	if($(this).siblings('#stageselectDetail').is(':hidden')){
    		$('#stagesmenu .iconRight').addClass('active');
        // 先隐藏其他的下拉菜单
        $(this).parent().parent().find('.detail').hide();
    		$(this).siblings('#stageselectDetail').show();
    	}else{
    		$('#stagesmenu .iconRight').removeClass('active');
    		$(this).siblings('#stageselectDetail').hide();
    	}
  });
  //阻止冒泡
  $('#stageselectPart').on('click',function(e){
     e.stopPropagation();
  });
  $('#multiplePart').on('click',function(e){
    e.stopPropagation();
  });
  $('#featuresPart').on('click',function(e){
    e.stopPropagation();
  });
  // 点击选中，单选
  stageselectLabel.click(function(){
   	   $(this).addClass('active');
   	   $(this).siblings('label').removeClass('active');
   	   var value=$(this).html();
   	   $('#stageselect').html(value);
       $('#stageselect').siblings('.form').attr('value',value);
   });
  // 点击显示和隐藏
  multiplemenu.click(function(){
    	if($(this).siblings('#multipleDetail').is(':hidden')){
    		$('#multiplemenu .iconRight').addClass('active');
         // 先隐藏其他的下拉菜单
        $(this).parent().parent().find('.detail').hide();
    		$(this).siblings('#multipleDetail').show();
    	}else{
    		$('#multiplemenu .iconRight').removeClass('active');
    		$(this).siblings('#multipleDetail').hide();
    	}
    });
  // 点击显示和隐藏
  featuresmenu.click(function(){
      if($(this).siblings('#featuresDetail').is(':hidden')){
            var _data = {};
            _data.label = PredictingTarget;
            _data.step_name = $('#stageselect').html();
            _data.equip_list = $('#multiple').html().split(',');
            _data.equip_list.pop();
              for(index in _data){
                  if(_data[index]==null || _data[index].length ==0){
                      alert('请选择正确的阶段和设备再选择特征');
                      return false;
                  }
              }
            if(oldStep){
                if(_data.step_name == oldStep[0] && _data.equip_list.toString() == oldStep[1].toString()){
                    $('#featuresmenu .iconRight').addClass('active');
                    $(this).parent().parent().find('.detail').hide();
                    $(this).siblings('#featuresDetail').show();
                }else{
                    var features = ['特征1','特征2','特征3','特征4'];
                    ////////////////////////////////////////////////////////////////////////////////////////
                    $.post(featuresLink,_data,function(data){
                      if(data.status == 200){
                          featureContainer.html("");
                          $('#features').html("");
                          var labels = "";
                          for(var i = 0 ; i < data.features.length ; i++){
                              labels += '<label>' + data.features[i] + '</label>';
                          }
                          featureContainer.append(labels);
                          oldStep = [];
                          oldStep.push(_data.step_name);
                          oldStep.push(_data.equip_list);
                          var featuresLabel=$('#featuresPart label');
                          var featuresvalue="";
                          featuresLabel.click(function(e){
                            e.stopPropagation();
                              if($(this).attr('class')=='active'){
                                  $(this).removeClass('active');
                                  featuresvalue = featuresvalue.replace($(this).html()+',',"");
                                  $('#features').html(featuresvalue);
                                  $('#features').siblings('.form').attr('value',featuresvalue);
                              }else{
                                  $(this).addClass('active');
                                  featuresvalue=featuresvalue+$(this).html()+',';
                                  $('#features').html(featuresvalue);
                                  $('#features').siblings('.form').attr('value',featuresvalue);
                              }
                          });
                           featuresLabel.on('mouseover',function(event){
                               tip_info.html($(this).html());
                               tip_info.show();
                               $(this).on('mousemove',function(event){
                                   tip_info.css({'left':event.pageX,'top':event.pageY-15})
                               });
                           });
                           featuresLabel.on('mouseout',function(){
                               $(this).off('mousemove');
                               tip_info.hide();
                           });
                          $('#featuresmenu .iconRight').addClass('active');
                          $(this).parent().parent().find('.detail').hide();
                          $(this).siblings('#featuresDetail').show();
                      }else{
                          alert(data.status);
                      }
                    });
                    ///////////////////////////////////////////////////////////////////////////////////////////////////
                    //我虚拟的数据测试用
                    // featureContainer.html("");
                    // $('#features').html("");
                    // var labels = "";
                    // for(var i = 0 ; i < features.length ; i++){
                    //     labels += '<label>' + features[i] + '</label>';
                    // }
                    // featureContainer.append(labels);
                    // oldStep = [];
                    // oldStep.push(_data.step_name);
                    // oldStep.push(_data.equip_list);
                    // var featuresLabel=$('#featuresPart label');
                    // var featuresvalue="";
                    // featuresLabel.click(function(){
                    //     if($(this).attr('class')=='active'){
                    //         $(this).removeClass('active');
                    //         featuresvalue = featuresvalue.replace($(this).html()+',',"");
                    //         $('#features').html(featuresvalue);
                    //         $('#features').siblings('.form').attr('value',featuresvalue);
                    //     }else{
                    //         $(this).addClass('active');
                    //         featuresvalue=featuresvalue+$(this).html()+',';
                    //         $('#features').html(featuresvalue);
                    //         $('#features').siblings('.form').attr('value',featuresvalue);
                    //     }
                    // });
                    // featuresLabel.on('mouseover',function(event){
                    //     tip_info.html($(this).html());
                    //     tip_info.show();
                    //     $(this).on('mousemove',function(event){
                    //         tip_info.css({'left':event.pageX,'top':event.pageY-15})
                    //     });
                    // });
                    // featuresLabel.on('mouseout',function(){
                    //    $(this).off('mousemove');
                    //    tip_info.hide();
                    // });
                    // $('#featuresmenu .iconRight').addClass('active');
                    // $(this).parent().parent().find('.detail').hide();
                    // $(this).siblings('#featuresDetail').show();
                    //对上接口把这些删了或者注释了就行了.
                    //////////////////////////////////////////////////////
                }
            }else{
                oldStep = [];
                oldStep.push(_data.step_name);
                oldStep.push(_data.equip_list);
                var features = ['特征1','特征233333333333333','特征3','特征4'];
                ///////////////////////////////////////////////////////////////////////////////////////////////////
                $.post(featuresLink,_data,function(data){
                   if(data.status == 200){
                       featureContainer.html("");
                       $('#features').html("");
                       var labels = "";
                       for(var i = 0 ; i < data.features.length ; i++){
                           labels += '<label>' + data.features[i] + '</label>';
                       }
                       featureContainer.append(labels);
                       oldStep = [];
                       oldStep.push(_data.step_name);
                       oldStep.push(_data.equip_list);
                       var featuresLabel=$('#featuresPart label');
                       var featuresvalue="";
                       featuresLabel.click(function(e){
                        e.stopPropagation();
                           if($(this).attr('class')=='active'){
                               $(this).removeClass('active');
                               featuresvalue = featuresvalue.replace($(this).html()+',',"");
                               $('#features').html(featuresvalue);
                               $('#features').siblings('.form').attr('value',featuresvalue);
                           }else{
                               $(this).addClass('active');
                               featuresvalue=featuresvalue+$(this).html()+',';
                               $('#features').html(featuresvalue);
                               $('#features').siblings('.form').attr('value',featuresvalue);
                           }
                       });
                       featuresLabel.on('mouseover',function(event){
                           tip_info.html($(this).html());
                           tip_info.show();
                           $(this).on('mousemove',function(event){
                               tip_info.css({'left':event.pageX,'top':event.pageY-15})
                           });
                       });
                       featuresLabel.on('mouseout',function(){
                           $(this).off('mousemove');
                           tip_info.hide();
                       });
                       $('#featuresmenu .iconRight').addClass('active');
                       $(this).parent().parent().find('.detail').hide();
                       $(this).siblings('#featuresDetail').show();
                   }else{
                       alert(data.status);
                   }
                });
                ///////////////////////////////////////////////////////////////////////////////////////////////////
                //和上面同理
                ///////////////////////////////////////////////////////////////////////////////////////////////////
                // featureContainer.html("");
                // var labels = "";
                // for(var i = 0 ; i < features.length ; i++){
                //     labels += '<label>' + features[i] + '</label>';
                // }
                // featureContainer.append(labels);
                // var featuresLabel=$('#featuresPart label');
                // var featuresvalue="";
                // featuresLabel.click(function(){
                //     if($(this).attr('class')=='active'){
                //         $(this).removeClass('active');
                //         featuresvalue = featuresvalue.replace($(this).html()+',',"");
                //         $('#features').html(featuresvalue);
                //     }else{
                //         $(this).addClass('active');
                //         featuresvalue = featuresvalue+$(this).html()+',';
                //         $('#features').html(featuresvalue);
                //     }
                // });
                // featuresLabel.on('mouseover',function(event){
                //     tip_info.html($(this).html());
                //     tip_info.show();
                //     $(this).on('mousemove',function(event){
                //         tip_info.css({'left':event.pageX,'top':event.pageY-15})
                //     });
                // });
                // featuresLabel.on('mouseout',function(){
                //     $(this).off('mousemove');
                //     tip_info.hide();
                // });
                // $('#featuresmenu .iconRight').addClass('active');
                // $(this).parent().parent().find('.detail').hide();
                // $(this).siblings('#featuresDetail').show();
                ///////////////////////////////////////////////////////////////////////////////////////////////////
            }
      }
      else{
        $('#featuresmenu .iconRight').removeClass('active');
        $(this).siblings('#featuresDetail').hide();
      }
    });
  // $(document).bind('click',function(e){
  //   var target=$(e.target);
  //   if(!target.is('.detail')){
  //     if($('.detail').is(':visible')){
  //         $('.detail').hide();
  //     }
  //     e.stopPropagation();
  //   }
  // });

  // 点击提交按钮
  submitattr.click(function(){
      var stage = $('#stageselect').html();
      var multi = $('#multiple').html().split(",");
      var featureselected = $('#features').html().split(",");
      multi = multi.splice(0,multi.length-1);
      featureselected = featureselected.splice(0,featureselected.length-1);
      console.log(stage);
      console.log(multi);
      console.log(featureselected);
  });
});
