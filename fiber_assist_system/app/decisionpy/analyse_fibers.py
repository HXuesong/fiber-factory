# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 10:09:00 2017
最终版本的光纤数据分析（包含断点率）
@author: Administrator
"""

import app.decisionpy.hdfsClient as hdfsClient
import pandas as pd
import numpy as np
from numpy import mean, std
from sklearn.ensemble import RandomForestRegressor
# import pylab as pl
from scipy.interpolate import interp1d
from sklearn import tree as TreeModel
from sklearn import linear_model
import math

hdfs_conf = {
    'server_url': 'http://172.23.27.203:50070',
    'cache_days': 3,
    'user': 'dm'
}

loc_conf = {
    'final_table_local_path': 'final_table.csv',
    'nearest_point_table_local_path': 'nearest_point_table.csv',
    'merged_point_table_local_path': 'merged_point_table.csv',
    'feature_names': 'feature_names.csv',

    'final_table_remote_path': '/user/dm/final_table.csv',
    'nearest_point_table_remote_path': '/user/dm/nearest_point_table.csv',
    'merged_point_table_remote_path': '/user/dm/merged_point_table.csv',
    'feature_names_remote_path': '/user/dm/feature_names_table.csv',
}

c = hdfsClient.HdfsClient(conf=hdfs_conf)
fibersData = c.get_table(loc_conf['nearest_point_table_local_path'], loc_conf['nearest_point_table_remote_path'])  #从hdfs得到最终的完整大表
featurenames = ['光纤总长度', 'fiber_step_lens_ratio', '预计soot_VAD沉积', '实际soot_VAD沉积', '包层直径上_VAD沉积', '包层直径中_VAD沉积',
                '包层直径下_VAD沉积', '沉积实际长度_VAD烧结', '烧结芯棒长度_VAD烧结', '长度_PK2600芯棒', '位置_PK2600芯棒', 'DeltaPlus检验值_PK2600芯棒',
                'DeltaMinus检验值_PK2600芯棒', 'DeltaTotal检验值_PK2600芯棒', 'OD_Core检验值_PK2600芯棒', 'OD_Clad检验值_PK2600芯棒',
                'CoreSlope检验值_PK2600芯棒', 'D_d检验值_PK2600芯棒', 'Non_core检验值_PK2600芯棒', 'Non_clad检验值_PK2600芯棒',
                'A_esi检验值_PK2600芯棒', 'Index1检验值_PK2600芯棒', 'Index2检验值_PK2600芯棒', '实际有效长度_拉伸', '目标直径_拉伸', '拉伸长度_拉伸',
                'D1处直径_拉伸', 'D2处直径_拉伸', 'D3处直径_拉伸', 'D4处直径_拉伸', 'D5处直径_拉伸', '分切后长度_粗切', '原芯棒长度_粗切', '精切前长度_精切',
                '精切后长度_精切', '最大跳动值_OVD跳动测试', '总长_OVD成品检', '假芯棒长度_OVD成品检', '有效长度_OVD成品检', '净重_OVD成品检', '有效预拉长度_OVD成品检',
                '计费长度_OVD成品检', '计费重量_OVD成品检', '计费预拉长度_OVD成品检', 'Bottom_B_OVD成品检', 'Top_A_OVD成品检', 'Cut_Off_OVD成品检',
                '最大直径_OVD成品检', '最小直径_OVD成品检', '平均直径_OVD成品检', '密度_密度测试', '重量_密度测试', '沉积速率_密度测试', 'Soot直径_密度测试',
                '有效长度_密度测试', '重量误差_密度测试']



# fibersData = pd.read_csv("fibers_finallData_1114.csv")
# fiber_breakpointData = pd.read_csv("1201.csv")

stepname = ['VAD塔线', 'VAD烧结塔线', '拉伸塔线', 'OVD塔线']
Fibers_level = '等级'  # 光纤等级的列名
bad_level = "不合格"  # 光纤不合格的等级
Fibers_code = "芯棒编码_密度测试"
breakpoint = "断点率"
breakflag = '小盘筛选长度'
feature_importance = 0.00  # 特征的重要系数
samplenumoffibers = 5  # 光纤数据采样后的最少个数
trendstep = 0.23  # 画图时的趋势线的部署

print(list(fibersData.columns.values))


def getBreakpointData():
    data = fibersData

    data['是否标准盘'] = data[breakflag] - 48.0

    fiber_data_temp = data.loc[:, [Fibers_code, '是否标准盘', breakflag]]

    def break_count(group):
        count = 0
        for i in group:
            if i < 0:
                count = count + 1
        return count

    t1 = pd.pivot_table(fiber_data_temp, index=[Fibers_code], values=['是否标准盘'], aggfunc={'是否标准盘': break_count})
    t1.to_csv("temp1.csv", header=None)
    t3 = pd.pivot_table(fiber_data_temp, index=[Fibers_code], values=[breakflag], aggfunc=np.sum)
    t3.to_csv("temp3.csv", header=None)

    f1 = pd.read_csv("temp1.csv", header=None, names=[Fibers_code, '断点次数'])
    f3 = pd.read_csv("temp3.csv", header=None, names=[Fibers_code, '光纤总长度'])

    fi = pd.merge(f1, f3, on=[Fibers_code])
    fi = fi.drop_duplicates()
    fi['断点率'] = fi['断点次数'] * 1.0 / fi['光纤总长度']
    data = pd.merge(data, fi, how='inner', on=Fibers_code)
    return data

fiber_breakpointData = getBreakpointData()


'''
获得不合格率
'''


def get_Qualified_rate(group):
    count = 0
    for i in group:
        if i == bad_level:
            count = count + 1
    return (count) * 1.0 / len(group)





'''
#获取阶段名
'''


def get_stepName():
    step = [i for i in stepname]
    res = ";".join(step)
    return res


'''
#获取每个阶段可以选择的设备名
'''


def get_step_chooseName(stepName):
    data = fibersData
    print(fibersData)
    if len(stepName) == 0:
        stepName = stepname[0]
    choosename = list(set(data.loc[:, stepName].values))
    print(choosename)
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
    fibers = fibersData.loc[:, tempfeature]
    step = stepname
    res = {}
    for i in step:
        temp = get_step_chooseName(i).split(";")
        for sy in temp:
            tempdata = fibers[fibers[i] == sy]
            allcount = len(tempdata)
            nopasscount = len(tempdata[tempdata[Fibers_level] == bad_level])
            res[i + ":" + sy] = (allcount - nopasscount) * 1.0 / (allcount + 1)
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


'''
#特征选择，根据重要系数排名
#用决策树的信息增益来进行特征选择
#返回每个特征的重要系数（大于feature_importance的特征名）
'''


def chooseFeature(label, stepName, chooseName):
    fibers = get_stepSYS_ChooseName(stepName, chooseName)
    X = fibers.loc[:, featurenames]
    Y = fibers.loc[:, label]
    names = list(X.columns.values)
    df = TreeModel.DecisionTreeRegressor(random_state=42)
    df.fit(X, Y)
    mylist = sorted(zip(map(lambda x: round(x, 4), df.feature_importances_), names), reverse=True)
    resdict = {}
    for i in mylist:
        if i[0] > feature_importance:
            templist = [float("{0:.2f}".format(yt)) for yt in fibers.loc[:, i[1]].values]
            templens = len(set(templist))
            print(i[1], templens)
            if templens > 1:
                resdict[i[1]] = i[0]
    return resdict


'''
与阶段及设备无关
'''


def chooseFeature_TopK(label):
    fibers = fibersData
    X = fibers.loc[:, featurenames]
    Y = fibers.loc[:, label]
    names = list(X.columns.values)
    df = TreeModel.DecisionTreeRegressor(random_state=42)
    df.fit(X, Y)
    mylist = sorted(zip(map(lambda x: round(x, 4), df.feature_importances_), names),
                    reverse=True)
    resdict = {}
    mysum = 0.0
    for i in mylist:
        if i[0] > feature_importance:
            templens = len(set(fibers.loc[:, i[1]].values))
            print(i[1], templens)
            if templens > 1:
                resdict[i[1]] = i[0]
                mysum = mysum + i[0]

    for key in resdict.keys():
        resdict[key] = resdict[key] * 1.0 / mysum
    return resdict


'''
返回所选择的特征的原始的最大最小值
选择的特征用;隔开
默认全选
'''


def get_feature_min_max(chooseFeatures):
    fibers = fibersData
    if len(chooseFeatures) == 0:
        featurelist = [i for i in featurenames]
    else:
        featurelist = chooseFeatures.split(";")
    resdict = {}
    for i in featurelist:
        tt = fibers[i].values
        t0 = min(tt)
        t0 = float("{0:.3f}".format(t0))
        t1 = max(tt)
        t1 = float("{0:.3f}".format(t1))
        resdict[i] = str(t0) + "," + str(t1)
    return resdict


'''
#曲线分析
#根据上一个的值，来选择下一个的值
(阶段名，选择的设备，{'密度'：'0.3,0.31','长度'：'0.3,0.31'},"重量")
#注意有判断的条件：数据量小于samplenumoffibers时，返回None,None,None
'''


def getNextBig_Samll(stepName, chooseName, mydict, nextfeature, target_label):
    fibers = get_stepSYS_ChooseName(stepName, chooseName)  # 选择设备之后的特征
    train_featurename = [i for i in mydict.keys()]
    train_featurename.append(nextfeature)
    train_featurename.append(target_label)
    train_featurename.append(Fibers_level)
    fibers = fibers.loc[:, train_featurename]
    for i in mydict.keys():
        smaller = float(mydict[i].split(",")[0])
        bigger = float(mydict[i].split(",")[1])
        fibers = fibers[(fibers[i] >= smaller) & (fibers[i] <= bigger)]
        if len(fibers) <= samplenumoffibers:
            print("画曲线部分，有效样本数过少：请重新选择 " + str(i) + " 的范围")
            return 404, fibers, 0, 0
    themax = max(fibers[nextfeature])
    themin = min(fibers[nextfeature])
    return 0, fibers, themax, themin


'''
画曲线
阶段：stepName
设备：chooseName
target_label = "ECC"
target_feature = "最大跳动值"
static_feature ={ }# {"密度":"0.4,1","重量":"46000,50000"}#{}#
'''


def getTrend_newmodel(stepName, chooseName, target_label, target_feature, static_feature, jie=2):
    flag, fibers, themax, themin = getNextBig_Samll(stepName, chooseName, static_feature, target_feature, target_label)
    if flag == 404:
        print("画曲线部分，有效样本数过少：请重新选择特征范围")
        return None, None, None, None
    else:
        train_featurename = [i for i in static_feature.keys()]
        train_featurename.append(target_feature)

        def get_Qualified_rate(group):
            count = 0
            for i in group:
                if i == bad_level:
                    count = count + 1
            return float("{0:.3f}".format((count) * 1.0 / (len(group) + 0.1)))

        temp_target_feature = [float("{0:.3f}".format(i)) for i in fibers.loc[:, target_feature].values]
        temp_target_label = [float("{0:.3f}".format(i)) for i in fibers.loc[:, target_label].values]
        fibers[target_feature] = [i for i in temp_target_feature]
        fibers[target_label] = [i for i in temp_target_label]

        temp = pd.pivot_table(fibers, index=target_feature, values=[target_label, Fibers_level],
                              aggfunc={target_label: np.mean, Fibers_level: get_Qualified_rate})
        temp.to_csv("getTrend_newmodel_temp.csv", header=None)
        myheader = [target_feature]
        templist = [i for i in list(temp.columns.values)]
        myheader.extend(templist)
        fibers = pd.read_csv("getTrend_newmodel_temp.csv", header=None, names=myheader)
        fibers = fibers.sort_values([target_feature], ascending=[1]).reset_index(drop=True).drop_duplicates()
        X = [float("{0:.3f}".format(i)) for i in fibers.loc[:, target_feature].values]
        Y = [float("{0:.3f}".format(i)) for i in fibers.loc[:, target_label].values]
        Z = [float("{0:.3f}".format(i)) for i in fibers.loc[:, Fibers_level].values]

        if len(X) >= 100:
            mywindows = int(math.ceil(len(X) * 0.2 * trendstep))
        else:
            mywindows = int(math.ceil(len(X) * 1.0 * trendstep))

        # newX = []
        #
        #        for idx, x_value in enumerate(Y):
        #            if idx < 8:
        #                newX.append(np.average(Y[idx:idx+mywindows]))
        #            else:
        #                newX.append(np.average(Y[idx-8:idx+1]))
        #        print(newX)

        fY = pd.Series(Y).rolling(window=mywindows, min_periods=1, center=True).mean()
        fZ = pd.Series(Z).rolling(window=mywindows, min_periods=1, center=True).mean()

        fY = pd.Series(fY).rolling(window=mywindows, min_periods=1, center=True).mean()
        fZ = pd.Series(fZ).rolling(window=mywindows, min_periods=1, center=True).mean()

        ry = pd.Series(fY).rolling(window=mywindows, min_periods=1, center=True).mean()
        rz = pd.Series(fZ).rolling(window=mywindows, min_periods=1, center=True).mean()

        formulae = np.polyfit(X, ry, jie)
        print("test")
        print(formulae)
        if formulae[-1] > 0.0:
            tempvaluesb = "(" + str("%.3e" % (formulae[-1])) + ")"
        else:
            tempvaluesb = "(" + str("%.3e" % (formulae[-1])) + ")"

        myform = target_label + " = " + tempvaluesb
        for i in range(jie):
            if abs(formulae[i] - 0.0) > 0.0000001:
                if formulae[i] > 0.0:
                    # tempvalues = str("%.3e"%(formulae[i]))
                    tempvalues = "(" + str("%.3e" % (formulae[i])) + ")"
                else:
                    tempvalues = "(" + str("%.3e" % (formulae[i])) + ")"
                if jie - i > 1:
                    myform = myform + "+" + target_feature + '^' + str(jie - i) + "*" + tempvalues
                else:
                    myform = myform + "+" + target_feature + "*" + tempvalues
        print("影响因子分析：" + myform)
        return X, Y, Z, ry, rz, myform


'''
#表格型的规则
1.得到树模型 get_model_dot(target_label, features)
2.解析树 def gettree(filename)
3.形成规则 find_rule(stepName, chooseName, target_label, featurestring, min_samples_leaf=10 ,max_depth=4)
'''


def get_model_dot(stepName, chooseName, target_label, featurestring, minsamplesleaf, maxdepth):
    fibers = get_stepSYS_ChooseName(stepName, chooseName)  # 选择设备之后的有效数据
    if len(featurestring) == 0:
        myfeature = [i for i in featurenames]
    else:
        myfeature = featurestring.split(";")

    mylable = fibers.loc[:, [target_label]]
    fibers_data = fibers.loc[:, myfeature]

    X_train = fibers_data.fillna(0)
    y_train = mylable

    clf = TreeModel.DecisionTreeRegressor(min_samples_leaf=minsamplesleaf, max_depth=maxdepth)
    clf.fit(X_train, y_train)
    mydotname = target_label
    with open(mydotname, 'w') as f:
        f = TreeModel.export_graphviz(clf, out_file=f, feature_names=myfeature)

    myfeature.append(target_label)
    fibers = fibers.loc[:, myfeature]
    print(fibers)

    return fibers, mydotname


def gettree(filename):
    inputfile = open(filename, 'r')
    leaf = dict()
    realtion = dict()
    lastleaf = []
    for line in inputfile:
        if line.find("[label=\"") > -1:
            templeaf = line.strip('\n').split(" [")
            num = int(templeaf[0])
            lables = templeaf[1]
            leaf[num] = lables
            if line.find("label=\"mse =") > -1:
                lastleaf.append(num)
        else:
            if line.find("->") > -1:
                if line.find("[") > -1:
                    tempstr = line.strip('\n').split("[")[0].strip(" ")
                else:
                    tempstr = line.strip('\n').strip(";").strip(" ")
                corr = tempstr.split(" -> ")
                corr1 = int(corr[0].strip(" "))
                corr2 = int(corr[1].strip(" "))
                realtion[corr2] = corr1
    inputfile.close()
    return leaf, realtion, lastleaf


def find_rule(stepName, chooseName, target_label, featurestring, min_samples_leaf=10, max_depth=4):
    fibers, filename = get_model_dot(stepName, chooseName, target_label, featurestring, min_samples_leaf, max_depth)
    sourceFile = fibers
    leaf, realtion, lastleaf = gettree(filename)
    print(leaf, realtion, lastleaf)
    # 得到“结点-左结点-右结点”
    relas = pd.DataFrame(np.array([list(realtion.keys()), list(realtion.values())]).T, columns=['after', 'before'])
    tree = pd.pivot_table(relas, index='before', values='after', aggfunc=[np.min, np.max])
    tree.columns = ['left', 'right']
    if len(tree) == 0:
        print('所选特征不能构造规则，请重新选择')
        return
    # 得到“目标-特征（大于）-特征（小于）”dataframe
    rule = []
    for i in lastleaf:
        flag = 0
        if i in realtion:
            flag = 1
            temp_zi = i
            temp_fu = realtion.get(temp_zi)
            temprule = [i, temp_fu]
            while (flag > 0):
                if temp_fu in realtion:
                    temp_fuu = realtion.get(temp_fu)
                    temprule.append(temp_fuu)
                    temp_fu = temp_fuu
                else:
                    flag = 0
            temprule.reverse()
            lastrule = []
            for i in range(len(temprule)):
                if 'nmse' in leaf.get(temprule[i]):
                    if (i != len(temprule)) and (tree.loc[temprule[i], 'right'] == temprule[i + 1]):
                        lastrule.append(leaf.get(temprule[i]).split('\\')[0].lstrip('label=\"').replace('<', '>'))
                    elif (i != len(temprule)) and (tree.loc[temprule[i], 'left'] == temprule[i + 1]):
                        lastrule.append(leaf.get(temprule[i]).split('\\')[0].lstrip('label=\"'))
                else:
                    lastrule.append(leaf.get(temprule[i]).split('\\')[-1].split(' = ')[-1].replace('\"] ;', '') + \
                                    '(mse:' + leaf.get(temprule[i]).split('\\')[0].split(' = ')[-1].replace('\"] ;',
                                                                                                            '') + ')')
            ts = " -> ".join(lastrule)
            rule.append(ts)
        else:
            if 'nmse' in leaf.get(temprule[i]):
                rule.append(leaf.get(i).split('\\')[0].lstrip('label=\"'))
            else:
                rule.append(leaf.get(i).split('\\')[-1].split(' = ')[-1].replace('\"] ;', '') + \
                            '(mse:' + leaf.get(i).split('\\')[0].split(' = ')[-1].replace('\"] ;', '') + ')')
    ruleDictList = []
    for r in rule:
        ruleDict = {}
        for rr in r.split('->'):
            if '=' in rr:
                ruleDict[rr.split('=')[0].strip()] = ' = ' + rr.split('=')[1]
            else:
                ruleDict['label' + filename.replace(r'./dot/', '').replace('.dot', '')] = rr
        ruleDictList.append(ruleDict)
    ruleDF = pd.DataFrame(ruleDictList)
    for column in ruleDF.columns:
        if 'label' in column:
            label = column
            break
    feat = list(ruleDF.columns)
    feat.remove(label)
    feat = list(set([x.rstrip(' >').rstrip(' <') for x in feat]))
    ruleDF.rename(columns={label: label.lstrip('label')}, inplace=True)
    label = label.lstrip('label')
    print(sourceFile)
    b = pd.DataFrame()
    b['fname'] = sourceFile.columns.tolist()[0:]
    b['min'] = sourceFile.min().tolist()[0:]
    b['max'] = sourceFile.max().tolist()[0:]
    sourceFile = b
    sourceFile = sourceFile.set_index(sourceFile['fname'])
    print(sourceFile)
    for fe in feat:
        ruleDF[fe + ' <'].fillna(' =  ' + str(sourceFile.loc[fe, 'max']), downcast='infer', inplace=True)
        ruleDF[fe + ' >'].fillna(' =  ' + str(sourceFile.loc[fe, 'min']), downcast='infer', inplace=True)
    # 得到规则字典
    columns = ruleDF.columns.tolist()
    columns.remove(label)
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            if columns[i].rstrip(' >').rstrip(' <') == columns[j].rstrip(' >').rstrip(' <'):
                column = columns[i].rstrip(' >').rstrip(' <')
                left = column + ' <'
                right = column + ' >'
                newCol = list(map(
                    lambda l, r: '(' + str(round(float(str(r).replace('=', '').replace(' ', '')),3)) + ',' + str(round(float(str(l).replace('=', '').replace(' ', '')),3)) + ']', ruleDF[left], ruleDF[right]))
                newCol = [x.replace(column, '') if x.strip() == column else x for x in newCol]
                # print('new!!!!!!!!!')
                # print(newCol)
                ruleDF[column] = newCol
                del ruleDF[left]
                del ruleDF[right]
    # 转为结果字典
    results = []
    for i in ruleDF.index:
        result = {}
        for j in ruleDF.columns:
            result[j] = ruleDF.loc[i, j]
        results.append(result)
    return results


'''
树形的规则
'''


class mytree(object):
    def __init__(self, stepName, chooseName, target_label, target_feature, minsamplesleaf=10, maxdepth=4):

        self.stepName = stepName
        self.chooseName = chooseName
        self.minsamplesleaf = minsamplesleaf
        self.maxdepth = maxdepth

        if len(target_feature) == 0:
            self.target_feature = [i for i in featurenames]
        else:
            self.target_feature = target_feature.split(";")

        self.target_label = target_label
        self.data = fibersData
        self.dot_str = ''
        self.leaf_id = []
        self.relation_zf = dict()
        self.node = dict()
        self.node_value = dict()
        self.relation_line = []
        self.left = None
        self.right = None
        self.lrRule = target_label + " = "

    def GetDataPath(self):
        '''get data path'''
        return self.data_path

    def GetData(self):
        '''get the final table'''
        return self.data

    def TrainTree(self):
        '''train the tree'''
        fibers = get_stepSYS_ChooseName(self.stepName, self.chooseName)  # 选择设备之后的有效数据

        mylable = fibers.loc[:, [self.target_label]]
        fibers_data = fibers.loc[:, self.target_feature]
        X_train = fibers_data
        y_train = mylable
        lr = linear_model.LinearRegression(normalize=True).fit(X_train, y_train)
        print("my LR")
        weight = lr.coef_[0]
        formulate = ["(" + str("%.3e" % (lr.intercept_[0])) + ")"]

        tempstring = []
        for myindex in range(len(self.target_feature)):
            if weight[myindex] > 0:
                #                tempsd =str("%.3e"%(weight[myindex]))
                tempsd = "(" + str("%.3e" % (weight[myindex])) + ")"
            else:
                tempsd = "(" + str("%.3e" % (weight[myindex])) + ")"
            tempstring.append(self.target_feature[myindex] + "*" + tempsd)

        formulate.extend(tempstring)
        self.lrRule = self.lrRule + "+".join(formulate)
        print(self.lrRule)

        clf = TreeModel.DecisionTreeRegressor(min_samples_leaf=self.minsamplesleaf, max_depth=self.maxdepth)
        clf.fit(X_train, y_train)
        f = TreeModel.export_graphviz(clf, out_file=None, feature_names=self.target_feature)
        self.dot_str = f

    def FindLeaf(self):
        '''find the leaf id'''
        for line in self.dot_str.split('\n'):
            if '[label=' in line:
                num = int(line.split(' [')[0]) + 1
                if 'label=\"mse' in line:
                    self.leaf_id.append(num)

    def FindRelation(self):
        '''find the relation of son and father'''
        for line in self.dot_str.split('\n'):
            if '[label=' not in line:
                if '->' in line:
                    fu = int(line.split(' -> ')[0]) + 1
                    zi = int(line.split(' -> ')[1].split(' ')[0]) + 1
                    self.relation_zf[zi] = fu

    def FindRelationLine(self):
        '''find the relation line'''
        for line in self.dot_str.split('\n'):
            if '[label=' not in line:
                if '->' in line:
                    self.relation_line.append(line)

    def FindNode(self):
        '''find the node, return its id and name'''
        for line in self.dot_str.split('\n'):
            if '[label=' in line:
                num = int(line.split(' [')[0]) + 1
                if 'label=\"mse' in line:
                    self.node[num] = line.split(' [')[1].strip('\"] ;\n').split('\\n')[-1].split(' = ')[-1]
                else:
                    self.node[num] = line.split('\\n')[0].split('=\"')[1]  # .split(' ')[0]  如果加上这个就是把判断条件分开

    def FindNodeValue(self):
        '''find the node value, return its id and value'''
        for line in self.dot_str.split('\n'):
            if '[label=' in line:
                num = int(line.split(' [')[0]) + 1
                self.node_value[num] = []
                if 'label=\"mse' in line:
                    self.node_value[num].append(float(line.split('\\n')[0].split(' = ')[-1]))
                else:
                    self.node_value[num].append(float(line.split('\\n')[1].split(' = ')[-1]))
                self.node_value[num].append(float(line.split('\\n')[-1].split(' = ')[-1].strip('"] ;\n')))

    def FindSon(self, i, a_list, relation_line):
        '''find all son node'''
        for j in relation_line:
            if str(i) == j.split(' -> ')[0]:
                temp_num = int(j.split(' -> ')[1].split(' ')[0])
                a_list.append(temp_num + 1)
                self.FindSon(temp_num, a_list, relation_line)
        return a_list

    def get_left_right(self):
        '''
        获取哪些左节点，哪些是右节点
        '''
        len_data = len(self.relation_zf)
        left = []
        right = []
        id_pId_list = [(key, value) for key, value in self.relation_zf.items()]

        for i in range(1, len_data):
            temp = []
            for list_i in id_pId_list:
                if list_i[-1] == i:
                    temp.append(list_i[0])
            if temp:
                left.append(min(temp))
                right.append(max(temp))
        self.left = left
        self.right = right

    def get_pre_condition(self, Id, pId):
        '''
        获取父节点的判断条件
        '''
        if Id in self.left:
            return self.node[pId]
        elif Id in self.right:
            return self.node[pId].replace('<=', '>')
        else:
            return None

    def get_rule(self, Id, path):
        '''
        获取未去重的规则
        '''
        start = 1
        end = Id
        rule = []
        for i in range(len(path)):
            rule.append(self.get_pre_condition(end, path[i + 1]))
            end = path[i + 1]
            if end == start:
                break
        return rule

    def rule_filter(self, rule):
        '''
        对规则进行缩小范围处理
        '''
        import pandas as pd

        name_list = [x.split(' ')[0] for x in rule]
        symbol_list = [x.split(' ')[1] for x in rule]
        value_list = [x.split(' ')[2] for x in rule]
        col_name = ['name', 'symbol', 'value']
        frame = pd.DataFrame([name_list, symbol_list, value_list]).T
        frame.columns = col_name
        frame['value'] = frame['value'].astype('float')

        big_frame = frame[frame['symbol'] == '>']
        big_frame = big_frame.groupby(by=['name', 'symbol'], as_index=False, sort=False).max()
        small_frame = frame[frame['symbol'] == '<=']
        small_frame = small_frame.groupby(by=['name', 'symbol'], as_index=False, sort=False).min()
        frame = big_frame.append(small_frame, ignore_index=True)

        name_list = frame['name'].drop_duplicates().tolist()
        rules = []
        for name in name_list:
            if len(frame[frame['name'] == name]) == 1:
                for row in frame[frame['name'] == name].itertuples():
                    rule = str(row.name) + ' ' + str(row.symbol) + ' ' + str(row.value)
                    rules.append(rule)
            else:
                temp_max = frame[frame['name'] == name]['value'].max()
                temp_min = frame[frame['name'] == name]['value'].min()
                rule = str(temp_min) + ' < ' + str(name) + ' <= ' + str(temp_max)
                rules.append(rule)

        rules_str = ' and '.join(rules)
        return rules_str

    def Start(self):
        '''run all find func'''
        self.TrainTree()
        self.FindLeaf()
        self.FindNode()
        self.FindNodeValue()
        self.FindRelation()
        self.FindRelationLine()
        self.get_left_right()

    def ToJson(self):
        '''
        include: {id, pId, name, isempty,
                  label, isleaf, mean, mse}
        '''
        str_temp = '{"json":['
        for key, value in self.node.items():
            temp_list = []
            line = dict()
            if key in self.leaf_id:
                line['id'] = str(key)
                line['pId'] = str(self.relation_zf[key])
                line['name'] = self.node[key]
            else:
                line['id'] = str(key)
                if key == 1:
                    line['pId'] = '0'
                else:
                    line['pId'] = str(self.relation_zf[key])
                line['name'] = self.node[key]
            line['isempty'] = 'false'
            line['label'] = ''
            if key in self.leaf_id:
                line['isleaf'] = 'true'
            else:
                line['isleaf'] = 'false'
            temp_list = self.FindSon(key - 1, temp_list, self.relation_line)
            value_list_mean = [self.node_value[x][1] for x in temp_list if x in self.leaf_id]
            value_list_mean.append(self.node_value[key][1])
            value_list_mse = [self.node_value[x][0] for x in temp_list if x in self.leaf_id]
            value_list_mse.append(self.node_value[key][0])

            if key in self.leaf_id:
                line['mean'] = str(self.node_value[key][1])
                line['mse'] = str(self.node_value[key][0])
            else:
                line['mean'] = str(np.mean(value_list_mean, dtype=np.float16))
                line['mse'] = str(np.mean(value_list_mse, dtype=np.float16))
            str_temp = str_temp + str(line)
            str_temp
            if key != len(self.node):
                str_temp += ','
        str_temp += ']}'
        str_temp = str_temp.replace("'", '"')
        return str_temp

    def ToPath(self):
        '''the path of node to root'''
        str_temp = '{"json":['
        str_temp = str_temp + "{'id': 1, 'path': [1], 'isleaf': 'false', 'rule': ''},"
        for key, value in self.relation_zf.items():
            line = dict()
            path_node_root = dict()
            if value in self.relation_zf.keys():
                flag = 1
                zi = key
                fu = value
                temp_path = [zi, fu]
                while flag == 1:
                    if fu in self.relation_zf.keys():
                        temp_fu_fu = self.relation_zf[fu]
                        temp_path.append(temp_fu_fu)
                        fu = temp_fu_fu
                    else:
                        flag = 0
                path_node_root[key] = temp_path
            else:
                path_node_root[key] = [key, value]
            line['id'] = key
            line['path'] = path_node_root[key]
            if key in self.leaf_id:
                line['isleaf'] = 'true'
            else:
                line['isleaf'] = 'false'
            rule = self.get_rule(key, path_node_root[key])
            rule_str = self.rule_filter(rule)
            line['rule'] = rule_str
            str_temp = str_temp + str(line)
            str_temp
            if key != len(self.relation_zf) + 1:
                str_temp += ','

        str_temp += ']}'
        str_temp = str_temp.replace("'", '"')
        return str_temp


'''
所有阶段及其设备对应的断点率分析
只用光纤数据即可
'''

def get_sys_breakpointrate():
    data = fiber_breakpointData
    print(data)
    tempfeature = [i for i in stepname]
    tempfeature.append(breakpoint)
    fibers = data.loc[:, tempfeature]
    step = stepname
    res = {}
    for i in step:
        temp = get_step_chooseName(i).split(";")
        for sy in temp:
            tempdata = fibers[fibers[i] == sy]
            breakpointratio = float("{0:.5f}".format(mean(tempdata.loc[:, breakpoint].values)))
            res[i + ":" + sy] = breakpointratio
    return res


'''
返回选择的阶段和设备的断点率
'''


def get_breakpointrate_stepAndsys(stepName, chooseName):
    fibers = fiber_breakpointData
    tempfeature = [stepName]
    tempfeature.append(breakpoint)
    fibers = fibers.loc[:, tempfeature]
    res = {}
    temp = chooseName.split(";")
    for sy in temp:
        tempdata = fibers[fibers[stepName] == sy]
        breakpointratio = float("{0:.5f}".format(mean(tempdata.loc[:, breakpoint].values)))
        res[sy] = breakpointratio
    return res


'''
返回选择的阶段和设备的断点率
阶段是多选
'''
# def get_breakpointrate_stepAndsys(stepName,chooseName):
#    fibers = fiber_breakpointData
#    stepname = stepName.split(";")
#    tempfeature = stepName.split(";")
#    tempfeature.append(breakpoint)
#    fibers = fibers.loc[:, tempfeature]
#    res = {}
#    temp = chooseName.split(";")
#    for i in stepname:
#        for sy in temp:
#            tempdata = fibers[fibers[stepName] == sy]
#            breakpointratio = float("{0:.5f}".format(mean(tempdata.loc[:, breakpoint].values)))
#            res[sy] = breakpointratio
#    return res



if __name__ == '__main__':
    stepName = 'VAD烧结塔线'
    print(get_step_chooseName(stepName))
    chooseName = "H;G"
    label = "λc"



    static_feature ={}#,"重量":"50712,54226","沉积速率":"21.04,26.13"}#{}#
    #    mydict = {'长度':'1500,2000'}
    #    nextfeature = "重量"
    target_feature = "沉积速率_密度测试"
    #
    #    se = chooseFeature(label, stepName, chooseName)
    #    print(se)
    #
    X, Y, X1, Z1, yu, form = getTrend_newmodel(stepName, chooseName, label, target_feature, static_feature)
    print('------------')
    print(form)
    print('------------')
    # pl.plot(X, Y,'g')
    # pl.plot(X, Z,'r')
    # pl.show()
    # print(X)
    # print(Y)
    # print(Z)
    #
    target_feature = "预计soot_VAD沉积;实际soot_VAD沉积"
    stepName = 'OVD塔线'
    chooseName = "E;C"
    sub_tree = mytree(stepName, chooseName, label, target_feature)
    sub_tree.Start()
    print('------------')
    print(sub_tree.lrRule)
    print('------------')
    # print(sub_tree.ToPath())
    # print(sub_tree.ToJson())
    #
    #    s1 = get_sys_passrate()
    #    print(s1)
    #
    # s2 = get_sys_breakpointrate()
    # print(s2)
    # bkdata = get_breakpointrate_stepAndsys(stepName, "E;G")
    # data_list = {"status": 200}
    # data_list['data'] = bkdata
    # print(data_list)
    # s4 = chooseFeature_TopK(label)
    # print(s4)
    # #
    # #
    # #
    # #
    # #
    # choose_features = '最大跳动值_OVD跳动测试;重量误差_密度测试;Top_A_OVD成品检'
    # rule = find_rule(stepName,chooseName,label,choose_features,max_depth=7)
    # print(rule)




