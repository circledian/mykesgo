import threading
from time import sleep

import requests
import xlrd

from Brain_test.Tphone import ScreenOperationOne,ScreenOperationTwo
from Brain_test.Tscreen import test_screen
from Storming.Take_OtherToList import *
from Storming.excel import *
from Storming.logger import *
from Storming.readexcel import *
from Storming.score import *
from Storming.Generate_Random import *

#if __name__ == "__main__":
def wexcel(base_url,base_url1,mb,exname):
    #base_url = "http://192.168.0.167/"
    #base_url1 = "http://192.168.0.167/kesgo/login.html"
    s = requests.session()
    #mb = "13123123123"
    #exname = "9.19_7"
    interoperone = ScreenOperationOne(s,base_url,mb,exname)
    numb = random.randint(1,5)#??????????
    stulen = interoperone.StuLen#班级学生总数
    i = random.randint(1,stulen)#随机取数i
    stulisti = interoperone.Random_StuSel(i)#随机取i个学生的列表
    stulistsum = interoperone.StuList#学生总数的列表
    ExperimentID = interoperone.ExperimentID1#实验id
    curpath = os.path.dirname(os.path.realpath(__file__))
    testxlsx = os.path.join(curpath, "write.xlsx")
# wt = Write_excel("C:\\Users\\Administrator\\PycharmProjects\\Kesgotd_screen_CountScore\\case\\write.xlsx")
    wt = Write_excel(testxlsx)
    #wt = Write_excel("C:\\September_skill\\Brain_Storming\\Brain_test\\write.xlsx")

    log = Log()
    uioper = test_screen(base_url1)
    uioper.login(mb,"1")#大屏登录
#进入实验提交思考题
    listcount1 = []
    for stui in stulisti:#从随机生成的学生列表里取学生提交思考题
        interoperone.WriteQuestion(str(stui[0]))#手机写思考题、获取写的内容、提交思考题
        listcount1.append(str(stui[0]))

    listcount11 = uioper.clickexper(i)#大屏点击进入实验并点评思考题然后点击分组、开始讨论，记录评了第几条思考题以及评星数
    log.info("提交思考题的学生id列表,按时间顺序排列：%s"%listcount1+","+"评第几个思考题评多少星列表：%s"%listcount11)


    #uioper.clickexper(i)#大屏点击进入实验并点评思考题然后选择任意分组方式分组
    setgroupno = choice(range(1,6))
    uioper.Comgroup(setgroupno)

    interopertwo = ScreenOperationTwo(s,base_url,mb,exname)
    stu_len = interopertwo.Alen#学生数量
    k1 = random.randint(1,stu_len)#随机取数K1
    stu_listk = interopertwo.Random_ASel(k1)#随机取K1个学生的列表
    stu_listsum = interopertwo.GroupStuList#学生总数的列表
    groupstulen = interopertwo.GroupStuLen#小组数量
    k = random.randint(1,groupstulen)#随机取数k
    groupstulistk = interopertwo.Random_GroupStuSel(k)#随机取K个组长的列表
    groupstulistsum = interopertwo.GroupStuList#组长总数的列表

