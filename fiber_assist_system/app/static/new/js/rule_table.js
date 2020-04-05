/**
 * Created by Zain on 19/3/2018.
 */

function outRepeat(a){
    var hash=[],arr=[];
    for (var i = 0; i < a.length; i++) {
        hash[a[i]]!=null;
        if(!hash[a[i]]){
            arr.push(a[i]);
            hash[a[i]]=true;
        }
    }
    return arr;
}
function json_sort(aj,m){
    var arr = [];
    var r = [];
    for(var x in aj){
        arr.push(aj[x][m]);
    }
    arr.sort();
    arr = outRepeat(arr);
    for(var i = 0 ; i < arr.length ; i++){
        for(var j = 0 ; j < aj.length ; j++){
            if(aj[j][m] == arr[i]){
                r.push(aj[j]);
            }
        }
    }
    return r;
}
function createTable(aj,c){
    c.html("");
    var row = document.createElement('tr');
    for(var index in aj[0]){
        if(index != "用户总体评分" && index != 'rulestr'){
            var _td = document.createElement('td');
            var _img = document.createElement('img');
            _img.className = "rank_btn";
            _img.src = "static/new/imgs/rank_btn.png";
            _img.setAttribute('feature',index);
            $(_img).on('click',function(){
                var m = json_sort(table_data,$(this).attr('feature'));
                if(JSON.stringify(m) == JSON.stringify(table_data)){
                    table_data = m.reverse();
                }else{
                    table_data = m;
                }
                createTable(table_data,c);
            });
            if(index == "我的评分"){
                _td.innerHTML = "查看评分";
            }else{
                _td.innerHTML = index;
            }
            _td.appendChild(_img);
            row.appendChild(_td);
        }else if(index == 'rulestr'){
            continue;
        }else{
            var _td = document.createElement('td');
            _td.innerHTML = "条状图";
            row.appendChild(_td);
        }
    }
    c[0].appendChild(row);
    rule_draw_list = [];
    for(var i = 0 ; i < aj.length ; i++){
        var _tr = document.createElement('tr');
        for(var index in aj[i]){
            if(index != "我的评分" && index != "用户总体评分" && index != 'rulestr'){
                var _td = document.createElement('td');
                _td.innerHTML = aj[i][index];
                _tr.appendChild(_td);
            }else if(index == "我的评分"){
                var _td = document.createElement('td');
                var _span = document.createElement('span');
                var _img = document.createElement('img');
                _span.className = "start_num";
                if(aj[i][index]){
                    _span.innerHTML = aj[i][index]+"\ X\ ";
                }else{
                    _span.innerHTML = "0\ X \ ";
                }
                _img.src = 'static/new/imgs/star.png';
                _img.className = "star";
                _img.setAttribute('no',i);
                $(_img).on('click',function(){
                    var n = parseInt($(this).attr('no'));
                    var all_score = parseFloat(table_data[n]["用户总体评分"]);
                    var my_score = parseFloat(table_data[n]["我的评分"]);
                    var whole_score = $('#whole_score');
                    var user_score = $('#user_score');
                    var ScoreContainer = $('.ScoreContainer');
                    if(all_score){
                        whole_score.raty({
                            path: 'static/new/js/img',
                            half:true,
                            readOnly: true,
                            score:all_score
                        })
                    }else{
                        whole_score.raty({
                            path: 'static/new/js/img',
                            half:true,
                            score:0,
                            readOnly: true
                        });
                    }
                    if(my_score){
                        user_score.raty({
                            path: 'static/new/js/img',
                            half:true,
                            readOnly:true,
                            score:my_score
                        })
                    }else{
                        user_score.raty({
                            path: 'static/new/js/img',
                            score:0,
                            half:true,
                            click: function(score,evt) {
                                var _data = {};
                                _data.score = score;
                                _data.rulestr = table_data[n]['rulestr'];
                                for(var j = 0 ; j < _data.rulestr.length ; j++){
                                    _data.rulestr[j] = JSON.stringify(_data.rulestr[j]);
                                }
                                _data.rulestr = _data.rulestr.toString();
                                $.post(score_url,_data,function(data){
                                    if(data.status != 200){
                                        alert(data.status);
                                    }else{
                                        alert("评分提交成功!");
                                        whole_score.raty({
                                            path: 'static/new/js/img',
                                            half:true,
                                            readOnly: true,
                                            score: parseFloat(data.ave_score)
                                        });
                                        user_score.raty({
                                            path: 'static/new/js/img',
                                            score: score,
                                            half:true,
                                            readOnly: true
                                        });
                                        $(this).siblings('.start_num').html(score+"\ X\ ");
                                        table_data[n]["用户总体评分"] = data.ave_score;
                                        table_data[n]["我的评分"] = score;
                                    }
                                })
                            }
                        })
                    }
                    ScoreContainer.show();
                });
                _td.appendChild(_span);
                _td.appendChild(_img);
                _tr.appendChild(_td);
            }else if(index == 'rulestr'){
                rule_draw_list.push(aj[i][index]);
            }else{
                var _td = document.createElement('td');
                var _img = document.createElement('img');
                _img.setAttribute('no',i);
                _img.src = 'static/new/imgs/graph.png';
                _img.className = 'graph_btn';
                $(_img).on('click',function(){
                    var n = $(this).attr('no');
                    var BarGraph = $('.BarGraph');
                    var colors = ['#f55066','#cf8878','#b7d28d','#ff9b6a','#d9b8f1','#b8f1ed','#e1622f','#ed9678','#ed9678','#ff8240','#aa5b71'];
                    var _colors = randomColor(colors,gs[n].title.length);
                    var _html = gs[n].generateHtml(_colors);
                    BarGraph.find('.graph_deleteBox').remove();
                    BarGraph.append(_html);
                    BarGraph.css({'left':($(window).width()-900)/2,'top':"23%"});
                    BarGraph.show();
                });
                _td.appendChild(_img);
                _tr.appendChild(_td);
            }
        }
        c[0].appendChild(_tr);
    }
    gs = createSequence(rule_draw_list);
}
$(function(){
   var table_container = $('.rules_table');
   table_data = json_sort(table_data,Object.keys(table_data[0])[0]);
   createTable(table_data,table_container);
   console.log(table_data);
});