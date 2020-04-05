"""tongding_projrct URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app.views import *

urlpatterns = [
    url(r'^register',do_register,name='register'),
    url(r'^login',do_login,name='login'),
    url(r'^logout',do_logout,name='logout'),

    url(r'^userinfo', user_info, name='user_info'),
    url(r'^userloginfo', user_login_info, name='user_login_info'),
    # url(r'^changepsw', change_psw, name='change_psw'),
    url('^decisionmanage', decision_manege, name='decision_manege'),

    url(r'^decision', decision, name='decision'),
    url(r'^breakpointpage', breakpoint_page, name="breakpoint_page"),


    url(r'^mdfpic', mdf_pic, name='mdf_pic'),
    url(r'^getbreakpoint', analy_breakpoint, name="getbreakpoint"),
    url(r'^mdfgetfeas',analy_get_feas,name='mdf_get_feas'),
    url('^pageredirect', info_page_redirect, name='info_page_redirect'),
    url(r'^getdecision', decision_analy, name='admin_analy_feas_min_max'),
    url(r'^markscore', mark_score, name='mark_score'),


    url('^adminsyslogs',admin_sys_logs,name='admin_sys_logs'),
    url('^datamanage', data_manage, name='data_manage'),
    url('^refreshdatamanage', refresh_data_manage, name='refresh_data_manage'),
    url('^hivelogs', get_hive_logs, name='get_hive_logs'),
    url('^mysqllogs', get_mysql_logs, name='get_mysql_logs'),
    url('^adminteammanage',admin_team_manage,name='admin_team_manage'),
    url('^admincheckteam',admin_check_team,name='admin_check_team'),
    url('^adminteamlist',admin_team_list,name='admin_team_list'),
    url('^sysmessage',sys_message,name='sys_message'),
    url('^admingetresetpsw',admin_get_reset_psw,name='admin_get_reset_password'),

    url('^foundergetjoinlist', founder_get_join_list, name='founder_get_join_list'),
    url('^foundergetmanagerlist', founder_get_manager_list, name='founder_get_manager_list'),
    url('^foundergetteamuserlist', founder_get_team_user_list, name='founder_get_team_user_list'),
    url('^foundercheckjoin', founder_check_join, name='founder_check_join'),
    url('^founderchangeusertype', founder_change_user_type, name='founder_change_user_type'),

    url('^usermanagerlist', user_get_manager_list, name='user_get_manager_list'),
    url('^useruserlist', user_get_team_user_list, name='user_get_team_user_list'),
    url('^screendispaly', screen_dis, name='screen_dis'),



    # url(r'^loginverify',login_verify,name='loginVerify'),
    # url(r'^index_gly',index_gly,name='inedx_gly'),
    # url(r'^userinfo',userinfo,name='userinfo'),
    # url(r'^checkuser',check_user,name='checkuser'),
    # url(r'^teammanager', team_manager, name='teammanager'),
    # url(r'^teampass',teamer_is_pass,name='teampass'),
    # url(r'^teammember',team_member,name='teammember'),
    # url(r'^changetype',change_teamuser_type,name='changetype'),
    # url(r'^hivelogs',get_hive_logs,name='hivelogs'),
    # url(r'^decisionpy',decisionpy,name='decisionpy'),
    # url('^getXY',getXY,name='getXY'),
    # url('^uploadimg',uploadImg,name='uploadImg'),
    # url('^showimg',showImg,name='showimg'),
    # url('^adminmessage',admin_message,name='admin_meassage'),
    # url('^sysmanage',sys_logs,name='sys_manage'),

    #
    # #-----admin--------#
    # url(r'^admininfo',admin_info,name='admin_info'),
    # url(r'^adminbreakpointpage', admin_breakpoint_page, name="admin_breakpoint_page"),
    # url(r'^adminlogininfo',admin_login_info,name='admin_login_info'),
    # url('^admingetresetpsw',admin_get_reset_psw,name='admin_get_reset_password'),
    # url('^adminteammanage',admin_team_manage,name='admin_team_manage'),
    # url('^adminteamlist',admin_team_list,name='admin_team_list'),
    # url('^adminresetpsw',admin_reset_psw,name='admin_reset_password'),
    # url('^admincheckteam',admin_check_team,name='admin_check_team'),
    # url('^admindatamanage', admin_data_manage, name='admin_data_manage'),
    #
    # #-------creater-------#
    # url('^createrjoinlist', founder_get_join_list, name='creater_get_join_list'),
    # url('^createrinfo', creater_info, name='creater_info'),
    # url(r'^crealogininfo',creater_login_info,name='creater_login_info'),
    # url('^creatermanagerlist', creater_get_manager_list, name='creater_get_manager_list'),
    # url('^createruserlist', creater_get_team_user_list, name='creater_get_team_user_list'),
    # url('^creatercheckjoin', creater_check_join, name='creater_check_join'),
    # url('^createrchangeuttype', creater_change_user_type, name='creater_change_user_type'),
    # url('^creatermessage', creater_message_list, name='creater_message_list'),
    # url('^createrdatamanage', creater_data_manage, name='creater_data_manage'),
    #
    #
    # #---------manager------#
    # url('^managerjoinlist', manager_get_join_list, name='manager_get_join_list'),
    # url('^managermanagerlist', manager_get_manager_list, name='manager_get_manager_list'),
    # url('^manageruserlist', manager_get_team_user_list, name='manager_get_team_user_list'),
    #
    # #-------- user -------#
    # url('^userinfo', user_info, name='user_info'),
    # url('^userlogininfo', user_login_info, name='user_login_info'),
    # url('^userbreakpointpage', user_breakpoint_page, name='user_breakpoint_page'),
    # url('^usermessage', user_message_list, name='user_message_list'),
    # url('^usermanagerlist', user_get_manager_list, name='user_get_manager_list'),
    # url('^useruserlist', user_get_team_user_list, name='user_get_team_user_list'),
    # # url('^loginredirect', login_redirect, name='login_redirect'),
    # url('^pageredirect', info_page_redirect, name='info_page_redirect'),
    #
    #
    # #======decisionpy=======#

    #
    # url(r'^getdecision', analy_feas_min_max, name='analy_feas_min_max'),

    # # url(r'^mdfpage',decisionpy,name='decisionpy'),
    #
    # url(r'^decisionpage',decison,name='decison'),
    # url(r'^admindecisionpage',admin_decison,name='admin_decison'),
    # url(r'^admingetdecision', decision_analy, name='admin_analy_feas_min_max'),
    # url(r'^founderdecisionpage', founder_decison, name='founder_decison'),
    # url(r'^foundergetdecision', founder_analy_feas_min_max, name='founder_analy_feas_min_max'),
    # url(r'^founderbreakpointpage', founder_breakpoint_page, name='founder_breakpoint_page'),
    # url(r'^decisionredict', decisionredict, name='decisionredict'),
]
