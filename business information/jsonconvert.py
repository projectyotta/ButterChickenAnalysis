import json
from pprint import pprint

with open('4-seasons-curry-and-kabab-crofton.json') as data_file:    
    data = json.load(data_file)

"""
what all columns do we need in here 
1. working hours monday 
2. working hours tuesday 
3. working hours wednesday 
4. working hours thursday 
5. working hours friday 
6. working hours saturday 
7. working hours sunday 



pprint(data['working_hours'][0]['Mon'])

