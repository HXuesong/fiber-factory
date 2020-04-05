$(function () {
    var characteristicBar = echarts.init(document.getElementById('characteristicBar'));
    var characteristicBarOption = {
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
            }
        ],
        yAxis : [
            {
                type : 'value',
                //  改变y轴字体颜色和大小
                max:0.7,
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
                        color:function(params){
                            var colorList = [
                                '#0064FD','#BB7DFD','#FF7CA2','#FEDA52','#92FABE',
                                '#3FA9F5'];
                            return colorList[params.dataIndex]
                        }
                    }
                }
            }
        ]
    };

    var count=0;

    var stage=['ECC','1310MFD','λc','Zero DML'];
    var characteristicBarX=[
        ['fiber_step','最大跳', '有效', 'OD_Clad', 'OD_Core'],
        ['fiber_step','Delta', 'Non_Clad', '重量', '最大跳'],
        ['fiber_step','OD_Co','OD_Cl','Non_Co','最大跳'],
        ['fiber_step','D/d','最大跳','OD_Co','OD_Cl']
    ];

    var characteristicBarY=[
        [0.647, 0.165, 0.069, 0.06, 0.058],
        [0.619, 0.224, 0.054, 0.054, 0.049],
        [0.637, 0.139, 0.089, 0.07, 0.065],
        [0.597, 0.158, 0.097, 0.075, 0.074]
    ];

    var currentX=characteristicBarX[count%4];
    var currentY=characteristicBarY[count%4];
    characteristicBarOption.xAxis[0].data=currentX;
    characteristicBarOption.series[0].data=currentY;
    characteristicBarOption.title.text='阶段:'+stage[count%4];

    characteristicBar.setOption(characteristicBarOption);

    window.CBinterval=setInterval(function () {
        count++;
        var currentX=characteristicBarX[count%4];
        var currentY=characteristicBarY[count%4];
        characteristicBarOption.title.text='阶段:'+stage[count%4];
        characteristicBarOption.xAxis[0].data=currentX;
        characteristicBarOption.series[0].data=currentY;
        characteristicBar.setOption(characteristicBarOption);
    },5000)

    characteristicBar.setOption(characteristicBarOption);

    $("#speedSelect").change(function(){
        var counter = $('#speedSelect').val();
        clearInterval(CBinterval);
        var myFunction = function(){
            counter = $('#speedSelect').val();
            count++;
            var currentX=characteristicBarX[count%4];
            var currentY=characteristicBarY[count%4];
            characteristicBarOption.title.text='阶段:'+stage[count%4];
            characteristicBarOption.xAxis[0].data=currentX;
            characteristicBarOption.series[0].data=currentY;
            characteristicBar.setOption(characteristicBarOption);
        }
        window.CBinterval = setInterval(myFunction, counter);
    });
});