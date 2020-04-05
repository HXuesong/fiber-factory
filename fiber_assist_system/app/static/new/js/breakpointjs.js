
$(function(){
    var impactfactordiv = $('#impactfactordiv');
    impactfactordiv.show();

    var myChart = echarts.init(document.getElementById("impactfactordiv"));
    //提交按钮
    $('#submitbt').on('click', function () {
        var a={'status': 200, 'data': {'H': 0.02274, 'G': 0.02007}}
        var xArray=[];
        var yArray=[];

        var json={};
        json["stage_name"]=$('#stageselect').html();
        json["equip_lists"]=$('#multiple').text().split(',');

        console.log(json);

        $.post(drawurl,json,function(data){
            console.log(data);
            if(data.status == 200){
                for (var key in data['data'])
                {
                    xArray.push(key);
                    yArray.push(data['data'][key]);
                }
                myChart.clear();
                var option = {
                     tooltip : {
                        trigger: 'axis'
                    },
                    legend: {
                        data:['断点率'],
                        textStyle:{
                            color:"#ffffff"
                        }
                    },
                    xAxis : [
                        {
                            type : 'category',
                            data : xArray,
                            axisTick: {
                                alignWithLabel: true
                            },
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
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value',
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
                            }
                        }
                    ],
                    series : [
                        {
                            name:'断点率',
                            type:'bar',
                            barWidth: '60%',
                            data:[],
                            itemStyle : {
                                normal : {
                                    color:'#60d4ff',
                                }
                            },
                            label: {
                                normal: {
                                    show: true,
                                    position: 'top',
                                    color:'#ffffff'
                                 }
                             },
                        }
                    ]
                };
                // 使用刚指定的配置项和数据显示图表。
                option.series[0].data=yArray;

                myChart.setOption(option);
            }else{
                alert(data.status);
            }
        });

    });
});
