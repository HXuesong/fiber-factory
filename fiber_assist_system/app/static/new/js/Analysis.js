// // var optionArray=[];//存放影响因子分析页面中渲染的选项，郭英杰写的
// // $(function(){
// //     var tablediv = $('#tablediv');
// //     var treediv = $('#treediv');
// //     var impactfactordiv = $('#impactfactordiv');
// //     var multiple = $('#multiple');
// //     var table  = $("#table");
// //     var tree = $('#tree');
// //     var containers = [];
// //     var impactfactor = $('#impactfactor');
// //     var parameterclass = $('.parameter');
// //     var buttonclass =  $('.button');
// //     var slideclass = $('.slide');
// //     var submitattr = $("#submitattr");
// //     var tagBtn = $('.tagbar');
// //     var contents = $('.analysis_content');
// //     var tag_input = $('.tag_input');
// //     containers.push(tablediv,treediv,impactfactordiv);
// //     tablediv.hide();
// //     treediv.hide();
// //     impactfactordiv.hide();
// //     buttonclass.hide();
// //     slideclass.hide();
// //     tagBtn.on('click',function(){
// //        tagBtn.removeClass('active');
// //        $(this).addClass('active');
// //        contents.hide();
// //        containers[parseInt($(this).attr('d_index'))].show();
// //        tag_input.attr('value',$(this).html());
// //        if(parseInt($(this).attr('d_index'))==1){
// //            createTreeV("树");
// //        }
// //     });
// //         switch(tag_selected){
// //             case 1:
// //                 tagBtn.eq(0).click();
// //                 break;
// //             case 2:
// //                 tagBtn.eq(1).click();
// //                 break;
// //             case 3:
// //                 tagBtn.eq(2).click();
// //                 break;
// //             default:
// //                 alert(渲染格式错误);
// //     }
// //
// //     var numClick1 = 0;
// //     var numClick2 = 0;
// //     var numClick3 = 0;
// //     parameterclass.click(function() {
// //         var parameter_tag = $(this).attr('tag');
// //         var slide_tag = $('.slide[tag=' + parameter_tag + ']');
// //         slide_tag.slideToggle();
// //
// //
// //         if(parameter_tag == "p_1") {
// //             var img_right = $(this).children('img.right');
// //             var img_button = $(this).children('img.button');
// //
// //             if(numClick1 == 0) {
// //                 img_right.hide();
// //                 img_button.show();
// //                 numClick1 ++;
// //             }
// //             else {
// //                 img_right.show();
// //                 img_button.hide();
// //                 numClick1 --;
// //             }
// //         }
// //
// //         if(parameter_tag == "p_2") {
// //             var img_right = $(this).children('img.right');
// //             var img_button = $(this).children('img.button');
// //
// //             if(numClick2 == 0) {
// //                 img_right.hide();
// //                 img_button.show();
// //                 numClick2 ++;
// //             }
// //             else {
// //                 img_right.show();
// //                 img_button.hide();
// //                 numClick2 --;
// //             }
// //
// //         }
// //
// //         if(parameter_tag == "p_3") {
// //             var img_right = $(this).children('img.right');
// //             var img_button = $(this).children('img.button');
// //
// //             if(numClick3 == 0) {
// //                 img_right.hide();
// //                 img_button.show();
// //                 numClick3 ++;
// //             }
// //             else {
// //                 img_right.show();
// //                 img_button.hide();
// //                 numClick3 --;
// //             }
// //         }
// //     });
// //     var target = document.querySelectorAll('.range-slider');
// //     var limitscontent = $('#impactfactordiv .limit');
// //     var namecontent=$('.parameter #temperaturefont');
// //     var limits = [];
// //     var ranges = [];
// //     var names  = [];
// //
// //     for(var i = 0 ; i < namecontent.length ; i++){
// //         var arr = namecontent.eq(i).html().trim() ;
// //         names.push(arr);
// //     }
// //
// //     for(var i = 0 ; i < limitscontent.length ; i++){
// //         var arr = limitscontent.eq(i).html().split(',');
// //         var x = arr.map(function(index){
// //             return parseFloat(index).toFixed(2);
// //         });
// //         limits.push(x);
// //     }
// //     for(var i = 0 ; i < target.length ; i++){
// //         var ll = parseFloat(limits[i][0]);
// //         var ul = parseFloat(limits[i][1]);
// //         var x = rangeSlider.init(target[i],ll,ul,function(obj,lock){
// //             var btns = $('.range-btn');
// //             if(lock){
// //                 btns.removeClass('selected');
// //                 obj.className = 'range-btn selected';
// //             }else{
// //                 obj.className = 'range-btn'
// //             }
// //         });
// //         ranges.push(x);
// //         x = null;
// //     }
// //
// //     //提交按钮
// //     $('.submit-btn').on('click', function () {
// //         // 通过 get 方法获取滑动输入条的范围，如果 range 已被锁定，get 方法返回空数组
// //         var values = [];
// //         for(var i = 0 ; i < target.length ; i++){
// //             values.push(ranges[i].get());
// //         }
// //         var json={};
// //         var staticJson={};
// //         json["stage_name"]=$('#stageselect').html();
// //         json["equip_lists"]=$('#multiple').text();
// //         // json.equip_lists = json.equip_lists.splice(0,json.equip_lists.length-1);
// //         json["feature_name"]=$('#features').html().split(',');
// //         json.feature_name = json.feature_name.splice(0,json.feature_name.length-1);
// //         json['target_label'] = PredictingTarget
// //         for(var i=0;i<values.length;i++){
// //             if(values[i]!=""){
// //                 staticJson[names[i]]=values[i];
// //             }
// //             else {json["target_feature"]=names[i];}
// //
// //         }
// //
// //         json["static_feature"]=JSON.
//
//
// (staticJson);
// //         console.log(json);
// //         $.post(drawurl,json,function(data){
// //             if(data.status == 200){
// //                 var myChart = echarts.init(document.getElementById('staticdiv'));
// //                 var option = {
// //                     title: {
// //
// //                     },
// //                     tooltip: {
// //                         trigger: 'axis'
// //                     },
// //                       legend: {
// //                         data:[],
// //                         itemGap:25
// //                     },
// //
// //                     grid: {
// //                         left: '3%',
// //                         right: '4%',
// //                         bottom: '3%',
// //                         containLabel: true
// //                     },
// //                     toolbox: {
// //                         feature: {
// //                             saveAsImage: {}
// //                         }
// //                     },
// //                     xAxis: {
// //                         type: 'category',
// //                         boundaryGap: false,
// //                         // data: ['周一','周二','周三','周四','周五','周六','周日'],
// //                         data: [],
// //                         // 控制网格线是否显示
// //                         splitLine: {
// //                             show: false,
// //                         },
// //                         //  改变x轴字体颜色和大小
// //                         axisLabel: {
// //                             textStyle: {
// //                                 color:'#60d4ff'
// //                             },
// //                         },
// //                     },
// //                     yAxis: [
// //                         {
// //                             type: 'value',
// //                             position:"left",
// //                             splitLine: {
// //                                 show: false,
// //                             },
// //                             //  改变y轴字体颜色和大小
// //                             axisLabel: {
// //                                 textStyle: {
// //                                     color: '#60d4ff'
// //                                 },
// //                             }
// //                         },
// //                         {
// //                             name:'不合格率',
// //                             type: 'value',
// //                             position: 'right',
// //                             splitLine: {
// //                                 show: false,
// //                             },
// //                             //  改变y轴字体颜色和大小
// //                             axisLabel: {
// //                                 textStyle: {
// //                                     color: '#60d4ff'
// //                                 },
// //                             },
// //                         },
// //                     ],
// //                     dataZoom: [
// //                         {
// //                             show: true,
// //                             start: 65,
// //                             end: 85
// //                         },
// //                         {
// //                             type: 'inside',
// //                             start: 65,
// //                             end: 85
// //                         }
// //                     ],
// //                     series: [
// //                         {
// //                             // name:'邮件营销',
// //                             type:'line',
// //                             smooth:true,
// //                             stack: '总量',
// //                             // data:[120, 132, 101, 134, 90, 230, 210],
// //                             data:[],
// //                             itemStyle : {
// //                                 normal : {
// //                                     lineStyle:{
// //                                         color:'#60d4ff',
// //                                         type:'dashed'
// //                                     },
// //                                     color:'#60d4ff'
// //                                 }
// //                             },
// //                         },
// //                         {
// //                             // name:'邮件营销2',
// //                             type:'line',
// //                             smooth:true,
// //                             stack: '总量',
// //                             // data:[120, 132, 101, 134, 90, 230, 210],
// //                             yAxisIndex: 1,
// //                             data:[],
// //                             itemStyle : {
// //                                 normal : {
// //                                     lineStyle:{
// //                                         color:'#ff2f41',
// //                                         type:'dashed'
// //                                     },
// //                                     color:'#ff2f41'
// //                                 }
// //                             },
// //                         },
// //                     ]
// //                 };
// //                 option.xAxis.data = data["X"];
// //                 option.series[0].data = data["Y"];
// //                 option.series[1].data = data["Y1"];
// //                 option.yAxis[0].name=data['X_NAME'];
// //                 option.series[0].name=data['X_NAME'];
// //                 option.legend.data=[data['X_NAME'],'不合格率'];
// //
// //
// //                 // 使用刚指定的配置项和数据显示图表。
// //                 myChart.setOption(option);
// //             }else{
// //                 alert(data.status);
// //             }
// //         });
// //     });
// // });
//
// var optionArray=[];//存放影响因子分析页面中渲染的选项，郭英杰写的
// var msgSpan = document.createElement("span");//路径提示
// $(function(){
//     var tablediv = $('#tablediv');
//     var treediv = $('#treediv');
//     var impactfactordiv = $('#impactfactordiv');
//     var multiple = $('#multiple');
//     var table  = $("#table");
//     var tree = $('#tree');
//     var containers = [];
//     var impactfactor = $('#impactfactor');
//     var parameterclass = $('.parameter');
//     var buttonclass =  $('.button');
//     var slideclass = $('.slide');
//     var submitattr = $("#submitattr");
//     var tagBtn = $('.tagbar');
//     var contents = $('.analysis_content');
//     var tag_input = $('.tag_input');
//     containers.push(tablediv,treediv,impactfactordiv);
//     tablediv.hide();
//     treediv.hide();
//     impactfactordiv.hide();
//     buttonclass.hide();
//     slideclass.hide();
//     tagBtn.on('click',function(){
//        tagBtn.removeClass('active');
//        $(this).addClass('active');
//        contents.hide();
//        containers[parseInt($(this).attr('d_index'))].show();
//        tag_input.attr('value',$(this).html());
//        if(parseInt($(this).attr('d_index'))==1){
//            createTreeV("树");
//        }
//             if(parseInt($(this).attr('d_index'))==2){
//             msgSpan.style.position="absolute";
//             // declareSpan.style.top=node.y+$('#analysismat').height()*0.19-(6-node.level)*1.5+'px';
//             msgSpan.style.top=350+'px';
//             msgSpan.style.left=450+'px';
//             msgSpan.style.fontSize=30+'px';
//             msgSpan.innerHTML = "请选择分析变量";
//             document.getElementById("staticdiv").appendChild(msgSpan);
//         }
//
//     });
//         switch(tag_selected){
//             case 1:
//                 tagBtn.eq(0).click();
//                 break;
//             case 2:
//                 tagBtn.eq(1).click();
//                 break;
//             case 3:
//                 tagBtn.eq(2).click();
//                 break;
//             default:
//                 alert(渲染格式错误);
//     }
//
//     var numClick1 = 0;
//     var numClick2 = 0;
//     var numClick3 = 0;
//     parameterclass.click(function() {
//         var parameter_tag = $(this).attr('tag');
//         var slide_tag = $('.slide[tag=' + parameter_tag + ']');
//         slide_tag.slideToggle();
//
//
//         if(parameter_tag == "p_1") {
//             var img_right = $(this).children('img.right');
//             var img_button = $(this).children('img.button');
//
//             if(numClick1 == 0) {
//                 img_right.hide();
//                 img_button.show();
//                 numClick1 ++;
//             }
//             else {
//                 img_right.show();
//                 img_button.hide();
//                 numClick1 --;
//             }
//         }
//
//         if(parameter_tag == "p_2") {
//             var img_right = $(this).children('img.right');
//             var img_button = $(this).children('img.button');
//
//             if(numClick2 == 0) {
//                 img_right.hide();
//                 img_button.show();
//                 numClick2 ++;
//             }
//             else {
//                 img_right.show();
//                 img_button.hide();
//                 numClick2 --;
//             }
//
//         }
//
//         if(parameter_tag == "p_3") {
//             var img_right = $(this).children('img.right');
//             var img_button = $(this).children('img.button');
//
//             if(numClick3 == 0) {
//                 img_right.hide();
//                 img_button.show();
//                 numClick3 ++;
//             }
//             else {
//                 img_right.show();
//                 img_button.hide();
//                 numClick3 --;
//             }
//         }
//     });
//     var target = document.querySelectorAll('.range-slider');
//     var limitscontent = $('#impactfactordiv .limit');
//     var namecontent=$('.parameter #temperaturefont');
//     var limits = [];
//     var ranges = [];
//     var names  = [];
//
//     for(var i = 0 ; i < namecontent.length ; i++){
//         var arr = namecontent.eq(i).html().trim() ;
//         names.push(arr);
//     }
//
//     for(var i = 0 ; i < limitscontent.length ; i++){
//         var arr = limitscontent.eq(i).html().split(',');
//         var x = arr.map(function(index){
//             return parseFloat(index).toFixed(2);
//         });
//         limits.push(x);
//     }
//     for(var i = 0 ; i < target.length ; i++){
//         var ll = parseFloat(limits[i][0]);
//         var ul = parseFloat(limits[i][1]);
//         var x = rangeSlider.init(target[i],ll,ul,function(obj,lock){
//             var btns = $('.range-btn');
//             if(lock){
//                 btns.removeClass('selected');
//                 obj.className = 'range-btn selected';
//             }else{
//                 obj.className = 'range-btn'
//             }
//         });
//         ranges.push(x);
//         x = null;
//     }
//
//     //提交按钮
//     $('.submit-btn').on('click', function () {
//         // 通过 get 方法获取滑动输入条的范围，如果 range 已被锁定，get 方法返回空数组
//         var values = [];
//         for(var i = 0 ; i < target.length ; i++){
//             values.push(ranges[i].get());
//         }
//         var json={};
//         var staticJson={};
//         json["stage_name"]=$('#stageselect').html();
//         json["equip_lists"]=$('#multiple').text();
//         // json.equip_lists = json.equip_lists.splice(0,json.equip_lists.length-1);
//         json["feature_name"]=$('#features').html().split(',');
//         json.feature_name = json.feature_name.splice(0,json.feature_name.length-1);
//         json['target_label'] = PredictingTarget
//         for(var i=0;i<values.length;i++){
//             if(values[i]!=""){
//                 staticJson[names[i]]=values[i];
//             }
//             else {json["target_feature"]=names[i];}
//
//         }
//
//         json["static_feature"]=JSON.stringify(
//
// );
//         console.log(json);
//         msgSpan.style.display='none';
//
//         $.post(drawurl,json,function(data){
//             if(data.status == 200){
//             var myChart = echarts.init(document.getElementById('staticdiv'));
//             alert(echarts);
//                 var option = {
//                     title: {
//
//                     },
//                     tooltip: {
//                         trigger: 'axis'
//                     },
//                     grid: {
//                         left: '3%',
//                         right: '4%',
//                         bottom: '3%',
//                         containLabel: true
//                     },
//                     legend: {
//                         data:[],
//                         itemGap:25,
//                         textStyle:{
//                             color:"#ffffff"
//                         }
//                     },
//                     xAxis: {
//                         type: 'category',
//                         boundaryGap: false,
//                         data: [],
//                         // 控制网格线是否显示
//                         splitLine: {
//                             show: false,
//                         },
//                         //  改变x轴字体颜色和大小
//                         axisLabel: {
//                             textStyle: {
//                                 color:'#ffffff'
//                             },
//                         },
//                         nameTextStyle:{
//                             color:"#ffffff"
//                         }
//                     },
//                     yAxis: [
//                         {
//                             type: 'value',
//                             position:"left",
//                             splitLine: {
//                                 show: false,
//                             },
//                             //  改变y轴字体颜色和大小
//                             axisLabel: {
//                                 textStyle: {
//                                     color: '#ffffff'
//                                 },
//                             },
//                             nameTextStyle:{
//                                 color:"#ffffff"
//                             },
//                             axisLine: {
//                                 onZero: false,
//                                 lineStyle: {
//                                     color: "#ffffff"
//                                 }
//                             },
//                         },
//                         {
//                             name:'不合格率',
//                             type: 'value',
//                             position: 'right',
//                             splitLine: {
//                                 show: false,
//                             },
//                             //  改变y轴字体颜色和大小
//                             axisLabel: {
//                                 textStyle: {
//                                     color: '#ffffff'
//                                 },
//                             },
//                             nameTextStyle:{
//                                 color:"#ffffff"
//                             },
//                             axisLine: {
//                                 onZero: false,
//                                 lineStyle: {
//                                     color: "#ffffff"
//                                 }
//                             },
//                         },
//                     ],
//                     dataZoom: [{
//                         type: 'inside',
//                         start: 50,
//                         end: 70
//                     }, {
//                         type: 'slider',
//                         start: 50,
//                         end: 70
//                     }],
//                     series: [
//                         {
//                             type:'line',
//                             smooth:true,
//                             data:[],
//                             itemStyle : {
//                                 normal : {
//                                     lineStyle:{
//                                         color:'#60d4ff',
//                                         type:'solid'
//                                     },
//                                     color:'#60d4ff'
//                                 }
//                             },
//                             areaStyle: {normal: {
//                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                     offset: 0,
//                                     color: '#46e2ff'
//                                 }, {
//                                     offset: 1,
//                                     color: '#1b1cff'
//                                 }]),
//                                 opacity:0.4
//                             }
//                             }
//                         },
//                         {
//                             name:'不合格率',
//                             type:'line',
//                             smooth:true,
//                             stack: '总量',
//                             yAxisIndex: 1,
//                             data:[],
//                             itemStyle : {
//                                 normal : {
//                                     lineStyle:{
//                                         color:'#FFDB53',
//                                         type:'solid'
//                                     },
//                                     color:'#FFDB53'
//                                 }
//                             },
//                             areaStyle: {
//                                 normal: {
//                                     color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
//                                         offset: 0,
//                                         color: '#fff96b'
//                                     }, {
//                                         offset: 1,
//                                         color: '#ffe31d'
//                                     }]),
//                                     opacity: 0.3
//                                 }
//                             }
//                         },
//                     ]
//                 };
//                 option.xAxis.data = data["X"];
//                 option.series[0].data = data["Y"];
//                 option.series[1].data = data["Y1"];
//                 option.yAxis[0].name=data['X_NAME'];
//                 option.series[0].name=data['X_NAME'];
//                 option.legend.data=[data['X_NAME'],'不合格率'];
//
//                 // 使用刚指定的配置项和数据显示图表。
//                 myChart.setOption(option);
//             }else{
//                 alert(data.status);
//             }
//         });
//     });
// });

