# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 08:55:40 2021

@author: A2433
"""
import pandas as pd
import numpy as np
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
import shutil
import glob
import os

save_dir = os.path.join('.\escape_pics')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    
first = Tk()
first.title('G_AI_R')
user_input = tk.StringVar(first)
function = IntVar()
weekly_check = 0

def start(path,pb1):
    path_list = path.split('\\')
    for net_address in path_list:
        if len(net_address) != 0:
            break
    first.update()
    pb1["value"] = 0
    if function.get() == 1:
        weekly_check = 1
    else:
        weekly_check = 0
    lot = path.split('\\')[-1]
    lot_path = os.path.join(save_dir,lot)
    if not os.path.exists(lot_path):
        os.makedirs(lot_path)
    if 'Panel' in os.listdir(path)[0]:
        all_csv = [os.path.join(path,i,'AI.csv') for i in os.listdir(path)]
    else:
        all_csv = glob.glob(os.path.join(path,'**\AI.csv'),recursive=True)
    change = 100/len(all_csv)
    sum_df = pd.DataFrame()
    for csv_path in all_csv:
        first.update()
        pb1['value'] += change
        try:   
            df = pd.read_csv(csv_path,header=9)
            sum_df = pd.concat([sum_df,df])
            if len(df.dropna(subset=['AI_Flag'])) == 0:
                    but.pack()
                    pb1.destroy()
                    error.pack()
                    break
            if weekly_check == 1:  
                df.dropna(subset=['VRS_Judge'])
                
                df = df[(df.AI_Flag == 'OK')]
                df['VRS_Judge'] = df['VRS_Judge'].fillna('OK')
                df = df[(df.VRS_Judge != 'OK')].reset_index(drop=True)
                target = 'VRS_Judge'
            else:
                target = 'AI_Flag'
            for c in df.index:
                first.update()
                if not os.path.exists(os.path.join(lot_path,df.iloc[c][target][:3])):
                    os.makedirs(os.path.join(lot_path,df.iloc[c][target][:3]))
                purpose = os.path.join(lot_path,df.iloc[c][target][:3],df.iloc[c]['AVI_Image_Path'].split('\\')[-1])
                shutil.copyfile(df.iloc[c]['AVI_Image_Path'].replace('\\192.168.0.111\\','\\{}\\'.format(net_address)), purpose)
        except:
            pass
    
    
    if weekly_check ==1:
        sum_df['VRS_Judge'] = sum_df['VRS_Judge'].fillna('OK')
        sum_df.to_csv(os.path.join(lot_path,'result2.csv'),index=False)
        ai_list = sum_df.groupby('AI_Flag').first().reset_index().AI_Flag.tolist()
        ai_list.remove('OK')
        ai_list.append('OK')
        df_columns = ['VRS/AI'] + ai_list
        df_content = []
        #sum_df[sum_df.VRS_Judge.str.match('Copper')].to_csv(os.path.join(lot_path,'result2.csv'),index=False)
        for a in ai_list:
            ans = sum_df[sum_df.VRS_Judge.str.match(a[:2])].groupby('AI_Flag').count().reset_index()
            
            ans_list = []
            for b in ai_list:
                try:
                    ans_list.append(ans.loc[ans.AI_Flag==b,'VRS_Judge'].tolist()[0])
                except:
                    ans_list.append(0)
            df_content.append([a] + ans_list)
        result_df = pd.DataFrame(np.array(df_content),columns = df_columns)
        result_df.to_csv(os.path.join(lot_path,'result.csv'),index=False)
            
    
    but.pack()    
    pb1.destroy()
                    
                    
        
        
        
        
    
def get_result():
    error.pack_forget()
    but.pack_forget()
    first.update_idletasks()
    search_path = user_input.get()
    pb1 = Progressbar(first, orient='horizontal', length=300, mode='determinate')
    pb1.pack(expand=True)
    start(search_path,pb1)
    
if __name__ == '__main__':
    first.geometry("360x150")
    textboxes = tk.Canvas(first, width = 360, height = 80,  relief = 'raised')
    textboxes.pack()
    lbel = tk.Label(first, text='Insert Path:')
    lbel.config(font=('helvetica', 17))
    textboxes.create_window(100, 50, window=lbel)
    e = tk.Entry (first, textvariable=user_input)
    textboxes.create_window(250, 50, window=e)
    c = Checkbutton(first, text = "Weekly Check", variable=function)
    c.pack()
    but=Button(first, text="Submit", command=get_result)
    but.pack()
    error = tk.Label(first, text='No AI ans',fg='#4A7A8C')
    first.mainloop()