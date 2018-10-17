
import requests
import random
import json
import time
import pymssql
import random
import uuid
from flask import json



from Storming.test1 import MssqlUtil
import sys
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
from random import choice


class ScreenOperationOne():
 def __init__(self, s,base_url,mb,exname):
       # s = requests.session()  # 全局参数
       self.s = s
       self.base_url = base_url
       self.A = MssqlUtil()
       sql1 = "select a.ExperimentID,a.CaseID from dbo.AFCS_Experiment a join dbo.AFCS_TeacherInfo b " \
           "on a.AddUser = b.TeacherID " \
           "where MobileNo = '"+mb+"' " \
           "and ExperimentName = '"+exname+"' " \
           "and ExperimentStatus = '1'"
       B1 = self.A.mssql_getrows(sql1)   #根据教师手机号、实验名找该教师下已开始的实验id、案例id

       self.ExperimentID1 = str(B1[0][0])
       self.CaseID1 = str(B1[0][1])
       sql2 = "SELECT ClassID FROM dbo.AFCS_ClassSelect where ExperimentID ='"+self.ExperimentID1+"'"
       B2 = self.A.mssql_getrows(sql2)  #根据教师实验id找实验下的班级id 取第1个班级
       self.ClassID2 = str(B2[0][0])
       sql3 = "select QuestionsID,QuestionsContent,QuestionOrderNo from   dbo.AFCS_PolicyCaseQuestions where CaseID = '"+self.CaseID1+"' and QuestionType='1'"
       sql3s = "select * from   dbo.AFCS_PolicyCaseQuestions where CaseID = '"+self.CaseID1+"' and QuestionType='2'"
       B3 = self.A.mssql_getrows(sql3) #根据案例id找思考题id (简答题)
       B3s = self.A.mssql_getrows(sql3s) #根据案例id找思考题id (选择题)
       self.QuestionsID3 = str(B3[0][0])
       self.QuestionsContent3 = str(B3[0][1])
       self.QuestionOrderNo3 = str(B3[0][2])
       self.QuestionsID3s = str(B3s[0][0])
       self.QuestionsContent3s = str(B3s[0][1])
       self.QuestionOrderNo3s =  str(B3s[0][2])
       sql4 = "select StudentID FROM  dbo.AFCS_ClassStudents where ClassID = '"+self.ClassID2+"'"
       B4 = self.A.mssql_getrows(sql4) #根据班级id找学生id 获取学生id
       self.StudentID4 = str(B4[0][0])#获取第一个学生
       self.StuLen = len(B4)#获取学生总数
       self.StuList = B4
       self.RanStu = str(choice(self.StuList)[0])#随机选择学生数，第一个[]中数字，在学生数中随机

 def Random_StuSelone(self):#随机抽取一个学生
    liststu = self.StuList
    RanStu = str(choice(liststu)[0])
    return RanStu

 def Random_StuSel(self,n):#随机取n个学生
    liststu = self.StuList
    slice = random.sample(liststu, n)
    return slice
 def WriteQuestion(self,stu):
#填写思考题（问答题）
     #url = "http://192.168.0.167/kesgo.Service/wcf/CaseService.svc/AddOrUpdateQuestionPreview"
     url = urljoin(self.base_url,"kesgo.Service/wcf/CaseService.svc/AddOrUpdateQuestionPreview")
     body = {"questionpreviewinfo":
     "{\"QuestionsID\":\""+self.QuestionsID3+"\","
     "\"QuestionsContent\":\""+self.QuestionsContent3+"\","
     "\"CaseID\":\""+self.CaseID1+"\","
     "\"QuestionOrderNo\":"+self.QuestionOrderNo3+","
     "\"QuestionType\":1,"
     #"\"PreviewID\":\"280b969f-08be-439e-9f75-19500545598d\","
     "\"PreviewID\":\"00000000-0000-0000-0000-000000000000\","
     "\"ExperimentID\":\""+self.ExperimentID1+"\","
     "\"PreviewContent\":\""+str(random.randint(1,1000))+"\","
     "\"StudentID\":\""+stu+"\","
     "\"AddTime\":\"/Date(-62135596800000)/\","
     "\"Grade\":0,"
     "\"IsSubmit\":2,"
     "\"CaseQuesOption\":\"[]\","
     "\"PicList\":\"[]\"}"}
     h = {"Content-Type": "application/json;charset=UTF-8"}
     r = self.s.post(url, json=body, headers=h)
     #print(r.status_code)
 #def GetPreviewID(self):
     url3 = urljoin(self.base_url,"kesgo.Service/wcf/CaseService.svc/GetQuesByWhere")
     #url3 = "http://192.168.0.167/kesgo.Service/wcf/CaseService.svc/GetQuesByWhere"
     par = {"expID":self.ExperimentID1,
            "stuID":stu
            }
     h3= {"Accept": "application/json, text/plain, */*",
     "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
         }
     r3 = requests.get(url3,params=par,headers=h3)
     #print(r3.content.decode("utf-8"))
     a = r3.json()
     b = json.loads(a)
     c= b["Table"]
     for i in c:
         idt = dict(i)
         if idt["QuestionsID"]==self.QuestionsID3:
            d = idt["PreviewID"]
            #return d


 #def SubmitQuestion(self,d):