//计算字符串像素长度的工具类，郭英杰找的，
function calcStringPixelsCount(str, strFontSize) {
    // 字符串字符个数
    var stringCharsCount = str.length;

    // 字符串像素个数
    var stringPixelsCount = 0;

    // JS 创建HTML元素：span
    var elementPixelsLengthRuler = document.createElement("span");
    elementPixelsLengthRuler.style.fontSize = strFontSize;  // 设置span的fontsize
    elementPixelsLengthRuler.style.visibility = "hidden";  // 设置span不可见
    elementPixelsLengthRuler.style.display = "inline-block";
    elementPixelsLengthRuler.style.wordBreak = "break-all !important";  // 打断单词

    // 添加span
    document.body.appendChild(elementPixelsLengthRuler);

    for (var i =0; i < stringCharsCount; i++) {
        // 判断字符是否为空格，如果是用&nbsp;替代，原因如下：
        // 1）span计算单个空格字符（ ），其像素长度为0
        // 2）空格字符在字符串的开头或者结果，计算时会忽略字符串
        if (str[i] == " ") {
            elementPixelsLengthRuler.innerHTML = "&nbsp;";
        } else {
            elementPixelsLengthRuler.innerHTML = str[i];
        }

        stringPixelsCount += elementPixelsLengthRuler.offsetWidth;
    }

    return stringPixelsCount;
}

