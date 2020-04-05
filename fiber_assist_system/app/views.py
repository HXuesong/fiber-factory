import pandas as pd
import simplejson as simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from sklearn.tree import DecisionTreeRegressor

from app.models import *
from app.forms import *
from django.contrib.auth import authenticate, login, logout
import app.hive_mysql.hive_api as hive_app
import app.hive_mysql.mysql_api as mysql_app
import app.hive_mysql.AzkabanMonitor as AzkabanMonitor
import platform

from PIL import Image
import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


import app.decisionpy.analyse_fibers as fs
import  app.decisionpy.hdfsClient as hdfs

hdfs_conf = {
    'server_url': 'http://172.23.27.203:50070',
    'cache_days': 1,
    'user': 'dm'
}
dbConf = {'host': '172.23.27.203', 'port': 3306, 'charset': 'utf8',
          'user': 'root', 'passwd': '123456', 'db': 'azkaban'}
base = 'https://172.23.27.203:8443'
# Create your views here.

click_refresh = False




#=============== 用户管理 =============#

#注册
@csrf_exempt
def do_register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")
            filterResult = User.objects.filter(username=username)
            if len(filterResult) > 0:
                return render(request, 'login_register/Register.html', {'reason': '用户已存在'})
            usertype = request.POST.get("usertype")
            user = User.objects.create(username=username,
                                       is_active=True,
                                       password=make_password(password),
                                       is_reset ='否')
            # is_active=False)
            user.save()
            user_id = user.id
            print(11111)
            if usertype == '团队创建者':  # 团队创建者
                team_temp = Team_temp.objects.create(teamname=request.POST.get('teamname'),user_id=user.id, is_pass='待审核')
                team_temp.save()
                # team = Team.objects.create(teamname=request.POST.get('teamname'))
                # team.save()
                # team_id = team.id
                # team_user = Team_User.objects.create(team_id=team_id, user_id=user_id, ut_type='团队创建者')
                # team_user.save()
                return redirect('/login')
            elif usertype == '普通成员':
                team_name = request.POST.get("teamname")
                team_id = Team.objects.filter(teamname = team_name)[0].id
                print(team_id)
                teamer = Teamer_temp.objects.create(team_id=team_id, user_id=user_id, is_pass='待审核')
                teamer.save()
                return redirect('/login')
        else:
            teamlist = Team.objects.all()
    except Exception as e:
        print(e)

    return render(request, 'login_register/Register.html', locals())

#注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    return redirect('/login')


#添加用户登录日志
@login_required
def add_user_login_log(request,user_id,system):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        login_ip = x_forwarded_for.split(',')[-1].strip()
    else:
        login_ip = request.META.get('REMOTE_ADDR')
    user_log = User_login_log.objects.create(login_ip=login_ip,user_id=user_id,login_system =system)
    user_log.save()

