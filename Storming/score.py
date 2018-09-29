
from operator import itemgetter, attrgetter
from Storming.test1 import MssqlUtil
class Score():
 def __init__(self):
    self.A = MssqlUtil()
 def TNscore_count(self,a):
    b = range(100,-5,-5)
    #print(b[20])
    sumspeak = []
    set_a = set(a) #List_set是另外一个列表，里面的内容是List里面的无重复 项
   # print(set_a)
    #print(type(set_a))
    for item in set_a:
        #print("the %s has found %d" %(item,a.count(item)))
        sumspeak.append((item,a.count(item)))
    sumspeaksort = sorted(sumspeak, key=itemgetter(1), reverse=True)
    len1 = len(sumspeaksort)#5
    TN_stage = [(sumspeaksort[0][0],100)]
    for i in  range(len1-1):#0开始到3
        if sumspeaksort[i][1]==sumspeaksort[i+1][1]:
            TN_stage.append((sumspeaksort[i+1][0],TN_stage[i][1]))
        else:
            TN_stage.append((sumspeaksort[i+1][0],b[i+1]))
    return TN_stage
    #print(TN_stage)

 def getscore(self,a,b):
    bb=b[::-1]#列表反序评分
    ii = []
    scored = {}
    for i in bb:
        for key,value in i.items():
            #print(key,value)
            if key not in ii:
                stuid = a[-key]
                defen = value
                scored[stuid]=defen
                #print("学生%s评%s分"%(stuid,defen))
                ii.append(key)
    return scored

 def getscore1(self,a,b):
    scored = {}#反序评星
    for i in b:
        for key,value in i.items():
                stuid = a[-key]
                if stuid in scored.keys() and value ==scored[stuid]:
                    scored[stuid]=value-1
                else:
                    scored[stuid]=value
    return scored
 # def getscore2(self,a,b):#取实际评分（评星）
 #        aa = []
 #        scored = {}
 #        for i in b:
 #            if aa.count(i)%2==1:
 #                for key,value in i.items():
 #                    stuid = a[-key]
 #                    defen = value-1
 #                    scored[stuid]=defen
 #            else:
 #                for key,value in i.items():
 #                    stuid = a[-key]
 #                    defen = value
 #                    scored[stuid]=defen
 #            aa.append(i)
 #        return scored
 def getscore2(self,a,b):#正序评星
    scored = {}
    for i in b:
        for key,value in i.items():
                stuid = a[key-1]
                if stuid in scored.keys() and value ==scored[stuid]:
                    scored[stuid]=value-1
                else:
                    scored[stuid]=value
    return scored
 def gettecscored(self,listcount,listcountscored,fz):#取教师评分
    scoredlist = {}
    set_listcount = set(listcount)
    set_set_listcountsort = sorted(set_listcount, key=itemgetter(2), reverse=True)
    groupscored = self.getscore1(set_set_listcountsort,listcountscored)#获取组长发言的实际评分
    # print(groupscored)
    for groupkey,groupvalue in groupscored.items():
        groupidscored = groupkey
        # print("小组id是%s"%groupidscored)
        scoredsql = "select StudentID from dbo.AFCS_GroupStudents where GroupID ='"+groupidscored+"'"
        scoredgetstulist= self.A.mssql_getrows(scoredsql)
        for scoredgetstu in scoredgetstulist:
            scoredStudentID = str(scoredgetstu[0])
            # print("学生id是%s"%scoredStudentID)
            stuscored = groupvalue
            #print(type(stuscored))
            # print("星数是%s"%stuscored)
            scoredlist[scoredStudentID]=stuscored*fz
    # print("学生发言评分%s"%scoredlist)
    return scoredlist



 def getsysscore1(self,listcount,fz):
    scorelist = {}
    groupspercent = self.TNscore_count(listcount)
    # print(groupspercent)
    for grouppercent in groupspercent:
        # print(grouppercent)
        # print(type(grouppercent[0]))
        if type(grouppercent[0])== tuple:
            grouppercentid = grouppercent[0][0]
        else:
            grouppercentid = grouppercent[0]
        # print("小组id是%s"%grouppercentid)
        scoresql = "select StudentID from dbo.AFCS_GroupStudents where GroupID ='"+grouppercentid+"'"
        scoregetstulist= self.A.mssql_getrows(scoresql)
        for scoregetstu in scoregetstulist:
            scoreStudentID = str(scoregetstu[0])
            # print("学生id是%s"%scoreStudentID)
            stupercent = grouppercent[1]
            # print(type(stupercent))
            # print("百分比是%s"%stupercent)
            scorelist[scoreStudentID]=((stupercent)/100)*fz
    # print("学生得分%s"%scorelist)
    return scorelist
 def getsysscore2(self,listcount,fz):
    scorelist = {}
    groupspercent = self.TNscore_count(listcount)
    # print(groupspercent)
    for grouppercent in groupspercent:
        # print(grouppercent)
        # print(type(grouppercent[0]))
        if type(grouppercent[0])== tuple:
            grouppercentid = grouppercent[0][0]
        else:
            grouppercentid = grouppercent[0]
        # print("小组id是%s"%grouppercentid)
        scoresql = "select StudentID from dbo.AFCS_GroupStudents where StudentID ='"+grouppercentid+"'"
        scoregetstulist= self.A.mssql_getrows(scoresql)
        for scoregetstu in scoregetstulist:
            scoreStudentID = str(scoregetstu[0])
            # print("学生id是%s"%scoreStudentID)
            stupercent = grouppercent[1]
            # print(type(stupercent))
            # print("百分比是%s"%stupercent)
            scorelist[scoreStudentID]=((stupercent)/100)*fz
    # print("学生得分%s"%scorelist)
    return scorelist
 def gettecscored3(self,listcount,listcountscored,fz):#取教师评分
    scoredlist = {}
    set_listcount = set(listcount)
    set_set_listcountsort = sorted(set_listcount, key=itemgetter(2), reverse=True)
    groupscored = self.getscore(set_set_listcountsort,listcountscored)#获取组长发言的实际评分
    #print(groupscored)
    for groupkey,groupvalue in groupscored.items():
        groupidscored = groupkey[0]
        #print("小组id是%s"%groupidscored)
        scoredsql = "select StudentID from dbo.AFCS_GroupStudents where GroupID ='"+groupidscored+"'"
        scoredgetstulist= self.A.mssql_getrows(scoredsql)
        for scoredgetstu in scoredgetstulist:
            scoredStudentID = str(scoredgetstu[0])
            # print("学生id是%s"%scoredStudentID)
            stuscored = groupvalue
            #print(type(stuscored))
            # print("星数是%s"%stuscored)
            scoredlist[scoredStudentID]=stuscored*fz
    # print("学生发言评分%s"%scoredlist)
    return scoredlist

 def gettecscored4(self,listcount,listcountscored,fz):#诊断总结评星
    scoredlist = {}
    #set_listcount = set(listcount)
    # set_set_listcountsort = sorted(set_listcount, key=itemgetter(2), reverse=True)
    groupscored = self.getscore2(listcount,listcountscored)
    # print(groupscored)
    for groupkey,groupvalue in groupscored.items():
        groupidscored = groupkey
        # print("小组id是%s"%groupidscored)
        scoredsql = "select StudentID from dbo.AFCS_GroupStudents where GroupID ='"+groupidscored+"'"
        scoredgetstulist= self.A.mssql_getrows(scoredsql)
        for scoredgetstu in scoredgetstulist:
            scoredStudentID = str(scoredgetstu[0])
            # print("学生id是%s"%scoredStudentID)
            stuscored = groupvalue
            #print(type(stuscored))
            # print("星数是%s"%stuscored)
            scoredlist[scoredStudentID]=stuscored*fz
    # print("学生发言评分%s"%scoredlist)
    return scoredlist

 def system(self,all_student_id,fz):
    System = {}
    System_score = self.TNscore_count(all_student_id)
    #print(System_score)
    for System_grouppercent in System_score:
            StudentID = str(System_grouppercent[0])
            #print("学生id是%s"%StudentID)
            System_stupercent = System_grouppercent[1]
            #print(type(System_stupercent))
            #print("百分比是%s"%System_stupercent)
            System[StudentID]=((System_stupercent)/100)*fz
    return System
