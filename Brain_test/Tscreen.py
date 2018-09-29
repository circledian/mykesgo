#头脑风暴大屏端的操作
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import os,sys
import requests
import random
import json
import time
#import pymssql
import random
from Storming.test1 import MssqlUtil
import sys
from random import choice
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
#后台，教师端，导入10个左右的学生，添加好学号，其余资料，手机端运行时，可以自行进行填写，手机端运行时，选择学号最前的一位进行登录
class test_screen():
 def __init__(self,base_url1):
        #self.url = urljoin(base_url,"kesgo/login.html")
        self.url = base_url1
        self.driver = webdriver.Chrome()

 def login(self,txtUsername,txtPassword):
        #大屏端
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(".//*[@id='txtUsername']").click()
        self.driver.find_element_by_xpath(".//*[@id='txtUsername']").send_keys(txtUsername)
        self.driver.find_element_by_xpath(".//*[@id='txtPassword']").click()
        self.driver.find_element_by_xpath(".//*[@id='txtPassword']").send_keys(txtPassword)
        # sleep(3)
        self.driver.find_element_by_xpath(". //body").click()
        sleep(1)
        self.driver.find_element_by_xpath(".//*[@id='btnLogin']").click()
        sleep(3)
#写思考题并提交432423423423423444444444444444444444444444444444444
 def clickexper(self,i):
        #教师只有一个正在进行中的实验时，这边可以直接点击，多个进行中的这边涉及冒泡了，不能直接用这个
        self.driver.find_element_by_xpath(".//*[@id='rtoolbar']/div[1]/a").click()
        sleep(2)
        self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/ul/li").click()
        sleep(2)