#登录
@csrf_exempt
def do_login(request):
    try:
        logout(request)
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            system = request.POST.get('system')

            user = authenticate(username=username, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                add_user_login_log(request,user.id,system)
                if user.is_superuser:
                    request.session['usertype'] = "超级管理员"

                else:
                    if(Team_User.objects.filter(user_id=user.id)):
                        team = Team_User.objects.filter(user_id=user.id)[0]
                        ut_type = team.ut_type
                        request.session['usertype'] = ut_type
                        request.session['team_id'] = team.team.id
                        request.session['team_name'] = team.team.teamname
                    else:
                        request.session['usertype'] = "正在审核中"
                return redirect("/userinfo")

            else:
                return render(request, 'login_register/Login.html', {'reason': '用户名密码或者错误'})
    except Exception as e:
        print(e)
    return render(request, 'login_register/Login.html', locals())


# #修改密码
# @login_required
# @csrf_exempt
# def change_psw(request):
#     try:
#         user = request.user
#         team_user_list = Team_User.objects.filter(user_id=user.id)
#
#     except Exception as e:
#         print(e)
#     return render(request,'user_info/user_info.html',locals())

#用户信息页面
@login_required
@csrf_exempt
def user_info(request):
    try:
        ana_menu =Analysis_manage.objects.filter(is_show=True)
        user = request.user
        team_user_list = Team_User.objects.filter(user_id=user.id)
        if request.method =="POST":
            username = request.user.username
            newpsw1 = request.POST.get("newpsw1")
            newpsw2 = request.POST.get("newpsw2")
            oldpsw = request.POST.get("oldpsw")
            if newpsw1!=newpsw2:
                error_tip = 1
                return render(request, 'user_info/user_info.html', locals())
            else:
                user = authenticate(username=username, password=oldpsw)
                if user is not None:
                    user.set_password(newpsw1)
                    user.save()
                    return redirect('/login')
                else:
                    error_tip = 2
                    return render(request, 'user_info/user_info.html', locals())
    except Exception as e:
        print(e)
    return render(request, 'user_info/user_info.html',locals())


#用户登录信息页面
@login_required
def user_login_info(request):
    try:
        ana_menu = Analysis_manage.objects.filter(is_show=True)
        user = request.user
        # team = Team_User.objects.filter(user_id=user.id)[0]
        if len(User_login_log.objects.filter(user_id=user.id)) > 1:
            user_log_last = User_login_log.objects.filter(user_id=user.id)[1]
            user_log_latest = User_login_log.objects.filter(user_id=user.id)[0]
        else:
            user_log_last = User_login_log.objects.filter(user_id=user.id)[0]
            user_log_latest = user_log_last
    except Exception as e:
        print(e)

    return render(request,'user_info/user_login_info.html',locals())

#切换团队跳转
@login_required
def info_page_redirect(request):
    try:

        user= request.user
        team_id = request.GET.get('teamid')
        if team_id ==None:
            team_id = Team_User.objects.filter(user_id=user.id)[0].team_id
        team = Team_User.objects.filter(user_id=user.id,team_id=team_id)[0]
        ut_type = team.ut_type
        print(ut_type)
        request.session['usertype'] = ut_type
        request.session['team_id'] = team.team_id
        request.session['team_name'] = team.team.teamname
        return redirect('/userinfo')
    except Exception as e:
        print(e)
    return redirect('/userinfo')


#分析页面
@login_required
@csrf_exempt
def decision(request):
    if request.method =="GET":
        ana_menu = Analysis_manage.objects.filter(is_show=True)
        target_label =request.GET.get('target_label',"ECC")
        print(target_label)
        tag_name = 1
        oldStep = ""
        tree_data = ""
    return render(request,'decision/decisionPage.html',locals())


# 分页代码
@login_required
def getPage(request, list,n):
    paginator = Paginator(list, n)
    try:
        page = int(request.GET.get('page', 1))
        list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        list = paginator.page(1)
    return list


def decision_manege(request):
    if request.method =="GET":
        decison_id =  request.GET.get("id",None)
        action = request.GET.get("action",None)
        if action and decison_id:
            if action == "show":
                Analysis_manage.objects.filter(ana_id=decison_id).update(is_show=True)
            elif action == "not_show":
                Analysis_manage.objects.filter(ana_id=decison_id).update(is_show=False)
        ana_menu = Analysis_manage.objects.filter(is_show=True)
        for i in ana_menu:
            print(i)
        not_show_menu = Analysis_manage.objects.filter(is_show=False)

    return render(request, "decision/decison_manage.html", locals())

@csrf_exempt
@login_required
def decision_analy(request):
    feas_data = {}
    tag_name = 1
    oldStep = ""
    target_label = "ECC"
    if request.method == "POST":

        target_label = request.POST.get('target_label')
        tag_name = request.POST.get('tag_name').replace(" ", "").strip()
        if tag_name == '表格':
            tag_name = 1
        elif tag_name == "树状图":
            tag_name = 2
        elif tag_name == "影响因子分析":
            tag_name = 3
        else:
            tag_name = 1
        step_name = request.POST.get('step_name')
        ori_choose_name = request.POST.get('choose_name')
        choose_name_list = ori_choose_name.replace(' ', '')[0:-1].split(",")
        oldStep = []
        oldStep.append(step_name)
        oldStep.append(choose_name_list)
        ori_choose_feas = request.POST.get('choose_feas')
        choose_feas_list = ori_choose_feas.replace(' ', '')[0:-1].split(",")
        choose_feas = ori_choose_feas.replace(",", ";")[0:-1]
        choose_name = ori_choose_name.replace(",", ";")[0:-1]
        values_list = []
        #
        # equip_list = fs.get_step_chooseName(step_name).split(";")
        equip_list = ['E', 'G', 'H', 'D', 'F', 'C']
        # print(equip_list)
        # print(";".join(choose_name_list))
        fea_list = fs.chooseFeature(str(target_label), str(step_name), str(";".join(choose_name_list)))
        print("target_label：" + target_label)
        print("step_name："+step_name)
        print("choose_name："+";".join(choose_name_list))
        print(fea_list)
        print("=================================")

        feas_data = fs.get_feature_min_max(choose_feas)
        print(".............................................")
        print(feas_data)
        for k in feas_data:
            print(k)
            print(feas_data[k])
        print(".............................................")

        rule_data = fs.find_rule(step_name, choose_name, target_label, choose_feas)
        print("=================================")

        table_data =[]
        for i in rule_data:
            rule_score = Rule_score.objects.filter(rulestrs=str(i))
            # print(i)
            # print(type(i))
            rs={}
            temp = []
            for key in i:
                item_draw = {}
                if key != target_label:
                    item_draw['title'] = key
                    rule_m_m = feas_data[key].split(",")
                    item_draw['min'] = rule_m_m[0]
                    item_draw['max'] = rule_m_m[1]
                    rule_sope = i[key][1:-1].split(",")
                    item_draw['intervalMin'] = rule_sope[0]
                    item_draw['intervalMax'] = rule_sope[1]
                    temp.append(item_draw)

                else:
                    temp_str = key + ":" + i[key]
                    temp.append(temp_str)

            rs['rulestr'] = temp
            if rule_score:
                print(str(i))
                print(rule_score[0].score)
                rs['用户总体评分'] = rule_score[0].score
                user_score = Rule_user.objects.filter(rule_id=rule_score[0].id, user_id=request.user.id)
                if user_score:
                    rs['我的评分'] = user_score[0].myscore
                else:
                    rs['我的评分'] = ''
            else:
                # Rule_score.objects.create(rulestrs=str(i), score=0.0)
                rs['用户总体评分'] = ''
                rs['我的评分'] = ''
            rs = dict(i, **rs)
            table_data.append(rs)
        print(table_data)

        print("=================================")
        new_rule_data = []
        rule_draw = []
        print(target_label)
        for i in rule_data:
            temp = []
            for key in i:
                item_draw = {}
                if key != target_label:
                    item_draw['title'] = key
                    rule_m_m = feas_data[key].split(",")
                    item_draw['min'] = rule_m_m[0]
                    item_draw['max'] = rule_m_m[1]
                    rule_sope = i[key][1:-1].split(",")
                    item_draw['intervalMin'] = rule_sope[0]
                    item_draw['intervalMax'] = rule_sope[1]
                    temp.append(item_draw)

                else:
                    temp_str =key+":"+ i[key]
                    temp.append(temp_str)

            rule_draw.append(temp)

            # for k in feas_data:
            #     print(k)
            #     item_draw['title']= k
            #     rule_m_m =feas_data[k].split(",")
            #     item_draw['min'] = rule_m_m[0]
            #     item_draw['max'] = rule_m_m[1]
            #     rule_sope = i[k][1:-1].split(",")
            #     item_draw['intervalMin'] = rule_sope[0]
            #     item_draw['intervalMax'] = rule_sope[1]
            rule_score = Rule_score.objects.filter(rulestrs=str(i))
            i['rulestr']=str(i)
            if rule_score:
                print(str(i))
                print(rule_score[0].score)
                i['用户总体评分'] = rule_score[0].score
                user_score = Rule_user.objects.filter(rule_id = rule_score[0].id,user_id = request.user.id)
                if user_score:
                    i['我的评分'] = user_score[0].myscore
                else:
                    i['我的评分'] = ''
            else:
                # Rule_score.objects.create(rulestrs=str(i), score=0.0)
                i['用户总体评分'] = ''
                i['我的评分'] = ''

            new_rule_data.append(i)
        rule_draw_list = json.dumps(rule_draw,ensure_ascii=False)
        print(rule_draw_list)
        print('----------------------------------')
        print('----------------------------------')
        keys_list = new_rule_data[0].keys()
        for item in new_rule_data:
            values = []
            for key in keys_list:
                v = item[key]
                values.append(v)
            values_list.append(values)

        sub_tree = fs.mytree(step_name, choose_name, target_label, choose_feas)
        sub_tree.Start()
        tree_rule = sub_tree.lrRule
        print(tree_rule)
        tree_data = json.loads(sub_tree.ToJson())['json']
        print(tree_data)
        tree_data = json.dumps(tree_data)
        tree_path =sub_tree.ToPath()
        tree_path = json.loads(sub_tree.ToPath())['json']
        tree_path = json.dumps(tree_path)
        values_list = getPage(request, values_list, 10)
        ana_menu = Analysis_manage.objects.filter(is_show=True)
    return render(request,"decision/decisionPage.html",locals())

@csrf_exempt
def mark_score(request):
    res={}
    if request.method == "POST":
        print(request.POST)
        rulestr = request.POST.get("rulestr")
        print(rulestr)

        user_id = request.user.id
        score = float(request.POST.get("score"))
        print(score)
        rule_score = Rule_score.objects.filter(rulestrs=rulestr)
        if rule_score:
            all_score = rule_score[0].score+score
            user_num = rule_score[0].user_num
            rule_score.update(score=all_score, user_num=int(user_num)+1)
            Rule_user.objects.create(myscore=score, rule_id=rule_score[0].id, user_id=user_id)
        else:
            rule_score = Rule_score.objects.create(rulestrs=rulestr, score=score, user_num=1)
            Rule_user.objects.create(myscore = score,rule_id=rule_score.id,user_id=user_id)
        rule_score = Rule_score.objects.filter(rulestrs=rulestr)[0]
        ave_score = rule_score.score/int(rule_score.user_num)*1.0
        res = {"status": 200}
        res['ave_score']=ave_score
        print(res)
    return HttpResponse(json.dumps(res), content_type="application/json")

@csrf_exempt
def analy_breakpoint(request):
    data_list = {}
    if request.method == "POST":
        step_name = request.POST.get('stage_name')
        equip_name = request.POST.getlist('equip_lists[]')[0:-1]
        equip_name = ";".join(equip_name)
        print(step_name)
        print(equip_name)
        bkdata = fs.get_breakpointrate_stepAndsys(step_name,equip_name)
        data_list = {"status": 200}
        data_list['data'] = bkdata
    return HttpResponse(json.dumps(data_list), content_type="application/json")



#获取特征
@csrf_exempt
@login_required
def analy_get_feas(request):
    data_list = {}
    if request.method == "POST":
        target_label = request.POST.get('label')
        print(target_label)
        step_name = request.POST.get('step_name')
        print(request.POST)
        equip_name = request.POST.getlist('equip_list[]')
        print(equip_name)
        data = fs.chooseFeature(str(target_label), str(step_name), str(";".join(equip_name)))
        data_list ={"status":200}
        fea_list = []
        for i in data:
            fea_list.append(i)
        data_list['features'] = fea_list
    return HttpResponse(json.dumps(data_list),content_type="application/json")

@csrf_exempt
@login_required
def mdf_pic(request):
    data_list = {}
    if request.method=="POST":
        print(request.POST)
        step_name = request.POST.get("stage_name")
        equip_lists = request.POST.getlist("equip_lists[]")
        equip_lists = ";".join(i for i in equip_lists)
        target_label = request.POST.get("target_label")
        target_feature = request.POST.get("target_feature")

        static_feature = request.POST.get("static_feature")
        print(static_feature)
        fea = json.loads(static_feature)
        static_fea_dist = {}
        for k in fea:
            static_fea_dist[k] = ",".join([i for i in fea[k]])
        draw_data = fs.getTrend_newmodel(step_name,equip_lists,target_label,target_feature,static_fea_dist)
        print(draw_data)
        print("===================")
        x = [float("{0:.3f}".format(i)) for i in draw_data[0]]
        y = [float("{0:.3f}".format(i)) for i in draw_data[1]]

        y1 = [float("{0:.3f}".format(i)) for i in draw_data[2]]
        ry = [float("{0:.3f}".format(i)) for i in draw_data[3]]
        rz = [float("{0:.3f}".format(i)) for i in draw_data[4]]
        form = draw_data[5]
        min_y = float("{0:.3f}".format(min(y)*0.8))
        max_y = float("{0:.3f}".format(max(y)*1.2))
        min_ry = min(ry)
        max_ry = max(ry)
        data_list = {"status": 200,'X':x,'Y':y,'Z':y1,"RY":ry,"RZ":rz,'min_y':min_y,'max_y':max_y,'min_ry':min_ry, "max_ry":max_ry,'X_NAME':target_label,'form':form}

        print(data_list)
    return HttpResponse(json.dumps(data_list),content_type="application/json")




def breakpoint_page(request):
    ana_menu = Analysis_manage.objects.filter(is_show=True)
    return render(request,'decision/breakpoint.html',locals())


#获得重置密码列表
@login_required
def admin_get_reset_psw(request):
    try:
        ana_menu = Analysis_manage.objects.filter(is_show=True)
        reset_user_list = User.objects.exclude(is_reset='否')
        reset_user_list = getPage(request, reset_user_list, 5)
    except Exception as e:
        pass
    return render(request, 'admin/admin_password_reset_audit.html',locals())

@login_required
def admin_sys_logs(request):
    try:
        ana_menu = Analysis_manage.objects.filter(is_show=True)
        hive_logs = hive_app.hive_fetchExecutionJobLogs()
        hive_log = []
        for log in hive_logs:
            log = log['data'].split('\n')
            log.reverse()
            hive_log += log
            hive_log +=['============================================']
        # print(hive_log)
        mysql_logs = mysql_app.mysql_fetchExecutionJobLogs()
        mysql_logs = mysql_logs['data'].split('\n')
        mysql_logs.reverse()
    except Exception as e:
        print(e)
    return render(request, 'admin/admin_sys_manage.html', locals())


@login_required
@csrf_exempt
def get_mysql_logs(request):
    try:

        mysql_logs = mysql_app.mysql_fetchExecutionJobLogs()
        mysql_logs = mysql_logs['data'].split('\n')
        mysql_logs.reverse()
        mysql_log = {"status": 200, "data": mysql_logs}
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(mysql_log),content_type="application/json")

@login_required
@csrf_exempt
def get_hive_logs(request):
    try:
        hive_logs = hive_app.hive_fetchExecutionJobLogs()[1:]
        hive_log = []
        for log in hive_logs:
            log = log['data'].split('\n')
            log.reverse()
            hive_log += log
            hive_log += ['============================================']
        hive_log = {"status": 200,"data": hive_log}
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(hive_log), content_type="application/json")


