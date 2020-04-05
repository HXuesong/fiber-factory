// $(function () {
//     var breakpointPie = echarts.init(document.getElementById('breakpointPie'));
//     var breakpointPieOption = {
//         title:{
//             text:[],
//             textStyle:{
//                 color:'#7dceff',
//                 fontSize:13,
//                 left:'50%'
//             }
//         },
//         tooltip : {
//             trigger: 'item',
//         },
//         series : [
//             {
//                 type: 'pie',
//                 radius : '65%',
//                 center: ['50%', '50%'],
//                 selectedMode: 'single',
//                 data:[
//                 ],
//                 itemStyle: {
//                     emphasis: {
//                         shadowBlur: 10,
//                         shadowOffsetX: 0,
//                         shadowColor: 'rgba(0, 0, 0, 0.5)'
//                     }
//                 }
//             }
//         ]
//     };
//
//     var count=0;
//     var stage=['VAD塔线', 'VAD烧结塔线', '拉伸塔线', 'OVD塔线'];
//     var color=['#57a9ff','#FFDB53','#FF7CA2','#0064FD'];
//
//     var name=[
//         ['C_1', 'C_2', 'C_3', 'C_4',
//         'D_1', 'D_2', 'D_3', 'D_4',
//         'E_1', 'E_2', 'E_3', 'E_4',
//         'F_1', 'F_2', 'F_3', 'F_4',
//         'G_1', 'G_2', 'G_3', 'G_4',
//         'H_1', 'H_2', 'H_3', 'H_4'],
//
//         ['C_1', 'C_2', 'C_3', 'C_4',
//             'D_1', 'D_2', 'D_3', 'D_4',
//             'E_1', 'E_2', 'E_3', 'E_4',
//             'F_1', 'F_2', 'F_3', 'F_4',
//             'G_1', 'G_2', 'G_3', 'G_4',
//             'H_1', 'H_2', 'H_3', 'H_4'],
//
//         ['B_1', 'B_2', 'B_3', 'B_4'],
//
//         ['C_1', 'C_2', 'C_3', 'C_4',
//             'D_1', 'D_2', 'D_3', 'D_4',
//             'E_1', 'E_2', 'E_3', 'E_4']
//     ];
//     var value=[
//         [0.039, 0.038, 0.039, 0.044,
//             0.045, 0.041, 0.041, 0.043,
//             0.043, 0.042, 0.044, 0.045,
//             0.047, 0.046, 0.047, 0.048,
//             0.037, 0.037, 0.036, 0.038,
//             0.04, 0.041, 0.041, 0.039],
//
//         [0.039, 0.038, 0.038, 0.044,
//             0.044, 0.041, 0.04, 0.042,
//             0.041, 0.04, 0.037, 0.037,
//             0.041, 0.041, 0.042, 0.04,
//             0.041, 0.04, 0.043, 0.044,
//             0.047, 0.046, 0.047, 0.047],
//
//         [0.25, 0.245, 0.25, 0.256],
//
//         [0.085, 0.083, 0.084, 0.083,
//             0.076, 0.078, 0.08, 0.081,
//             0.087, 0.084, 0.086, 0.093]
//     ];
//
//     var data=[];
//     var json={};
//     json['value']=value[count%4];
//     json['name']=name[count%4];
//     for(var i=0;i<json['name'].length;i++){
//         data.push({
//             name: json['name'][i],
//             value:json['value'][i],
//             itemStyle:{
//                 normal:{
//                     color:color[i%4]
//                 }
//             }
//         });
//     }
//     breakpointPieOption.series[0].data=data;
//     breakpointPieOption.title.text='阶段:'+stage[0];
//
// // 使用刚指定的配置项和数据显示图表。
//     breakpointPie.setOption(breakpointPieOption);
//
//     setInterval(function () {
//         count++;
//         var data=[];
//         var json={};
//         json['value']=value[count%4];
//         json['name']=name[count%4];
//         for(var i=0;i<json['name'].length;i++){
//             data.push({
//                 name: json['name'][i],
//                 value:json['value'][i],
//                 itemStyle:{
//                     normal:{
//                         color:color[i%4]
//                     }
//                 }
//             });
//         }
//         breakpointPieOption.series[0].data=data;
//         breakpointPieOption.title.text='阶段:'+stage[count%4];
//
// // 使用刚指定的配置项和数据显示图表。
//         breakpointPie.setOption(breakpointPieOption);
//     },5000)
//
// });