#开始观点讨论
    listcount_case1 = []#记录发言的小组id，组长id、小组orderno
    listcount_case1_1 = []
    def case1():
        for groupstuk in groupstulistk:
            for i in range(random.randint(1,3)):
                interopertwo.TNBrainCreateSpeak(str(groupstuk[0]),str(groupstuk[1]),str(groupstuk[2]),str(groupstuk[3]),str(groupstuk[5])) #观点讨论组长发言
                listcount_case1.append((str(groupstuk[0]),str(groupstuk[1]),str(groupstuk[2])))
                listcount_case1_1.append(str(groupstuk[1]))
                #uioper.driver.refresh()
                sleep(3)
    #print("组长数是%s"%k)
    listcount_case2 = []#记录发言的小组id，组长id、小组名称
    listcount_case2_1 = []
    def case2():
        for groupstuk1 in stu_listk:
            for i in range(random.randint(1,3)):
                interopertwo.TNGroupDiscussion(str(groupstuk1[0]),str(groupstuk1[1]),str(groupstuk1[3])) #观点讨论组内讨论
                listcount_case2.append((str(groupstuk1[0]),str(groupstuk1[1]),str(groupstuk1[3])))
                listcount_case2_1.append(str(groupstuk1[1]))
                sleep(3)
    #print("组员数是%s"%k)
    listcount_case3 = []#记录发言的小组id，组长id、小组名称
    listcount_case3_1 = []
    def case3():
        ii = random.randint(1,stulen)#随机取数ii
        stulistii = interoperone.Random_StuSel(ii)#随机取ii个学生
        for stuii in stulistii:
            for i in range(random.randint(1,4)):
                interopertwo.TNBrainCreateTimeInteraction(str(stuii[0]))#观点讨论我的互动
                listcount_case3.append([str(stuii[0])])
                listcount_case3_1.append(str(stuii[0]))
                sleep(3)
    funcs = [case1,case2,case3]
    athreads = []
    for func in funcs:
          thread = threading.Thread(target=func)
          athreads.append(thread)
    for thread in athreads:
          thread.start()
    for thread in athreads:
          thread.join()
    sleep(0.1)
    #print("发言的小组id、组长id、小组orderno列表：%s"%listcount_case1,"互动的学生id列表：%s"%listcount_case3,"组内讨论小组id，学生id，小组组名：%s"%listcount_case2)
    log.info("发言的小组id、组长id、小组orderno列表：%s"%listcount_case1+","+"互动的学生id列表：%s"%listcount_case3+","+"组内讨论小组id，学生id，小组组名：%s"%listcount_case2)

    all_student_id= listcount_case2_1+listcount_case1_1+listcount_case3_1
    #print("发言的学生id：%s"%all_student_id)
    log.info("发言的学生id：%s"%all_student_id)




    uioper.screenevaluate()#大屏端开始组内互评

    #基础条件
    Member_stu_len = interopertwo.GroupStuLen1#组员的数量
   # print(Member_stu_len)
    T = random.randint(1,Member_stu_len)#随机取数K1
   # print(T)
    Mem_stu_listk = interopertwo.Random_Stu_Num(T)#随机取K1个组员学生的列表
   # print(Mem_stu_listk)
    #组内互评
    listcount_discuss = {}
    for groupstuk in Mem_stu_listk:
        Mem_Stu_Id = str(groupstuk[1])#组员的id
        Mem_Stu_Id1 = str(groupstuk[1])#组员的id
        #print (Mem_Stu_Id)
        Group_Id = str(groupstuk[0])
        #print(Group_Id)#根据组员的id找到的组的id
        Group_Stu_Id = interopertwo.Random_Mem_GroupStuSel(Group_Id)
        Group_Stu_Id1 = interopertwo.Random_Mem_GroupStuSel(Group_Id)
        #print(Group_Stu_Id)#根据组员找到的组长的id
        e = str(random.randint(1,5))
        f = str(random.randint(1,5))
        interopertwo.TNSubmitBrainEvaluation(Group_Id,Mem_Stu_Id,Group_Stu_Id,e)
        listcount_discuss[Mem_Stu_Id]=e
        interopertwo.TNSubmitBrainEvaluation(Group_Id,Group_Stu_Id1,Mem_Stu_Id1,f)
        listcount_discuss[Group_Stu_Id1]=f
        #uioper.driver.refresh()
        sleep(3)
    log.info("被评星的学生id和星数：%s"%listcount_discuss)