@login_required
def data_manage(request):
    global click_refresh
    monitor = AzkabanMonitor.AzkabanMonitor(base, 'azkaban', 'azkaban', dbConf, 'INFO', 'file')
    flag = monitor.restartProject(is_first=False)
    if click_refresh and flag:
        info = hdfs.HdfsClient(conf=hdfs_conf)
        info.refresh_info()
        click_refresh = False

    info = hdfs.HdfsClient(conf=hdfs_conf)
    info_table = info.general_info(info.loc_conf['general_info_local_path'], info.loc_conf['general_info_remote_path'])
    final_table_info = info.get_final_table_info()
    print(type(final_table_info))
    f_table_name = []
    f_table = []
    for k,v in final_table_info.items():
        f_table_name.append(k)
        f_table.append(v)
    tabel_values = []
    table_name=[]
    for name in info_table.columns:
        table_name.append(name)
    for values in info_table.values:
        tabel_values.append(values)
    tabel_values = getPage(request,tabel_values,20)
    ana_menu = Analysis_manage.objects.filter(is_show=True)
    return render(request, 'admin/admin_data_manage.html', locals())


@login_required
def refresh_data_manage(request):
    global click_refresh
    click_refresh = True
    monitor = AzkabanMonitor.AzkabanMonitor(base, 'azkaban', 'azkaban', dbConf, 'INFO', 'file')
    monitor.restartProject(is_first=True)
    flag = False
    info = hdfs.HdfsClient(conf=hdfs_conf)
    info_table = info.general_info(info.loc_conf['general_info_local_path'], info.loc_conf['general_info_remote_path'])
    final_table_info = info.get_final_table_info()
    f_table_name = []
    f_table = []
    for k, v in final_table_info.items():
        f_table_name.append(k)
        f_table.append(v)
    tabel_values = []
    table_name = []
    for name in info_table.columns:
        table_name.append(name)
    for values in info_table.values:
        tabel_values.append(values)
    tabel_values = getPage(request, tabel_values, 20)
    ana_menu = Analysis_manage.objects.filter(is_show=True)
    return render(request, 'admin/admin_data_manage.html', locals())


#获取团队审核列表
@login_required
def admin_team_manage(request):
    try:
        team_temp_list = Team_temp.objects.all()
        team_temp_list = getPage(request,team_temp_list,10)
        ana_menu = Analysis_manage.objects.filter(is_show=True)
    except Exception as e:
        print(e)
    return render(request, 'admin/admin_team_manage_audit.html',locals())


#审核团队
@login_required
def admin_check_team(request):
    try:

        flag = request.GET.get("flag")
        user_id = request.GET.get('userid')
        team_name = request.GET.get('teamname')
        if flag == 'y':#通过
            Team_temp.objects.filter(user_id=user_id,teamname=team_name).update(is_pass ='是')
            team = Team.objects.create(teamname=team_name)
            team.save()
            team_id = team.id
            team_user = Team_User.objects.create(team_id=team_id, user_id=user_id, ut_type='团队创建者')
            team_user.save()
        elif flag == 'n':
            Team_temp.objects.filter(user_id=user_id, teamname=team_name).update(is_pass='否')
    except Exception as e:
        print(e)
    return redirect('/adminteammanage/')


#获取团队列表
@login_required
def admin_team_list(request):
    team_temp = Team_temp.objects.all()
    team_temp_list = getPage(request, team_temp, 10)
    ana_menu = Analysis_manage.objects.filter(is_show=True)
    return render(request,'admin/admin_team_manage_list.html',locals())


@login_required
def sys_message(request):
    team_temp = Team_temp.objects.all()
    team_temp_list = getPage(request,team_temp,10)
    ana_menu = Analysis_manage.objects.filter(is_show=True)
    return render(request,'admin/admin_message.html',locals())

@login_required
def founder_get_join_list(request):
    team_id = request.session['team_id']
    team_name = request.session['team_name']
    print(team_name)
    print(team_id)
    team_user_list = Teamer_temp.objects.filter(team_id=team_id)
    for i in team_user_list:
        print(i.is_pass)
    team_user_list = getPage(request,team_user_list,10)
    ana_menu = Analysis_manage.objects.filter(is_show=True)
    return render(request,'founder/founder_manage_audit.html',locals())


@login_required
def founder_get_manager_list(request):
    try:
        user = request.user
        user_id = user.id
        # team = Team_User.objects.filter(user_id = user_id)[0]
        team_id = request.session.get("team_id")
        teamerlist = Teamer_temp.objects.filter(team_id=team_id)
        teamuserlist = Team_User.objects.filter(team_id=team_id)
        teamadminlist = Team_User.objects.filter(team_id=team_id).filter(ut_type='团队管理员')
        teamadminlist = getPage(request, teamadminlist, 10)
        ana_menu = Analysis_manage.objects.filter(is_show=True)
    except Exception as e:
        print(e)
    return render(request, 'founder/founder_manage_admin.html', locals())


@login_required
def founder_get_team_user_list(request):
    try:
        user = request.user
        user_id = user.id
        team_id = request.session.get("team_id")
        teamuserlist = Team_User.objects.filter(team_id=team_id)
        memberlist = []
        for teamuser in teamuserlist:
            tmp_dic = {}

            if len(User_login_log.objects.filter(user_id=teamuser.user_id)) > 0:
                user_log_last = User_login_log.objects.filter(user_id=teamuser.user_id)[0]
                tmp_dic['login_date'] = user_log_last.login_date
                tmp_dic['login_ip'] = user_log_last.login_ip
                tmp_dic['login_system'] = user_log_last.login_system
            else:
                tmp_dic['login_date'] = ""
                tmp_dic['login_ip'] = ""
                tmp_dic['login_system'] = ""

            tmp_dic['user_id'] = teamuser.user_id
            tmp_dic['user_name'] = teamuser.user.username
            tmp_dic['user_type'] = teamuser.ut_type
            tmp_dic['team_name'] = teamuser.team.teamname
            memberlist.append(tmp_dic)
        memberlist = getPage(request, memberlist,10)
        ana_menu = Analysis_manage.objects.filter(is_show=True)
    except Exception as e:
        print(e)
    return render(request, 'founder/founder_manage_all_user.html', locals())

@login_required
def founder_check_join(request):
    try:
        teamer_id = request.GET.get('userid')
        pass_flag = request.GET.get('flag')
        team_id = request.GET.get('teamid')

        if pass_flag == 'y':
            Teamer_temp.objects.filter(user_id=teamer_id).update(is_pass='是')
            team_user = Team_User.objects.create(team_id =team_id,user_id = teamer_id,ut_type='成员')
            team_user.save()
        elif pass_flag == 'n':
            Teamer_temp.objects.filter(user_id=teamer_id).update(is_pass='否')
    except Exception as e:
        print(e)
    return redirect('/foundergetjoinlist')

@login_required
def founder_change_user_type(request):
    try:

        flag = request.GET.get('flag')

        team_id = request.GET.get('teamid')
        user_id = request.GET.get('userid')
        if flag == 'gly':
            Team_User.objects.filter(team_id =team_id,user_id = user_id).update(ut_type='团队管理员')
        elif flag == 'cy':
            Team_User.objects.filter(team_id=team_id, user_id=user_id).update(ut_type='成员')
    except Exception as e:
        print(e)
    return redirect('/foundergetteamuserlist')


@login_required
def user_get_manager_list(request):
    try:
        ana_menu = Analysis_manage.objects.filter(is_show=True)
        user = request.user
        user_id = user.id
        # user_id = 2
        team_id = request.session.get("team_id")
        teamerlist = Teamer_temp.objects.filter(team_id=team_id)
        teamuserlist = Team_User.objects.filter(team_id=team_id)
        teamadminlist = Team_User.objects.filter(team_id=team_id).filter(ut_type='团队管理员')
        teamadminlist = getPage(request,teamadminlist,10)
    except Exception as e:
        print(e)
    return render(request, 'user/user_manage_admin.html', locals())


@login_required
def user_get_team_user_list(request):
    try:
        ana_menu = Analysis_manage.objects.filter(is_show=True)
        user = request.user
        user_id = user.id
        team_id = request.session.get("team_id")
        teamuserlist = Team_User.objects.filter(team_id=team_id)
        memberlist = []
        for teamuser in teamuserlist:
            tmp_dic = {}

            if len(User_login_log.objects.filter(user_id=teamuser.user_id)) > 0:
                user_log_last = User_login_log.objects.filter(user_id=teamuser.user_id)[0]
                tmp_dic['login_date'] = user_log_last.login_date
                tmp_dic['login_ip'] = user_log_last.login_ip
                tmp_dic['login_system'] = user_log_last.login_system
            else:
                tmp_dic['login_date'] = ""
                tmp_dic['login_ip'] = ""
                tmp_dic['login_system'] = ""

            tmp_dic['user_id'] = teamuser.user_id
            tmp_dic['user_name'] = teamuser.user.username
            tmp_dic['user_type'] = teamuser.ut_type
            tmp_dic['team_name'] = teamuser.team.teamname
            memberlist.append(tmp_dic)
        memberlist = getPage(request, memberlist,10)
    except Exception as e:
        print(e)
    return render(request, 'user/user_manage_all_user.html', locals())


def screen_dis(request):
    f = open(r"decision_name.txt")
    name_list = f.read().split(",")
    # for name in name_list:
    #     Analysis_manage.objects.create(ana_id=name, ana_name=str(name + "分析"), is_show=False)
    print("down!")
    return render(request, 'screen_display/screen_dispaly.html')


# def login_redirect(request):
#     try:
#         print(111)
#         # user_id = request.GET.get('userid')
#         # team_id = request.GET.get('teamid')
#         # ut_type = Team_User.objects.filter(user_id=user_id,team_id=team_id)[0].ut_type
#         # print(team_id)
#         # if ut_type =='团队创建者':
#         #     return render(request,'new/teamCreater/founder_info.html',locals())
#         pass
#     except Exception as e:
#         print(e)
#     return render(request,'new/manager_user/user_message.html',locals())