var optionArray=[];//存放影响因子分析页面中渲染的选项，郭英杰写的
var msgSpan = document.createElement("span");//"请选择分析变量提示"

$(function(){

        window.CruleSpan = document.createElement("span");
        CruleSpan.style.position="absolute";
        CruleSpan.style.top=100+'px';
        CruleSpan.style.left=100+'px';
        CruleSpan.style.fontSize=20+'px';
        document.getElementById("staticdiv").appendChild(CruleSpan);

    var tablediv = $('#tablediv');
    var treediv = $('#treediv');
    var impactfactordiv = $('#impactfactordiv');
    var multiple = $('#multiple');
    var table  = $("#table");
    var tree = $('#tree');
    var containers = [];
    var impactfactor = $('#impactfactor');
    var parameterclass = $('.parameter');
    var buttonclass =  $('.button');
    var slideclass = $('.slide');
    var submitattr = $("#submitattr");
    var tagBtn = $('.tagbar');
    var contents = $('.analysis_content');
    var tag_input = $('.tag_input');
    containers.push(tablediv,treediv,impactfactordiv);
    tablediv.hide();
    treediv.hide();
    impactfactordiv.hide();
    buttonclass.hide();
    slideclass.hide();
    tagBtn.on('click',function(){
       tagBtn.removeClass('active');
       $(this).addClass('active');
       contents.hide();
       containers[parseInt($(this).attr('d_index'))].show();
       tag_input.attr('value',$(this).html());

       if(parseInt($(this).attr('d_index'))==1){
           createTreeV("树");
       }
        if(parseInt($(this).attr('d_index'))==2){

            msgSpan.style.position="absolute";
            // declareSpan.style.top=node.y+$('#analysismat').height()*0.19-(6-node.level)*1.5+'px';
            msgSpan.style.top=280+'px';
            msgSpan.style.left=670+'px';
            msgSpan.style.fontSize=30+'px';
            msgSpan.innerHTML = "请选择分析变量";
            document.getElementById("staticdiv").appendChild(msgSpan);
        }
    });

            switch(tag_selected){
            case 1:
                tagBtn.eq(0).click();
                break;
            case 2:
                tagBtn.eq(1).click();
                break;
            case 3:
                tagBtn.eq(2).click();
                break;
            default:
                alert(渲染格式错误);
    }
    var numClick = [];
    for(var i = 0 ; i < parameterclass.length ; i++){
        numClick.push(0);
    }
    parameterclass.click(function() {
        var parameter_tag = $(this).attr('tag');
        var slide_tag = $('.slide[tag=' + parameter_tag + ']');
        slide_tag.slideToggle();
        var img_right = $(this).children('img.right');
        var img_button = $(this).children('img.button');
        var n = parseInt(parameter_tag);
        var m = numClick[n];
        if(m == 0){
            img_right.hide();
            img_button.show();
            numClick[n]++;
            $(this).find('.feature_range').hide();
        }else{
            img_right.show();
            img_button.hide();
            numClick[n]--;
            var r = ranges[n].get();
            if(r.length != 0){
                $(this).find('.feature_range').show();
                $(this).find('.feature_range').html('('+r[0]+','+r[1]+')');
            }
        }
    });
    var target = document.querySelectorAll('.range-slider');
    var limitscontent = $('#impactfactordiv .limit');
    var namecontent=$('#impactfactordiv .feature_label .feature_name');
    var limits = [];
    var ranges = [];
    var names  = [];

    for(var i = 0 ; i < namecontent.length ; i++){
        var arr = namecontent.eq(i).html().trim() ;
        names.push(arr);
    }

    for(var i = 0 ; i < limitscontent.length ; i++){
        var arr = limitscontent.eq(i).html().split(',');
        var x = arr.map(function(index){
            return parseFloat(index).toFixed(2);
        });
        limits.push(x);
    }
    for(var i = 0 ; i < target.length ; i++){
        var ll = parseFloat(limits[i][0]);
        var ul = parseFloat(limits[i][1]);
        var x = rangeSlider.init(target[i],ll,ul,function(obj,lock){
            var btns = $('.range-btn');
            if(lock){
                btns.removeClass('selected');
                obj.className = 'range-btn selected';
            }else{
                obj.className = 'range-btn'
            }
        });
        ranges.push(x);
        x = null;
    }



    //提交按钮
    $('.submit-btn').on('click', function () {

        document.getElementById("staticdiv").removeChild(CruleSpan);

        // 通过 get 方法获取滑动输入条的范围，如果 range 已被锁定，get 方法返回空数组
        var values = [];
        for(var i = 0 ; i < target.length ; i++){
            values.push(ranges[i].get());
        }
        var json={};
        var staticJson={};
        json["stage_name"]=$('#stageselect').html();
        json["equip_lists"]=$('#multiple').text().split(',');
        json.equip_lists = json.equip_lists.splice(0,json.equip_lists.length-1);
        json["feature_name"]=$('#features').html().split(',');
        json['target_label'] = PredictingTarget
        json.feature_name = json.feature_name.splice(0,json.feature_name.length-1);

        for(var i=0;i<values.length;i++){
            if(values[i]!=""){
                staticJson[names[i]]=values[i];
            }
            else {json["target_feature"]=names[i];}

        }

        json["static_feature"]=JSON.stringify(staticJson);
        console.log(json);

        var myChart = echarts.init(document.getElementById('staticdiv'));//echarts实例
       $.post(drawurl,json,function(data){
            if(data.status == 200){
                msgSpan.style.display='none';
                var myChart = echarts.init(document.getElementById('staticdiv'));
                var option = {
                    title: {

                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataZoom : {show: true},
                            dataView : {show: true, readOnly: false},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    grid: {
                        left: '6%',
                        right: '6%',
                        bottom: '20%',
                        containLabel: true
                    },
                    legend: {
                        data:[],
                        itemGap:25,
                        textStyle:{
                            color:"#ffffff"
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: [],
                        // 控制网格线是否显示
                        splitLine: {
                            show: false,
                        },
                        //  改变x轴字体颜色和大小
                        axisLabel: {
                            textStyle: {
                                color:'#ffffff'
                            },
                        },
                        nameTextStyle:{
                            color:"#ffffff"
                        },
                        axisLine: {
                                onZero: false,
                                lineStyle: {
                                    color: "#ffffff"
                                }
                            }
                    },
                    yAxis: [
                        {
                            type: 'value',
                            position:"left",
                            splitLine: {
                                show: false,
                            },
                            //  改变y轴字体颜色和大小
                            axisLabel: {
                                textStyle: {
                                    color: '#ffffff'
                                },
                            },
                            nameTextStyle:{
                                color:"#ffffff"
                            },
                            axisLine: {
                                onZero: false,
                                lineStyle: {
                                    color: "#ffffff"
                                }
                            },
                        },
                        {
                            name:'不合格率',
                            type: 'value',
                            position: 'right',
                            splitLine: {
                                show: false,
                            },
                            //  改变y轴字体颜色和大小
                            axisLabel: {
                                textStyle: {
                                    color: '#ffffff'
                                },
                            },
                            nameTextStyle:{
                                color:"#ffffff"
                            },
                            axisLine: {
                                onZero: false,
                                lineStyle: {
                                    color: "#ffffff"
                                }
                            },
                        },
                    ],
                    dataZoom: [{
                        type: 'slider',
                        start: 0,
                        end: 100,
                        bottom:'15%',
                        handleSize:50,
                        height:20,
                        textStyle:{
                            color: "#ffffff"
                        },
                        dataBackground:{
                            areaStyle:{
                                color: "#ffffff"
                            }
                        }
                    },{
                        type: 'slider',
                        start: 0,
                        end: 100,
                        yAxisIndex:0,
                        left:30,
                        handleSize:50,
                        width:20,
                        textStyle:{
                            color: "#ffffff"
                        },
                        dataBackground:{
                            areaStyle:{
                                color: "#ffffff"
                            }
                        }
                    },{
                        type: 'slider',
                        start: 0,
                        end: 100,
                        right:30,
                        handleSize:50,
                        yAxisIndex:1,
                        width:20,
                        textStyle:{
                            color: "#ffffff"
                        },
                        dataBackground:{
                            areaStyle:{
                                color: "#ffffff"
                            }
                        }
                    }],
                    series: [
                        {
                            type:'line',
                            smooth:true,
                            data:[],
                            itemStyle : {
                                normal : {
                                    lineStyle:{
                                        color:'#60d4ff',
                                        type:'solid'
                                    },
                                    color:'#60d4ff'
                                }
                            },
                            // areaStyle: {normal: {
                            //     color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            //         offset: 0,
                            //         color: '#46e2ff'
                            //     }, {
                            //         offset: 1,
                            //         color: '#1b1cff'
                            //     }]),
                            //     opacity:0.4
                            // }
                            // }
                        },
                        {
                            name:'不合格率',
                            type:'line',
                            smooth:true,
                            yAxisIndex: 1,
                            data:[],
                            itemStyle : {
                                normal : {
                                    lineStyle:{
                                        color:'#FFDB53',
                                        type:'solid'
                                    },
                                    color:'#FFDB53'
                                }
                            },
                            // areaStyle: {
                            //     normal: {
                            //         color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            //             offset: 0,
                            //             color: '#fff96b'
                            //         }, {
                            //             offset: 1,
                            //             color: '#ffe31d'
                            //         }]),
                            //         opacity: 0.3
                            //     }
                            // }
                        },
                        {
                            type:'line',
                            smooth:true,
                            data:[],
                            itemStyle : {
                                normal : {
                                    lineStyle:{
                                        color:'#02ff32',
                                        type:'solid'
                                    },
                                    color:'#02ff32'
                                }
                            }
                            // areaStyle: {
                            //     normal: {
                            //         color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            //             offset: 0,
                            //             color: '#fff96b'
                            //         }, {
                            //             offset: 1,
                            //             color: '#ffe31d'
                            //         }]),
                            //         opacity: 0.3
                            //     }
                            // }
                        },
                        {
                            name:'不合格率趋势',
                            type:'line',
                            smooth:true,
                            yAxisIndex: 1,
                            data:[],
                            itemStyle : {
                                normal : {
                                    lineStyle:{
                                        color:'#ff8b09',
                                        type:'solid'
                                    },
                                    color:'#ff8b09'
                                }
                            }
                            // areaStyle: {
                            //     normal: {
                            //         color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            //             offset: 0,
                            //             color: '#fff96b'
                            //         }, {
                            //             offset: 1,
                            //             color: '#ffe31d'
                            //         }]),
                            //         opacity: 0.3
                            //     }
                            // }
                        },
                    ]
                };
                option.xAxis.data = data["X"];
                option.series[0].data = data["Y"];
                option.series[1].data = data["Z"];
                option.series[2].data = data["RY"];
                option.series[3].data = data["RZ"];
                option.yAxis[0].name=data['X_NAME'];
                option.series[0].name=data['X_NAME'];
                option.series[2].name=data['X_NAME']+"趋势";
                option.legend.data=[data['X_NAME'],data['X_NAME']+"趋势",'不合格率',"不合格率趋势"];

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);


                window.CruleSpan = document.createElement("span");
                CruleSpan.style.position="absolute";
                CruleSpan.style.top='90%';
                CruleSpan.style.left=$('#staticdiv').width()/2-calcStringPixelsCount(data['form'],20)/2+'px';
                CruleSpan.style.fontSize=20+'px';
                CruleSpan.innerHTML=data['form'];

                String.prototype.myReplace=function(f,e){//吧f替换成e
                    var reg=new RegExp(f,"g"); //创建正则RegExp对象
                    return this.replace(reg,e);
                }

                CruleSpan.innerHTML=CruleSpan.innerHTML.myReplace("\\+",'<span style="backgroundColor:#000c3c;color:red;">+</span>');
                CruleSpan.innerHTML=CruleSpan.innerHTML.myReplace('\\*','<span style="backgroundColor:#000c3c;color:red;">*</span>');
                CruleSpan.innerHTML=CruleSpan.innerHTML.myReplace('= ','<span style="backgroundColor:#000c3c;color:yellow;">' + ' = ' + '</span>');

                document.getElementById("staticdiv").appendChild(CruleSpan);

            }else{
                alert(data.status);
            }
        });
    });
});