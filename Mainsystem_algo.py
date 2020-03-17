# -*- coding: utf-8 -*-

#功能:演算法
from datetime import datetime
import Mainsystem_main as Mm
import json
from time import sleep 

dic={'Temp_20C':'20','Temp_21C':'21','Temp_22C':'22','Temp_23C':'23','Temp_24C':'24','Temp_25C':'25','Temp_26C':'26'} #包含13~30度的控制碼，彼此間格2度
############收即使的耗電量(空調+冷凍櫃)##############
def catch_data(): #抓取到的資料格式>>>{'大廳空調': 100003, '客席區空調': 100003}
    Meter_list={}
    with open("Configuration.json",'rb') as cf:
        json_imf=cf.read()
        json_imf=json.loads(json_imf)   
    AC_list,AC_number=Mm.AC_obj(json_imf)
    cf.close()
    for i in range(AC_number):
        if AC_list[i].Mode=='Coordinating':
            # dic={AC_list[i].Name:int(AC_list[i].Meter_AC)+int(AC_list[i].Meter_SC)}
            # Meter_list.update(dic)     
                               
            return int(AC_list[i].Meter_AC)+int(AC_list[i].Meter_SC)


##############計算剛運轉的耗電量和減溫一次的耗電量##############
def init_total_C(Temp,T1,T2,Temp_lower,Temp_upper): 
    set_time=[T1,T2]
    time_start=datetime.now() 
    for i in range(2):
        start=1 
        if i==1:    
           Temp-=1     
        if Temp>=Temp_lower and Temp<=Temp_upper:     
            print(dic['Temp_'+str(Temp)+'C'])  #送紅外線
            while(start):
                time_end=datetime.now()
                if((time_end-time_start).seconds<set_time[i]*60 and start): 
                    print('data collect...')
                    sleep(4)
                else:
                    print('data collect over')      
                    if i==0:       
                        collect=catch_data()
                    else:          
                        collect2=catch_data()
                    start=0
        else:
            print('below min_temp or over max_temp')    
            
    return collect,collect2
    
####################計算耗電量##############################
def total_C(Temp,T3):   
    print(dic['Temp_'+str(Temp)+'C'])  #送紅外線
    start=1        
    time_start=datetime.now() 
    while(start):
        time_end=datetime.now()
        if((time_end-time_start).seconds<T3*60 and start):                
            print('data collect...')
            sleep(4)
        else:
            print('data collect over')
            collect=catch_data()
            start=0           
    return collect

###############協調控制演算法########################
def control(pre,mode,Temp,T3,Temp_lower,Temp_upper): 
    if Temp>=Temp_lower and Temp<=Temp_upper:                   
        if(mode):     
            Temp+=1      
        else:
            Temp-=1     
        while(1):  
            if Temp>=Temp_lower and Temp<=Temp_upper:         
                current=total_C(str(Temp),T3) 
                if(current-pre<0 and mode): 
                    pre=current       
                    Temp+=1
                elif(current-pre<0 and not mode):
                    pre=current    
                    Temp-=1         
                elif(not current-pre<0 and mode):   #如果>0就轉換模式
                    pre=current       
                    Temp-=1
                    mode=0
                elif(not current-pre<0 and not mode):
                    pre=current       
                    Temp+=1            
                    mode=1
            else:
                print('below min_temp or over max_temp')            
    else:
        print('below min_temp or over max_temp')       


def main(Temp,T1,T2,T3,Temp_lower,Temp_upper):
    if Temp>=Temp_lower and Temp<=Temp_upper:     
        init_C,init_cool_C=init_total_C(int(Temp),T1,T2,int(Temp_lower),int(Temp_upper)) #需要先得到初值的2個總耗電量才能做計算
        if(init_cool_C - init_C<0):   #mode=1 為加熱模式 mode=0為降溫模式 
            mode=0
            control(init_cool_C,mode,int(Temp),T3,int(Temp_lower),int(Temp_upper)) 
        else:
            mode=1
            control(init_cool_C,mode,int(Temp),T3,int(Temp_lower),int(Temp_upper)) 
    else:
        print('below min_temp or over max_temp')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    