# #上传头像
# @login_required
# def uploadImg(request):
#     username = request.GET.get('username')
#     if request.method == 'POST':
#         # new_img = IMG(
#         #     img=request.FILES.get('img'),
#         #     name=request.FILES.get('img').name
#         # )
#         # new_img.save()
#         # return redirect('/showimg')
#         img = request.FILES.get('img')
#         if img != None:
#             User.objects.filter(username=username).update(photo=img)
#             i = Image.open(img)
#             i.save(BASE_DIR+'/media/'+img.name)
#             return redirect('/userinfo')
#     return render(request, 'upload.html',locals())
#
# @csrf_exempt
# def showImg(request):
#     imgs = IMG.objects.all()
#     content = {
#         'imgs':imgs,
#     }
#     for i in imgs:
#         print(i.img.url)
#     return render(request, 'showimg.html', locals())




# @login_required
# def change_psw(request):
#     try:
#         username = request.GET.get('username')
#         oldpassword = request.GET.get('oldpassword')
#         newpassword = request.GET.get('newpassword')
#         user = authenticate(username=username, password=oldpassword)
#         if user is not None:
#            User.objects.filter(username=username, password=oldpassword).update(password = make_password(newpassword))
#         else:
#             return render({"msg":'旧密码错误'})
#     except Exception as e:
#         print(e)
#     return render({"msg": '旧密码错误'})

# def login_page(request):
#     return render(request, 'login.html')
#
# def login_verify(request):
#     print(111111)
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         system = request.POST.get('system')
#         print(111111)
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
#                 login(request, user)
#                 add_user_login_log(request, user.id)
#                 return HttpResponse('1')
#             else:
#                 return HttpResponse('-1')
#         else:
#             return HttpResponse('0')



