# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:42:35 2017
feature selection
@author: Administrator
"""
import pandas as pd
import numpy as np
from numpy import mean, std
from sklearn.ensemble import RandomForestRegressor
# import pylab as pl
from scipy.interpolate import interp1d
from sklearn import tree as TreeModel

featurenames = ['pk_ration', '小盘筛选长度', '密度', '重量', '沉积速率', 'SOOT直径', '有效长度', '重量误差', '长度', '测试参考值', '跳动合格', '手工判定合格',
                '最大跳动值(对接前)', '最大跳动值', 'test_lens_sum', 'fiber_step_lens', 'fiber_step_lens_ratio', '合格', '位置', '反面',
                'DeltaPlus检验值', 'DeltaMinus检验值', 'DeltaTotal检验值', 'OD_Core检验值', 'OD_Clad检验值', 'CoreSlope检验值', 'D/d检验值',
                'Non_Core检验值', 'Non_Clad检验值', 'A_esi检验值', 'Index1检验值', 'Index2检验值']
target = ['Cladding Dia.', 'Cladding Cir.', 'Fiber Dia.', 'OCE', 'Fiber Cir.', 'ECC', '芯不圆度', 'Primary coating Dia.',
          'PCE', 'Core Dia.', '测试长度', 'Att.-1310nm', '1310nmA端衰减', '1310nmB端衰减', 'Att.-1550nm', '1550nmA端衰减',
          '1550nmB端衰减', '1310端差', '1550端差', '1310nm衰减不连续性', '1550nm衰减不连续性', '1310nm衰减不均匀性', '1550nm衰减不均匀性',
          'Att.-1383nm', 'Att.-1625nm', '1310MFD', '1550MFD', 'λc', '1383谱衰减', '1625谱衰减', '1285-1330nm范围内最大衰减与1310nm相比',
          '1525-1575nm范围内最大衰减与1550nm相比', '1310谱衰减', '1550谱衰减', '1460谱衰减', '宏弯衰减/弯曲半径7.5mm圈数1(1550nm)',
          '宏弯衰减/弯曲半径7.5 mm圈数1(1625nm)', '宏弯衰减/弯曲半径10mm圈数1(1550nm)', '宏弯衰减/弯曲半径10mm圈数1(1625nm)',
          '宏弯衰减/弯曲半径15mm圈数10(1550nm)', '宏弯衰减/弯曲半径15mm圈数10(1625nm)', 'Curl.', 'Zero DML.', 'Slope zero DML.',
          '1285-1339nm色散', '1271-1360nm色散', 'Dispersion 1550nm', 'Dispersion 1625nm', '1530-1565nm色散', '1565-1625nm色散',
          'PMD']
keytarget = ['ECC''1310MFD', '1550MFD', 'λc', ]
stepname = ['VAD塔线', 'VAD烧结塔线', '拉伸塔线', 'OVD塔线']
# 关于设备的特征以及等级的特征：
# featuresys = ['拉丝塔号', '等级_x','等级', '等级_y',  '等级', '光纤类型', 'VAD塔线', 'VAD烧结塔线', '拉伸塔线', 'OVD塔线', 'OVD间轴']
file = r"G:\tongding_projrct\app\data\fibers_finallData_1114.csv"
Fibers_level = '等级_x'
bad_level = "不合格"
fibersData = pd.read_csv(file)

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
    choosename = list(set(data.loc[:, stepName].values))
    res = ";".join(choosename)
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
#用随机森林中的信息增益来进行特征选择
#返回每个特征的重要系数
'''


def chooseFeature(label, stepName, chooseName):
    fibers = get_stepSYS_ChooseName(stepName, chooseName)
    X = fibers.loc[:, featurenames]
    Y = fibers.loc[:, label]
    names = list(X.columns.values)
    rf = RandomForestRegressor()
    rf.fit(X, Y)
    mylist = sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names),
                    reverse=True)
    resdict = {}
    for i in mylist:
        resdict[i[1]] = i[0]
    return resdict


'''
原始的、与选择的设备无关
返回所选择的特征的原始的最大最小值
选择的特征用;隔开
默认全选
'''


def get_feature_min_max(chooseFeatures):
    fibers = fibersData
    if len(chooseFeatures) == 0:
        featurelist = featurenames
    else:
        featurelist = chooseFeatures.split(";")
    resdict = {}
    for i in featurelist:
        tt = fibers[i].values
        t0 = min(tt)
        t1 = max(tt)
        resdict[i] = str(t0) + "," + str(t1)
    return resdict


'''       
#曲线分析
#根据上一个的值，来选择下一个的值
(阶段名，选择的设备，{'密度'：'0.3,0.31','长度'：'0.3,0.31'},"重量")

#注意有判断的条件
'''


def getNextBig_Samll(stepName, chooseName, mydict, nextfeature):
    themax = 0.0
    themin = 0.0
    fibers = get_stepSYS_ChooseName(stepName, chooseName)  # 选择设备之后的特征
    for i in mydict.keys():
        smaller = float(mydict[i].split(",")[0])
        bigger = float(mydict[i].split(",")[1])
        tempdata = fibers
        fibers = fibers[(fibers[i] >= smaller) & (fibers[i] < bigger)]
        if len(fibers) == 0:
            print("请重新选择 " + str(i) + " 的范围")
            return tempdata, themax, themin
    themax = max(fibers[nextfeature])
    themin = min(fibers[nextfeature])
    #    print(fibers)
    #    print(themax)
    #    print(themin)
    return fibers, themax, themin


'''
画曲线
阶段：stepName
设备：chooseName
target_label = "ECC"  
target_feature = "最大跳动值" 
static_feature ={ }# {"密度":"0.4,1","重量":"46000,50000"}#{}#
'''


def getTrend_newmodel(stepName, chooseName, target_label, target_feature, static_feature):
    # 1.获得数据，不需要训练和测试
    fibers, themax, themin = getNextBig_Samll(stepName, chooseName, static_feature, target_feature)
    train_featurename = [i for i in static_feature.keys()]
    train_featurename.append(target_feature)

    def get_Qualified_rate(group):
        count = 0
        for i in group:
            if i == bad_level:
                count = count + 1
        return (count) * 1.0 / len(group)

    temp = pd.pivot_table(fibers, index=train_featurename, values=[target_label, Fibers_level],
                          aggfunc={target_label: np.mean, Fibers_level: get_Qualified_rate})
    temp.to_csv("temp.csv", header=None)
    myheader = [i for i in train_featurename]
    templist = [i for i in list(temp.columns.values)]
    myheader.extend(templist)
    fibers = pd.read_csv("temp.csv", header=None, names=myheader)
    fibers = fibers.sort_values([target_feature], ascending=[1]).reset_index(drop=True)
    X = fibers.loc[:, target_feature].values
    Y = fibers.loc[:, target_label].values
    Z = fibers.loc[:, Fibers_level].values
    #    f2 = interp1d(X, Y,kind='slinear') #nearest、zero、slinear、
    #    delta = (max(X) - min(X))*1.0/100
    #    Xnew = np.arange(min(X),max(X),delta)
    #    Ynew = f2(Xnew)
    return X, Y, X, Z


'''
#表格型的规则
1.得到树模型 get_model_dot(target_label,features)
2.解析树 def gettree(filename)
3.形成规则 find_rule(stepName,chooseName,target_label,featurestring,min_samples_leaf = 10 ,max_depth = 4)
'''


## target_label是目标，features是选择好的特征，用“；”隔开
def get_model_dot(stepName, chooseName, target_label, featurestring, minsamplesleaf, maxdepth):
    fibers = get_stepSYS_ChooseName(stepName, chooseName)  # 选择设备之后的有效数据
    if len(featurestring) == 0:
        myfeature = featurenames
    else:
        myfeature = featurestring.split(";")

    mylable = fibers.loc[:, [target_label]]
    fibers_data = fibers.loc[:, myfeature]
    X_train = fibers_data
    y_train = mylable

    clf = TreeModel.DecisionTreeRegressor(min_samples_leaf=minsamplesleaf, max_depth=maxdepth)
    clf.fit(X_train, y_train)
    mydotname = target_label
    with open(mydotname, 'w') as f:
        f = TreeModel.export_graphviz(clf, out_file=f, feature_names=myfeature)
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
    # 得到“结点-左结点-右结点”
    relas = pd.DataFrame(np.array([list(realtion.keys()), list(realtion.values())]).T, columns=['after', 'before'])
    tree = pd.pivot_table(relas, index='before', values='after', aggfunc=[np.min, np.max])
    tree.columns = ['left', 'right']
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
    b = pd.DataFrame()
    b['fname'] = sourceFile.columns.tolist()[2:]
    b['min'] = sourceFile.min().tolist()[2:]
    b['max'] = sourceFile.max().tolist()[2:]
    sourceFile = b
    sourceFile = sourceFile.set_index(sourceFile['fname'])
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
                    lambda l, r: '(' + str(r).replace('=', '').replace(' ', '') + ',' + str(l).replace('=', '').replace(
                        ' ', '') + ']', ruleDF[left], ruleDF[right]))
                newCol = [x.replace(column, '') if x.strip() == column else x for x in newCol]
                ruleDF[column] = newCol
                del ruleDF[left];
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
增加的从308行往下
'''


class mytree(object):
    def __init__(self, stepName, chooseName, target_label, target_feature, minsamplesleaf=10, maxdepth=6):
        self.stepName = stepName
        self.chooseName = chooseName
        self.minsamplesleaf = minsamplesleaf
        self.maxdepth = maxdepth

        if len(target_feature) == 0:
            self.target_feature = featurenames
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

    def Start(self):
        '''run all find func'''
        self.TrainTree()
        self.FindLeaf()
        self.FindNode()
        self.FindNodeValue()
        self.FindRelation()
        self.FindRelationLine()

    def ToJson(self):
        '''include: {id, pId, name, isempty,
                    label, isleaf, mean, mse}'''
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
        str_temp = str_temp + "{'id': 1, 'path': [1], 'isleaf': 'false'}"
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
            str_temp = str_temp + str(line)
            str_temp
            if key != len(self.relation_zf) + 1:
                str_temp += ','
        str_temp += ']}'
        str_temp = str_temp.replace("'", '"')
        return str_temp

def get_step_and_sys():
    step = stepname
    res = {}
    for i in step:
        res[i] = get_step_chooseName(i)
    return res

if __name__ == '__main__':
    #    stepName = 'OVD塔线'
    #    chooseName = "E;C"
    #    ll = get_step_chooseName(stepName)
    ##    print(ll)
    #    dd = get_stepSYS_ChooseName(stepName,"E;C")
    ##    print(dd)
    #    label = "ECC"
    ##    print(chooseFeature(label,stepName,""))
    #
    ##    print("特征的最大最小值")
    #    ss = ";".join(featurenames[:3])
    ##    print(get_feature_min_max(ss))
    #
    #    static_feature ={"密度":"0.3,0.4","重量":"46000,56000"}#{}#
    #    mydict = {'密度':'0.3,0.8','长度':'1500,2000'}
    #    nextfeature = "重量"
    #    target_feature = "最大跳动值"
    #
    #    getNextBig_Samll(stepName,chooseName,mydict,nextfeature)
    #    X,Y,X,Z  = getTrend_newmodel(stepName,chooseName,label,target_feature,static_feature)
    ##    pl.plot(Xnew,Ynew,'b')
    #    pl.plot(X, Y,'g')
    #    pl.plot(X, Z,'r')
    #    pl.show()
    #
    #    print(X[:5])
    #    print(Y[:5])
    #    print(Z[:5])
    ###
    #    target_label = "1310MFD"
    #    choose_features = "有效长度;密度;重量"
    #    rule = find_rule(stepName,chooseName,target_label,choose_features)
    #    print(rule)

    target_label = '1310MFD'
    target_feature = "有效长度;密度;重量"
    stepName = 'OVD塔线'
    chooseName = "E;C"
    sub_tree = mytree(stepName, chooseName, target_label, target_feature)
    sub_tree.Start()
    # print(sub_tree.ToPath())
    print(sub_tree.ToJson())
