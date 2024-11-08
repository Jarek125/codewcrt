from encodings.utf_8 import encode
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import time

from uiautomation import WindowControl, MenuControl


wx = WindowControl(Name='微信')
print(wx)
wx.SwitchToThisWindow()

 # 获取会话列表控件
hw = wx.ListControl(Name='会话')
print('寻找会话控制件绑定', hw)

 #读取自动回复内容
df = pd.read_csv('自动回复内容.csv', encoding='utf-8')

 # 在这里指定想要的聊天框名称
target_chat_name = '' # 替换为你的目标聊天框名称
while True:
 # 查找未读消息控件
    we = hw.TextControl(searchDepth=4)

 # 等待未读消息
    while not we.Exists(0):
        time.sleep(1) # 延时1秒，避免快速轮询
        print('查找未读消息', we)

 # 如果存在未读消息
    if we.Exists(0) and we.Name:
        we.Click(simulateMove=False)

 # 获取消息控件的最后一条消息
        msg_controls = wx.ListControl(Name='消息').GetChildren()
        if msg_controls: # 检查是否有消息控件
            last_msg = msg_controls[-1].Name
            print('读取最后一条消息', last_msg)

 #处理自动回复内容
            msg = df.apply(lambda x: x['回复内容'] if x['关键词'] in last_msg else None, axis=1)
            msg.dropna(axis=0, how='any', inplace=True)

            ar = np.array(msg).tolist()

 # 检查目标聊天框是否存在
            target_chat = next((child for child in hw.GetChildren() if child.Name == target_chat_name), None)

            if target_chat:
 # 点击指定的聊天框
                target_chat.Click(simulateMove=False)

 # 若有自动回复消息
                if ar:
 #发送消息
                    wx.SendKeys(ar[0].replace('{br}', '{Shift}{Enter}'), waitTime=0)
                    wx.SendKeys('{Enter}', waitTime=0)

 # 在指定聊天框上右键点击
                    target_chat.RightClick()
                else:
 # 如果没有匹配的回复，发送默认回复
                    wx.SendKeys('我没有理解你的意思,但你说的都对(此消息为自动回复)', waitTime=0)
                    wx.SendKeys('{Enter}', waitTime=0)
                    target_chat.RightClick()
            else:
                print(f"没有找到目标聊天框: {target_chat_name}")
        else:
            print("没有找到消息控件")
    else:
        print("没有找到未读消息控件")

 # 稍微延时，避免过于频繁的循环
    time.sleep(8)

# except Exception as e:
#  print(f"发生错误: {str(e)}")

