$(function () {

    var bestCharacteristicLine = echarts.init(document.getElementById('bestCharacteristicLine'));
    var bestCharacteristicLineOption = {
        color: ['#3398DB'],
        title:{
            text:[],
            subtext:[],
            textStyle:{
                color:'#7dceff',
                fontSize:14,
                left:'30%'
            },
            subtextStyle:{
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
                data :[],
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
                min:[],
                max:[],
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
                name:'最佳特征值',
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

    var target=["ECC","1310MFD","截止波长","Zero DML."];
    var features=["最大跳动值","DeltaTotal检验值","重量误差","包层直径上"];
    var range=[[0.220,0.290],[8.940,9.360],[1208.050,1242.050],[1307.500,1312.000]];
    // var colorList=['#0064FD','#FEDA52','#92FABE', '#3FA9F5'];
    // var colorList=['#26dfe5','#FEDA52','#92FABE', '#3FA9F5'];
    var colorList = ['#1873b2','rgb(255, 178, 123)','#3FA9F5', 'rgb(206, 105, 255)'];

    var qualificationLineX=[
        [0.516, 0.532, 0.552, 0.556, 0.578, 0.58, 0.592, 0.6, 0.662, 0.676, 0.73, 0.74, 0.8, 0.806, 0.812, 0.838, 0.884, 0.936, 0.978, 1.012, 1.034, 1.056, 1.11, 1.154, 1.164, 1.19, 1.382],
        [0.317, 0.32, 0.322, 0.325, 0.326, 0.328, 0.329, 0.33, 0.332, 0.333, 0.334, 0.335, 0.336, 0.337, 0.338, 0.339, 0.34, 0.341, 0.342, 0.343,
            0.344, 0.345, 0.346, 0.347, 0.348, 0.349, 0.35, 0.351, 0.352, 0.353, 0.354, 0.355, 0.356, 0.357, 0.358, 0.359, 0.36, 0.361, 0.362, 0.363, 0.364,
            0.365, 0.366, 0.367, 0.368, 0.369, 0.37, 0.371, 0.372, 0.373, 0.374, 0.375, 0.376, 0.377, 0.378, 0.379, 0.38, 0.381, 0.382, 0.383, 0.384, 0.385,
            0.386, 0.387, 0.388, 0.389, 0.39, 0.391, 0.392, 0.393, 0.394, 0.399, 0.402],
        [-1745.0, -1488.0, -1236.0, -1155.0, -1117.0, -1020.0, -1016.0, -998.0, -995.0, -978.0, -893.0, -860.0, -849.0, -839.0, -821.0, -770.0, -
            666.0, -662.0, -647.0, -590.0, -583.0, -569.0, -526.0, -522.0, -501.0, -469.0, -442.0, -441.0, -373.0, -359.0, -352.0, -316.0, -313.0, -283.0, -
            264.0, -259.0, -252.0, -228.0, -218.0, -216.0, -166.0, -164.0, -159.0, -151.0, -147.0, -145.0, -122.0, -119.0, -65.0, -36.0, -3.0, 0.0, 34.0, 41.0,
            52.0, 78.0, 80.0, 110.0, 145.0, 152.0, 165.0, 173.0, 201.0, 246.0, 298.0, 319.0, 328.0, 329.0, 334.0, 347.0, 377.0, 395.0, 456.0, 495.0, 499.0,
            563.0, 586.0, 604.0, 610.0, 645.0, 691.0, 744.0, 755.0, 773.0, 775.0, 779.0, 814.0, 825.0, 834.0, 862.0, 991.0, 1023.0, 1044.0, 1150.0, 1164.0,
            1262.0, 1266.0, 1426.0, 1503.0, 1732.0, 2075.0, 2351.0, 2366.0, 2536.0],
        [167.2, 167.9, 168.7, 168.9, 169.4, 170.4, 170.5, 170.6, 170.8, 171.0, 171.2, 171.3, 171.4, 171.5, 171.7, 172.1, 173.0, 173.2, 173.4, 173.7,
            173.8, 173.9, 174.2, 174.5, 175.1, 175.2, 175.3, 176.0, 176.4, 176.7, 176.8, 176.9, 177.0, 177.2, 177.3, 177.9, 178.0, 178.1, 178.9, 179.3, 179.5,
            179.6, 179.7, 179.8, 180.0, 180.1, 180.2, 180.5, 180.7, 180.8, 181.0, 181.1, 181.2, 181.3, 181.4, 181.5, 181.7, 182.4, 182.6, 182.8, 182.9, 183.0,
            183.2, 183.4, 183.9, 184.0, 184.1, 184.2, 184.4, 184.5, 185.5, 192.8]
    ];
    var qualificationLineY=[
        [0.224, 0.227, 0.231, 0.235, 0.242, 0.249, 0.257, 0.264, 0.271, 0.277, 0.281, 0.283, 0.284, 0.282, 0.278, 0.272, 0.265, 0.259, 0.253, 0.246,
            0.241, 0.237, 0.235, 0.234, 0.233, 0.232, 0.233],

        [9.329, 9.327, 9.326, 9.324, 9.323, 9.321, 9.319, 9.318, 9.316, 9.313, 9.31, 9.306, 9.303, 9.299, 9.295, 9.291, 9.287, 9.283, 9.278, 9.274,
            9.269, 9.264, 9.258, 9.252, 9.245, 9.239, 9.231, 9.224, 9.215, 9.207, 9.198, 9.188, 9.179, 9.168, 9.158, 9.147, 9.136, 9.125, 9.114, 9.103, 9.092,
            9.082, 9.072, 9.062, 9.053, 9.044, 9.035, 9.028, 9.021, 9.014, 9.008, 9.003, 8.998, 8.994, 8.991, 8.987, 8.984, 8.981, 8.979, 8.976, 8.974, 8.972,
            8.971, 8.969, 8.968, 8.967, 8.966, 8.966, 8.965, 8.964, 8.963, 8.962, 8.961],

        [1240.288, 1241.407, 1241.202, 1241.619, 1239.333, 1236.457, 1232.479, 1230.479, 1229.347, 1230.219, 1231.65, 1233.953, 1234.424, 1234.358,
            1233.673, 1232.831, 1231.35, 1229.811, 1226.826, 1222.697, 1217.95, 1213.181, 1209.386, 1208.065, 1208.929, 1211.532, 1215.274, 1220.173, 1225.046,
            1229.468, 1233.456, 1236.903, 1238.553, 1238.667, 1238.37, 1236.954, 1235.742, 1235.142, 1235.678, 1236.064, 1237.425, 1238.118, 1238.791, 1238.964,
            1239.483, 1239.008, 1237.685, 1234.393, 1229.406, 1222.394, 1215.759, 1211.412, 1210.838, 1213.743, 1220.297, 1228.325, 1235.364, 1239.812, 1241.915,
            1241.169, 1237.56, 1232.969, 1228.949, 1225.141, 1222.516, 1222.198, 1223.215, 1224.81, 1227.086, 1229.665, 1231.921, 1233.917, 1235.134, 1236.226,
            1236.113, 1235.06, 1232.874, 1230.365, 1227.06, 1224.598, 1223.65, 1224.71, 1227.699, 1231.905, 1236.113, 1238.135, 1237.594, 1233.41, 1227.07,
            1219.954, 1214.268, 1210.925, 1211.96, 1215.868, 1220.632, 1225.272, 1228.537, 1228.868, 1227.623, 1226.424, 1225.285, 1224.974, 1225.132, 1225.754],

        [1308.325, 1308.337, 1308.352, 1308.366, 1308.382, 1308.398, 1308.418, 1308.44, 1308.468, 1308.507, 1308.559, 1308.622, 1308.697, 1308.786,
            1308.888, 1309.003, 1309.127, 1309.256, 1309.387, 1309.521, 1309.659, 1309.801, 1309.946, 1310.091, 1310.234, 1310.372, 1310.503, 1310.625, 1310.736,
            1310.833, 1310.915, 1310.981, 1311.033, 1311.073, 1311.106, 1311.131, 1311.152, 1311.17, 1311.185, 1311.197, 1311.206, 1311.215, 1311.223, 1311.232,
            1311.241, 1311.255, 1311.273, 1311.296, 1311.326, 1311.361, 1311.402, 1311.443, 1311.485, 1311.525, 1311.562, 1311.593, 1311.622, 1311.649, 1311.672,
            1311.692, 1311.71, 1311.728, 1311.744, 1311.756, 1311.766, 1311.772, 1311.776, 1311.776, 1311.775, 1311.77, 1311.766, 1311.761],
    ];

    var currentX=qualificationLineX[count%4];
    var currentY=qualificationLineY[count%4];
    bestCharacteristicLineOption.xAxis[0].data=currentX;
    bestCharacteristicLineOption.yAxis[0].min=range[count%4][0];
    bestCharacteristicLineOption.yAxis[0].max =range[count%4][1];

    bestCharacteristicLineOption.series[0].data=currentY;
    bestCharacteristicLineOption.series[0].itemStyle.normal.color=colorList[count%colorList.length];

    bestCharacteristicLineOption.title.text='目标:'+target[count%4];
    bestCharacteristicLineOption.title.subtext='特征值:'+features[count%4];
    bestCharacteristicLine.setOption(bestCharacteristicLineOption);



    window.BCLinterval=setInterval(function () {
        count++;
        var currentX=qualificationLineX[count%4];
        var currentY=qualificationLineY[count%4];
        bestCharacteristicLineOption.xAxis[0].data=currentX;

        bestCharacteristicLineOption.yAxis[0].min=range[count%4][0];
        bestCharacteristicLineOption.yAxis[0].max =range[count%4][1];

        bestCharacteristicLineOption.series[0].data=currentY;
        bestCharacteristicLineOption.series[0].itemStyle.normal.color=colorList[count%colorList.length];

        bestCharacteristicLineOption.title.text='目标:'+target[count%4];
        bestCharacteristicLineOption.title.subtext='特征值:'+features[count%4];
        bestCharacteristicLine.setOption(bestCharacteristicLineOption);
    },5000)
    // 使用刚指定的配置项和数据显示图表。
    bestCharacteristicLine.setOption(bestCharacteristicLineOption);




    $("#speedSelect").change(function(){
        var counter = $('#speedSelect').val();
        clearInterval(BCLinterval);
        var myFunction = function(){
            counter = $('#speedSelect').val();
            count++;
            var currentX=qualificationLineX[count%4];
            var currentY=qualificationLineY[count%4];
            bestCharacteristicLineOption.xAxis[0].data=currentX;

            bestCharacteristicLineOption.yAxis[0].min=range[count%4][0];
            bestCharacteristicLineOption.yAxis[0].max =range[count%4][1];

            bestCharacteristicLineOption.series[0].data=currentY;
            bestCharacteristicLineOption.series[0].itemStyle.normal.color=colorList[count%colorList.length];

            bestCharacteristicLineOption.title.text='目标:'+target[count%4];
            bestCharacteristicLineOption.title.subtext='特征值:'+features[count%4];
            bestCharacteristicLine.setOption(bestCharacteristicLineOption);
        }
            window.BCLinterval = setInterval(myFunction, counter);
    });
});
