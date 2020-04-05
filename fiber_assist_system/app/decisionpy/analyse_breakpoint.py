# -*- coding: utf-8 -*-

"""
Created on Tue Dec  5 15:34:32 2017
针对“断点率”的分析
@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:42:35 2017
feature selection
@author: Administrator
"""
import pandas as pd
import numpy as np


breakpoint = "断点率"
label = breakpoint     
featurenames = ['密度', '重量', '沉积速率', 'SOOT直径', '有效长度', '重量误差',  '断点次数', '光纤总盘数', '光纤总长度', 'A_esi检验值*100.0*0.0', 'A_esi检验值*100.0*1.0', 'A_esi检验值*200.0*0.0', 'A_esi检验值*200.0*1.0', 'A_esi检验值*300.0*0.0', 'A_esi检验值*300.0*1.0', 'A_esi检验值*400.0*0.0', 'A_esi检验值*400.0*1.0', 'A_esi检验值*700.0*0.0', 'A_esi检验值*700.0*1.0', 'A_esi检验值*平均值*0.0', 'CoreSlope检验值*100.0*0.0', 'CoreSlope检验值*100.0*1.0', 'CoreSlope检验值*200.0*0.0', 'CoreSlope检验值*200.0*1.0', 'CoreSlope检验值*300.0*0.0', 'CoreSlope检验值*300.0*1.0', 'CoreSlope检验值*400.0*0.0', 'CoreSlope检验值*400.0*1.0', 'CoreSlope检验值*700.0*0.0', 'CoreSlope检验值*700.0*1.0', 'CoreSlope检验值*平均值*0.0', 'D/d检验值*100.0*0.0', 'D/d检验值*100.0*1.0', 'D/d检验值*200.0*0.0', 'D/d检验值*200.0*1.0', 'D/d检验值*300.0*0.0', 'D/d检验值*300.0*1.0', 'D/d检验值*400.0*0.0', 'D/d检验值*400.0*1.0', 'D/d检验值*700.0*0.0', 'D/d检验值*700.0*1.0', 'D/d检验值*平均值*0.0', 'DeltaMinus检验值*100.0*0.0', 'DeltaMinus检验值*100.0*1.0', 'DeltaMinus检验值*200.0*0.0', 'DeltaMinus检验值*200.0*1.0', 'DeltaMinus检验值*300.0*0.0', 'DeltaMinus检验值*300.0*1.0', 'DeltaMinus检验值*400.0*0.0', 'DeltaMinus检验值*400.0*1.0', 'DeltaMinus检验值*700.0*0.0', 'DeltaMinus检验值*700.0*1.0', 'DeltaMinus检验值*平均值*0.0', 'DeltaPlus检验值*100.0*0.0', 'DeltaPlus检验值*100.0*1.0', 'DeltaPlus检验值*200.0*0.0', 'DeltaPlus检验值*200.0*1.0', 'DeltaPlus检验值*300.0*0.0', 'DeltaPlus检验值*300.0*1.0', 'DeltaPlus检验值*400.0*0.0', 'DeltaPlus检验值*400.0*1.0', 'DeltaPlus检验值*700.0*0.0', 'DeltaPlus检验值*700.0*1.0', 'DeltaPlus检验值*平均值*0.0', 'DeltaTotal检验值*100.0*0.0', 'DeltaTotal检验值*100.0*1.0', 'DeltaTotal检验值*200.0*0.0', 'DeltaTotal检验值*200.0*1.0', 'DeltaTotal检验值*300.0*0.0', 'DeltaTotal检验值*300.0*1.0', 'DeltaTotal检验值*400.0*0.0', 'DeltaTotal检验值*400.0*1.0', 'DeltaTotal检验值*700.0*0.0', 'DeltaTotal检验值*700.0*1.0', 'DeltaTotal检验值*平均值*0.0', 'Index1检验值*100.0*0.0', 'Index1检验值*100.0*1.0', 'Index1检验值*200.0*0.0', 'Index1检验值*200.0*1.0', 'Index1检验值*300.0*0.0', 'Index1检验值*300.0*1.0', 'Index1检验值*400.0*0.0', 'Index1检验值*400.0*1.0', 'Index1检验值*700.0*0.0', 'Index1检验值*700.0*1.0', 'Index1检验值*平均值*0.0', 'Index2检验值*100.0*0.0', 'Index2检验值*100.0*1.0', 'Index2检验值*200.0*0.0', 'Index2检验值*200.0*1.0', 'Index2检验值*300.0*0.0', 'Index2检验值*300.0*1.0', 'Index2检验值*400.0*0.0', 'Index2检验值*400.0*1.0', 'Index2检验值*700.0*0.0', 'Index2检验值*700.0*1.0', 'Index2检验值*平均值*0.0', 'Non_Clad检验值*100.0*0.0', 'Non_Clad检验值*100.0*1.0', 'Non_Clad检验值*200.0*0.0', 'Non_Clad检验值*200.0*1.0', 'Non_Clad检验值*300.0*0.0', 'Non_Clad检验值*300.0*1.0', 'Non_Clad检验值*400.0*0.0', 'Non_Clad检验值*400.0*1.0', 'Non_Clad检验值*700.0*0.0', 'Non_Clad检验值*700.0*1.0', 'Non_Clad检验值*平均值*0.0', 'Non_Core检验值*100.0*0.0', 'Non_Core检验值*100.0*1.0', 'Non_Core检验值*200.0*0.0', 'Non_Core检验值*200.0*1.0', 'Non_Core检验值*300.0*0.0', 'Non_Core检验值*300.0*1.0', 'Non_Core检验值*400.0*0.0', 'Non_Core检验值*400.0*1.0', 'Non_Core检验值*700.0*0.0', 'Non_Core检验值*700.0*1.0', 'Non_Core检验值*平均值*0.0', 'OD_Clad检验值*100.0*0.0', 'OD_Clad检验值*100.0*1.0', 'OD_Clad检验值*200.0*0.0', 'OD_Clad检验值*200.0*1.0', 'OD_Clad检验值*300.0*0.0', 'OD_Clad检验值*300.0*1.0', 'OD_Clad检验值*400.0*0.0', 'OD_Clad检验值*400.0*1.0', 'OD_Clad检验值*700.0*0.0', 'OD_Clad检验值*700.0*1.0', 'OD_Clad检验值*平均值*0.0', 'OD_Core检验值*100.0*0.0', 'OD_Core检验值*100.0*1.0', 'OD_Core检验值*200.0*0.0', 'OD_Core检验值*200.0*1.0', 'OD_Core检验值*300.0*0.0', 'OD_Core检验值*300.0*1.0', 'OD_Core检验值*400.0*0.0', 'OD_Core检验值*400.0*1.0', 'OD_Core检验值*700.0*0.0', 'OD_Core检验值*700.0*1.0', 'OD_Core检验值*平均值*0.0', '合格*100.0*0.0', '合格*100.0*1.0', '合格*200.0*0.0', '合格*200.0*1.0', '合格*300.0*0.0', '合格*300.0*1.0', '合格*400.0*0.0', '合格*400.0*1.0', '合格*700.0*0.0', '合格*700.0*1.0', '合格*平均值*0.0', '长度',  '测试参考值', '跳动合格', '手工判定合格', '最大跳动值(对接前)', '最大跳动值']
file = r"g:\\fiber_assist_system\app\data\1201.csv"
stepname = ['VAD塔线', 'VAD烧结塔线', '拉伸塔线', 'OVD塔线']    
nopassrate = '不合格率'
Fibers_level = '等级_x'
bad_level = "不合格"
fibersData = pd.read_csv(file).fillna(0)

