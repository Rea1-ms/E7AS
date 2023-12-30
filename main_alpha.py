import os
import time
import numpy as np
import cv2
import datetime
import random
from adbutils import adb, AdbDevice
import json
from numpy import asarray
from notify import send



def Customization():
    if 4<=hour<=7:
        
        daily()

        calling()
    
        olbs()

        pets()

        knights()

        pvp()            #白天要肝要上分就注释掉
        
        fight()

        if match('merchant_launch',0.8,True):
            loop('merchant_launch',0.8,3)
            getbookmark()
            rt(5)

        videos()          #看视频，若网络不好则注释掉
        
        community()

        end()
    elif 8<=hour<=22:
        dttb()
        

        olbs()
        dttb()

        pvp()           #白天要肝要上分就注释掉
        dttb()

        crusade()       #上线清体力,建议保留
        dttb()
        
        if match('merchant_launch',0.8,True):
            loop('merchant_launch',0.8,3)
            getbookmark()                            
            rt(3)
        dttb()

        mail()           #领邮件，想要体力攒着周末刷就注释掉

        end()

    elif 23<=hour<=24:

        dttb()   
        mail()

        dttb()
        pvp()

        dttb()
        if match('merchant_launch',0.8,True): 
            loop('merchant_launch',0.8,3)
            getbookmark()
            rt(3)

        dttb()
        daliytasks()

        dttb()
        knights()

        dttb()
        activity()

        dttb()
        transfer()

        end()

#---------------------------BASIC-FUNCTIONS----------------------------------#以下为基础功能模块
def sleep_with_random(a):
    time.sleep(a * (1 + random.uniform(0, 0.25)))

