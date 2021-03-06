# coding=utf-8
import unittest
import time
from Storming import HTMLTestRunner_td
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import datetime
from Brain_test import Tstorming
import unittest

from Brain_test.Backstage_interface import *

#from Brain_test.Backstage import Operation_back_screen
from Storming.Generate_Random import *
#下面三行代码python2报告出现乱码时候可以加上####
'''import sys
reload(sys)
sys.setdefaultencoding('utf8')'''

# 这个是执行所有用例并发送报告，分四个步骤
# 第一步加载用例
# 第二步执行用例
# 第三步获取最新测试报告
# 第四步发送邮箱

# 当前脚本的真实路径
cur_path = os.path.dirname(os.path.realpath(__file__))

def add_case(caseName="case", rule="test*.py"):
    '''第一步：加载所有的测试用例'''
    case_path = os.path.join(cur_path, caseName)  # 用例文件夹
    # 如果不存在这个case文件夹，就自动创建一个
    if not os.path.exists(case_path):os.mkdir(case_path)
    print("test case path:%s"%case_path)
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(case_path,
                                                  pattern=rule,
                                                  top_level_dir=None)
    # print(discover)
    '''
    testcase = unittest.TestSuite()
    # 直接加载discover
    testcase.addTests(discover)
    runner = unittest.TextTestRunner()
    runner.run(testcase)
    '''
    return discover



def run_case(all_case, reportName="report"):
    '''第二步：执行所有的用例, 并把结果写入HTML测试报告'''
    report_path = os.path.join(cur_path, reportName)  # 用例文件夹
    # 如果不存在这个report文件夹，就自动创建一个
    if not os.path.exists(report_path):os.mkdir(report_path)
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    report_abspath = os.path.join(report_path, "result_"+now+".html")
    print("report path:%s"%report_abspath)
    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner_td.HTMLTestRunner(stream=fp,
                                           title=u'自动化测试报告,测试结果如下：',
                                           description=u'用例执行情况如下：')

    # 调用add_case函数返回值
    runner.run(all_case)
    fp.close()

def get_report_file(report_path):
    '''第三步：获取最新的测试报告'''
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print (u'最新测试生成的报告： '+lists[-1])
    # 找到最新生成的报告文件
    report_file = os.path.join(report_path, lists[-1])
    return report_file

def send_mail(sender, psw, receiver, smtpserver, report_file, port):
    '''
    file_path = "result.html"
    with open(file_path, "rb") as fp:
        mail_body = fp.read()

    第四步：发送最新的测试报告内容'''
    with open(report_file, "rb") as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()
    msg['Subject'] = u"自动化测试报告"  #主题
    msg["from"] = sender
    msg["to"] = ",".join(receiver)     # 只能字符串
    #msg["to"] = ";".join(receiver)  多个收件人list转str
    body = MIMEText(mail_body, _subtype='html', _charset='utf-8')  #正文
    msg.attach(body)
    # 添加附件
    att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename= "report.html"' #filename参数是发送的附件重新命名
    msg.attach(att)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)                      # 连服务器
        smtp.login(sender, psw)
    except:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
        smtp.login(sender, psw)                       # 登录
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('test report email has send out !')


if __name__ == "__main__":
    import os
    import configparser
    from config import readConfig

    base_url = readConfig.base_url
    base_url1 = readConfig.base_url1

    # mb = readConfig.mb
    # exname = readConfig.exname

    mb = tecphone_num()
    exname = GBK2312(3)
    tcname = GBK2312(3)
    print("生成的手机号码是%s"%mb)
    print("生成的实验名是%s"%exname)
    cur_path = os.path.dirname(os.path.realpath(__file__))
    configPath = os.path.join(cur_path,"config\\cfg.ini")
    conf = configparser.ConfigParser()
    conf.read(configPath)
    conf.set("experiment", "exname",exname)
    conf.write(open(configPath, "r+"))

    Process(base_url).all_Technological_process(tcname,mb,exname)
    Tstorming.wexcel(base_url,base_url1,mb,exname)
    all_case = add_case(caseName="Brain_test", rule="test*.py")   #  加载用例
    # # 生成测试报告的路径
    run_case(all_case)        #  执行用例
    # # 获取最新的测试报告文件

    report_path = os.path.join(cur_path, "report")  # 测试报告路径
    report_file = get_report_file(report_path)  # 获取最新的测试报告
    # #邮箱配置
    sender = readConfig.sender
    psw = readConfig.psw
    smtp_server = readConfig.smtp_server
    port = readConfig.port
    receiver = readConfig.receiver
    #print(sender,psw,smtp_server,port,receiver)
    send_mail(sender, psw, receiver, smtp_server, report_file, port)


    # sender = "992147569@qq.com"
    # psw = "wccrgllaygvrbfbf"
    # smtp_server = "smtp.qq.com"
    # port = 465
    # #receiver = ["aa@qq.com", "bb@qq.com"] 发给多个收件人
    # receiver = "364456215@qq.com"
    # send_mail(sender, psw, receiver, smtp_server, report_file, port)  # 最后一步发送报告




