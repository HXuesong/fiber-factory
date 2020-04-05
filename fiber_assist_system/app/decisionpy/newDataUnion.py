# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:57:29 2017
重新合大表
在pk中[[位置][对应比例]]
暂时不要删选中间的
@author: Administrator
"""

import pandas as pd
import numpy as np
from numpy import mean, std


def simple_core_id(mylist):
    result = []
    for cid in mylist:
        pos_1 = cid[1]
        if '0' <= pos_1 <= '9':
            mycid = cid[:5]
        else:
            mycid = cid[:6]
        result.append(mycid)
    return result


def getfourtabels():
     PK_data = pd.read_excel("E:\\Python_workspace\\Ciber\\Data\\PK data.xlsx")
     PK_data_2 = pd.read_excel("E:\\Python_workspace\\Ciber\\Data\\PK data2.xlsx")
     PK_data = PK_data.append(PK_data_2)
     # print(PK_data.columns)
     # 用一个新的只有位置的newPK来表示
     tempNewPk = PK_data.loc[:, ['芯棒代码', '长度', '位置', '反面']]
     #位置对应的长度
     tempNewPk = tempNewPk[tempNewPk['位置'] != "平均值"]
     tempNewPk['位置'] = [float(str(i).strip(" ")) for i in tempNewPk['位置']]
     tempNewPk['pos_lens'] = abs(tempNewPk['长度']*(tempNewPk['反面']-1)+tempNewPk['位置'])
     tempNewPk['pos_lens_ratio'] = tempNewPk['pos_lens']*1.0/tempNewPk['长度'] 
     temppos = []
     lenlist = tempNewPk['位置'].values
     resverlist = tempNewPk['反面'].values
     for i in range(len(lenlist)):
         if resverlist[i] == 0:
             temppos.append(lenlist[i])
         else:
            temppos.append(0-lenlist[i])            
     tempNewPk['posflag'] = temppos       
         
     #合成两个字符串
     basepk = tempNewPk.loc[:, ['芯棒代码', '长度']].drop_duplicates()
     def set_flag(group):
         temp = [str(i) for i in group]
         temp1 = ";".join(temp)
         return temp1
     
     addPk = pd.pivot_table(tempNewPk, index=['芯棒代码'], values=['posflag', 'pos_lens_ratio'], aggfunc=set_flag)
     addPk['芯棒代码'] = addPk.index
     NewBasedpk = pd.merge(basepk, addPk, how='inner', left_on=['芯棒代码'], right_on=['芯棒代码'])
     
     #core，之后的相连
     core_rod_runout = pd.read_excel("E:\\Python_workspace\\Ciber\\Data\\core rod runout.xlsx")
     core_rod_runout = core_rod_runout.drop(['单据编号', '状态', '芯棒类型', '测试人', '班组', '设备',
        '异常原因', '备注', '建单人', '建单日期'], axis=1)
     core_rod_runout = core_rod_runout.sort_values(['芯棒编码', '测试日期'], ascending=False)
     core_rod_runout = core_rod_runout.drop_duplicates(['芯棒编码'])
     core_rod_runout = core_rod_runout.drop(['测试日期'], axis=1)

     #OVD，之后的相连
     OVD_soot_data = pd.read_excel("E:\\Python_workspace\\Ciber\\Data\\OVD soot data.xlsx") 
     OVD_soot_data = OVD_soot_data[OVD_soot_data['芯棒编码']>'A']
     OVD_soot_data = OVD_soot_data.sort_values(['芯棒编码','测试日期'],ascending=False)
     OVD_soot_data = OVD_soot_data.drop_duplicates(['芯棒编码'])
     OVD_soot_data = OVD_soot_data.drop(['单据编号', '状态', '测试人', '测试日期', '班组', '设备', '备注', '建单人', '建单日期'], axis = 1)


     #fiber
     fiber_data = pd.read_excel(r'E:\Python_workspace\Ciber\Data\fiberdata.xlsx')
     fiber_data['条码'] = [ i.upper() for i in fiber_data['条码'].values]
     fiber_data[u'拉丝塔号']= [ str(i)[:3] for i in fiber_data[u'条码']]
     fiber_data[u'光纤编号'] = [str(i)[3:17] for i in fiber_data[u'条码']]
     fiber_data[u'大盘'] = [str(i)[17:18] for i in fiber_data[u'条码']]
     fiber_data[u'小盘'] = [str(i)[18:] for i in fiber_data[u'条码']] 


     #rod to fiber
     rod_fiber = pd.read_excel(r'E:\Python_workspace\Ciber\Data\rod_fiber.xlsx')
     rod_fiber = rod_fiber.drop(['序号', '厂商', '入库日期'],axis = 1)
    
 
     '''
     1.以PK data为基础，将core join，保留PK data
     '''
     core_inform = pd.merge(NewBasedpk, core_rod_runout, how='inner', left_on=['芯棒代码'], right_on=['芯棒编码'])
     core_inform['simple_id'] = simple_core_id(core_inform['芯棒编码'])
#     core_inform = core_inform.drop(['芯棒代码'],axis = 1)
    
     '''
#     2. join OVD：由于OVD的芯棒编码不同，所以需要进行划分
#     '''
     OVD_soot_data['simple_id'] = simple_core_id(OVD_soot_data['芯棒编码'])

     '''
     3. 将fiber data 也join起来 : 由于OVD中的编码是唯一的，将OVD与fiber相join
     3.1 用光棒-光纤对应编号，先将 OVD_soot_data 中的芯棒编码连起来 “芯棒编码_y”
     3.2 将fiber data 中的条码先进行划分为4部分,然后与 OVD_soot_data 相连接
     '''
     ovd_and_fiber = pd.merge(OVD_soot_data, rod_fiber, how='inner', left_on='芯棒编码', right_on='光棒编号')
     fiber_jon_OVD = pd.merge(fiber_data, ovd_and_fiber, how='inner', left_on=u'光纤编号', right_on=u'光纤编号')
     '''
     4. 将所有的信息相连接，最终初版的打标:将fiber_jon_OVD 与 core_inform 相join
     '''
     fin_data_v0 = pd.merge(fiber_jon_OVD, core_inform, how='inner', on='simple_id')
     
     t3 = pd.pivot_table(fin_data_v0, index=['芯棒编码_x'], values=['小盘筛选长度'], aggfunc=np.sum)
     t3.to_csv("temp3.csv", header=None)
     f3 = pd.read_csv("temp3.csv", header=None,names=['芯棒编码_x', 'test_lens_sum']).drop_duplicates()
     fin_data_v0 = pd.merge(fin_data_v0, f3, on=['芯棒编码_x'])

     fin_data_v0.to_csv("C:\\Users\\Administrator\\Desktop\\ciber\\1122\\fin_data_new_v1.csv",encoding = 'utf8')
     return fin_data_v0


def find_min_diff(ratio,la,lb):
    #la 是比例
    #lb 是位置
    lista = [float(i) for i in la.split(";")]
    listb = [float(i) for i in lb.split(";")]
    temp = [abs(i-ratio) for i in lista]
    tempmin = min(temp)
    tempminpos = temp.index(tempmin)
    
    res = listb[tempminpos]
    pos = abs(res)
    if res > 0:
        resflag = 0
    else:
        resflag = 1
           
    return pos,resflag,lista[tempminpos]


def get_fiberlens_and_ratio():
     #得到简单的4张大表
    fibers = getfourtabels()
     
    #计算长度
    fibers = fibers.sort_values(['光纤编号', '大盘', '小盘'], ascending=[1, 1, 0]).reset_index(drop=True)
    fiber_test_lens = fibers['小盘筛选长度'].values 
    fiber_id = fibers['芯棒编码_x'].values
    
    result_test = [fiber_test_lens[0]]
    sum = fiber_test_lens[0]
    for i in range(1,len(fiber_test_lens)):
        if fiber_id[i] == fiber_id[i-1]:
            sum = sum + fiber_test_lens[i]
            result_test.append(sum)
        else:
            result_test.append(fiber_test_lens[i])
            sum = fiber_test_lens[i]
            
    fibers['fiber_step_lens'] = pd.Series(result_test)
    fibers['fiber_step_lens_ratio'] = pd.Series(result_test)*1.0/fibers['test_lens_sum']

    #添加[位置]，[反面]..然后再与 PK 内连接
    posAndresv = []
    temp_ratio = fibers.loc[:, 'fiber_step_lens_ratio'].values
    temp_la = fibers.loc[:, 'pos_lens_ratio'].values
    temp_lb = fibers.loc[:, 'posflag'].values
    for i in range(0, len(temp_ratio)):
        pos, resflag, rob = find_min_diff(temp_ratio[i], temp_la[i], temp_lb[i])
        posAndresv.append([pos, resflag, rob])
    fibers['mypos_pk'] = [i[0] for i in posAndresv]
    fibers['myresv_pk'] = [i[1] for i in posAndresv]
    fibers['pk_ration'] = [i[2] for i in posAndresv]
    return fibers


def deal_outlier(flist, stdtimes=3):
    avgf = mean(flist)
    stdf = std(flist)
    small = avgf - stdtimes*stdf
    big = avgf + stdtimes*stdf
    result = []
    for i in range(len(flist)):
        if flist[i]<= big and flist[i]>= small:
            result.append(flist[i])
        else:
            result.append(avgf)
    return result
            
if __name__ == '__main__':
    #得到简单的4张大表
    fibers = get_fiberlens_and_ratio()
#    #对fiber中的小盘筛选长度进行处理
#    columse = list(fibers.columns.values)
#    print(columse)
    
    #连接PKdata
    PK_data = pd.read_excel("E:\\Python_workspace\\Ciber\\Data\\PK data.xlsx")
    PK_data_2 = pd.read_excel("E:\\Python_workspace\\Ciber\\Data\\PK data2.xlsx")
    PK_data = PK_data.append(PK_data_2)
    PK_data = PK_data.drop(['单据编号', '状态','操作人', '生产线', '操作日期', '产线代码', '班组代码', '班组名称',
       '职员代码', '设备代码', '设备名称', '长度'], axis=1)
    PK_data = PK_data[PK_data['位置'] != "平均值"]
    PK_data['位置'] = [float(str(i).strip(" ")) for i in PK_data['位置']]

   #得到较粗糙的大表
    fibers = pd.merge(fibers, PK_data, how='left', left_on=['芯棒代码', 'mypos_pk', 'myresv_pk'], right_on=['芯棒代码', '位置', '反面'])
    #分ID：先过滤
    fibers['tempIDlens'] = [len(i) for i in fibers['光棒编号']]
    fibers = fibers[fibers['tempIDlens'] == 11]
    fibers = fibers.drop(['tempIDlens'], axis=1)
    myfiber_id = fibers['光棒编号'].values
    fibers['光纤类型'] = [s[0] for s in myfiber_id]
    fibers['VAD塔线'] = [t[1] for t in myfiber_id]
    fibers['VAD烧结塔线'] = [t[6] for t in myfiber_id]
    fibers['拉伸塔线'] = [t[7] for t in myfiber_id]
    fibers['OVD塔线'] = [t[9] for t in myfiber_id]
    fibers['OVD间轴'] = [t[10] for t in myfiber_id]
    fibers = fibers.drop(['pos_lens_ratio', 'posflag', '芯棒代码', '光纤编号', '大盘', '小盘', '芯棒编码_y', 'simple_id',
                          '条码', '计划物料编码', '实际物料编码', '生产日期', '检验日期', '备注', '光棒编号',' mypos_pk',
                          'myresv_pk'], axis=1)
    columse3 = list(fibers.columns.values)
    # print(columse3)


    #异常值处理
    need_deal_outlier = ['密度', '重量', '沉积速率', 'SOOT直径', '有效长度', '重量误差', '长度', '测试参考值', '跳动合格',
                         '手工判定合格', '最大跳动值(对接前)', '最大跳动值', 'DeltaPlus检验值', 'DeltaMinus检验值',
                         'DeltaTotal检验值', 'OD_Core检验值', 'OD_Clad检验值', 'CoreSlope检验值', 'D/d检验值',
                         'Non_Core检验值', 'Non_Clad检验值', 'A_esi检验值', 'Index1检验值', 'Index2检验值']
    for i in need_deal_outlier:
        temprr = fibers[i].values
        result = deal_outlier(temprr, stdtimes=3)
    fibers[i] = [k for k in result]
    
    fibers.to_csv("C:\\Users\\Administrator\\Desktop\\ciber\\1122\\fibers_finallData_1114.csv", index=None, encoding = 'utf8')
     



'''
目标：fiber中的
target = ['Cladding Dia.', 'Cladding Cir.', 'Fiber Dia.', 'OCE', 'Fiber Cir.', 'ECC', '芯不圆度', 'Primary coating Dia.', 
'PCE', 'Core Dia.', '测试长度', 'Att.-1310nm', '1310nmA端衰减', '1310nmB端衰减', 'Att.-1550nm', 
'1550nmA端衰减', '1550nmB端衰减', '1310端差', '1550端差', '1310nm衰减不连续性', '1550nm衰减不连续性', 
'1310nm衰减不均匀性', '1550nm衰减不均匀性', 'Att.-1383nm', 'Att.-1625nm', '1310MFD', '1550MFD', 
'λc', '1383谱衰减', '1625谱衰减', '1285-1330nm范围内最大衰减与1310nm相比', 
'1525-1575nm范围内最大衰减与1550nm相比', '1310谱衰减', '1550谱衰减', '1460谱衰减', 
'宏弯衰减/弯曲半径7.5mm圈数1(1550nm)', '宏弯衰减/弯曲半径7.5 mm圈数1(1625nm)', 
'宏弯衰减/弯曲半径10mm圈数1(1550nm)', '宏弯衰减/弯曲半径10mm圈数1(1625nm)', 
'宏弯衰减/弯曲半径15mm圈数10(1550nm)', '宏弯衰减/弯曲半径15mm圈数10(1625nm)', 
'Curl.', 'Zero DML.', 'Slope zero DML.', '1285-1339nm色散', 
'1271-1360nm色散', 'Dispersion 1550nm', 'Dispersion 1625nm', 
'1530-1565nm色散', '1565-1625nm色散', 'PMD']

关于设备的特征以及等级的特征：
['拉丝塔号', '等级_x','等级', '等级_y',  '等级', '光纤类型', 'VAD塔线', 'VAD烧结塔线', '拉伸塔线', 'OVD塔线', 'OVD间轴']

数值型的特征：
['pk_ration','小盘筛选长度', '密度', '重量', '沉积速率', 'SOOT直径', '有效长度', '重量误差', '长度', '测试参考值', '跳动合格', '手工判定合格', '最大跳动值(对接前)', '最大跳动值', 'test_lens_sum', 'fiber_step_lens', 'fiber_step_lens_ratio', '合格', '位置', '反面', 'DeltaPlus检验值', 'DeltaMinus检验值', 'DeltaTotal检验值', 'OD_Core检验值', 'OD_Clad检验值', 'CoreSlope检验值', 'D/d检验值', 'Non_Core检验值', 'Non_Clad检验值', 'A_esi检验值', 'Index1检验值', 'Index2检验值']

'''
   
    
        
        

      




    