if __name__ == '__main__':
   test= Score()
   a = ['aaa', 'ccc', 'eee', 'fff', 'ggg']#思考题提交的学生id 按时间顺序
   b = [{2: 2}, {5: 5},{5:5},{5:4}]#思考题评分
   # print(test.getscore2(a,b))
   #  c = [('c', 'c3', '3'),('c', 'c3', '3'),('c', 'c3', '3'),
   #     ('e', 'e5', '5'),('e', 'e5', '5'),('e', 'e5', '5'), ('e', 'e5', '5'),
   #     ('i', 'i9', '9'),('i', 'i9', '9'),('i', 'i9', '9'),('i', 'i9', '9'),
   #     ('d', 'd4', '4'),('d', 'd4', '4'),('d', 'd4', '4'),
   #   ('a','a1','1')]
   #  d = [('e', 'c3', '3'),('e', 'c3', '3'),('c', 'c3', '3'),
   #     ('e', 'e5', '5'),('e', 'e5', '5'),('h', 'e5', '5'), ('h', 'e5', '5'),
   #     ('i', 'i9', '9'),('f', 'i9', '9'),('g', 'i9', '9'),('i', 'i9', '9'),
   #     ('t', 'd4', '4'),('t', 'd4', '4'),('d', 'd4', '4'),
   #   ('a','a1','1')]
   #  A = ['aaa','bbb','ccc','ddd','eee','fff','ggg','hhh']#学生id
   #  e = ['1','2','1','3','1','4','2','3']
   # zhenduanzongjie  = ['a','b','c','d','e','f','g','h','i']
   # listcount1 = [{4:2},{5:3},{4:5},{3:4}]
   #
   # print(test.getscore2(zhenduanzongjie,listcount1,6))
   # listcount = [('xiaozu2','zuzhang2','2'),('xiaozu5','zuzhang5','5'),('xiaozu4','zuzhang4','4'),('xiaozu1','zuzhang1','1'),('xiaozu3','zuzhang3','3')]
   # listcount1 = {4:60},{5:30},{4:80},{3:100}
   # print(test.gettecscored3(listcount,listcount1,5))

   listcount_count=['1f36fb3e-d3e8-49ef-bb42-a56125267014', 'fed058ac-fec7-454e-bf5f-621dd231f5f3', '9486d7c4-2107-4d9e-aff5-f034e985c0de']
   listcount_count1=[{1: 5}]
   score = Score()
   Diagnosissummary = score.gettecscored4(listcount_count,listcount_count1,6)
   print(Diagnosissummary)
   listcount_count2=[{1: 62}]