#        self.driver.find_element_by_xpath(".//*[@id='header']/div[3]/a").click()

        #只有第一次才需要
       # sleep(2)
        self.driver.find_element_by_xpath(".//*[@id='btnSave']").click()
        sleep(2)
        #点击思考题进行点评
        self.driver.find_element_by_xpath(".//*[@id='btQuestion']").click()
        sleep(3)
        list = []
        for ii in range(random.randint(1,i)):#随机点评几次
               a = choice(range(1,i+1))
               b = random.randint(1,5)
               self.driver.find_element_by_xpath("//*[@id='quesPicView']/div/div[1]/div/div/div[{}]/div[2]/div[1]/div/i[{}]".format(a,b)).click()#随机选择某条点评
               list.append({a:b})
               sleep(3)
        # #点击关闭控件关弹出框
        # driver.find_element_by_xpath(".//*[@id='closeFullleft']").click()
        sleep(3)
        #直接点击思考题按钮关闭
        self.driver.find_element_by_xpath(".//*[@id='btQuestion']").click()
        # #点击打开视频
        # self.driver.find_element_by_xpath(".//*[@id='btVideo']").click()
        # #关闭视频
        # sleep(3)
        # self.driver.find_element_by_xpath(".//*[@id='closeVideo']").click()
        #点击画笔
        # driver.find_element_by_xpath(".//*[@id='icon-editpen']").click()
        sleep(3)
        #点击课堂讨论按钮
        self.driver.find_element_by_xpath(".//*[@id='kttlbtn']").click()
        #提示
        self.driver.find_element_by_xpath(".//*[@class='u-button org']").click()
        return list

 def Comgroup(self,n):
        sleep(3)
        #点击分组按钮
        self.driver.find_element_by_xpath(".//*[@id='fzbtn']").click()
        #选择学号分组
        sleep(3)
        self.driver.find_element_by_xpath(".//div[@id='g-grounpcont']/div[3]/ul/li[{}]/i".format(n)).click()
        #self.driver.find_element_by_xpath(".//*[@id='g-grounpcont']/div[3]/ul/li[2]/i").click()
        #点击下一步
        self.driver.find_element_by_xpath(".//*[@id='groupnext']").click()
        #点击完成分组
        sleep(3)
        self.driver.find_element_by_xpath(".//*[@id='g-departGrounp']/div[4]/button[2]").click()

        sleep(3)
        #进入讨论
        #self.driver.find_element_by_xpath(".//*[@id='fzbtn']").click()
        #sleep(3)



 def screenevaluate(self):
        #组内互评
        self.driver.find_element_by_xpath(".//*[@id='btnGroupEval']").click()
        sleep(3)
        #提示点击确定
        self.driver.find_element_by_xpath(".//*[@id='btnGroupEvalTipConfirm']").click()
        sleep(3)
 def Again(self):
        #点击再来一轮
        self.driver.find_element_by_xpath("//*[@id='btnNextNowStage']").click()
        sleep(3)
        #提示点击确定
        self.driver.find_element_by_xpath("//*[@id='btnNowStageTipConfirm']").click()
        sleep(3)
 def Viewclassification(self):
        #点击观点分类
        self.driver.find_element_by_xpath(".//*[@id='btnOpinion']").click()
        sleep(3)
        #提示点击确定
        self.driver.find_element_by_xpath("//*[@id='btnOpinionTipConfirm']").click()
        sleep(3)
 def Diagnosticsummary(self):
        #点击诊断总结按钮
        self.driver.find_element_by_xpath("//*[@id='btnDiagnosis']").click()
        sleep(3)
        #提示点击确定
        self.driver.find_element_by_xpath("//*[@id='btnDiagnosisTipConfirm']").click()
        sleep(3)
        #点击知道了按钮
        self.driver.find_element_by_xpath("//*[@id='summytips']/div[3]/button").click()
        sleep(3)
 def Comments(self,i):
        #结束诊断总结，到小组投票阶段
        #点击知道了按钮
        self.driver.find_element_by_xpath("//*[@id='summytips']/div[3]/button").click()
        sleep(3)
        #点击诊断点评按钮
        self.driver.find_element_by_xpath("//*[@id='fydpbtn']").click()
        sleep(3)
       #提示点击确定
        self.driver.find_element_by_xpath("//*[@id='poptips']/div[3]/button[2]").click()
        # #对诊断进行点评
        sleep(3)
        list = []
        for ii in range(random.randint(1,i)):#随机点评几次
               a = choice(range(1,i+1))
               b = random.randint(1,5)
               self.driver.find_element_by_xpath(".//*[@id='drawCoverDiv']/div[{}]/div[3]/div/i[{}]".format(a,b)).click()#随机选择某条点评
               list.append({a:b})
               sleep(3)

        #self.driver.find_element_by_xpath(".//*[@id='drawCoverDiv']/div[1]/div[3]/div/i[5]").click()
        sleep(3)
        #点击课堂成绩
        self.driver.find_element_by_xpath("//*[@id='fydpbtn']").click()
        sleep(3)
        #提示点击确定
        self.driver.find_element_by_xpath("//*[@id='poptips']/div[3]/button[2]").click()
        sleep(3)
        return list

 def Vote(self,i):
        #结束小组投票环节，教师评分，到个人投票阶段
        #结束投票
        self.driver.find_element_by_xpath(".//*[@id='overVote']").click()
        sleep(3)
        #提示点击确定按钮
        self.driver.find_element_by_xpath(".//*[@id='btnSubmit']").click()
        sleep(3)
        #点击教师评分
        list = []
        for ii in range(random.randint(1,i)):
               # 获取滑动条的size
               anumber = choice(range(1,i+1))
               span_background = self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/div[2]/div/div[{}]/div/input".format(anumber))
               span_background_size = span_background.size
               a = (span_background_size["width"]/100)
               # 获取滑块的位置
               button = span_background
               #print(button)
               button_location = button.location
               n = random.randint(-63,37)
               x_location = button_location["x"]+n*a
               #x_location = button_location["x"]
               y_location = button_location["y"]
               ActionChains(self.driver).drag_and_drop_by_offset(button, x_location, y_location).perform()
               # self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/div[2]/div/div[{}]/p/span[contains(text(),'48')]".format(choice(range(1,i+1)))).click()
               # self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/div[2]/div/div[{}]/div/input".format(choice(range(1,i+1)))).send_keys("33")
               sleep(2)
               asd = self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/div[2]/div/div[{}]/p/span".format(anumber)).text
               list.append({anumber:int(asd)})

        sleep(3)
        #点击结束评分
        self.driver.find_element_by_xpath(".//*[@id='overGrade']").click()
        sleep(3)
        #提示点击确定按钮
        self.driver.find_element_by_xpath(".//*[@id='btnSubmit']").click()
        sleep(3)
        #点击个人表现
        self.driver.find_element_by_xpath(".//*[@class='m-tabnavi']/a[2]").click()
        sleep(3)
        return list

 def End(self):
        #点击结束投票
        self.driver.find_element_by_xpath(".//*[@id='overVote']").click()
        sleep(3)
        #提示点击确定按钮
        self.driver.find_element_by_xpath(".//*[@id='btnSubmit']").click()
        sleep(3)
 def screenexit(self):
        #关闭mvp按钮
        self.driver.find_element_by_xpath(".//*[@id='closemvp']").click()
        sleep(3)
        #点击成绩统计
        self.driver.find_element_by_xpath(".//*[@class='m-tabnavi']/a[3]").click()
        sleep(3)
        #点击左边退出按钮
        self.driver.find_element_by_xpath(".//*[@id='u-infol']/span/i").click()
        #退出课程
        sleep(3)
        self.driver.find_element_by_xpath(".//*[@class='infobtns']/a[1]").click()
        sleep(3)
        #点击左边退出按钮
        self.driver.find_element_by_xpath(".//*[@id='u-infol']/span/i").click()
        sleep(3)
        #退出登录
        self.driver.find_element_by_xpath(".//*[@id='m-InfoBar']/div[2]/a").click()
if __name__ == "__main__":
   test_screen('13789789789','1','rett453')
