import numpy as np
from sklearn.datasets import make_blobs
from sklearn import linear_model

x = ['Cladding Dia.', 'Cladding Cir.', 'Fiber Dia.', 'OCE', 'Fiber Cir.', 'ECC', '芯不圆度', 'Primary coating Dia.',
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

print(x[0])