#提交思考题
     url2 = urljoin(self.base_url,"kesgo.Service/wcf/CaseService.svc/SaveQuesAnswer")
     #url2 = "http://192.168.0.167/kesgo.Service/wcf/CaseService.svc/SaveQuesAnswer"
     body2 = {"previewInfo":
     "[{\"PreviewID\":\""+d+"\","
     "\"ExperimentID\":\""+self.ExperimentID1+"\","
     "\"QuestionsID\":\""+self.QuestionsID3+"\","
     "\"StudentID\":\""+stu+"\","
     "\"IsSubmit\":1},"
     "{\"PreviewID\":\"00000000-0000-0000-0000-000000000000\","
     "\"ExperimentID\":\""+self.ExperimentID1+"\","
     "\"QuestionsID\":\""+self.QuestionsID3s+"\","
     "\"StudentID\":\""+stu+"\","
     "\"IsSubmit\":1}]"
            }
     h = {"Content-Type": "application/json;charset=UTF-8"}
     r2 = self.s.post(url2, json=body2, headers=h)
     #print(r2.status_code)



class ScreenOperationTwo(ScreenOperationOne):
 def __init__(self,s,base_url,mb,exname):
#分组后发送观点讨论的组长发言
    super().__init__(s,base_url,mb,exname)
    sql5 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName,GroupAnotherName,RealName,* from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID join dbo.AFCS_StudentInfo c on b.StudentID = c.StudentID where a.ExperimentID = '"+self.ExperimentID1+"' and b.IsLeader = '1'"
    #B10 = self.A.mssql_getrows(sql10) #根据实验id找小组组号、组长学生id 取第一个小组

    sql7 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName,* from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID " \
       "where a.ExperimentID = '"+self.ExperimentID1+"'"
    B6 = self.A.mssql_getrows(sql7)
    self.Alist = B6
    self.Alen = len(B6)
    self.a = str(choice(self.Alist)[1])
    sql10 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName,* from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID " \
       "where a.ExperimentID = '"+self.ExperimentID1+"' and b.IsLeader = '1'"
    B5 = self.A.mssql_getrows(sql5) #根据实验id找小组组号、组长学生id 取第一个小组
    self.toGroupID5 = str(B5[1][0])
    self.toStudentID5 = str(B5[1][1])
    self.GroupStuList = B5
    self.GroupStuLen = len(B5)
    self.RanGroupStu = str(choice(self.GroupStuList)[1])
    sql8 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName,* from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID " \
       "where a.ExperimentID = '"+self.ExperimentID1+"' and b.IsLeader = '2'"
    B7=self.A.mssql_getrows(sql8)
    self.GroupStuList1 = B7
    self.GroupStuLen1 = len(B7)
    self.RanGroupStu1 = str(choice(self.GroupStuList1)[1])
    self.Group_memberID1 = str(B7[0][1])
    self.GroupID5 = str(B7[0][0])
    sql9 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName,* from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID " \
       "where a.ExperimentID = '"+self.ExperimentID1+"' and b.IsLeader = '1'and a.GroupID ='"+self.GroupID5+"'"
    B8=self.A.mssql_getrows(sql9)
    self.GroupStuList2 = B7
    self.GroupStuLen12 = len(B7)
    self.StudentID5 = str(B8[0][1])#Group_leaderID1
    self.GroupOrderNo5 = str(B8[0][2])
    self.GroupName5 = str(B8[0][3])

 def Random_ASel(self,n):#随机取n个学生
    listA = self.Alist
    Aslice = random.sample(listA, n)
    return Aslice
 def Random_GroupStuSelone(self):
    listgroupstu = self.GroupStuList
    RanGroupStu = str(choice(listgroupstu)[1])
    return RanGroupStu
 def Random_GroupStuSeltwo(self):
    listgroupstu = self.GroupStuList1
    RanGroupStu = str(choice(listgroupstu)[1])
    return RanGroupStu
 def Random_GroupStuSel(self,n):#随机取n个组长
    listGroupstu = self.GroupStuList
    Groupslice = random.sample(listGroupstu, n)
    return Groupslice

 def Random_Stu_Num(self,n):#随机取在组中的一个组员
    listGroupstu = self.GroupStuList1
    Groupslice = random.sample(listGroupstu, n)
    return Groupslice

 def Random_Mem_GroupStuSel(self,groupid):#取有组员的一个 组长
    sql9 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID " \
       "where a.ExperimentID = '"+self.ExperimentID1+"' and b.IsLeader = '1'and a.GroupID ='"+groupid+"'"

    A=self.A.mssql_getrows(sql9)
    Group_leaderID =str(A[0][1])
    return Group_leaderID

 def TNGroupDiscussion(self,GroupID,StudentID,GroupName):
     #头脑风暴，组内讨论
     TNurl1 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/BrainCreateGroupDiscussion")
     #TNurl1 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/BrainCreateGroupDiscussion"
     TNbody1 = {

	     "groupDiscussionEntity":
             "{\"GroupDiscussionID\":\"00000000-0000-0000-0000-000000000000\","
             "\"StudentID\":\""+StudentID+"\","
             "\"GroupID\":\""+GroupID+"\","
             "\"InteractionContent\":\""+"组内讨论"+GroupName+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"NowStage\":1,"
             "\"GroupName\":\""+GroupName+"\","
             "\"IsSendSpeak\":2,"
             "\"AddTime\":\"1900-1-1\"}"

     }
     TNh1 = {
         "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36"
     }
     TNr1 = self.s.post(TNurl1, json=TNbody1, headers=TNh1)
    # print("发表组内讨论学生ID%s"%StudentID)
 def TNBrainCreateSpeak(self,GroupID,StudentID,GroupOrderNo,GroupName,Realname):
     #头脑风暴，小组观点
     TNurl2 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/BrainCreateSpeak")
     #TNurl2 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/BrainCreateSpeak"
     TNbody2 = {
         "speakEntity":
             "{\"SpeakID\":\"00000000-0000-0000-0000-000000000000\","
             "\"GroupID\":\""+GroupID+"\","
             "\"SpeakContent\":\"小组观点+"+GroupName+"\","
             "\"Grade\":0,"
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"GroupOrderNo\":\""+GroupOrderNo+"\","
             "\"NowStage\":1,"
             "\"GroupName\":\""+GroupName+"\","
             "\"StudentID\":\""+StudentID+"\","
             "\"IsDelete\":2,"
             "\"AddTime\":\"1900-1-1\"}"


     }
     TNh2 ={
         "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36"
     }
     TNr2 = self.s.post(TNurl2, json=TNbody2, headers=TNh2)
     speakid = TNr2.text
     speakid = speakid.replace("\"", "")
    # print("发表小组观点组名%s"%GroupName,"发表小组观点学生ID%s"%StudentID)
     TNurl2_siglar = "http://192.168.0.249:18199/signalr/signalr/send?transport=longPolling&connectionToken=AQAAANCMnd8BFdERjHoAwE%2FCl%2BsBAAAAVdYmo0qzSEea%2BwEs7MZ4ngAAAAACAAAAAAAQZgAAAAEAACAAAACZn3n0d8sXPa9%2F9yQVafaaDByIzNd%2F47o4YJENdf7sVQAAAAAOgAAAAAIAACAAAADwnOTM%2BG3%2B6dyxtSLsStkFRSYmG%2BwB0%2BTW2PNPmCsWOTAAAABLZWKSf8JFizkRc4t8o2nnJWSv54WCsVMoQuXoDDBlAF70xSG0qULMpwgY731QKTlAAAAACBygiv41yeYiWcH%2B5sBYESrfJDYogaSBh4rP%2BESMAZkesTFXgpb5bpubOthRlJWDUWevL5PtGX9fQ8NhNj0OBg%3D%3D&groupid="+self.ExperimentID1

     TNbody2_siglar = {"data":"{\"H\":\"kesgohub\",\"M\":\"sendGroupSpeakData\",\"A\":[1,\"{\\\"speakID\\\":\\\""+speakid+"\\\",\\\"groupOrderNo\\\":\\\""+GroupOrderNo+"\\\",\\\"groupName\\\":\\\""+GroupName+"\\\",\\\"speakContent\\\":\\\"小组观点+"+GroupName+"\\\",\\\"groupID\\\":\\\""+GroupID+"\\\",\\\"isLeader\\\":\\\"1\\\",\\\"studentId\\\":\\\""+StudentID+"\\\",\\\"realName\\\":\\\""+Realname+"\\\",\\\"headImage\\\":\\\"/images/common/normalFace.png\\\",\\\"groupAnotherName\\\":\\\""+GroupName+"\\\",\\\"HourAndMinute\\\":\\\"11:28\\\"}\"],\"I\":0}"}
     TNh2_siglar = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
           "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36"}
     r = requests.post(TNurl2_siglar, data=TNbody2_siglar, headers=TNh2_siglar)




 def TNBrainCreateTimeInteraction(self,StudentID):