$(function () {
    var breakpointPie = echarts.init(document.getElementById('breakpointPie'));
    var breakpointPieOption = {
        color: ['#3398DB'],
        title:{
            text:[],
            textStyle:{
                color:'#7dceff',
                fontSize:14,
                left:'center'
            }
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                data:[],
                axisTick: {
                    alignWithLabel: true
                },
                //  改变y轴字体颜色和大小
                axisLabel: {
                    textStyle: {
                        color: '#ffffff',
                        fontSize:5
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
            }
        ],
        yAxis : [
            {
                type : 'value',
                //  改变y轴字体颜色和大小
                axisLabel: {
                    textStyle: {
                        color: '#ffffff',
                        opacity:0.5
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
                splitLine:{
                    lineStyle:{
                        width:0.5,
                        opacity:0.5
                    }
                }
            }
        ],
        series : [
            {
                type:'bar',
                barWidth: '60%',
                data:[],
                itemStyle:{
                    normal:{
                        color:[]
                        //     function(params){
                        //     var colorList = [
                        //         '#0064FD','#BB7DFD','#FF7CA2','#FEDA52','#92FABE', '#3FA9F5'];
                        //     return colorList[params.dataIndex]
                        // }
                    }
                }
            }
        ]
    };

    var count=0;

    var colorList = ['#0064FD','#FEDA52','#92FABE', '#3FA9F5'];

    var stage=['VAD塔线','VAD烧结塔线','拉伸塔线','OVD塔线'];
    var breakpointPieX=[
        ['C_1', 'C_2', 'C_3', 'C_4', 'D_1', 'D_2', 'D_3', 'D_4', 'E_1', 'E_2', 'E_3', 'E_4', 'F_1', 'F_2', 'F_3', 'F_4', 'G_1', 'G_2', 'G_3', 'G_4', 'H_1', 'H_2', 'H_3', 'H_4'],
        ['C_1', 'C_2', 'C_3', 'C_4', 'D_1', 'D_2', 'D_3', 'D_4', 'E_1', 'E_2', 'E_3', 'E_4', 'F_1', 'F_2', 'F_3', 'F_4', 'G_1', 'G_2', 'G_3', 'G_4', 'H_1', 'H_2', 'H_3', 'H_4'],
        ['B_1', 'B_2', 'B_3', 'B_4'],
        ['C_1', 'C_2', 'C_3', 'C_4', 'D_1', 'D_2', 'D_3', 'D_4', 'E_1', 'E_2', 'E_3', 'E_4']
    ];

    var breakpointPieY=[
        [76.29, 67.2, 70.73, 128.81, 136.91, 94.12, 90.54, 113.07, 116.31, 103.86, 133.94, 146.97, 185.91, 163.82, 182.7, 191.32, 62.87, 56.71, 51.59, 64.94, 82.04, 90.2, 97.15, 76.23],
        [76.29, 67.2, 70.73, 128.81, 136.91, 94.12, 90.54, 113.07, 91.09, 84.93, 60.2, 63.59, 90.84, 96.12, 102.87, 86.63, 98.63, 89.27, 122.59, 132.81, 185.91, 163.82, 182.7, 191.32],
        [106.41, 97.12, 107.2, 119.24],
        [111.78, 99.94, 107.87, 100.45, 68.86, 77.91, 84.85, 90.19, 123.14, 103.94, 121.74, 173.97]
    ];

    var currentX=breakpointPieX[count%4];
    var currentY=breakpointPieY[count%4];
    breakpointPieOption.xAxis[0].data=currentX;
    breakpointPieOption.series[0].data=currentY;
    breakpointPieOption.series[0].itemStyle.normal.color=colorList[count%4];
    breakpointPieOption.title.text='阶段:'+stage[count%4];

    breakpointPie.setOption(breakpointPieOption);

    setInterval(function () {
        count++;
        var currentX=breakpointPieX[count%4];
        var currentY=breakpointPieY[count%4];
        breakpointPieOption.xAxis[0].data=currentX;
        breakpointPieOption.series[0].data=currentY;
        breakpointPieOption.series[0].itemStyle.normal.color=colorList[count%4];
        breakpointPieOption.title.text='阶段:'+stage[count%4];

        breakpointPie.setOption(breakpointPieOption);
    },7000)
});