# #登录
# @csrf_exempt
# def do_login(request):
#     try:
#         logout(request)
#         # ip = getip(request)
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             system = request.POST.get('system')
#
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
#                 login(request, user)
#                 add_user_login_log(request,user.id,system)
#                 if user.is_superuser:
#                     return redirect('/admininfo')
#                 else:
#                     team = Team_User.objects.filter(user_id=user.id)[0]
#                     ut_type = team.ut_type
#                     print(ut_type)
#                     if ut_type == '成员':
#                         print()
#                         return redirect('/userinfo?teamid=' + str(team.team_id))
#                     elif ut_type == '团队创建者':
#                         print(11111)
#                         return redirect('/createrinfo?teamid=' + str(team.team_id))
#                     elif ut_type == '团队管理员':
#                         pass
#             else:
#                 return render(request, './login_register/Login.html', {'reason': '用户名密码或者错误'})
#     except Exception as e:
#         print(e)
#
#     return render(request, './login_register/Login.html', locals())
#
# def info_page_redirect(request):
#     try:
#         user= request.user
#         team_id = request.GET.get('teamid')
#         if team_id ==None:
#             team_id = Team_User.objects.filter(user_id=user.id)[0].team_id
#         team = Team_User.objects.filter(user_id=user.id,team_id=team_id)[0]
#         ut_type = team.ut_type
#         print(ut_type)
#         if ut_type == '成员':
#             return redirect('/userinfo?teamid=' + str(team_id))
#         elif ut_type == '团队创建者':
#             # return render(request,'new/teamCreater/founder_info.html',locals())
#             return redirect('/createrinfo?teamid=' + str(team.team_id))
#         elif ut_type == '团队管理员':
#             pass
#     except Exception as e:
#         print(e)
#     return
#
#
#
# #=============== 团队管理 =============#
#
# #用户信息页面
# @login_required
# @csrf_exempt
# def userinfo(request):
#     try:
#         user = request.user
#         team = Team_User.objects.filter(user_id=user.id)[0]
#         if len(User_login_log.objects.filter(user_id=user.id)) > 1:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[1]
#             user_log_latest = User_login_log.objects.filter(user_id=user.id)[0]
#         else:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[0]
#             user_log_latest = user_log_last
#         #修改密码
#         if request.method == 'POST':
#             username = request.user.username
#             oldpsw = request.POST.get('oldpassword')
#             newpsw1 = request.POST.get('newpassword1')
#             newpsw2 = request.POST.get('newpassword2')
#             if newpsw1 != newpsw2:
#                 reason = '密码不一致'
#                 return render(request, 'new/userinfo.html', locals())
#             user = authenticate(username=username, password=oldpsw)
#             if user is not None:
#                 user.set_password(newpsw1)
#                 user.save()
#                 return redirect('/login')
#             else:
#                 reason = '用户名不存在或原始密码错误'
#                 return render(request, 'new/userinfo.html', locals())
#     except Exception as e:
#         print(e)
#     return render(request,'./new/userinfo.html',locals())
#
# #获取审核用户列表
# @login_required
# def check_user(request):
#     try:
#         user = request.user
#         team = Team_User.objects.filter(user_id = user.id)[0]
#         teamerlist = Teamer_temp.objects.filter(team_id=team.team_id)
#
#     except Exception as e:
#         print(e)
#     print(locals())
#     return render(request, 'team_check_user.html', locals())
#
# #审核普通用户是否通过
# @login_required
# def teamer_is_pass(request):
#     try:
#         teamer_id = request.GET.get('userid')
#         pass_flag = request.GET.get('flag')
#         team_id = request.GET.get('teamid')
#
#         if pass_flag == '1':
#             Teamer_temp.objects.filter(user_id=teamer_id).update(is_pass='是')
#             team_user = Team_User.objects.create(team_id =team_id,user_id = teamer_id,ut_type='成员')
#             team_user.save()
#         elif pass_flag == '0':
#             Teamer_temp.objects.filter(user_id=teamer_id).update(is_pass='否')
#         user = request.user
#         team = Team_User.objects.filter(user_id = user.id)[0]
#         teamerlist = Teamer_temp.objects.filter(team_id=team.team_id)
#     except Exception as e:
#         print(e)
#     return render(request, 'team_check_user.html', locals())
#
# #获取团队管理员
# @login_required
# def team_manager(request):
#     try:
#         user = request.user
#         team = Team_User.objects.filter(user_id = user.id)[0]
#         teamerlist = Teamer_temp.objects.filter(team_id=team.team_id)
#         teamuserlist = Team_User.objects.filter(team_id=team.team_id)
#         teamadminlist = Team_User.objects.filter(team_id=team.team_id).filter(ut_type='团队管理员')
#         if len(User_login_log.objects.filter(user_id=user.id))>0:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[0]
#         else:
#             user_log_last = None
#     except Exception as e:
#         print(e)
#     return render(request, 'team_manager.html', locals())
#
# #获取团队成员
# @login_required
# def team_member(request):
#     try:
#         user = request.user
#         team = Team_User.objects.filter(user_id = user.id)[0]
#         teamuserlist = Team_User.objects.filter(team_id=team.team_id)
#         memberlist = []
#         for teamuser in teamuserlist:
#             tmp_dic = {}
#
#             if len(User_login_log.objects.filter(user_id=teamuser.user_id)) > 0:
#                 user_log_last = User_login_log.objects.filter(user_id=teamuser.user_id)[0]
#                 tmp_dic['login_date'] = user_log_last.login_date
#                 tmp_dic['login_ip'] = user_log_last.login_ip
#                 tmp_dic['login_system'] = user_log_last.login_system
#             else:
#                 tmp_dic['login_date'] = ""
#                 tmp_dic['login_ip'] = ""
#                 tmp_dic['login_system'] =""
#
#             tmp_dic['user_id'] = teamuser.user_id
#             tmp_dic['user_name'] = teamuser.user.username
#             tmp_dic['user_type'] = teamuser.ut_type
#             tmp_dic['team_name'] = teamuser.team.teamname
#
#             memberlist.append(tmp_dic)
#     except Exception as e:
#         print(e)
#     # print(memberlist)
#     return render(request, 'team_member.html', locals())
#
# #团队管理员->普通成员/普通成员->团队管理员
# @login_required
# def change_teamuser_type(request):
#     try:
#         user_name = request.GET.get('username')
#         user_id = User.objects.filter(username=user_name)[0]
#         team_id = request.GET.get('teamid')
#         flag = request.GET.get('operate')
#         if flag == 'set':
#             updata_type = '团队管理员'
#         elif flag == 'cancel':
#             updata_type = '成员'
#
#         Team_User.objects.filter(user_id=user_id, team_id=team_id).update(ut_type=updata_type)
#     except Exception as e:
#         print(e)
#     return redirect('/teammember')
#
#
# ###########超级管理员###############
#
# #超级管理员重置密码
# @login_required
# def reset_psw(request):
#     try:
#         user_id = request.GET.get("user_id")
#         new_password = 111111
#         User.objects.filter(id = user_id).update(password=make_password(new_password))
#     except Exception as e:
#         print(e)
#     return 0
#
#
# #获取团队列表
# @login_required
# def get_team_temp_list(request):
#     try:
#         pass
#     except Exception as e:
#         print(e)
#
# #审核团队申请
# @login_required
# def check_team_temp(request):
#     try:
#         flag = request.GET.get("flag")
#         user_id = request.GET.get('userid')
#         team_name = request.GET.get('teamname')
#         if flag == 1:#通过
#             Team_temp.objects.filter(user_id=user_id,teamname=team_name).update(is_pass ='是')
#             team = Team.objects.create(teamname=request.POST.get('teamname'), is_pass='是')
#             team.save()
#             team_id = team.id
#             team_user = Team_User.objects.create(team_id=team_id, user_id=user_id, ut_type='团队创建者')
#             team_user.save()
#         else:
#             Team_temp.objects.filter(user_id=user_id, teamname=team_name).update(is_pass='否')
#     except Exception as e:
#         print(e)
#
# # =============== admin =============#
# @login_required
# def admin_info(request):
#     try:
#         user = request.user
#         #修改密码
#         if request.method == 'POST':
#             username = request.user.username
#             oldpsw = request.POST.get('oldpassword')
#             newpsw1 = request.POST.get('newpassword1')
#             newpsw2 = request.POST.get('newpassword2')
#             if newpsw1 != newpsw2:
#                 reason = '密码不一致'
#                 return render(request, 'new/admin/admin_info.html', locals())
#             user = authenticate(username=username, password=oldpsw)
#             if user is not None:
#                 user.set_password(newpsw1)
#                 user.save()
#                 return redirect('/login')
#             else:
#                 reason = '用户名不存在或原始密码错误'
#                 return render(request, 'new/admin/admin_info.html', locals())
#     except Exception as e:
#         print(e)
#     return render(request,'new/admin/admin_info.html',locals())
#
# @login_required
# def admin_login_info(request):
#     try:
#         user = request.user
#         # team = Team_User.objects.filter(user_id=user.id)[0]
#         if len(User_login_log.objects.filter(user_id=user.id)) > 1:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[1]
#             user_log_latest = User_login_log.objects.filter(user_id=user.id)[0]
#         else:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[0]
#             user_log_latest = user_log_last
#     except Exception as e:
#         print(e)
#     return render(request,'new/admin/admin_login_info.html',locals())
#
# # 分页代码
# def getPage(request, list,n):
#     paginator = Paginator(list, n)
#     try:
#         page = int(request.GET.get('page', 1))
#         list = paginator.page(page)
#     except (EmptyPage, InvalidPage, PageNotAnInteger):
#         list = paginator.page(1)
#     return list
#
# @login_required
# def admin_message(request):
#     team_temp = Team_temp.objects.all()
#     team_temp_list = getPage(request,team_temp,10)
#     return render(request,'new/admin/admin_message.html',locals())
#
# #hive/mysql日志
#
# @login_required
# def sys_logs(request):
#     try:
#         hive_logs = hive_app.hive_fetchExecutionJobLogs()
#         hive_log = []
#         for log in hive_logs:
#             log = log['data'].split('\n')
#             log.reverse()
#             hive_log += log
#             hive_log +=['============================================']
#         # print(hive_log)
#         mysql_logs= mysql_app.mysql_fetchExecutionJobLogs()
#         mysql_logs = mysql_logs['data'].split('\n')
#         mysql_logs.reverse()
#     except Exception as e:
#         print(e)
#     return render(request, 'new/admin/admin_sys_manage.html', locals())
#
# #获得重置密码列表
# @login_required
# def admin_get_reset_psw(request):
#     try:
#         reset_user_list = User.objects.exclude(is_reset='否')
#         reset_user_list = getPage(request, reset_user_list, 5)
#     except Exception as e:
#         pass
#     return render(request, 'new/admin/admin_password_reset_audit.html',locals())
#
# #重置密码
# @login_required
# def admin_reset_psw(request):
#     try:
#         if request.method == 'GET':
#             flag = request.GET.get('flag')
#             username = request.GET.get('username')
#             if flag == 'n':
#                 User.objects.filter(username=username).update(is_reset = '未通过')
#             elif flag == 'y':
#                 User.objects.filter(username=username).update(is_reset='通过',password = make_password(111111))
#
#     except Exception as e:
#         pass
#     return redirect('/admingetresetpsw/')
#
# #获取团队审核列表
# @login_required
# def admin_team_manage(request):
#     try:
#         team_temp_list = Team_temp.objects.all()
#         team_temp_list = getPage(request,team_temp_list,10)
#     except Exception as e:
#         print(e)
#     return render(request,'new/admin/admin_team_manage_audit.html',locals())
#
# #获取团队列表
# @login_required
# def admin_team_list(request):
#     team_temp = Team_temp.objects.all()
#     team_temp_list = getPage(request, team_temp, 10)
#     return render(request,'new/admin/admin_team_manage_list.html',locals())
#
# #审核团队
# @login_required
# def admin_check_team(request):
#     try:
#         flag = request.GET.get("flag")
#         user_id = request.GET.get('userid')
#         team_name = request.GET.get('teamname')
#         if flag == 'y':#通过
#             Team_temp.objects.filter(user_id=user_id,teamname=team_name).update(is_pass ='是')
#             team = Team.objects.create(teamname=team_name)
#             team.save()
#             team_id = team.id
#             team_user = Team_User.objects.create(team_id=team_id, user_id=user_id, ut_type='团队创建者')
#             team_user.save()
#         elif flag == 'n':
#             Team_temp.objects.filter(user_id=user_id, teamname=team_name).update(is_pass='否')
#     except Exception as e:
#         print(e)
#     return redirect('/adminteammanage/')
#
# def admin_data_manage(request):
#     import  app.decisionpy.hdfsClient as hdfs
#     hdfs_conf = {
#         'server_url': 'http://172.23.27.203:50070',
#         'cache_days': 1,
#         'user': 'dm'
#     }
#
#     info = hdfs.HdfsClient(conf=hdfs_conf)
#     info_table = info.general_info(info.loc_conf['general_info_local_path'], info.loc_conf['general_info_remote_path'])
#     tabel_values = []
#     table_name=[]
#     for name in info_table.columns:
#         table_name.append(name)
#     for values in info_table.values:
#         tabel_values.append(values)
#     tabel_values = getPage(request,tabel_values,20)
#     return render(request,'new/admin/admin_data_manage.html',locals())
#
#
# #============== creater ============#
# @login_required
# def creater_info(request):
#     try:
#         user = request.user
#         team_id = request.GET.get('teamid')
#         if team_id ==None:
#            team_id = Team_User.objects.filter(user_id=user.id)[0].team_id
#         # dteam_id = request.GET.get('dteamid')
#         # print('dteamid')
#         # print(dteam_id)
#         # if dteam_id ==None:
#         #     dteam_id = team_id
#         # print('dteamid')
#         # print(dteam_id)
#         # info_page_redirect(request,dteam_id)
#         team_user_list = Team_User.objects.filter(user_id=user.id)
#         user = User.objects.filter(id=user.id)[0]
#         team = Team_User.objects.filter(user_id=user.id,team_id=team_id)[0]
#         ut_type = team.ut_type
#         # print(ut_type)
#         # if ut_type == '成员':
#         #     print()
#         #     return redirect('/userinfo?dteamid=' + str(team.team_id))
#         # elif ut_type == '团队创建者':
#         #     print(11111)
#         #     return redirect('/createrinfo?dteamid=' + str(team.team_id))
#         # elif ut_type == '团队管理员':
#         #     pass
#
#     except Exception as e:
#         print(e)
#     return render(request,'new/teamCreater/founder_info.html',locals())
#
#
# @login_required
# def creater_login_info(request):
#     try:
#         user = request.user
#         # team = Team_User.objects.filter(user_id=user.id)[0]
#         if len(User_login_log.objects.filter(user_id=user.id)) > 1:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[1]
#             user_log_latest = User_login_log.objects.filter(user_id=user.id)[0]
#         else:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[0]
#             user_log_latest = user_log_last
#     except Exception as e:
#         print(e)
#     return render(request,'new/teamCreater/founder_login_info.html',locals())
#
# @login_required
# def creater_get_join_list(request):
#     team_id = request.GET.get('team_id')
#     team_user_list = Teamer_temp.objects.filter(team_id=1)
#     for i in team_user_list:
#         print(i.is_pass)
#     team_user_list = getPage(request,team_user_list,10)
#
#     return render(request,'new/teamCreater/founder_manage_audit.html',locals())
#
#
# @login_required
# def creater_check_join(request):
#     try:
#         teamer_id = request.GET.get('userid')
#         pass_flag = request.GET.get('flag')
#         team_id = request.GET.get('teamid')
#
#         if pass_flag == 'y':
#             Teamer_temp.objects.filter(user_id=teamer_id).update(is_pass='是')
#             team_user = Team_User.objects.create(team_id =team_id,user_id = teamer_id,ut_type='成员')
#             team_user.save()
#         elif pass_flag == 'n':
#             Teamer_temp.objects.filter(user_id=teamer_id).update(is_pass='否')
#     except Exception as e:
#         print(e)
#     return redirect('/createrjoinlist')
#
# @login_required
# def creater_get_manager_list(request):
#     try:
#         # user = request.user
#         # user_id = user.id
#         user_id = 2
#         team = Team_User.objects.filter(user_id = user_id)[0]
#         teamerlist = Teamer_temp.objects.filter(team_id=team.team_id)
#         teamuserlist = Team_User.objects.filter(team_id=team.team_id)
#         teamadminlist = Team_User.objects.filter(team_id=team.team_id).filter(ut_type='团队管理员')
#         teamadminlist = getPage(request, teamadminlist, 10)
#     except Exception as e:
#         print(e)
#     return render(request,'new/teamCreater/founder_manage_admin.html',locals())
#
#
# @login_required
# def creater_get_team_user_list(request):
#     try:
#         # user = request.user
#         user_id = 2
#         team = Team_User.objects.filter(user_id=user_id)[0]
#         teamuserlist = Team_User.objects.filter(team_id=team.team_id)
#         memberlist = []
#         for teamuser in teamuserlist:
#             tmp_dic = {}
#
#             if len(User_login_log.objects.filter(user_id=teamuser.user_id)) > 0:
#                 user_log_last = User_login_log.objects.filter(user_id=teamuser.user_id)[0]
#                 tmp_dic['login_date'] = user_log_last.login_date
#                 tmp_dic['login_ip'] = user_log_last.login_ip
#                 tmp_dic['login_system'] = user_log_last.login_system
#             else:
#                 tmp_dic['login_date'] = ""
#                 tmp_dic['login_ip'] = ""
#                 tmp_dic['login_system'] = ""
#
#             tmp_dic['user_id'] = teamuser.user_id
#             tmp_dic['user_name'] = teamuser.user.username
#             tmp_dic['user_type'] = teamuser.ut_type
#             tmp_dic['team_name'] = teamuser.team.teamname
#             memberlist.append(tmp_dic)
#         memberlist = getPage(request, memberlist,10)
#     except Exception as e:
#         print(e)
#     return render(request,'new/teamCreater/founder_manage_all_user.html',locals())
#
# @login_required
# def creater_change_user_type(request):
#     try:
#         flag = request.GET.get('flag')
#         team_id = request.GET.get('teamid')
#         user_id = request.GET.get('userid')
#         if flag == 'gly':
#             Team_User.objects.filter(team_id =team_id,user_id = user_id).update(ut_type='团队管理员')
#         elif flag == 'cy':
#             Team_User.objects.filter(team_id=team_id, user_id=user_id).update(ut_type='成员')
#     except Exception as e:
#         print(e)
#     return redirect('/createruserlist')
#
# @login_required
# def creater_message_list(request):
#     try:
#         team_user_list = Teamer_temp.objects.filter(team_id=1)
#         team_user_list = getPage(request,team_user_list,10)
#     except Exception as e:
#         print(e)
#     return  render(request,'new/teamCreater/founder_message.html',locals())
#
#
# def creater_data_manage(request):
#     import app.decisionpy.hdfsClient as hdfs
#     hdfs_conf = {
#         'server_url': 'http://172.23.27.203:50070',
#         'cache_days': 1,
#         'user': 'dm'
#     }
#
#     info = hdfs.HdfsClient(conf=hdfs_conf)
#     info_table = info.general_info(info.loc_conf['general_info_local_path'], info.loc_conf['general_info_remote_path'])
#     tabel_values = []
#     table_name=[]
#     for name in info_table.columns:
#         table_name.append(name)
#     for values in info_table.values:
#         tabel_values.append(values)
#     tabel_values = getPage(request,tabel_values,20)
#     print(tabel_values)
#     return render(request,'new/teamCreater/founder_data_manage.html',locals())
#
#
# #================== manager ==================#
#
# @login_required
# def manager_get_join_list(request):
#     team_id = request.GET.get('teamid')
#     print('id:'+str(team_id))
#     team_user_list = Teamer_temp.objects.filter(team_id=1)
#     for i in team_user_list:
#         print(i.is_pass)
#     team_user_list = getPage(request,team_user_list,10)
#     return render(request, 'new/manager_user/manager_manage_audit.html', locals())
#
# @login_required
# def manager_get_manager_list(request):
#     try:
#         user = request.user
#         user_id = user.id
#         # user_id = 2
#         team = Team_User.objects.filter(user_id = user_id)[0]
#         teamerlist = Teamer_temp.objects.filter(team_id=team.team_id)
#         teamuserlist = Team_User.objects.filter(team_id=team.team_id)
#         teamadminlist = Team_User.objects.filter(team_id=team.team_id).filter(ut_type='团队管理员')
#         teamadminlist = getPage(request,teamadminlist,10)
#     except Exception as e:
#         print(e)
#     return render(request, 'new/manager_user/manager_manage_admin.html', locals())
#
# @login_required
# def manager_get_team_user_list(request):
#     try:
#         user = request.user
#         user_id = user.id
#         # user_id = 2
#         team = Team_User.objects.filter(user_id=user_id)[0]
#         teamuserlist = Team_User.objects.filter(team_id=team.team_id)
#         memberlist = []
#         for teamuser in teamuserlist:
#             tmp_dic = {}
#
#             if len(User_login_log.objects.filter(user_id=teamuser.user_id)) > 0:
#                 user_log_last = User_login_log.objects.filter(user_id=teamuser.user_id)[0]
#                 tmp_dic['login_date'] = user_log_last.login_date
#                 tmp_dic['login_ip'] = user_log_last.login_ip
#                 tmp_dic['login_system'] = user_log_last.login_system
#             else:
#                 tmp_dic['login_date'] = ""
#                 tmp_dic['login_ip'] = ""
#                 tmp_dic['login_system'] = ""
#
#             tmp_dic['user_id'] = teamuser.user_id
#             tmp_dic['user_name'] = teamuser.user.username
#             tmp_dic['user_type'] = teamuser.ut_type
#             tmp_dic['team_name'] = teamuser.team.teamname
#             memberlist.append(tmp_dic)
#         memberlist = getPage(request, memberlist,10)
#     except Exception as e:
#         print(e)
#     return render(request, 'new/manager_user/manager_manage_all_user.html', locals())
#
# @login_required
# def manager_change_user_type(request):
#     try:
#         flag = request.GET.get('flag')
#         team_id = request.GET.get('teamid')
#         user_id = request.GET.get('userid')
#         if flag == 'cy':
#             Team_User.objects.filter(team_id=team_id, user_id=user_id).update(ut_type='成员')
#     except Exception as e:
#         print(e)
#     return redirect('/manageruserlist')
#
# @login_required
# def manager_check_join(request):
#     try:
#         teamer_id = request.GET.get('userid')
#         pass_flag = request.GET.get('flag')
#         team_id = request.GET.get('teamid')
#
#         if pass_flag == 'y':
#             Teamer_temp.objects.filter(user_id=teamer_id).update(is_pass='是')
#             team_user = Team_User.objects.create(team_id =team_id,user_id = teamer_id,ut_type='成员')
#             team_user.save()
#         elif pass_flag == 'n':
#             Teamer_temp.objects.filter(user_id=teamer_id).update(is_pass='否')
#     except Exception as e:
#         print(e)
#     return redirect('/managerjoinlist')
#
# #================ user ==================#
# @login_required
# def user_info(request):
#     try:
#         user = request.user
#         # team_id = request.GET.get('userid')
#         user_id = user.id
#         team_id = request.GET.get('teamid')
#         # if team_id ==None:
#         #     team_id = Team_User.objects.filter(user_id=user.id)[0].team_id
#             # info_page_redirect(request,team_id)
#         team_user_list = Team_User.objects.filter(user_id=user.id)
#         team = Team_User.objects.filter(user_id=user.id, team_id=team_id)[0]
#         # dteam_id = request.GET.get('teamid')
#         # print(dteam_id)
#         # if dteam_id == None:
#         #     dteam_id=team_id
#         # print(dteam_id)
#         # team = Team_User.objects.filter(user_id=user.id, team_id=team_id)[0]
#         #
#         # ut_type = team.ut_type
#         # print(ut_type)
#         # if ut_type == '成员':
#         #     return redirect('/userinfo?teamid=' + str(team.team_id))
#         # elif ut_type == '团队创建者':
#         #     # return render(request,'new/teamCreater/founder_info.html',locals())
#         #     return redirect('/createrinfo?teamid=' + str(team.team_id))
#         # elif ut_type == '团队管理员':
#         #     pass
#
#     except Exception as e:
#         print(e)
#     return render(request,'new/manager_user/user_info.html',locals())
#
# @login_required
# def user_message_list(request):
#     try:
#         team_user_list = Teamer_temp.objects.filter(team_id=1)
#         team_user_list = getPage(request,team_user_list,10)
#     except Exception as e:
#         print(e)
#     return  render(request,'new/manager_user/user_message.html',locals())
#
# @login_required
# def user_login_info(request):
#     try:
#         user = request.user
#         # team = Team_User.objects.filter(user_id=user.id)[0]
#         if len(User_login_log.objects.filter(user_id=user.id)) > 1:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[1]
#             user_log_latest = User_login_log.objects.filter(user_id=user.id)[0]
#         else:
#             user_log_last = User_login_log.objects.filter(user_id=user.id)[0]
#             user_log_latest = user_log_last
#     except Exception as e:
#         print(e)
#     return render(request,'new/manager_user/user_login_info.html',locals())
#
# @login_required
# def user_get_manager_list(request):
#     try:
#         user = request.user
#         user_id = user.id
#         # user_id = 2
#         team = Team_User.objects.filter(user_id = user_id)[0]
#         teamerlist = Teamer_temp.objects.filter(team_id=team.team_id)
#         teamuserlist = Team_User.objects.filter(team_id=team.team_id)
#         teamadminlist = Team_User.objects.filter(team_id=team.team_id).filter(ut_type='团队管理员')
#         teamadminlist = getPage(request,teamadminlist,10)
#     except Exception as e:
#         print(e)
#     return render(request, 'new/manager_user/user_manage_admin.html', locals())
#
# @login_required
# def user_get_team_user_list(request):
#     try:
#         user = request.user
#         user_id = user.id
#         # user_id = 2
#         team = Team_User.objects.filter(user_id=user_id)[0]
#         teamuserlist = Team_User.objects.filter(team_id=team.team_id)
#         memberlist = []
#         for teamuser in teamuserlist:
#             tmp_dic = {}
#
#             if len(User_login_log.objects.filter(user_id=teamuser.user_id)) > 0:
#                 user_log_last = User_login_log.objects.filter(user_id=teamuser.user_id)[0]
#                 tmp_dic['login_date'] = user_log_last.login_date
#                 tmp_dic['login_ip'] = user_log_last.login_ip
#                 tmp_dic['login_system'] = user_log_last.login_system
#             else:
#                 tmp_dic['login_date'] = ""
#                 tmp_dic['login_ip'] = ""
#                 tmp_dic['login_system'] = ""
#
#             tmp_dic['user_id'] = teamuser.user_id
#             tmp_dic['user_name'] = teamuser.user.username
#             tmp_dic['user_type'] = teamuser.ut_type
#             tmp_dic['team_name'] = teamuser.team.teamname
#             memberlist.append(tmp_dic)
#         memberlist = getPage(request, memberlist,10)
#     except Exception as e:
#         print(e)
#     return render(request, 'new/manager_user/user_manage_all_user.html', locals())
#
# #=========== decisionpy ===============#
# import app.decisionpy.analyse_fibers as fs
# import  app.decisionpy.analyse_breakpoint as bk
# import app.decisionpy.newDataUnion as du
#
#
# @login_required
# def decison(request):
#     if request.method =="GET":
#         target_label = request.GET.get('target_label', "ECC")
#
#         print(target_label)
#         tag_name = 1
#         oldStep = ""
#         tree_data = ""
#     return render(request, 'new/manager_user/decisionPage.html', locals())
#