#我的互动
    TNurl3 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/BrainCreateTimeInteraction")
    #TNurl3 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/BrainCreateTimeInteraction"
    TNbody3 = {
        	"timeInteractionEntity":
                "{\"TimeInteractionID\":\"00000000-0000-0000-0000-000000000000\","
                "\"InteractionContent\":\"我的互动\","
                "\"ExperimentID\":\""+self.ExperimentID1+"\","
                "\"NowStage\":1,"
                "\"StudentID\":\""+StudentID+"\","
                "\"AddTime\":\"1900-1-1\"}"
            }
    TNh3 = {

        "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36"
     }
    TNr3 = self.s.post(TNurl3, json=TNbody3, headers=TNh3)
   # print("发表我的互动学生ID%s"%StudentID)
 def TNSubmitBrainEvaluation(self,GroupID,StudentID,toStudentID,e):
     GetByNowStageList_url = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/GetByNowStageList")
     #GetByNowStageList_url = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/GetByNowStageList"
     GetByNowStageList_body = {
         "expID":self.ExperimentID1,
         "groupID":GroupID,
         "studentID":StudentID,
         "nowStage":"3"
     }
     GetByNowStageList_h = {
         "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36"
     }
     GetByNowStageList_r=requests.get(GetByNowStageList_url, params=GetByNowStageList_body, headers=GetByNowStageList_h)
     result3 = GetByNowStageList_r.content.decode("utf-8")
     #print(result3)
     a = GetByNowStageList_r.json()
     b = json.loads(a)
     c= b["Table"]
     for i in c:
         idt = dict(i)
         if idt["StudentID"]==toStudentID:
            d = idt["BrainEvaluationID"]
            #print(d)
           # return h
 #def TNSubmitBrainEvaluation(self,BrainEvaluationID,AddStudentID):
     #组内互评
     TNurl4 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/SubmitBrainEvaluation")
     #TNurl4 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/SubmitBrainEvaluation"
     TNbody4 = {

	    "brainEvaluationList":
        "[{\"BrainEvaluationID\":\""+d+"\","
        "\"Grade\":"+e+","
        "\"StudentID\":\""+StudentID+"\","#一个学生
        "\"ExperimentID\":\""+self.ExperimentID1+"\","
        "\"NowStage\":\"3\","
        "\"AddStudentID\":\""+toStudentID+"\","#另一个学生
        "\"AddTime\":\"2017-01-01\"}]"



     }
     TNh4 = {
         "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36"

     }
     TNr4 = self.s.post(TNurl4, json=TNbody4, headers=TNh4)
     #print (TNr4.text)
    # print("被评星学生的ID%s"%StudentID,"评星数为%s"%e)
 def TNCreateTimeInteraction(self,StudentID):
     #观点分类，我的互动
     TNurl5 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/CreateTimeInteraction")
     #TNurl5 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateTimeInteraction"
     TNbody5 = {
         "timeInteractionEntity":
             "{\"TimeInteractionID\":\"00000000-0000-0000-0000-000000000000\","
             "\"InteractionContent\":\"观点分类，我的互动\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"NowStage\":4,"
             "\"StudentID\":\""+StudentID+"\","
             "\"AddTime\":\"1900-1-1\"}"
     }
     TNh5 = {
         "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36"

     }
     TNr5 = self.s.post(TNurl5, json=TNbody5, headers=TNh5)
    # print("观点分类发表我的互动学生的ID%s"%StudentID)
 def AddBrainDiagnosis(self,GroupID,StudentID,GroupName):
     AddBrainDiagnosis_url = urljoin(self.base_url,"kesgo.Service/wcf/DiagnoseService.svc/AddBrainDiagnosis")
     #AddBrainDiagnosis_url = "http://192.168.0.167/kesgo.Service/wcf/DiagnoseService.svc/AddBrainDiagnosis"
     AddBrainDiagnosis_json = {
         "braindiagno":
             "{\"GroupID\":\""+GroupID+"\","
             "\"GroupName\":\""+GroupName+"\","
             "\"AddUser\":\""+StudentID+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"Grade\":0,"
             "\"IsSubmit\":2,"
             "\"TempType\":1,"
             "\"IsDelete\":2}"

     }
     AddBrainDiagnosis_h = {
         "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36",
         "Content-Type": "application/json;charset=UTF-8"
     }
     AddBrainDiagnosis_r = self.s.post(AddBrainDiagnosis_url, json=AddBrainDiagnosis_json, headers=AddBrainDiagnosis_h)
    # print(AddBrainDiagnosis_r.status_code)
 def SaveBrainDiagnosis(self,GroupID,content,title):
     SaveBrainDiagnosis_url = urljoin(self.base_url,"kesgo.Service/wcf/DiagnoseService.svc/SaveBrainDiagnosis")
     #SaveBrainDiagnosis_url = "http://192.168.0.167/kesgo.Service/wcf/DiagnoseService.svc/SaveBrainDiagnosis"
     SaveBrainDiagnosis_json = {
         "braindiagno":
             "{\"GroupID\":\""+GroupID+"\","
             "\"ContentImg\":\"\","
             "\"SpeakContent\":\""+content+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"Title\":\""+title+"\"}"


     }
     SaveBrainDiagnosis_h={
         "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36"
     }
     SaveBrainDiagnosis_r=self.s.post(SaveBrainDiagnosis_url, json=SaveBrainDiagnosis_json, headers=SaveBrainDiagnosis_h)


 def TNSubmitBrainDiagnosis(self,GroupID,content,title,GroupName):
   #诊断总结
   TNSubmitBrainDiagnosis_url = urljoin(self.base_url,"kesgo.Service/wcf/DiagnoseService.svc/SubmitBrainDiagnosis")
   #TNSubmitBrainDiagnosis_url = "http://192.168.0.167/kesgo.Service/wcf/DiagnoseService.svc/SubmitBrainDiagnosis"
   TNSubmitBrainDiagnosis_body = {"braindiagno":
                                      "{\"GroupID\":\""+GroupID+"\","
                                      "\"ContentImg\":\"\","
                                      "\"SpeakContent\":\""+content+"\","
                                      "\"ExperimentID\":\""+self.ExperimentID1+"\","
                                      "\"Title\":\""+title+"\"}"
                                  }
   TNSubmitBrainDiagnosis_h = {
       "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36",
       "Content-Type": "application/json;charset=UTF-8"

   }
   TNSubmitBrainDiagnosis_r = self.s.post(TNSubmitBrainDiagnosis_url, json=TNSubmitBrainDiagnosis_body, headers=TNSubmitBrainDiagnosis_h)
 #  print(TNSubmitBrainDiagnosis_r.status_code)
  # print("诊断总结小组ID%s"%GroupID)
   TNSubmitBrainDiagnosis_url_siglar = "http://192.168.0.249:18199/signalr/signalr/send?transport=longPolling&connectionToken=AQAAANCMnd8BFdERjHoAwE%2FCl%2BsBAAAAVdYmo0qzSEea%2BwEs7MZ4ngAAAAACAAAAAAAQZgAAAAEAACAAAAD45Yaiq1Auw4qqqhddwjCluzrX2ZJ3X0FCPjfPKyMiUwAAAAAOgAAAAAIAACAAAADoAAD0JMluFk4q3xnmOJVYCSWVBBBWvWMWrMPLQSW6TTAAAADm85%2BkLDLvNM9xhF9vSdfhMKOzbHqKsMj%2Bj7jOX4sh3q6n0UiteqnLlxqDfHO%2F4pdAAAAA%2F1T9E0sKXOk%2BQJ%2BzpkHSlNPE%2Bi1ftrnbYDe1yqDAsX0Vm%2BzXr8sA5C8VT8zkFNAhvqapZX3iGv1F91R8ucPSNg%3D%3D&groupid="+self.ExperimentID1

   TNSubmitBrainDiagnosis_body_siglar = {"data":"{\"H\":\"kesgohub\",\"M\":\"sendGroupSpeakData\",\"A\":[5,\"{\\\"groupName\\\":\\\""+GroupName+"\\\",\\\"speakContent\\\":\\\""+content+"\\\",\\\"groupID\\\":\\\""+GroupID+"\\\",\\\"title\\\":\\\""+title+"\\\",\\\"contentImg\\\":\\\"\\\"}\"],\"I\":0}"}
   TNSubmitBrainDiagnosis_h_siglar = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36"}
   r = requests.post(TNSubmitBrainDiagnosis_url_siglar, data=TNSubmitBrainDiagnosis_body_siglar, headers=TNSubmitBrainDiagnosis_h_siglar)


 def Groupvote(self,StudentID,toGroupID):
