$(function () {
    var flowChart = echarts.init(document.getElementById('flowChart'));
    var flowChartOption = {
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '1%',
            containLabel: true
        },
        xAxis:  {
            type: 'value',
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
                    color: "#ffffff",
                }
            },
            splitLine:{
                lineStyle:{
                    width:0.5,
                    opacity:0.5
                }
            }
        },
        yAxis: {
            type: 'category',
            // data: ['1', '2', '3', '4'],
            data:[],
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
            }
        },
        series: [
            {
                type: 'bar',
                label: {
                    normal: {
                        show: true,
                        position: 'right',
                        color:"#ffffff"
                    }
                },
                data: [],
                itemStyle:{
                    normal:{
                        color:function(params){
                            var colorList = ['#3FA9F5','#0064FD','#FF7CA2','rgb(255, 178, 123)','#BB7DFD',
                                '#1873b2']
                            return colorList[params.dataIndex]
                        }
                    }
                }
            }
        ]
    };

    var count=0;

    var characteristicBarX=[
        ['VAD塔线_C','VAD塔线_D','VAD塔线_E','VAD塔线_F','VAD塔线_G','VAD塔线_H'],
        ['VAD塔线_C','VAD塔线_D','VAD塔线_E','VAD塔线_F','VAD塔线_G','VAD塔线_H'],
        ['拉伸塔线_B'],
        ['OVD塔线_C','OVD塔线_D','OVD塔线_E']
    ];
    var characteristicBarY=[
        [30617948,8700900,37639950,29709195,9281042,37081786],
        [30617948,8700900,9153485,39856548,34992745,29709195],
        [153030821],
        [74345127,28300562,50385132]
    ];

    var currentX=characteristicBarX[count%4];
    var currentY=characteristicBarY[count%4];
    flowChartOption.yAxis.data=currentX;
    flowChartOption.series[0].data=currentY;
    flowChart.setOption(flowChartOption);

    window.FCinterval=setInterval(function () {
        count++;
        var currentX=characteristicBarX[count%4];
        var currentY=characteristicBarY[count%4];
        flowChartOption.yAxis.data=currentX;
        flowChartOption.series[0].data=currentY;
        flowChart.setOption(flowChartOption);
    },5000)

    flowChart.setOption(flowChartOption);

    $("#speedSelect").change(function(){
        var counter = $('#speedSelect').val();
        clearInterval(FCinterval);
        var myFunction = function(){
            counter = $('#speedSelect').val();
            count++;
            var currentX=characteristicBarX[count%4];
            var currentY=characteristicBarY[count%4];
            flowChartOption.yAxis.data=currentX;
            flowChartOption.series[0].data=currentY;
            flowChart.setOption(flowChartOption);
        }
        window.FCinterval = setInterval(myFunction, counter);
    });
});