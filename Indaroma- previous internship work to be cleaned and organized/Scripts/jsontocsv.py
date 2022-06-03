"""
data = []
f = open('C:\\Users\\raosa\\AnacondaProjects\\indaroma-dataviz-pythoncode\\20101.json')
lines = f.read().splitlines()
f.close()
for line in lines:
    data.append(line)

def list_to_dict(li):  
     dct = {}  
     for item in data:  
         if dct.has_key(item):  
             dct[item] = dct[item] + 1  
         else:  
             dct[item] = 1  
     return dct  

data1= list_to_dict(data)

xyz=data1['businesses'][2]['id']
print(xyz)
"""
import json
json2 = json.load('C:\\Users\\raosa\\AnacondaProjects\\indaroma-dataviz-pythoncode\\20101.json')
json1_data = json2[0]
datapoints = json1_data['businesses'][2]['id']