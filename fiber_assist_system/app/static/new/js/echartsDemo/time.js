setInterval(function () {
    var date = new Date();
    var year = date.getFullYear(); //获取当前年份   
    var mon = date.getMonth() + 1; //获取当前月份   
    var da = date.getDate(); //获取当前日    
    var h = date.getHours(); //获取小时   
    var m = date.getMinutes(); //获取分钟     
    
    var odateNYR = document.querySelector(".dateNYR");
    var numBac1 = document.querySelector(".numBac1");
    var numBac2 = document.querySelector(".numBac2");
    var numBac3 = document.querySelector(".numBac3");
    var numBac4 = document.querySelector(".numBac4");

    odateNYR.innerHTML = year + "/" + mon + "/" + da;

    if(h >= 10) {
        var h2 = h % 10;
        var h1 = (h - h2) / 10;
    }else {
        var h1 = 0;
        var h2 = h;
    }

    if(m >= 10) {
        var m2 = m % 10; 
        var m1 = (m - m2) / 10;
    }else {
        var m1 = 0;
        var m2 = m;
    }

    numBac1.innerHTML = h1;
    numBac2.innerHTML = h2;
    numBac3.innerHTML = m1;
    numBac4.innerHTML = m2;

}, 1000)