#诊断总结
    uioper.Viewclassification()#大屏选择观点分类
    uioper.Diagnosticsummary()#开始诊断总结
    kk = random.randint(1,groupstulen)#随机取数kk
    groupstulistkk = interopertwo.Random_GroupStuSel(kk)#随机取KK个组长
    listcount_count = []
    for groupstukk in groupstulistkk:
        interopertwo.AddBrainDiagnosis(str(groupstukk[0]),str(groupstukk[1]),str(groupstukk[3]))

        interopertwo.TNSubmitBrainDiagnosis(str(groupstukk[0]),Unicode(100)+groupstukk[3],Unicode(10),groupstukk[3])#发送诊断总结
        listcount_count.append(str(groupstukk[0]))

        #uioper.driver.refresh()
        sleep(3)

    alist = interopertwo.Alist#学生列表
    listcount_count1 = uioper.Comments(kk)#点击诊断点评后点击课堂成绩
    log.info("提交诊断总结按组名顺序：%s"%listcount_count+","+"评第几个诊断总结评多少星列表：%s"%listcount_count1)
#小组投票
    groupidlist = []#初始记录列表
    grouplist = []
    for groupstu in groupstulistsum:
        groupidlist.append(str(groupstu[0]))#取出所有groupid
        grouplist.append((str(groupstu[0]),str(groupstu[1]),str(groupstu[2])))#取出所有的小组id，组长id，order no
    algrovoted = []
    listcount6 = []
    #print (grouplist)
    for groupvotenum in  range(random.randint(1,10)):
        b = choice(alist)
        bpart1stuid = str(b[1])#随机选择一个学生去投票
        bpart1groupid = str(b[0])#所选学生所在小组
        if bpart1stuid not in algrovoted:
            Remainlist = Take(groupidlist,bpart1groupid)#获取除去当前所选学生所在的小组的小组列表
            toGroupID = choice(Remainlist)
            interopertwo.Groupvote(bpart1stuid,toGroupID)#小组投票
            listcount6.append(toGroupID)
            uioper.driver.refresh()
            sleep(3)
            algrovoted.append(bpart1stuid)
    num = random.randint(1,groupstulen)#随机取数kk
    listcount66 = uioper.Vote(num)#结束投票
    log.info("评第几个小组评多少分列表%s"%listcount66+","+"被投票小组id列表%s"%listcount6)
   # Group_num = random.randint(1,groupstulen)
   # uioper.Vote(Group_num)#结束投票
#个人投票
    alpervoted = []#初始记录列表
    listcount7 = []
    for personalvotenum in range(random.randint(1,10)):
        a = TakeOneToList(alist)
        apart1 = a[0]
        apart1stuid = str(apart1[1])#随机选择一个学生去投票
        if apart1stuid not in alpervoted:
            apart2 = a[1]
            apart2stuid = str(choice(apart2)[1])#随机选择一个学生被投票
            interopertwo.Personalvote(apart1stuid,apart2stuid)#投票
            listcount7.append(apart2stuid)
            uioper.driver.refresh()
            sleep(3)
            alpervoted.append(apart1stuid)#投过票的加入记录列表里
    log.info("被投票学生id列表%s"%listcount7)
    uioper.driver.refresh()
    sleep(3)
    uioper.End()
    uioper.screenexit()











    #写入标题
    score = Score()
    coln = 1
    colnames=["学生id","思考题系统得分","思考题教师评分","头脑风暴","诊断总结","学生之间相互投票","系统评分","小组互评","教师评分",
              "组内互评","头脑风暴=头脑风暴+诊断总结","个人表现=学生互评+系统评分+组内互评","小组表现=小组互评+教师评分","总分"]

    #colnames=["学生id","思考题系统得分","思考题教师评分","头脑风暴=头脑风暴+诊断总结","个人表现=学生互评+系统评分+组内互评","学生之间相互投票","系统评分","小组表现=小组互评+教师评分","总分","组内互评"]
    for colname in colnames:
        wt.writee(1,coln ,colname)
        coln+=1
    #将学生id写进excel第一列
    rown = 2
    for stuid in stulistsum:
        wt.writee(rown, 1,str(stuid[0]))
        rown+=1
    #curpath = os.path.dirname(os.path.realpath(__file__))
    #testxlsx = os.path.join(curpath, "write.xlsx")
    excel = Excelread(testxlsx,"Sheet")
    #excel = Excelread("C:\\September_skill\\Brain_Storming\\Brain_test\\write.xlsx","Sheet")
    table = excel.table
    rowNum = excel.rowNum    # 获取总行数
    colNum = excel.colNum


