/**
 * Created by Zain on 28/1/2018.
 */
function Gragh(){}
Gragh.prototype.generateHtml = function(colors){
    var html = "<p class='graph_result'>"+this.result+"</p>";
    for(var i = 0 ; i < this.title.length ; i++){
        html += '<p class="IntervalValue">'+
                '<span class="intervalMin" style="margin-left:'+ this.iLMin[i]+'px;">'+ this.intervalMin[i]+'</span>'+
                '</p>'+
                '<div class="p_bar">'+
                    '<div class="feature_title">'+ this.title[i]+'</div>'+
                    '<div class="ghostEle">'+
                        '<span class="mini">'+ this.min[i]+'</span>'+
                    '<span class="max">'+ this.max[i]+'</span>'+
                    '<div class="BarContainer">'+
                    '<div class="BarContext" style="width: '+this.width[i]+'px;left:'+this.left[i]+'px;background-color: '+colors[i]+'">'+
                    '</div>'+
                    '</div>'+
                    '</div>'+
                '</div>'+
                '<p class="IntervalValue">'+
                '<span class="intervalMax" style="margin-left: '+ this.iLMax[i]+'px;">'+ this.intervalMax[i]+'</span>'+
                '</p>';
    }
    html = "<div class='graph_deleteBox'>"+html+"</div>";
    return html;
};
function randomColor(colors,n){
    if(n >= colors.length){
        return colors;
    }
    var start = parseInt((colors.length-1)*Math.random());
    var re = [];
    while(n != 0){
        if(start == colors.length){
            start = 0;
        }
        re.push(colors[start]);
        start++;
        n--;
    }
    return re;
}
function createSequence(rule_draw_list){
    var sc = [];
    for(var i = 0 ; i < rule_draw_list.length ; i++){
        var g = new Gragh();
        g.result = '';
        g.title = [];
        g.max = [];
        g.min = [];
        g.width = [];
        g.left = [];
        g.intervalMin = [];
        g.intervalMax = [];
        g.iLMin = [];
        g.iLMax = [];
        for(var j = 1 ; j < rule_draw_list[i].length ; j++){
            g.title.push(rule_draw_list[i][j].title);
            g.max.push(parseFloat(rule_draw_list[i][j].max));
            g.min.push(parseFloat(rule_draw_list[i][j].min));
            g.intervalMax.push(parseFloat(rule_draw_list[i][j].intervalMax));
            g.intervalMin.push(parseFloat(rule_draw_list[i][j].intervalMin));
            g.width.push((456/(g.max[j-1]- g.min[j-1]))*(g.intervalMax[j-1]-g.intervalMin[j-1]));
            g.left.push((456/(g.max[j-1]- g.min[j-1]))*(g.intervalMin[j-1]-g.min[j-1]));
            g.iLMin.push(g.left[j-1]-15);
            g.iLMax.push(g.iLMin[j-1]+g.width[j-1]);
        }
        g.result = rule_draw_list[i][0];
        sc.push(g);
    }
    return sc;
}
$(function(){
    var close_bar = $('.close_bar');
    close_bar.on('click',function(){
        $(this).parent().hide();
    });
});