# @login_required
# def admin_decison(request):
#     if request.method =="GET":
#         target_label =request.GET.get('target_label',"ECC")
#         tag_name = 1
#         oldStep = ""
#         tree_data = ""
#     return render(request,'new/admin/admin_decision.html',locals())
#
# @login_required
# def founder_decison(request):
#     if request.method =="GET":
#         target_label = request.GET.get('target_label', "ECC")
#         tag_name = 1
#         tree_data = ""
#         oldStep = ""
#     return render(request,'new/teamCreater/founder_decision.html',locals())
#
#
#
# @csrf_exempt
# @login_required
# def admin_analy_feas_min_max(request):
#     feas_data = {}
#     tag_name = 1
#     oldStep = ""
#     target_label = "ECC"
#     if request.method == "POST":
#
#         target_label = request.POST.get('target_label')
#         tag_name = request.POST.get('tag_name').replace(" ", "")
#         if tag_name == '表格':
#             tag_name = 1
#         elif tag_name == "树状图":
#             tag_name = 2
#         elif tag_name == "影响因子分析":
#             tag_name = 3
#         else:
#             tag_name = 1
#         step_name = request.POST.get('step_name')
#         ori_choose_name = request.POST.get('choose_name')
#         choose_name_list = ori_choose_name.replace(' ', '')[0:-1].split(",")
#         oldStep = []
#         oldStep.append(step_name)
#         oldStep.append(choose_name_list)
#         ori_choose_feas = request.POST.get('choose_feas')
#         choose_feas_list = ori_choose_feas.replace(' ', '')[0:-1].split(",")
#         choose_feas = ori_choose_feas.replace(",", ";")[0:-1]
#         choose_name = ori_choose_name.replace(",", ";")[0:-1]
#         values_list = []
#
#         equip_list = fs.get_step_chooseName(step_name).split(";")
#         print(equip_list)
#         # print(";".join(choose_name_list))
#         fea_list = fs.chooseFeature(str(target_label), str(step_name), str(";".join(choose_name_list)))
#         print("target_label：" +target_label)
#         print("step_name："+step_name)
#         print("choose_name："+";".join(choose_name_list))
#         print(fea_list)
#         print("=================================")
#
#         feas_data = fs.get_feature_min_max(choose_feas)
#         rule_data = fs.find_rule(step_name, choose_name, target_label, choose_feas)
#         keys_list = rule_data[0].keys()
#         for item in rule_data:
#             values = []
#             for key in keys_list:
#                 v = item[key]
#                 values.append(v)
#             values_list.append(values)
#
#         sub_tree = fs.mytree(step_name, choose_name, target_label, choose_feas)
#         sub_tree.Start()
#         tree_data = json.loads(sub_tree.ToJson())['json']
#         tree_data = json.dumps(tree_data)
#         tree_path =sub_tree.ToPath()
#         tree_path = json.loads(sub_tree.ToPath())['json']
#         tree_path = json.dumps(tree_path)
#         values_list = getPage(request, values_list, 10)
#     return render(request,"decision/decisionPage.html",locals())
#
# @csrf_exempt
# @login_required
# def founder_analy_feas_min_max(request):
#     feas_data = {}
#     tag_name = 1
#     oldStep = ""
#     target_label = "ECC"
#     if request.method == "POST":
#
#         target_label = request.POST.get('target_label')
#         tag_name = request.POST.get('tag_name').replace(" ", "")
#         if tag_name == '表格':
#             tag_name = 1
#         elif tag_name == "树状图":
#             tag_name = 2
#         elif tag_name == "影响因子分析":
#             tag_name = 3
#         else:
#             tag_name = 1
#         step_name = request.POST.get('step_name')
#         ori_choose_name = request.POST.get('choose_name')
#         choose_name_list = ori_choose_name.replace(' ', '')[0:-1].split(",")
#         oldStep = []
#         oldStep.append(step_name)
#         oldStep.append(choose_name_list)
#         ori_choose_feas = request.POST.get('choose_feas')
#         choose_feas_list = ori_choose_feas.replace(' ', '')[0:-1].split(",")
#         choose_feas = ori_choose_feas.replace(",", ";")[0:-1]
#         choose_name = ori_choose_name.replace(",", ";")[0:-1]
#         values_list = []
#
#         equip_list = fs.get_step_chooseName(step_name).split(";")
#         # print(equip_list)
#         # print(";".join(choose_name_list))
#         fea_list = fs.chooseFeature(str(target_label), str(step_name), str(";".join(choose_name_list)))
#         feas_data = fs.get_feature_min_max(choose_feas)
#         rule_data = fs.find_rule(step_name, choose_name, target_label, choose_feas)
#         keys_list = rule_data[0].keys()
#
#         for item in rule_data:
#             values = []
#             for key in keys_list:
#                 v = item[key]
#                 values.append(v)
#             values_list.append(values)
#
#         sub_tree = fs.mytree(step_name, choose_name, target_label, choose_feas)
#         sub_tree.Start()
#         tree_data = json.loads(sub_tree.ToJson())['json']
#         tree_data = json.dumps(tree_data)
#         print(tree_data)
#         tree_path =sub_tree.ToPath()
#         tree_path = json.loads(sub_tree.ToPath())['json']
#         tree_path = json.dumps(tree_path)
#         values_list = getPage(request, values_list, 10)
#     return render(request,'new/teamCreater/founder_decision.html',locals())
#
#
#
# @csrf_exempt
# @login_required
# def analy_feas_min_max(request):
#     feas_data = {}
#     tag_name = 1
#     oldStep = ""
#
#     target_label= "ECC"
#     if request.method == "POST":
#         target_label = request.POST.get('target_label')
#         tag_name = request.POST.get('tag_name').replace(" ", "")
#         print("tag_name:"+tag_name)
#         if tag_name == '表格':
#             tag_name = 1
#         elif tag_name == "树状图":
#             tag_name = 2
#         elif tag_name == "影响因子分析":
#             tag_name = 3
#         else:
#             tag_name = 1
#         step_name = request.POST.get('step_name')
#         ori_choose_name = request.POST.get('choose_name')
#         choose_name_list = ori_choose_name.replace(' ', '')[0:-1].split(",")
#         oldStep = []
#         oldStep.append(step_name)
#         oldStep.append(choose_name_list)
#         ori_choose_feas = request.POST.get('choose_feas')
#         print("ori_choose_feas:" + ori_choose_feas)
#         choose_feas_list = ori_choose_feas.replace(' ', '')[0:-1].split(",")
#         choose_feas = ori_choose_feas.replace(",", ";")[0:-1]
#         choose_name = ori_choose_name.replace(",", ";")[0:-1]
#         values_list = []
#
#         equip_list = fs.get_step_chooseName(step_name).split(";")
#         # print(equip_list)
#         # print(";".join(choose_name_list))
#         fea_list = fs.chooseFeature(str(target_label), str(step_name), str(";".join(choose_name_list)))
#         print(fea_list)
#         print("=================================")
#
#         feas_data = fs.get_feature_min_max(choose_feas)
#         rule_data = fs.find_rule(step_name, choose_name, target_label, choose_feas)
#         keys_list = rule_data[0].keys()
#
#         for item in rule_data:
#             values = []
#             for key in keys_list:
#                 v = item[key]
#                 values.append(v)
#             values_list.append(values)
#
#         sub_tree = fs.mytree(step_name, choose_name, target_label, choose_feas)
#         sub_tree.Start()
#         tree_data = json.loads(sub_tree.ToJson())['json']
#         tree_data = json.dumps(tree_data)
#         tree_path =sub_tree.ToPath()
#         tree_path = json.loads(sub_tree.ToPath())['json']
#         tree_path = json.dumps(tree_path)
#         values_list = getPage(request, values_list, 10)
#         print("ori_choose_feas:"+ori_choose_feas)
#     return render(request, 'new/manager_user/decisionPage.html', locals())
#
# @csrf_exempt
# def analy_breakpoint(request):
#     data_list = {}
#     if request.method == "POST":
#         step_name = request.POST.get('stage_name')
#         equip_name = request.POST.getlist('equip_lists[]')[0:-1]
#         equip_name = ";".join(equip_name)
#         print(step_name)
#         print(equip_name)
#         bkdata = fs.get_breakpointrate_stepAndsys(step_name,equip_name)
#         data_list = {"status": 200}
#         data_list['data'] = bkdata
#     return HttpResponse(json.dumps(data_list), content_type="application/json")
#
# def admin_breakpoint_page(request):
#     return render(request,'new/admin/admin_breakpoint.html',locals())
#
# def founder_breakpoint_page(request):
#     return render(request,'new/teamCreater/founder_breakpoint.html',locals())
#
# def user_breakpoint_page(request):
#     return render(request,'new/manager_user/user_breakpoint.html',locals())
#
# #获取特征
# @csrf_exempt
# @login_required
# def analy_get_feas(request):
#     data_list = {}
#     if request.method == "POST":
#         target_label = request.POST.get('label')
#         print(target_label)
#         step_name = request.POST.get('step_name')
#         print(request.POST)
#         equip_name = request.POST.getlist('equip_list[]')
#         print(equip_name)
#         if target_label != "断点率":
#             data = fs.chooseFeature(str(target_label), str(step_name), str(";".join(equip_name)))
#         else:
#             data = bk.chooseFeature(str(target_label), str(step_name), str(";".join(equip_name)))
#         data_list ={"status":200}
#         fea_list = []
#         for i in data:
#             fea_list.append(i)
#         data_list['features'] = fea_list
#     return HttpResponse(json.dumps(data_list),content_type="application/json")
#
# @csrf_exempt
# @login_required
# def mdf_pic(request):
#     data_list = {}
#     if request.method=="POST":
#         print(request.POST)
#         step_name = request.POST.get("stage_name")
#         equip_lists = request.POST.getlist("equip_lists[]")
#         equip_lists = ";".join(i for i in equip_lists)
#         target_label = request.POST.get("target_label")
#         target_feature = request.POST.get("target_feature")
#
#         static_feature = request.POST.get("static_feature")
#         print(static_feature)
#         fea = json.loads(static_feature)
#         static_fea_dist = {}
#         for k in fea:
#             static_fea_dist[k] = ",".join([i for i in fea[k]])
#         draw_data = fs.getTrend_newmodel(step_name,equip_lists,target_label,target_feature,static_fea_dist)
#         print(draw_data)
#         print("===================")
#         x = [i for i in draw_data[0]]
#         y = [i for i in draw_data[1]]
#         y1 = [i for i in draw_data[2]]
#         ry = [i for i in draw_data[3]]
#         rz = [i for i in draw_data[4]]
#         data_list = {"status": 200,'X':x,'Y':y,'Z':y1,"RY":ry,"RZ":rz,'X_NAME':target_label}
#         print(data_list)
#     return HttpResponse(json.dumps(data_list),content_type="application/json")
#
# @login_required
# @csrf_exempt
# def get_mysql_logs(request):
#     try:
#         mysql_logs = mysql_app.mysql_fetchExecutionJobLogs()
#         mysql_logs = mysql_logs['data'].split('\n')
#         mysql_logs.reverse()
#         mysql_log = {"status":200,"data":mysql_logs}
#     except Exception as e:
#         print(e)
#     return HttpResponse(json.dumps(mysql_log),content_type="application/json")
#
# @login_required
# @csrf_exempt
# def get_hive_logs(request):
#     try:
#         hive_logs = hive_app.hive_fetchExecutionJobLogs()[1:]
#         hive_log = []
#         for log in hive_logs:
#             log = log['data'].split('\n')
#             log.reverse()
#             hive_log += log
#             hive_log +=['============================================']
#         hive_log = {"status":200,"data":hive_log}
#     except Exception as e:
#         print(e)
#     return HttpResponse(json.dumps(hive_log),content_type="application/json")