#写入思考题系统评分，和思考题教师评分，占比15%
    Thinking_score = score.getscore1(listcount1,listcount11)#获取学生思考题实际评分
    for i in range(1,rowNum):#循环取每一行的学生数据
        values = table.row_values(i)
        #将取到的学生id是否在提交思考题的学生id里
        if str(values[0]) in listcount1:
            wt.writee(i+1, 2,5)
            if str(values[0]) in Thinking_score.keys():#该学生是否被评分，评了多少星
                wt.writee(i+1, 3,Thinking_score[str(values[0])]*10/5)
            else:
                wt.writee(i+1, 3,0)
        else:
            wt.writee(i+1, 2,0)
            wt.writee(i+1, 3,0)

    listsum = []
#头脑风暴中，总共的发言条数的排序，得分，占比15%，不写入表
    Brain_storming = score.getsysscore1(listcount_case1,15)
    log.info("头脑风暴得分%s"%Brain_storming)
    listsum.append(Brain_storming)

#诊断总结根据评星数算分，占比30%，不写入表
    Diagnosissummary = score.gettecscored4(listcount_count,listcount_count1,6)
    log.info("诊断总结得分%s"%Diagnosissummary)
    listsum.append(Diagnosissummary)
#头脑风暴=头脑风暴+诊断总结，占45%




#个人表现 = 学生互评+系统评分+组内互评，占15%









#学生之间相互投票，学生互评，占比5%
    Mutual_evaluation_of_students = score.getsysscore2(listcount7,5)
    log.info("学生之间相互投票%s"%Mutual_evaluation_of_students)
    listsum.append(Mutual_evaluation_of_students)
#系统评分，发言的总条数，占比5%
    System = score.system(all_student_id,5)
    log.info("系统评分%s"%System)
    listsum.append(System)
#小组互评，占10%，不写入表格
    Groupevaluation = score.getsysscore1(listcount6,10)
    log.info("小组互评得分%s"%Groupevaluation)
    listsum.append(Groupevaluation)
#教师评分，占10%，不写入表格
    GroupTecscoredlist = score.gettecscored3(grouplist,listcount66,10/100)
    log.info("教师评分评分%s"%GroupTecscoredlist)
    listsum.append(GroupTecscoredlist)
#小组表现=小组互评+教师评分，占20%






#组内互评，占5%values1_listcount_discuss
    log.info("组内互评%s"%listcount_discuss)
    listsum.append(listcount_discuss)
    col = 4
    for list in listsum:
        for i in range(1,rowNum):
            values = table.row_values(i)
            if str(values[0]) in list.keys():
                wt.writee(i+1, col,float(list[str(values[0])]))
            else:
                wt.writee(i+1, col,0)
        col+=1

    #curpath = os.path.dirname(os.path.realpath(__file__))
    #testxlsx = os.path.join(curpath, "write.xlsx")
    excel1 = Excelread(testxlsx,"Sheet")
    #excel1 = Excelread("C:\\September_skill\\Brain_Storming\\Brain_test\\write.xlsx","Sheet")
    rr = excel1.dict_data()
    # print("excel中值列表为：%s"%rr)
    log.info("excel中值列表为：%s"%rr)

    for r in rr:
        Course_Score = (r["头脑风暴"])+(r["诊断总结"])
        Group_Score = (r["小组互评"])+(r["教师评分"])
        Personal_Score = (r["学生之间相互投票"])+(r["系统评分"])+(r["组内互评"])
        Total_Score = (r["思考题系统得分"])+(r["思考题教师评分"])+(r["头脑风暴"])+(r["诊断总结"])+(r["学生之间相互投票"])+(r["系统评分"])+\
                     (r["小组互评"])+(r["组内互评"])+(r["教师评分"])
        wt.writee((r["rowNum"]), 11,Course_Score)
        wt.writee((r["rowNum"]), 13,Group_Score)
        wt.writee((r["rowNum"]), 12,Personal_Score)
        wt.writee((r["rowNum"]), 14,Total_Score)
    log.info("----测试结束----")




















