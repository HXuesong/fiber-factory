$(function () {
    var qualificationLine = echarts.init(document.getElementById('qualificationLine'));
    var qualificationLineOption = {
        color: ['#3398DB'],
        title:{
            text:[],
            // subtext:[],
            textStyle:{
              color:'#7dceff',
              fontSize:14,
                align:'right'
            }
            // subtextStyle:{
            //   color:'#7dceff',
            //   fontSize:14,
            //     left:'center'
            // }
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data:[],
            // itemGap:25,
            top:30,
            textStyle:{
                color:"#ffffff"
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
                data :[],
                axisTick: {
                    alignWithLabel: true
                },
                //  改变y轴字体颜色和大小
                axisLabel: {
                    textStyle: {
                        color: '#ffffff',
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
            }
        ],
        yAxis : [
            {
                type : 'value',
                //  改变y轴字体颜色和大小
                min:0.72,
                max:1,
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
                name:[],
                type:'line',
                smooth:true,
                data:[],
                itemStyle:{
                    normal:{
                        color:[]
                    }
                }
            },
            {
                name:[],
                type:'line',
                smooth:true,
                data:[],
                itemStyle:{
                    normal:{
                        color:[]
                    }
                }
            },
            {
                name:[],
                type:'line',
                smooth:true,
                data:[],
                itemStyle:{
                    normal:{
                        color:[]
                    }
                }
            },
            {
                name:[],
                type:'line',
                smooth:true,
                data:[],
                itemStyle:{
                    normal:{
                        color:[]
                    }
                }
            },
            {
                name:[],
                type:'line',
                smooth:true,
                data:[],
                itemStyle:{
                    normal:{
                        color:[]
                    }
                }
            },
            {
                name:[],
                type:'line',
                smooth:true,
                data:[],
                itemStyle:{
                    normal:{
                        color:[]
                    }
                }
            }
        ]
    };

    var count=0;

    var colorList = [
        '#0064FD','#BB7DFD','#FF7CA2','#FEDA52','#92FABE',
        '#3FA9F5'];

    var stage=[
        'VAD塔线',
        'VAD烧结塔线',
        '拉伸塔线',
        'OVD塔线'
    ];
    var equipment=[
        ['C', 'G', 'F', 'E', 'H', 'D'],
        ['C', 'G', 'F', 'E', 'H', 'D'],
        ['B'],
        ['D', 'E', 'C']
    ];
    var qualificationLineX=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
    var qualificationLineY=[
        [[0.778, 0.842, 0.881, 0.978, 0.978, 0.978, 0.97, 0.974, 0.969, 0.97],
            [0.824, 0.881, 0.908, 0.961, 0.975, 0.975, 0.961, 0.979, 0.962, 0.952],
            [0.796, 0.857, 0.888, 0.973, 0.965, 0.966, 0.97, 0.977, 0.971, 0.968],
            [0.758, 0.808, 0.838, 0.938, 0.955, 0.971, 0.972, 0.972, 0.96, 0.956],
            [0.766, 0.839, 0.875, 0.985, 0.991, 0.975, 0.961, 0.948, 0.926, 0.929],
            [0.842, 0.893, 0.918, 0.993, 0.993, 0.974, 0.974, 0.975, 0.946, 0.954]],

        [[0.778, 0.842, 0.881, 0.978, 0.978, 0.978, 0.97, 0.974, 0.969, 0.97],
            [0.742, 0.793, 0.827, 0.933, 0.951, 0.969, 0.971, 0.971, 0.958, 0.953],
            [0.765, 0.839, 0.875, 0.986, 0.992, 0.976, 0.963, 0.951, 0.929, 0.931],
            [0.877, 0.916, 0.935, 0.966, 0.979, 0.979, 0.964, 0.979, 0.968, 0.96],
            [0.796, 0.857, 0.888, 0.973, 0.965, 0.966, 0.97, 0.977, 0.971, 0.968],
            [0.842, 0.893, 0.918, 0.993, 0.993, 0.974, 0.974, 0.975, 0.946, 0.954]],

            [[0.781, 0.843, 0.876, 0.97, 0.975, 0.973, 0.969, 0.969, 0.956, 0.955]],

        [[0.785, 0.851, 0.888, 0.984, 0.989, 0.993, 0.975, 0.975, 0.956, 0.943],
            [0.794, 0.863, 0.897, 0.992, 0.991, 0.984, 0.968, 0.967, 0.95, 0.944],
            [0.769, 0.825, 0.856, 0.949, 0.958, 0.96, 0.966, 0.967, 0.96, 0.966]]

    ];


    var currentX=qualificationLineX;
    var currentY=qualificationLineY[0];
    qualificationLineOption.xAxis[0].data=currentX;

    $.each(currentY,function (i) {
        qualificationLineOption.series[i].name=equipment[0][i];
        qualificationLineOption.series[i].data=this;
        qualificationLineOption.series[i].itemStyle.normal.color=colorList[i];
    })

    qualificationLineOption.legend.data=equipment[0];
    qualificationLineOption.title.text='阶段:'+stage[0];
    // qualificationLineOption.title.subtext='设备:'+equipment[0];
    qualificationLine.clear();
    qualificationLine.setOption(qualificationLineOption);

    setInterval(function () {

        count++;
        var currentX=qualificationLineX;
        var currentY=qualificationLineY[count%4];
        qualificationLineOption.xAxis[0].data=currentX;

        for(var i=0;i<6;i++){
            qualificationLineOption.series[i].data=[];
        }
        $.each(currentY,function (i) {
            qualificationLineOption.series[i].name=equipment[count%4][i];
            qualificationLineOption.series[i].data=this;
            qualificationLineOption.series[i].itemStyle.normal.color=colorList[i];
        })

        qualificationLineOption.legend.data=equipment[count%4];
        qualificationLineOption.title.text='阶段:'+stage[count%4];
        // qualificationLineOption.title.subtext='设备:'+equipment[count%4];
        qualificationLine.setOption(qualificationLineOption);
    },7500)
});