#主要匹配模块
def match(filename,threshold,f):       
    global res_path,retry_times       
    filename+='.png'
    if time.time()  - ttt > 7200 :
        log('运行超时，开始下一个账号.')
        raise Exception("程序执行超时！")
    # 设置重试次数和等待时间
    wait_times = [5, 5, 10, 20, 30, 30]
    for i in range(len(wait_times)):
        # 输出日志
        log(f'第{i+1}次查找 {filename} ...')
        # 加载模板图像
        template_con = cv2.imread(res_path + '\\' + 'connect.png', cv2.IMREAD_GRAYSCALE)
        template_fld = cv2.imread(res_path + '\\' + 'connect_break.png', cv2.IMREAD_GRAYSCALE)
        template_ter = cv2.imread(res_path + '\\' + 'time_error.png', cv2.IMREAD_GRAYSCALE)
        # 获取截图数据
        screenshot_data = asarray(device.screenshot())
        # 将截图数据转换为 OpenCV 图像对象
        screenshot = cv2.cvtColor(screenshot_data, cv2.COLOR_BGR2GRAY)
        # 模板匹配   原谅我用字母N来匹配connect，因为这个最准确，即使我用ps把connect完全扣下来匹配情况还是很感人
        result_con = cv2.matchTemplate(screenshot, template_con, cv2.TM_CCOEFF_NORMED)
        result_fld = cv2.matchTemplate(screenshot, template_fld, cv2.TM_CCOEFF_NORMED)
        result_ter = cv2.matchTemplate(screenshot, template_ter, cv2.TM_CCOEFF_NORMED)
        # 取出匹配结果中大于阈值的部分
        locations_con = np.where(result_con >= 0.95)            
        locations_con = list(zip(*locations_con[::-1]))
        locations_fld = np.where(result_fld >= 0.95)            
        locations_fld = list(zip(*locations_fld[::-1]))
        locations_ter = np.where(result_ter >= 0.95)            
        locations_ter = list(zip(*locations_ter[::-1]))          
        #网络不好
        if locations_ter:
            log('++++++++++++++++++++重启脚本++++++++++++++++++++')
            time.sleep(60)
            launch()
        if locations_fld :
            if not f:
                retry_times+=1
                if retry_times>=5:
                    retry_times=0
                    log('++++++++++++++++++++重启脚本++++++++++++++++++++')
                    time.sleep(600)
                    launch()
                    break
            else:
                return True
        if locations_con:
            wait_time = wait_times[i] 

            if i <= len(wait_times) :
                log(f"连接中，等待{wait_time}秒后重试")
            else:
                log('连接中断，开始下一个账号.')
                raise Exception("程序连接中断！")
            sleep_with_random(wait_time)
            continue
        if i == len(wait_times)+1:
            log('连接失败，开始下一个账号.')
            raise Exception("程序连接失败！")
        
        # 如果正常匹配
        template = cv2.imread(res_path + '\\' + filename, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        if locations:
            log(f'找到{filename}.')
        # 取出第一个匹配结果的中心坐标
            (x, y) = (int(locations[0][0] + 0.5 * template.shape[1]), int(locations[0][1] + 0.5 * template.shape[0]))
            
            if f==True:
                return x,y            
            log(f'找到目标！中心坐标: ({x}, {y})')
            #执行点击
            device.shell('input tap '+str(x)+' '+str(y))
            log(f'点击目标{filename}完成')
            
            break
        else:
            log(f'未找到{filename}.')
            return False



def loop(a,b,c):                 #如果在页面上存在，就一直点。
    while True:                  #优势：防xm部分按钮做虚按处理；劣势：对匹配精度配置要求高（放心大部分场景已测试通过）
        if match(a,b,True):
            match(a,b,False)
            sleep_with_random(c)
        else:
            sleep_with_random(0.5)#给个缓冲机会
            break

        

def swipe(start_x, start_y, end_x, end_y,t):       #滑动模块
    device.shell('input swipe {} {} {} {} 250'.format(start_x, start_y, end_x, end_y))
    sleep_with_random(t)

def rt(a):                                         #返回模块
    device.shell('input keyevent 4')
    print('返回，暂停{}s'.format(a))
    sleep_with_random(a)

def end():                                          #结束，强行停止游戏，降低服务器功耗
    global package_name
    log('运行完成，开始下一个账号')
    device.shell(f'am force-stop {package_name}')

def log(msg):                                        #日志记录模块
    log_file.write(f'{time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())} {msg}\n')
    print(msg)

def update():
    match('app_update',0.9,False)
    sleep_with_random(10)
    if match('app_update_play',0.9,True):
        match('app_update_play',0.9,False)
        sleep_with_random(5)
        while not match('app_update_done',0.9,True):
            sleep_with_random(5)
        match('app_update_done',0.9,False)
        
    else:
        raise Exception("程序更新失败！")

def restart():
        global application
        apps=APP.values()
        for i in apps:
            device.shell(f'am force-stop {i}')
            sleep_with_random(1)
        
        #防止上一次运行异常影响本次运行
        sleep_with_random(5)
        #任务走菜单是为了识别精准（除圣域），防止因背景不一样而报错
        if application=='google':
            device.shell(f'am start -n {package_name}/kr.supercreative.epic7.AppActivity')
                #停止：adb shell am force-stop com.stove.epic7.google
        else :
            match('app_icon',0.9,False)
        sleep_with_random(20)
        

def launch():
        global ready_to_send
        ready_to_send+='++++++++++++++++++++正在启动E7++++++++++++++++++++'
        try:
            restart()
            while (not (match('maintain',0.8,True) or match('YUNA',0.95,True))) or match('stuck',0.95,True) or match('connect_break',0.95,True):
                restart()
                sleep_with_random(2)
            if match('maintain',0.8,True):
                log('====================维护中====================')
                ready_to_send+='====================维护中====================\n'
                end()
                return

            while match('YUNA',0.95,True):
                if match('update',0.9,True):
                    match('update',0.9,False)
                    print('发现并执行游戏更新！')
                    sleep_with_random(2)
                if application=='china':
                    if match('launch_activity_close',0.7,True):
                        match('launch_activity_close',0.7,False)
                        sleep_with_random(2)
                elif application=='google':
                    if match('app_update',0.9,True):
                        log('发现游戏更新')
                        update()  
                    if match('login',0.9,True):
                        log('====================登录失败！请检查账号登录情况与网络环境！====================')
                        ready_to_send+='====================登录失败！请检查账号登录情况与网络环境！====================\n'
                        raise Exception('登录失败！')
                match('YUNA',0.95,False)
                sleep_with_random(5)
            sleep_with_random(30)

        except Exception as e:
            # 发生异常时记录日志
            print(f'运行账号{account_num}时程序启动异常：{e}')
            log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 运行账号{account_num}时程序启动异常：{e}\n')
            return
        
        try:
            Customization()
            #match('mystery',0.9,True)
            #loop('knight_stone',0.97,5) 
            #community()
        except Exception as e:
            # 发生异常时记录日志
            print(f'运行账号{account_num}时程序运行异常：{e}')
            log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 运行账号{account_num}时程序运行异常：{e}\n')
            end()
            return
















#------------------------------GAMING!----------------------------------#以下为具体游戏模块



#-----------------daily-----------------#每日首次进入，关闭顺序：官方提示、重新派遣、友情点数获取、每日签到、加成效果提示、礼包促销提示，最后领取大厅内宠物礼物
def daily():   
    global ready_to_send,buff
    ready_to_send += '----------开始每日奖励收取----------\n'                           
    loop('ads',0.9,5)
    loop('confirm_blue',0.8,15)
    sleep_with_random(5)
    loop('tap_to_close_yellow',0.8,8)
    sleep_with_random(5)
    loop('tap_to_close_white',0.8,8)
    sleep_with_random(5)
    loop('tap_to_close_yellow',0.8,8)
    loop('dispatch_restart',0.8,8)
    loop('tap_to_close_yellow',0.8,8)
    if match('buff_crusade',0.8,True):
        buff=True
    loop('tap_to_close_white',0.8,8)
    if match('announcement',0.8,True):
        match('announcement',0.8,False)
        sleep_with_random(2)
        loop('confirm_blue',0.8,2)
    loop('buying_close',0.8,8)
    loop('gift_from_pets',0.8,8)
    device.shell('input tap 525 715')
    sleep_with_random(5)
    device.shell('input tap 525 715')
    sleep_with_random(3)
    ready_to_send += '**********每日奖励收取完成**********\n'
#----------------calling-----------------#每日穷尽免费次数
def calling():
    global ready_to_send 
    ready_to_send += '----------开始每日圣约召唤----------\n'
    loop('menu_launch',0.8,2)
    loop('calling_launch',0.8,8)
    swipe(1300,700,1300,200,5)
    match('covenant_call',0.8,False)
    sleep_with_random(5)
    char_calling_time=0
    while True:
        if match('calling_free',0.92,True) or match('calling_ano',0.92,True):
            match('calling_free',0.92,False)
            match('calling_ano',0.92,False)
            sleep_with_random(3)
            loop('confirm_green',0.8,30)
            char_calling_time+=1
            screenshot_path = f'{char_calling_path}/char-ACCOUNT{account_num}-{date_str}{str(char_calling_time)}.png'
            device.screenshot().save(screenshot_path)

            if match('calling_new',0.8,True):
                sleep_with_random(5)
                match('calling_new',0.8,False)
                sleep_with_random(3)
        else:
            break
    loop('return_yellow',0.8,3)
    rt(5)
    ready_to_send +=  f'**********每日圣约召唤完成**********\n**********共抽{str(char_calling_time)}抽**********\n'

#----------------videos------------------#看视频，若网络不好则注释掉不要用了
def videos():
    global ready_to_send , application
    if application=='china':
        pass
    else:
        ready_to_send += '----------开始看视频----------\n'
        loop('menu_launch',0.8,2)
        loop('acvitity_launch',0.95,5)
        if not match('activity_all_blue',0.99,True):
            match('activity_all_grey',0.99,False)
            sleep_with_random(3)
        while not match('video',0.8,True):
            swipe(800,700,800,200,5)
        sleep_with_random(5)
        while True:
            if match('video',0.8,True):
                match('video',0.8,False)
                sleep_with_random(3)
            if match('tap_to_close_yellow',0.8,True):
                match('tap_to_close_yellow',0.8,False)
                rt(2)
                break
            sleep_with_random(30)
            rt(3)
            loop('tap_to_close_yellow',0.8,5)
        rt(3)
        ready_to_send += '**********看视频完成**********\n'

#------------------olbs------------------#收企鹅、收取/加速摩罗戈拉、收幻影、收欧勒毕斯之心
def olbs():
    global ready_to_send
    ready_to_send += '----------开始收菜----------\n'
    loop('menu_launch',0.8,2)
    loop('sanctuary_launch',0.8,7)
    loop('angels_forest',0.7,5)          
    loop('moluogela_foster',0.8,3)
    loop('eggs',0.9,10) 
    loop('tap_to_close_yellow',0.8,2)
    loop('moluogela',0.9,7) 
    loop('huanying',0.9,7) 
    loop('tap_to_close_yellow',0.8,2)
    rt(2)

    loop('olbs_heart',0.7,2)  
    loop('olbs_collect',0.99,2)  
    loop('tap_to_close_yellow',0.8,2)
    rt(2)
    rt(4)
    ready_to_send +='**********收菜完成**********\n'
#-----------------pets-------------------##穷尽每日抽取次数，照顾宠物暂无头绪
def pets():
    global ready_to_send 
    ready_to_send += '----------开始抽宠物----------\n'
    loop('menu_launch',0.8,2)
    loop('pets_launch',0.95,5)
    pets_calling_time=0
    loop('get_pets',0.9,5)
    while True:
        if match('pets_free',0.9,True):
            pets_calling_time+=1
            loop('pets_free',0.9,3)
            screenshot_path = f'{pets_calling_path}/pets-ACCOUNT{account_num}-{date_str}{str(pets_calling_time)}.png'
            device.screenshot().save(screenshot_path)
            rt(2)
            loop('get_pets',0.9,5)
        else:
            break
    rt(2)
    rt(4)
    ready_to_send += f'**********抽宠物完成**********\n**********共抽{str(pets_calling_time)}次**********\n'

#----------------knights----------------#建议早上一轮（签到）晚上一轮（达成率），兼顾捐赠、买每周一根的摩罗戈拉、领取每周任务奖励
def knights():
    global ready_to_send
    ready_to_send += '----------开始收取骑士团奖励----------\n'
    loop('menu_launch',0.8,2)
    loop('knight_launch',0.95,5)                              #国际服当时没截图
    if match('knight_empty',0.8,True) :
        ready_to_send += '----------未加入骑士团----------\n'
        log('----------未加入骑士团----------')
    else:
        loop('tap_to_close_yellow',0.8,2)                   #达成率没写,哪个好心人给个截图
        match('knight_donate',0.8,False)
        sleep_with_random(5)
        match('knight_donating',0.9,False)
        sleep_with_random(5)
        loop('tap_to_close_yellow',0.8,2) 
        match('knight_donating',0.9,False)
        sleep_with_random(5)
        loop('tap_to_close_yellow',0.8,2) 
        loop('knights_store_launch',0.999,5) 
        swipe(800,700,800,300,2)
        loop('knight_moluogela',0.95,5) 
        loop('knight_moluogela_buying',0.95,5) 
        swipe(800,700,800,300,2)
        swipe(800,700,800,300,2)
        swipe(800,700,800,300,2)
        swipe(800,700,800,300,2)
        loop('knight_stone',0.97,5) 
        loop('knight_stone_buying',0.95,5) 
        swipe(1300,700,1300,200,1)
        match('knight_weekly_tasks',0.9,False)
        sleep_with_random(5) 
        while True:
            loop('get_green',0.8,5)
            loop('tap_to_close_yellow',0.8,2) 
            if not match('get_green',0.8,True):
                swipe(800,700,800,200,2)
                if not match('get_green',0.8,True):
                    break

    rt(4)
    ready_to_send += '**********骑士团奖励收取完成**********\n'
#-----------------pvp-------------------#打人机，暂不支持选择人机难度，打默认而已
def pvp():
    global ready_to_send
    ready_to_send += '----------开始打pvp人机----------\n'
    loop('menu_launch',0.9,2)
    loop('arena_launch',0.8,2)
    loop('arena',0.8,5)
    match('pass',0.8,False)
    sleep_with_random(1)
    match('confirm_blue',0.8,False)
    sleep_with_random(2)
    loop('tap_to_close_yellow',0.8,2) 
    match('pvp_weekly_reward',0.8,False)
    sleep_with_random(2)
    loop('pvp_weekly_reward_get',0.8,1)

    match('pvp_npc_start',0.9,False)  
    match('pvp_npc_start',0.9,False)  
    sleep_with_random(5)
    flag=True                                     
    for i in range(2):
        if not match('pvp_challenge',0.8,True) and flag:
            swipe(1000,700,1000,200,2)
        while match('pvp_challenge',0.8,True) and flag:
            loop('pvp_challenge',0.8,5)
            match('pvp_battle_start',0.9,False)
            sleep_with_random(15)
            if match('cancel',0.8,True):
                match('cancel',0.8,False)
                sleep_with_random(1)
                rt(2)
                flag=False
                break
            match('pass',0.8,False)
            sleep_with_random(1)
            match('confirm_blue',0.8,False)
            sleep_with_random(2)
            match('pvp_auto_fight',0.8,False)
            while not (match('pass',0.8,True) or match('confirm_green',0.8,True)):
                print('战斗中 等待10s')
                sleep_with_random(10)
            match('pass',0.8,False)
            sleep_with_random(1)
            match('confirm_blue',0.8,False)
            sleep_with_random(8)
            loop('confirm_green',0.8,6)
            if not match('pvp_challenge',0.8,True) and flag:
                swipe(1000,700,1000,200,2)
    rt(4)
    ready_to_send += '**********打pvp人机完成**********\n'


#----------------fight-----------------#深渊+祭坛+殿堂
def fight():
    global ready_to_send 
    ready_to_send += '----------开始深渊+祭坛+殿堂----------\n'
    loop('cancel',0.8,2)
    loop('menu_launch',0.8,2)
    loop('fight',0.8,3)
    loop('abyss_start',0.8,3)
    
    match('abyss_pure',0.8,False)
    sleep_with_random(3)
    loop('confirm_blue',0.8,5)
    loop('tap_to_close_yellow',0.8,3)
    

    match('altar',0.8,False)
    match('altar',0.8,False)
    sleep_with_random(3)
    loop('altar_left',0.8,2)
    match('altar_pass',0.8,False)
    match('altar_pass',0.8,False)
    sleep_with_random(2)
    loop('pve_choose_team',0.8,3)
    if  match('pve_auto_fight_false',0.9,True):
        match('pve_auto_fight_true',0.9,False)
    match('pvp_battle_start',0.9,False)
    sleep_with_random(3)
    if match('cancel',0.9,True):
        rt(2)
        rt(2)
        rt(2)
        log('---------------------貌似背包满了，返回------------------')
        ready_to_send += '---------------------貌似背包满了，返回------------------\n'
    else:
        while not ( match('stage_clear',0.8,True) or match('level_up',0.8,True) ):
            print('战斗中 等待10s')
            sleep_with_random(10)
        if match('level_up',0.8,True):
            match('level_up_skip',0.9,False)
            sleep_with_random(1)
            loop('tap_to_close_yellow',0.9,2)
        match('stage_clear',0.8,False)
        sleep_with_random(3)
        loop('tap_to_close_yellow',0.8,3)
        loop('tap_to_close_white',0.8,3)
        loop('confirm_green',0.8,3)
        if match('level_up',0.8,True):
            match('level_up_skip',0.9,False)
            sleep_with_random(1)
        rt(4)
        rt(2)

    swipe(1300,700,1300,100,3)
    if match('temple',0.99,True):
        match('temple',0.99,False)
        match('temple',0.99,False)
        sleep_with_random(4)
        loop('tap_to_close_yellow',0.8,3)
        loop('temple_new',0.8,3)
        loop('get_blue',0.8,3)                                 
        device.shell('input tap 930 480')
        sleep_with_random(3)
        match('temple_battle_start',0.8,False)
        sleep_with_random(3)        
        match('temple_battle_start',0.8,False)
        sleep_with_random(3)
        if match('cancel',0.9,True):
            rt(2)
            rt(2)
            rt(2)
        else:
            while not match('confirm_green',0.8,True):
                print('战斗中 等待10s')
                sleep_with_random(10)
            match('confirm_green',0.8,False)
            rt(3)
    rt(5)
    ready_to_send += '**********深渊+祭坛+殿堂完成**********\n'

#----------------crusade----------------#讨伐，请提前选择好宠物的重复战斗次数
def crusade():
    global ready_to_send,buff
    if not buff:
        return
    
    ready_to_send += '----------开始讨伐----------\n'
    loop('menu_launch',0.8,2)
    loop('fight',0.8,3)
    loop('crusade_start',0.8,5)

    loop('crusade_fire',0.8,5)
    swipe(1050,825,1050,125,0.25)
    swipe(1050,825,1050,125,0.25)
    loop('pve_choose_team',0.8,3)
    if match('pve_auto_fight_false',0.8,True):
        match('pve_auto_fight_false',0.8,False)
        match('pve_auto_fight_false',0.8,False)
    match('pvp_battle_start',0.8,False)
    sleep_with_random(3)
    if match('cancel',0.9,True):
        rt(2)
        rt(2)
        rt(2)
        rt(6)
        log('---------------------貌似背包满了，返回---------------------')
        ready_to_send += '---------------------貌似背包满了，返回---------------------\n'
    else:
        while not (match('pve_autofight_done',0.95,True) or match('level_up',0.95,True) ):
            print('战斗中 等待10s')
            sleep_with_random(10)
        if match('level_up',0.8,True):
            match('level_up_skip',0.9,False)
            sleep_with_random(1)
            loop('tap_to_close_yellow',0.9,2)
        sleep_with_random(3)
        if match('cancel',0.8,True):
            match('cancel',0.8,False)
            sleep_with_random(1)
        match('confirm_green',0.8,False)
        sleep_with_random(5)
        if match('level_up',0.8,True):
            match('level_up_skip',0.9,False)
            sleep_with_random(1)
        rt(5)
        rt(2)
        rt(5)
    ready_to_send += '**********讨伐完成**********\n'

#-----------------mail------------------#会全部收取+收取三餐奖励
def mail():
    global ready_to_send
    ready_to_send += '----------开始收取邮件----------\n'
    match('mail',0.8,False)
    sleep_with_random(2)
    if not match('mail_collect_all',0.8,True) :
        match('mail',0.8,False)
    sleep_with_random(3)
    match('mail_collect_all',0.99,False)
    match('mail_collect_all',0.8,False)    
    sleep_with_random(3)
    loop('confirm_blue',0.8,5)
    loop('tap_to_close_yellow',0.8,2) 
    while match('dinner_bonus',0.9,True):
        loop('dinner_bonus',0.9,2) 
        loop('mail_get',0.9,2) 
        sleep_with_random(3)
    loop('tap_to_close_yellow',0.8,2) 
    loop('tap_to_close_white',0.8,2) 
    ready_to_send += '**********邮件收取完成**********\n'

#---------------bookmark--------------#请将主页设置为英雄/插画，防止酒馆无法正常启动

def bookmark_enhanced():       
    global res_path , bookmark_gettime , mystery_gettime 
    if time.time()  - ttt > 3600 :
        log('运行超时，开始下一个账号.')
        raise Exception("程序执行超时！")
    # 设置重试次数和等待时间
    wait_times = [0.1, 0.25, 0.5, 1, 1, 1, 5, 5, 10, 20, 30, 30]

    for i in range(len(wait_times)):
        # 获取截图数据
        screenshot_data = asarray(device.screenshot())
        # 将截图数据转换为 OpenCV 图像对象
        screenshot = cv2.cvtColor(screenshot_data, cv2.COLOR_BGR2GRAY)
        # 加载模板图像
        template_con = cv2.imread(res_path + '\\' + 'connect.png', cv2.IMREAD_GRAYSCALE)
        template_fld = cv2.imread(res_path + '\\' + 'connect_break.png', cv2.IMREAD_GRAYSCALE)
        # 获取截图数据
        screenshot_data = asarray(device.screenshot())
        # 将截图数据转换为 OpenCV 图像对象
        screenshot = cv2.cvtColor(screenshot_data, cv2.COLOR_BGR2GRAY)
        # 模板匹配
        result_con = cv2.matchTemplate(screenshot, template_con, cv2.TM_CCOEFF_NORMED)
        result_fld = cv2.matchTemplate(screenshot, template_fld, cv2.TM_CCOEFF_NORMED)

        # 取出匹配结果中大于阈值的部分
        locations_con = np.where(result_con >= 0.95)            
        locations_con = list(zip(*locations_con[::-1]))
        locations_fld = np.where(result_fld >= 0.95)            
        locations_fld = list(zip(*locations_fld[::-1]))
          
        #网络不好
        if locations_fld:
            log('运行超时，开始下一个账号.')
            raise Exception("程序执行超时！")   
        if locations_con:
            wait_time = wait_times[i] 
            if i <= len(wait_times) :
                log(f"连接中，等待{wait_time}秒后重试")
            else:
                log('连接中断，开始下一个账号.')
                raise Exception("程序连接中断！")
            sleep_with_random(wait_time)
            continue
        if i == len(wait_times)+1:
            log('连接失败，开始下一个账号.')
            raise Exception("程序连接失败！")
        break

    template_bkm = cv2.imread(res_path + '\\' + 'bookmark.png', cv2.IMREAD_GRAYSCALE)
    template_msy = cv2.imread(res_path + '\\' + 'mystery.png', cv2.IMREAD_GRAYSCALE)    
    result_bkm = cv2.matchTemplate(screenshot, template_bkm, cv2.TM_CCOEFF_NORMED)
    result_msy = cv2.matchTemplate(screenshot, template_msy, cv2.TM_CCOEFF_NORMED)   
    locations_bkm = np.where(result_bkm >= 0.8)            
    locations_bkm = list(zip(*locations_bkm[::-1]))    
    locations_msy = np.where(result_msy >= 0.8)            
    locations_msy = list(zip(*locations_msy[::-1])) 
    # 正常匹配
    if locations_bkm:
        log('********************找到圣约书签********************')
        # 点击匹配结果的中心坐标
        (x, y) = (int(locations_bkm[0][0] + 0.5 * template_bkm.shape[1]) + 800 , int(locations_bkm[0][1] + 0.5 * template_bkm.shape[0]) + 40)          
        device.shell('input tap '+str(x)+' '+str(y))
        device.shell('input tap '+str(x)+' '+str(y))
        sleep_with_random(0.5)
        log('正在购买')
        loop('000',0.8,0.25)
        bookmark_gettime+=1
    if locations_msy:
        log('********************找到神秘奖牌********************')
        # 点击匹配结果的中心坐标
        (x, y) = (int(locations_msy[0][0] + 0.5 * template_msy.shape[1]) + 800 , int(locations_msy[0][1] + 0.5 * template_msy.shape[0]) + 40)          
        device.shell('input tap '+str(x)+' '+str(y))
        device.shell('input tap '+str(x)+' '+str(y))
        sleep_with_random(0.5)
        log('--正在购买--')
        loop('000',0.8,0.25)
        mystery_gettime+=1
    else:
        log('----------本轮未找到----------\n')



#------------dailytasks---------------#若点数未100则去打支线故事（暂不支持每周奖励领取）
def daliytasks():
    global ready_to_send
    ready_to_send += '----------开始每日任务----------\n'
    loop('menu_launch',0.8,2)
    loop('archievements',0.8,4)
    '''
    if match('dac100',0.99,True):
        loop('menu_launch',0.8,2)
        loop('sidestory_launch',0.8,7)
        loop('undocumented_stories',0.8,7)
        loop('venture',0.8,10)
        loop('pve_adventure_ready',0.8,6)
        loop('pve_choose_team',0.8,3)
        if match('pve_auto_fight_false',0.8,True):
            match('pve_auto_fight_false',0.8,False)
        match('pvp_battle_start',0.8,False)
        sleep_with_random(3)
        if match('cancel',0.9,True):
            rt(3)
            rt(3)
            rt(6)
            log('---------------------貌似背包满了，返回------------------')
            ready_to_send += '---------------------貌似背包满了，返回------------------\n'
        else:
            while not match('pve_autofight_done',0.95,True):
                print('战斗中 等待10s')
                sleep_with_random(10)
            sleep_with_random(3)
            if match('cancel',0.8,True):
                match('cancel',0.8,False)
                sleep_with_random(1)
            match('confirm_green',0.8,False)
            sleep_with_random(5)
            if match('level_up',0.8,True):
                match('level_up_skip',0.9,False)
                sleep_with_random(1)
            rt(5)
            rt(5)
            loop('tap_to_close_yellow',0.8,8)
            loop('buying_close',0.8,8)   
        loop('menu_launch',0.8,2)
        loop('archievements',0.8,4)
    '''
    if match('dac100',0.95,True):
        log('---------------------每日任务点数仍未过百------------------')
        ready_to_send += '---------------------每日任务点数仍未过百------------------\n'
    if match('dac100_done',0.95,True):
        match('dac100_done',0.95,False)
        sleep_with_random(3)
        loop('tap_to_close_yellow',0.8,3)  
    
    match('weekly_bonus_launch',0.9,False)
    match('weekly_bonus_launch',0.9,False)
    log('---------------------开始收取每周任务奖励------------------')
    ready_to_send += '---------------------开始收取每周任务奖励------------------\n'
    if match('weekly_bonus_best',0.95,True):
        log('********************收取第一等每周奖励********************')
        ready_to_send += '********************收取第一等每周奖励********************\n'
        loop('weekly_bonus_best',0.95,3)
        loop('tap_to_close_yellow',0.8,3)  
    else:
        if match('weekly_bonus_senior',0.95,True):
            log('********************收取第二等每周奖励********************')
            ready_to_send += '********************收取第二等每周奖励********************\n'
            loop('weekly_bonus_senior',0.95,3)
            loop('tap_to_close_yellow',0.8,3) 
        elif match('weekly_bonus_junior',0.95,True):
            log('********************收取第三等每周奖励********************')
            ready_to_send += '********************收取第三等每周奖励********************\n'
            loop('weekly_bonus_junior',0.95,3)
            loop('tap_to_close_yellow',0.8,3)   

    loop('tap_to_close_yellow',0.8,3)   

    rt(5)
    ready_to_send += '**********每日/周任务奖励收取完成**********\n'

#-------------getbookmark---------------#同enhanced
def getbookmark():                                
    global flash_time , ready_to_send
    ready_to_send += '----------开始刷书签----------\n'
    i=0
    while i<bookmark_time:
        i+=1
        flash_time+=1
        log(f'-----------------第{flash_time}次刷书签-----------------')
        bookmark_enhanced()
        swipe(1300,700,1300,200,0.25)
        bookmark_enhanced()
        match('refresh',0.9,False)
        match('refresh',0.9,False)
        sleep_with_random(0.75)
        loop('confirm_blue',0.8,1)
        sleep_with_random(1)
    bookmark_enhanced()
    log(f'刷商店完成！\n共得到书签{bookmark_gettime*5}个\n奖牌{mystery_gettime*50}个')
    ready_to_send += f'**********刷商店完成！\n共得到书签{bookmark_gettime*5}个\n奖牌{mystery_gettime*50}个**********\n'

#----------------activity-----------------#活动多变，可能不具普遍性，需要及时更新，如果没有更新就踢我一脚（我摆烂除外）
def activity():
    global ready_to_send 
    ready_to_send += '----------开始收活动奖励----------\n'
    loop('menu_launch',0.8,2)
    loop('acvitity_launch',0.95,5)
    if application=='google':
        x,y=match('activity_regular',0.95,True)                   #一般来说活动4个按钮 这期摆了
        device.shell('input tap '+str(x)+' '+str(y+70))
        sleep_with_random(30)  
        for i in range(4):
            device.shell(f'input tap {435+i*225} 665')
            sleep_with_random(5)
            device.shell('input tap 655 645')
            sleep_with_random(2)
        
        x,y=match('activity_regular',0.8,True)                          
        device.shell('input tap '+str(x)+' '+str(y+150))                 
        sleep_with_random(30)  
        for i in range(4):
            device.shell(f'input tap {190+140*i} 425')
            sleep_with_random(2)  
            device.shell('input tap 515 700')
            sleep_with_random(8)
            device.shell('input tap 655 645')
            sleep_with_random(2)    
        device.shell('input tap 1050 700')   
        sleep_with_random(5)
        device.shell('input tap 655 645')
        sleep_with_random(2) 
        #8.14:4+1 光兰蒂(抛骰子);     9.1:8+1 伊杰拉建国礼(懒得做)        9.15:4+1 吸血鬼   10.6猜拳   11.21 原神姐大转盘
        #12.12 自行兑换 12.28 插画投票
        

    elif application=='china':
        while True:
            if not match('activity_regular',0.8,True) :
                swipe(1300,700,1300,100,3)
                swipe(1300,700,1300,100,3)
            else:
                break
        x,y=match('activity_regular',0.8,True)                   #一般来说活动4个按钮
        device.shell('input tap '+str(x)+' '+str(y+95))
        sleep_with_random(10) 

        for i in range(4):
            device.shell(f'input tap {395+i*240} 575')
            sleep_with_random(5)
            device.shell('input tap 640 635')
            sleep_with_random(2)

        #本期为大转盘
        device.shell('input tap '+str(x)+' '+str(y+190))
        sleep_with_random(10) 
        for i in range(4):
            device.shell('input tap 360 535')
            sleep_with_random(8)
            device.shell('input tap 640 635')
            sleep_with_random(2)    
        device.shell('input tap 930 710')   
        sleep_with_random(5)
        device.shell('input tap 640 635')
        sleep_with_random(2) 
        












        ''' 
        #超级大作战(国)
        for i in range(5):
            device.shell('input tap 1045 525')
            sleep_with_random(5)
            device.shell('input tap 635 660')
            sleep_with_random(2)


        device.shell('input tap 915 450')                #8.14:夏日超级大作战活动，有每日/周任务  9.1:光兰蒂        
        sleep_with_random(30) 
        for i in range(5):
            device.shell('input tap 1045 525')
            sleep_with_random(5)
            device.shell('input tap 635 660')
            sleep_with_random(2)
        
        for i in range(5):
            device.shell(f'input tap {505+i*155} 215')
            sleep_with_random(5)
            device.shell('input tap 635 660')
            sleep_with_random(2)

        #光兰蒂(抛骰子)(国)
        device.shell('input tap '+str(x)+' '+str(y+190))
        sleep_with_random(10) 
        for i in range(4):
            device.shell('input tap 545 545')
            sleep_with_random(8)
            device.shell('input tap 640 635')
            sleep_with_random(2)    
        device.shell('input tap 1015 660')   
        sleep_with_random(5)
        device.shell('input tap 640 635')
        sleep_with_random(2) 

        #大转盘(国)
        device.shell('input tap '+str(x)+' '+str(y+190))
        sleep_with_random(10) 
        for i in range(4):
            device.shell('input tap 360 535')
            sleep_with_random(8)
            device.shell('input tap 640 635')
            sleep_with_random(2)    
        device.shell('input tap 930 710')   
        sleep_with_random(5)
        device.shell('input tap 640 635')
        sleep_with_random(2) 



        #大转盘(外) 9.15 吸血鬼
        x,y=match('activity_regular',0.8,True)                          
        device.shell('input tap '+str(x)+' '+str(y+150))                 
        sleep_with_random(30)  
        for i in range(4):
            device.shell('input tap 450 545')
            sleep_with_random(8)
            device.shell('input tap 655 645')
            sleep_with_random(2)    
        device.shell('input tap 975 700')   
        sleep_with_random(5)
        device.shell('input tap 655 645')
        sleep_with_random(2) 

        #10.6猜拳(外) 雅卡泰丝
        x,y=match('activity_regular',0.8,True)                          
        device.shell('input tap '+str(x)+' '+str(y+150))                 
        sleep_with_random(30)  
        for i in range(4):
            device.shell('input tap 465 660')
            sleep_with_random(8)
            device.shell('input tap 655 645')
            sleep_with_random(2)    
        device.shell('input tap 975 700')   
        sleep_with_random(5)
        device.shell('input tap 655 645')
        sleep_with_random(2) 

        #12.28(外)  插画投票
        x,y=match('activity_regular',0.8,True)                          
        device.shell('input tap '+str(x)+' '+str(y+150))                 
        sleep_with_random(30)  
        for i in range(4):
            device.shell(f'input tap {190+140*i} 425')
            sleep_with_random(2)  
            device.shell('input tap 515 700')
            sleep_with_random(8)
            device.shell('input tap 655 645')
            sleep_with_random(2)    
        device.shell('input tap 1050 700')   
        sleep_with_random(5)
        device.shell('input tap 655 645')
        sleep_with_random(2) 
        '''

    rt(2)
    ready_to_send += '**********活动奖励收取完成**********\n'

#-----------------dttb-------------------#排除妨碍，消除危险
def dttb():
    global ready_to_send,buff
    ready_to_send += '----------排除妨碍中----------\n'
    sleep_with_random(10)
    loop('cancel',0.8,8)
    loop('tap_to_close_yellow',0.8,8)
    loop('ads',0.9,5)
    loop('dispatch_restart',0.8,8)
    if match('buff_crusade',0.8,True):
        buff=True
    loop('tap_to_close_white',0.8,8)
    if match('announcement',0.8,True):
        match('announcement',0.8,False)
        sleep_with_random(2)
        loop('confirm_blue',0.8,2)
    loop('tap_to_close_yellow',0.8,8)
    loop('buying_close',0.8,8)
    ready_to_send += '**********妨碍已排除**********\n'


#-------------community------------------#国服社区奖励
def community():    
    if application=='china':
        loop('menu_launch',0.8,2)
        loop('acvitity_launch',0.9,10)
        loop('game_community_launch',0.8,7)
        loop('game_community_checkin',0.8,7)
        loop('game_community_checkin_done',0.8,2)
        i=0
        while i<3:
            if match('game_community_like',0.95,True):
                match('game_community_like',0.95,False)
                sleep_with_random(3)
                match('game_community_comment',0.9,False)
                sleep_with_random(3)
                rt(3)
                match('game_community_share',0.9,False)
                sleep_with_random(3)
                match('game_community_copylink',0.9,False)
                sleep_with_random(3)
                match('game_community_cancel',0.9,False)
                sleep_with_random(3)
                i+=1
            else:
                swipe(450,800,450,100,2)
        rt(3)
        rt(3)


#---------------transfer------------------#传送2星杂鱼（危险！慎用！使用前请先将有用英雄锁定以防被传送！把6星传走作者概不负责！使用即同意您已知晓使用本脚本的风险并对使用本脚本所带来的所有后果承担全部责任）
def transfer():
    loop('menu_launch',0.8,2)
    loop('heroes_launch',0.8,7)
    loop('heroes_transfer',0.8,5)
    match('heroes_select_sort',0.8,False)
    sleep_with_random(2)
    loop('heroes_2star',0.9,7)
    match('heroes_select_sorted',0.8,False)
    sleep_with_random(2)
    while match('heroes_2star_selected',0.95,True):
        for i in range(12):
            match('heroes_2star_selected',0.95,False)
            sleep_with_random(0.75)
        match('heroes_do_transfer',0.8,False)
        sleep_with_random(3)
        loop('confirm_blue',0.8,5)
        loop('tap_to_close_yellow',0.8,5)
    rt(5)
    rt(5)







#--------------------------main------------------------#
try:
    ready_to_send = ''
    if not os.path.exists('char_calling'):      #初始化路径
        os.makedirs('char_calling')
    if not os.path.exists('pets_calling'):
        os.makedirs('pets_calling')
    if not os.path.exists('log'):
        os.makedirs('log')
    current_time = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
    log_file = open(f'log/{current_time}.txt', 'w')
    log('**********测试版程序成功启动**********')
    ready_to_send += '**********测试版程序成功启动**********\n'

    char_calling_path = os.path.join(os.getcwd(), 'char_calling')
    pets_calling_path = os.path.join(os.getcwd(), 'pets_calling')

    with open('config.json', 'r', encoding='UTF-8') as f:
        config = json.load(f)

    log('**********初始化已完成**********')
    ready_to_send += '**********初始化已完成**********\n'

    APP = {  # 保存不同游戏的包名,等待好心人来完善
        'google': 'com.stove.epic7.google' ,
        'china': 'com.zlongame.cn.epicseven'
    }

    now = datetime.datetime.now()   
    date_str = now.strftime("%Y-%m-%d")
    date_str+='-'
    hour=now.hour


    for accounts in config:
        '读取单个账号信息'
        res_path = os.path.join(os.getcwd(), 'res')  # 初始化文件夹
        account_num = str(accounts['num']) #读取账号编号
        account_nickname = accounts['nickname'] #读取账号备注名称
        waiting_before_launch = accounts['waiting_before_launch'] #启动预热时长
        ip = accounts['IP'] #读取对应模拟器ip
        if not ip:
            log(f'账号{account_num}(备注名为{account_nickname})未填写ip,下一个！')
            ready_to_send += f'账号{account_num}(备注名为{account_nickname})未填写ip,下一个！\n'
            continue
        else:
            log(f'******************************读取到账号{account_num}(备注名为{account_nickname})******************************')
            ready_to_send += f'******************************读取到账号{account_num}(备注名为{account_nickname})******************************\n'

        application = accounts['application'] #读取对应程序
        package_name=APP[application]         #匹配相应包名
        res_path+=('\\'+accounts['application'])    #按包名确定图片路径
        bookmark_time = int(accounts['bookmark_time'])  #刷商店次数
        buff=False  #讨伐buff


        retry_times=0       #重连次数
        ttt=time.time()        #时间获取，为了召唤后命名文件和不同时间不同命令   

        bookmark_gettime=0
        mystery_gettime=0
        flash_time=0

        time.sleep(waiting_before_launch)

        device=adb.connect(ip,timeout=10)
        device = adb.device(serial=ip)
        log('adb连接成功.')



        launch()



except Exception as e:
    # 发生异常时记录日志
    print(f'程序异常：{e}')
    log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 程序异常：{e}\n')
finally:
    end()
    log_file.close()
    send('【E7AS】运行日志' , ready_to_send)
    exit(0)





'''
1.轻触画面开始
2.点击蓝色确认 
3.如果有轻触后关闭（友情）
4.重派遣
5.关闭礼包推荐
6.宠物礼物
7.点击菜单——召唤
8.若免费，循环召唤
9.oulebisi
10.宠物系统，同召唤
11.骑士团
12.打竞技场npc
13.深渊净化
14.打个祭坛
15.打个殿堂
16.刷个商店
17.看视频
18.收个邮件

1.关掉一堆东西
2.oulebisi
3.打竞技场npc
4.刷个商店
5.收个邮件（包括三餐）

1.收个邮件
2.刷个商店
3.完成每日任务
4.捞个骑士团奖励
5.收个活动奖励
'''