'''
#获取阶段名
'''


def get_stepName():
    step = ['VAD塔线', 'VAD烧结塔线', '拉伸塔线', 'OVD塔线']
    res = ";".join(step)
    return res


'''
#获取每个阶段可以选择的设备名
'''


def get_step_chooseName(stepName):
    data = fibersData
    if len(stepName) == 0:
        stepName = stepname[0]   
    choosename = list(set(data.loc[:,stepName].values))
    res = ";".join(choosename)
    return res


'''
所有阶段和对应的设备
'''


def get_step_and_sys():
    step = stepname
    res = {}
    for i in step:
        res[i] = get_step_chooseName(i)
    return res


'''
所有阶段及其设备对应的合格率
'''


def get_sys_passrate():
    tempfeature = [i for i in stepname]
    tempfeature.append(Fibers_level)
    fibers = fibersData.loc[:,tempfeature]
    step = stepname
    res = {}
    for i in step:
        temp = get_step_chooseName(i).split(";")
        for sy in temp:
            tempdata = fibers[fibers[i] == sy]
            allcount = len(tempdata)
            nopasscount = len(tempdata[tempdata[Fibers_level] == bad_level])
            res[i+":"+sy] = (allcount-nopasscount)*1.0/allcount
    return res


'''
#根据阶段和选择的设备，返回data
'''


def get_stepSYS_ChooseName(stepName, chooseName):
    fibers = fibersData
    if len(stepName) == 0:
        stepName = stepname[0]        
    if len(chooseName) == 0:
        return fibers
    else: 
        tempres = chooseName.split(";")
        fibers = fibers[fibers[stepName].isin(tempres)]
        return fibers


def getNextBig_Samll(stepName,chooseName,mydict,nextfeature):
    themax = 0.0
    themin = 0.0
    fibers = get_stepSYS_ChooseName(stepName, chooseName)  # 选择设备之后的特征
    for i in mydict.keys():
        smaller = float(mydict[i].split(",")[0])
        bigger =float( mydict[i].split(",")[1])
        tempdata = fibers
        print(tempdata,i)
        fibers = fibers[(fibers[i]>= smaller) & (fibers[i] <= bigger)]
        if len(fibers)== 0:
            print("请重新选择 "+str(i)+" 的范围")
            return tempdata, themax, themin
    themax = max(fibers[nextfeature])
    themin = min(fibers[nextfeature])
#    print(fibers)
#    print(themax)
#    print(themin)
    return fibers, themax, themin


# 对于断点率的分析
def getTrend_newmodel_breakpoint(stepName, chooseName, target_label, target_feature, static_feature):
    fibers, themax, themin = getNextBig_Samll(stepName, chooseName, static_feature, target_feature)
    train_featurename = [i for i in static_feature.keys()]     
    train_featurename.append(target_feature)  
    temp = pd.pivot_table(fibers, index=train_featurename, values=[target_label, nopassrate],
                          aggfunc={target_label: np.mean, nopassrate: np.mean})
    temp.to_csv("temp.csv", header=None)
    myheader = [i for i in train_featurename]
    templist = [i for i in list(temp.columns.values)]
    myheader.extend(templist)    
    fibers = pd.read_csv("temp.csv", header=None, names=myheader)
    fibers = fibers.sort_values([target_feature], ascending=[1]).reset_index(drop=True).drop_duplicates() 
    print(fibers)
    X = fibers.loc[:, target_feature].values
    Y = fibers.loc[:, target_label].values
    Z = fibers.loc[:, nopassrate].values
    return X, Y, X, Z




