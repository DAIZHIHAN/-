# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:01:28 2020

@author: Troy
"""
import json
import Mainsystem_algo as MA
class AC_calss:
    def __init__(self,Name='',Location='',Company='',Temp_return='',Temp_control='',Power='',Suspend='',
                 Mode='',Meter_AC='',Meter_SC='',Normal='',Holiday='',Error_code=''):    
        self.Name=Name
        self.Location=Location
        self.Company=Company
        self.Temp_return=Temp_return
        self.Temp_control=Temp_control
        self.Power=Power
        self.Suspend=Suspend
        self.Mode=Mode
        self.Meter_AC=Meter_AC
        self.Meter_SC=Meter_SC
        self.Normal=Normal
        self.Holiday=Holiday
        self.Error_code=Error_code

def AC_obj(json_dict): #內有當前溫度，模式，耗電量
    AC_obj_list=[]
    AC_number=0
    for AC in json_dict["Setting"]:     
        AC_Temp_control=json_dict["Setting"][AC]["Temp_control"]
        AC_Mode=json_dict["Setting"][AC]["Mode"]
        if AC_Mode=='Coordinating':
            AC_Meter=json_dict["Setting"][AC]["Meter_AC"]
            SC_Meter=json_dict["Setting"][AC]["Meter_SC"]    
            AC_Name=json_dict["Setting"][AC]["Name"]  
            locals()['AC'+str(AC_number)]=AC_calss(Temp_control=AC_Temp_control,Mode=AC_Mode,Meter_AC=AC_Meter,Meter_SC=SC_Meter,Name=AC_Name)      
            AC_obj_list.append(locals()['AC'+str(AC_number)])
        else:
            locals()['AC'+str(AC_number)]=AC_calss(Temp_control=AC_Temp_control,Mode=AC_Mode)
            AC_obj_list.append(locals()['AC'+str(AC_number)])
        AC_number+=1
    return AC_obj_list,AC_number  #回傳空調物件和空調數
        

if __name__ == '__main__':  
    init_Time,init_cool_Time,normal_time=0.001,0.001,0.001
    with open("Configuration.json",'rb') as cf:
        json_imf=cf.read()
        json_imf=json.loads(json_imf)       
    AC,AC_number=AC_obj(json_imf)   
    
    for i in range(AC_number):      
        if AC[i].Mode=='Coordinating':             
            MA.main(AC[i].Temp_control,init_Time,init_cool_Time,normal_time,json_imf['Algo_setting']['Coordinating']['Temp_lower'],json_imf['Algo_setting']['Coordinating']['Temp_upper'])
                                          
        else:#非協調控制時
            pass
        
    
        
    
    
    