# def ana(request):
#     return  render(request,'new/decision/analysis.html',locals())
# #=============== Hive Views =============#
# #获取日志
# def get_hive_logs(request):
#     try:
#         logs =
#
#.hive_fetchExecutionJobLogs()
#         logs = logs['data']
#     except Exception as e:
#         print(e)
#     return render(request,'Logs.html',locals())
#
# #一键部署
# @login_required
# def hive_deploy(request):
#     try:
#         hive_app.hive_autoDeployProjectFlow()
#     except Exception as e:
#         print(e)
#     return
#
# #运行
# def hive_run(request):
#     try:
#         hive_app.hive_executeFlow()
#     except Exception as e:
#         print(e)
#     return
#
# #暂停
# def hive_pause(request):
#     try:
#         hive_app.hive_pauseFlowExecution()
#     except Exception as e:
#         print(e)
#     return
#
# #停止
# def hive_stop(request):
#     try:
#        hive_app.hive_cancelFlowExecution()
#     except Exception as e:
#         print(e)
#     return
#
# #重启
# def hive_restart(request):
#     try:
#         hive_app.hive_resumeFlowExecution()
#     except Exception as e:
#         print(e)
#     return
#
#
# #=============== Mysql Views =============#
# # def
#
# def mysql_start(request):
#     try:
#         mysql_app.mysql_executeFlow()
#     except Exception as e:
#         print(e)
#     return
#
# def mysql_stop(request):
#     try:
#         mysql_app.mysql_cancelFlowExecution()
#     except Exception as e:
#         print(e)
#     return
#
# def get_mysql_logs(request):
#     try:
#         mysql_app.mysql_executeFlow()
#     except Exception as e:
#         print(e)
#     return
#
#
#
#
#
#
# #====================decisionpy=================================#
#
#
# # #选人哥的代码
# # from sklearn import tree
# # import pandas as pd
#
# import  numpy as np
# @login_required
# def readData(file=r"G:\tongding_projrct\app\data\fin_data_v1.csv"):
#     fibers = pd.read_csv(file)
#     fibers = fibers.drop(
#         ['拉丝塔号', '光纤编号', '大盘', '小盘', '芯棒编码_y', '等级_y', 'simple_id', 'Unnamed: 0', '条码', '等级_x', '计划物料编码', '实际物料编码',
#          '生产日期', '检验日期', '备注', '光棒编号'], axis=1)
#     fibers = fibers.fillna(0)
#     fibers['filterlens_testlens'] = fibers['breakpoint_rate_1']
#     fibers = fibers.drop(
#         ['break_count', 'all_count', 'test_lens_sum', 'breakpoint_rate_0', 'breakpoint_rate_1', 'breakpoint_rate_2'],
#         axis=1)
#     columse = list(fibers.columns.values)
#     fibers.to_csv("temp.csv", index=None, encoding='utf8')
#     test = [columse[i] for i in range(len(columse))]
#     test.remove('芯棒编码_x')
#     temp_avg = pd.pivot_table(fibers, index=['芯棒编码_x'], values=test, aggfunc=np.mean)
#     temp_names = ['id']
#     temp_li = list(temp_avg.columns.values)
#     temp_names.extend(temp_li)
#     temp_avg.to_csv("temp_avg.csv", header=None)
#     temp_avg = pd.read_csv("temp_avg.csv", header=None)
#     temp_avg.columns = temp_names
#
#     result_data_v0 = pd.DataFrame()
#     result = []
#     for i in range(1, len(temp_names)):
#         tt = temp_avg.loc[:, temp_names[i]].values
#         iidex = temp_names[i]
#         t0 = min(tt)
#         t1 = max(tt)
#         t2 = np.mean(tt)
#         t3 = np.std(tt)
#         result.append([iidex, t0, t1, t2, t3])
#     result_data_v0["fname"] = [i[0] for i in result]
#     result_data_v0["min"] = [i[1] for i in result]
#     result_data_v0["max"] = [i[2] for i in result]
#     result_data_v0["mean"] = [i[3] for i in result]
#     result_data_v0["std"] = [i[4] for i in result]
#     result_data_v0 = result_data_v0.set_index("fname", drop=True)
#     return temp_avg, result_data_v0
#
# @login_required
# def getTrend_newmodel(target_label, target_feature, static_feature):
#     # 1.获得目标标签的模型，以及参与模型的特征
#     fibers, result_data_v0 = readData()
#     train_1 = [i for i in static_feature.keys()]
#     train_1.append(target_feature)
#     print(train_1)
#
#     mylable = fibers.loc[:, [target_label]]
#     fibers_data = fibers.loc[:, train_1]
#     X_train = fibers_data
#     y_train = mylable
#     clf = DecisionTreeRegressor()
#     clf.fit(X_train, y_train)
#
#     # 2.获得目标特征的范围,以及delat
#     mymin = result_data_v0.loc[target_feature][0]
#     mymax = result_data_v0.loc[target_feature][1]
#     mydelat = (mymax - mymin) / 100.0
#     print(result_data_v0.loc[target_label][2])
#
#     X = []
#     res = mymin
#     while res <= mymax:
#         X.append(res)
#         res = res + mydelat
#
#     # 3.获得模型中特征的值：动的，固定的，默认的
#     # 3.1 先全部默认均值,更改固定特征的值
#     feature_values = []
#     for i in range(len(train_1)):
#         if target_feature == train_1[i]:
#             changeindex = i
#         if train_1[i] in static_feature:
#             feature_values.append(static_feature[train_1[i]])
#         else:
#             feature_values.append(result_data_v0.loc[train_1[i]][2])
#
#     # 3.2 for循环更改动值
#     templist = [feature_values]
#     Y = []
#     for i in X:
#         templist[0][changeindex] = i
#         pre1 = clf.predict(templist)
#         Y.append(pre1[0])
#
#     return X, Y
# @csrf_exempt
# @login_required
# def getXY(request):
#
#     target_label=request.POST.get('targetlabel')
#     target_feature = request.POST.get('targetfeature')
#     # density = request.POST.get('density')
#     # weight = request.POST.get('weight')
#     static_feature=request.POST.get('staticfeature')
#     static_feature=eval(static_feature)
#     all=request.POST.getlist
#     print(all)
#     print(target_label)
#     print(target_feature)
#     print(static_feature)
#     # print(density)
#     # print(weight)
#     print('一次计算')
#     # target_label = "1310MFD"
#     # target_feature = "有效长度"
#     # static_feature = {"密度": density, "重量": weight}  # {}#
#
#     X, Y = getTrend_newmodel(target_label, target_feature, static_feature)
#     print('y:')
#     print(Y)
#     print('x:')
#     print(X)
#     result = {'x': X, 'y': Y}
#     return HttpResponse(pd.json.dumps(result))
#
# @login_required
# def decisionpy(request):
#     return render(request, './new/decisionpy.html', locals())