#小组投票
    url11 = urljoin(self.base_url,"kesgo.Service/wcf/CoursePerformService.svc/InsertGroupEvaluation")
    #url11 = "http://192.168.0.167/kesgo.Service/wcf/CoursePerformService.svc/InsertGroupEvaluation"
    par11 = {"stuID":StudentID,
         "groupID":toGroupID }
    h11 = {
         "Accept": "application/json, text/plain, */*",
         "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
      }
    r11 = self.s.get(url11,params=par11,headers=h11)
   # print("被投票小组ID%s"%toGroupID)


 def Personalvote(self,StudentID,Group_memberID):
#个人投票
    url12 = urljoin(self.base_url,"kesgo.Service/wcf/CoursePerformService.svc/AddStudentVote")
    #url12 = "http://192.168.0.167/kesgo.Service/wcf/CoursePerformService.svc/AddStudentVote"
    par12 = {"expID":self.ExperimentID1,
         "stuID":StudentID,
         "excellenceID":Group_memberID }
    h12 = {
         "Accept": "application/json, text/plain, */*",
         "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
      }
    r12 = self.s.get(url12,params=par12,headers=h12)
   # print("被投票组员ID%s"%Group_memberID)
 def SaveGrowth(self,think_content):
     SaveGrowth_url = urljoin(self.base_url,"kesgo.Service/wcf/StudentInfoService.svc/SaveGrowth")
     #SaveGrowth_url = "http://192.168.0.167/kesgo.Service/wcf/StudentInfoService.svc/SaveGrowth"
     SaveGrowth_json = {
         "growthInfo":
             "{\"Content\":\""+think_content+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"StudentID\":\""+self.StudentID5+"\","
             "\"SelfPicList\":\"\"}"

     }
     SaveGrowth_h = {
         "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36",
         "Content-Type": "application/json;charset=UTF-8"
     }
     SaveGrowth_r =self.s.post(SaveGrowth_url,params=SaveGrowth_json,headers=SaveGrowth_h)
    # print(SaveGrowth_r.status_code)


 def Closeconn(self):
     self.A.mssql_close()

if __name__ == "__main__":
    mb = '12345678922'
    exname = 'test0601'





