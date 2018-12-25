import requests
from flask import json
#登录管理员，添加教师，登录添加的教师添加课程，在该课程下添加章节，在章节下添加微课,在课程下，选择添加的章节、微课，添加案例
import string
import random
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
#from Brain_test.add_brain_student import *
from Storming.Generate_Random import *
class Process():
    def __init__(self,base_url):
       self.base_url = base_url
    def admin_login(self,loginName,loginPWD):
        admin_login_url = urljoin(self.base_url,"wcf/AdminService.svc/LoginIn")
        admin_login_par = {
            "v":"1545027927521",
            "loginName":loginName,
            "loginPWD":loginPWD,
            "loginIP":"%E6%B1%9F%E8%8B%8F%E7%9C%8149.65.2.50"
        }
        admin_login_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

        }
        admin_login_r = requests.get(admin_login_url, params=admin_login_par, headers=admin_login_header)
        result1 = admin_login_r.content.decode("utf-8")
        #print (admin_login_r.status_code)
        res = admin_login_r.json()
        return res
    def getadminid(self,res):
        dict1 = json.loads(res)
        useid = dict1["UserID"]
        return useid
    def add_teacher(self,realName,mobileNo,password,adminID):
        add_teacher_url = urljoin(self.base_url,"wcf/TeacherInfoService.svc/SaveTeacherInfo?v=1533173712271")

        add_teacher_json = {
	        "teacherEntity": "{\"teacherID\":\"00000000-0000-0000-0000-000000000000\",\"realName\":\""+realName+"\",\"sex\":1,\"schoolID\":\"F54EFF8D-73D3-489F-B27A-DBFF8E005B29\",\"mobileNo\":\""+mobileNo+"\",\"password\":\""+password+"\",\"email\":\"\",\"wechat\":\"\",\"qq\":\"\",\"addUser\":\""+adminID+"\"}"
        }
        add_teacher_h={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        add_teacher_r = requests.post(add_teacher_url, json=add_teacher_json, headers=add_teacher_h)
        a = add_teacher_r.text
        return a
    def get_all_add_teacher(self,adminID):
        get_add_teacher_url = urljoin(self.base_url,"wcf/TeacherInfoService.svc/GetTeacherList_Paged")

        get_add_teacher_par= {
            "v":"1538014932992",
            "pageIndex":"1",
            "pageSize":"10",
            "teacherName":"",
            "authStatus":"0",
            "courseID":"00000000-0000-0000-0000-000000000000",
            "qryType":"1",
            "UserID":adminID
        }
        get_add_teacher_h ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

        }
        get_add_teacher_r = requests.get(get_add_teacher_url, params=get_add_teacher_par, headers=get_add_teacher_h)
        result3 = get_add_teacher_r.content.decode("utf-8")
        return get_add_teacher_r.json()
    def get_add_teacherId(self,allteacherId,RealName):
        str1=allteacherId
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            print(type(dict1))
            print(dict1)
            if dict1["RealName"]==RealName:
                return (dict1["TeacherID"])

    def teacher_login(self, loginName, loginPWD):
        teacher_login_url = urljoin(self.base_url,"wcf/TeacherInfoService.svc/LoginIn")
        teacher_login_par = {
            "v": "1533181480621",
            "loginName": loginName,
            "loginPWD": loginPWD
        }
        teacher_login_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        teacher_login_r = requests.get(teacher_login_url, params=teacher_login_par, headers=teacher_login_h)
        result1 = teacher_login_r.content.decode("utf-8")
        res = teacher_login_r.json()
        return res
    def get_tecid(self,res):
        dict1 = json.loads(res)
        useid = dict1["UserID"]
        return useid
    def add_update(self,img_name):
        add_update_url = "http://192.168.0.202:21120/UploadService/UploadFile"
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '713304',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryaWl8GNHeukBwsiD4',
            'Referer': 'http://192.168.0.167/kesgo/admin/views/microlessonadd.html?id=83159a70-89ae-45c2-876a-3ed43dd24dc4&role=1&courseId=8174710c-c76a-4fe5-80c2-9567ae9c03d6',
            'X_FILE_IMAGEACTION':'',
            'X_FILE_IMAGEACTIONPARAMETER':'',
            'X_FILE_NAME': img_name,
            'X_FILE_PATH': 'AllPassKesgo',
            'X_FILE_UPLOAD_WITHBLOCK': '0',
            'Origin': 'http://192.168.0.167',
            'Connection': 'keep-alive',
            'Host': '192.168.0.202:21120'
    }
        f ={
             "fieldNameHere": ("3.png",open(r"c:\3.png", "rb"), "image/png")
            }
        add_update_r = requests.post(add_update_url,headers=headers, files=f)
        return add_update_r.json()
    def get_update(self,res):
        dict1 = json.loads(res)
        img_name = dict1["NewFileName"]
        return img_name


    def add_kecheng(self,CourseModeuleName,AddUser,img_name):
        add_kecheng_url = urljoin(self.base_url,"wcf/CourseService.svc/SaveCourse?v=1533181877812")
        add_kecheng_json= {
	        "courseInfo": "{\"CourseModuleID\":\"00000000-0000-0000-0000-000000000000\",\"CourseModeuleName\":\""+CourseModeuleName+"\",\"ExperimentType\":2,\"AddUser\":\""+AddUser+"\",\"AddUserRole\":1,\"CourseNumber\":0,\"CourseImage\":\""+img_name+"\"}"
        }
        add_kecheng_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        add_kecheng_r = requests.post(add_kecheng_url, json=add_kecheng_json, headers=add_kecheng_h)
        a = add_kecheng_r.text
        return a
    def get_all_kecheng(self,userId):
        get_all_kecheng_url = urljoin(self.base_url,"wcf/CourseService.svc/GetAllCourseModuleByUserID")
        get_all_kecheng_par = {
            "v":"1533181878879",
            "userId":userId,
            "userRole":"1",
            "pageIndex":"1",
            "pageSize":"8"
        }
        get_all_kecheng_h={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        get_all_kecheng_r = requests.get(get_all_kecheng_url, params=get_all_kecheng_par, headers=get_all_kecheng_h)
        result3 = get_all_kecheng_r.content.decode("utf-8")
        return get_all_kecheng_r.json()

    def get_add_kechengID(self,allkecheng,CourseModeuleName):
        str1=allkecheng
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            print(type(dict1))
            print(dict1)
            if dict1["CourseModeuleName"]==CourseModeuleName:
                return (dict1["CourseModuleID"])

    def add_zhangjie(self,AddUser,ChapterName,CourseModuleID):
        add_zhangjie_url = urljoin(self.base_url,"wcf/ChapterService.svc/CreateOrUpdateChapter?v=1533182266728")
        add_zhangjie_json = {
            "chapterInfo": "{\"ChapterID\":\"00000000-0000-0000-0000-000000000000\",\"CourseModuleID\":\""+CourseModuleID+"\",\"ChapterName\":\""+ChapterName+"\",\"AddUser\":\""+AddUser+"\",\"AddUserRole\":1,\"ChapterOrder\":1}"
        }
        add_zhangjie_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        add_zhangjie_r = requests.post(add_zhangjie_url, json=add_zhangjie_json, headers=add_zhangjie_h)
        #result4 = add_zhangjie_r.content.decode("utf-8")
        return add_zhangjie_r.json()
    def get_all_zhangjie(self,courseId,userId):
        get_all_zhangjie_url = urljoin(self.base_url,"wcf/ChapterService.svc/GetAllChapterByUserID")
        get_all_zhangjie_par = {
            "v":"1544057772732",
            "courseId":courseId,
            "userId":userId,
            "userRole":"1"

        }
        get_all_zhangjie_h={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        get_all_zhangjie_r = requests.get(get_all_zhangjie_url, params=get_all_zhangjie_par, headers=get_all_zhangjie_h)
        result3 = get_all_zhangjie_r.content.decode("utf-8")
        return get_all_zhangjie_r.json()

    def get_add_zhangjieID(self,allzhangjie,ChapterName):
        str1=allzhangjie
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            print(type(dict1))
            print(dict1)
            if dict1["ChapterName"]==ChapterName:
                return (dict1["ChapterID"])

    def add_Micro_lesson_file(self,file_name):
        add_Micro_lesson_file_url = "http://192.168.0.202:21120/UploadService/UploadFile"
        add_Micro_lesson_file_header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '713304',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryaWl8GNHeukBwsiD4',
            'Referer': 'http://192.168.0.167/kesgo/admin/views/microlessonadd.html?id=83159a70-89ae-45c2-876a-3ed43dd24dc4&role=1&courseId=8174710c-c76a-4fe5-80c2-9567ae9c03d6',
            'X_FILE_IMAGEACTION':'',
            'X_FILE_IMAGEACTIONPARAMETER':'',
            'X_FILE_NAME': file_name,
            'X_FILE_PATH': 'AllPassKesgo',
            'X_FILE_UPLOAD_WITHBLOCK': '0',
            'Origin': 'http://192.168.0.167',
            'Connection': 'keep-alive',
            'Host': '192.168.0.202:21120'

        }
        add_Micro_lesson_file_f ={
             "fieldNameHere": ("005.docx",open(r"c:\005.docx", "rb"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            }
        add_update_r = requests.post(add_Micro_lesson_file_url,headers=add_Micro_lesson_file_header, files=add_Micro_lesson_file_f)
        return add_update_r.json()
    # def get_update_MicroImagePath(self,all,FileName):
    #     str1=all
    #     list1 = json.loads(str1)
    #     for i in list1:
    #         dict1 = dict(i)
    #         print(type(dict1))
    #         print(dict1)
    #         if dict1["FileName"]==FileName:
    #             return (dict1["PdfFirstImagePath"])
    def get_update_MicroImagePath(self,res):
         dict1 = json.loads(res)
         MicroImagePath = dict1["PdfFirstImagePath"]
         return MicroImagePath
    def get_update_file_ResourcePath(self,res):
        dict1 = json.loads(res)
        ResourcePath = dict1["PdfPath"]
        return ResourcePath
    def get_update_file(self,res):
        dict1 = json.loads(res)
        file_name = dict1["NewFileName"]
        return file_name
    def add_Micro_lesson(self,ChapterID,AddUser,FromUser,CourseModuleID,MicroImagePath,MicroName,ResourceName,ResourcePath,ResourceFilePath):
        add_Micro_lesson_url = urljoin(self.base_url,"wcf/MicroLessionService.svc/CreateOrUpdateMicrolesson?v=1544406928596")
        add_Micro_lesson_json= {

	            "microlessonInfo": "{\"ChapterID\":\""+ChapterID+"\",\"AddUser\":\""+AddUser+"\",\"AddUserRole\":1,\"FromUser\":\""+FromUser+"\",\"FromUserRole\":1,\"CourseModuleID\":\""+CourseModuleID+"\",\"FileType\":\"docx\",\"MicroImagePath\":\"kesgo\\\\201812\\\\"+MicroImagePath+"\",\"MicroName\":\""+MicroName+"\",\"ResourceName\":\""+ResourceName+"\",\"ResourcePath\":\"kesgo\\\\201812\\\\"+ResourcePath+"\",\"ResourceFilePath\":\"kesgo\\\\"+ResourceFilePath+"\"}"

        }
        add_Micro_lesson_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        add_kecheng_r = requests.post(add_Micro_lesson_url, json=add_Micro_lesson_json, headers=add_Micro_lesson_h)
        print(type(add_kecheng_r))
        a = add_kecheng_r.json()
        return a
    def get_all_add_Micro_lessonID(self,courseId,UserID):
        get_all_add_Micro_lessonID_url =  urljoin(self.base_url,"wcf/MicroLessionService.svc/PageMicroInfos")
        get_all_add_Micro_lessonID_json ={
           "v":"1544424016317",
            "microName":"",
            "chapterId":"00000000-0000-0000-0000-000000000000",
            "courseId":courseId,
            "userRole":"1",
            "UserID":UserID,
            "pageIndex":"1",
            "pageSize":"20",
            "seachType":"1"

        }
        get_all_add_Micro_lessonID_h ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        get_all_add_Micro_lessonID_r = requests.get(get_all_add_Micro_lessonID_url, params=get_all_add_Micro_lessonID_json, headers=get_all_add_Micro_lessonID_h)

        return get_all_add_Micro_lessonID_r.json()
    def get_add_Micro_lessonID(self,allMicro_lesson,MicroName):
        str1=allMicro_lesson
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            print(type(dict1))
            print(dict1)
            if dict1["MicroName"]==MicroName:
                return (dict1["MicroLessonID"])
    def add_case(self,QuestionsContent1,QuestionsContent2,QuestionOptionContent_A,QuestionOptionContent_B,QuestionOptionContent_C,QuestionOptionContent_D,AddUser,CaseContent,CaseImage,CaseImageName,CaseIntroduction,CaseName,ChapterID,CourseModuleID,MicroLessonID,FromUser):
        add_case_url =  urljoin(self.base_url,"wcf/CaseService.svc/CreateOrUpdateCaseInfo?v=1544423123233")
        add_case_json = {

	        "caseInfo": "{\"PolicyCaseQues\":\"[{\\\"QuestionsContent\\\":\\\""+QuestionsContent1+"\\\",\\\"QuestionOrderNo\\\":1,\\\"QuestionType\\\":1},{\\\"QuestionsContent\\\":\\\""+QuestionsContent2+"\\\",\\\"QuestionOrderNo\\\":2,\\\"QuestionType\\\":2,\\\"CaseQuesOption\\\":[{\\\"QuestionOptionContent\\\":\\\""+QuestionOptionContent_A+"\\\",\\\"OptionOrderNo\\\":1,\\\"OptionLetter\\\":\\\"A\\\"},{\\\"QuestionOptionContent\\\":\\\""+QuestionOptionContent_B+"\\\",\\\"OptionOrderNo\\\":2,\\\"OptionLetter\\\":\\\"B\\\"},{\\\"QuestionOptionContent\\\":\\\""+QuestionOptionContent_C+"\\\",\\\"OptionOrderNo\\\":3,\\\"OptionLetter\\\":\\\"C\\\"},{\\\"QuestionOptionContent\\\":\\\""+QuestionOptionContent_D+"\\\",\\\"OptionOrderNo\\\":4,\\\"OptionLetter\\\":\\\"D\\\"}]}]\",\"PolicyCaseRead\":\"[]\",\"AddUser\":\""+AddUser+"\",\"AddUserRole\":1,\"CaseContent\":\""+CaseContent+"\",\"CaseImage\":\""+CaseImage+"\",\"CaseImageName\":\""+CaseImageName+"\",\"CaseIntroduction\":\""+CaseIntroduction+"\",\"CaseName\":\""+CaseName+"\",\"CaseVideo\":\"\",\"CaseVideoName\":\"\",\"ChapterID\":\""+ChapterID+"\",\"CourseModuleID\":\""+CourseModuleID+"\",\"IsEnd\":2,\"MicroLessonID\":\""+MicroLessonID+"\",\"FromUser\":\""+FromUser+"\",\"FromUserRole\":1,\"AuditState\":2}"

        }
        add_case_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        add_case_r = requests.post(add_case_url, json=add_case_json, headers=add_case_h)
        return add_case_r.json()
    def add_Diagnostic_tools(self,ToolName,ToolImage,AddUser,FromUser,ModuleName1,ModuleName2,ModuleName3):
        add_Diagnostic_tools_url = urljoin(self.base_url,"wcf/AdminService.svc/EditToolInfo?v=1544426158978")
        add_Diagnostic_tools_json = {

	        "allEntity": "{\"ToolID\":\"00000000-0000-0000-0000-000000000000\",\"ToolName\":\""+ToolName+"\",\"ToolSynopsis\":\"\",\"ToolImage\":\""+ToolImage+"\",\"IsEdit\":1,\"AddUser\":\""+AddUser+"\",\"AddUserRole\":1,\"FromUser\":\""+FromUser+"\",\"FromUserRole\":1,\"IsDelete\":2,\"moduleListString\":\"[{\\\"ModuleID\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ModuleName\\\":\\\""+ModuleName1+"\\\",\\\"ToolID\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ModuleOrderNo\\\":1,\\\"AddUser\\\":\\\""+AddUser+"\\\"},{\\\"ModuleID\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ModuleName\\\":\\\""+ModuleName2+"\\\",\\\"ToolID\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ModuleOrderNo\\\":2,\\\"AddUser\\\":\\\""+AddUser+"\\\"},{\\\"ModuleID\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ModuleName\\\":\\\""+ModuleName3+"\\\",\\\"ToolID\\\":\\\"00000000-0000-0000-0000-000000000000\\\",\\\"ModuleOrderNo\\\":3,\\\"AddUser\\\":\\\""+AddUser+"\\\"}]\"}"

        }
        add_Diagnostic_tools_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        add_Diagnostic_tools_r = requests.post(add_Diagnostic_tools_url, json=add_Diagnostic_tools_json, headers=add_Diagnostic_tools_h)
        return add_Diagnostic_tools_r.json()
    def get_add_Diagnostic_tools(self,UserID):
        get_add_Diagnostic_tools_url = urljoin(self.base_url,"wcf/AdminService.svc/PageToolInfo")
        get_add_Diagnostic_tools_json = {
            "v":"1544426160030",
            "pageIndex":"1",
            "pageSize":"25",
            "toolName":"",
            "userRole":"1",
            "UserID":UserID
        }
        get_add_Diagnostic_tools_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        get_add_Diagnostic_tools_r = requests.get(get_add_Diagnostic_tools_url, params=get_add_Diagnostic_tools_json, headers=get_add_Diagnostic_tools_h)

        return get_add_Diagnostic_tools_r.json()
    def get_add_Diagnostic_toolsID(self,allDiagnostic_tools,ToolName):
        str1=allDiagnostic_tools
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            print(type(dict1))
            print(dict1)
            if dict1["ToolName"]==ToolName:
                return (dict1["ToolID"])
    def add_case_file(self,file_name):
        add_case_file_url = "http://192.168.0.202:21120/UploadService/UploadFile"
        add_case_file_h ={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '713304',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryaWl8GNHeukBwsiD4',
            'Referer': 'http://192.168.0.167/kesgo/admin/views/microlessonadd.html?id=83159a70-89ae-45c2-876a-3ed43dd24dc4&role=1&courseId=8174710c-c76a-4fe5-80c2-9567ae9c03d6',
            'X_FILE_IMAGEACTION':'',
            'X_FILE_IMAGEACTIONPARAMETER':'',
            'X_FILE_NAME': file_name,
            'X_FILE_PATH': 'AllPassKesgo',
            'X_FILE_UPLOAD_WITHBLOCK': '0',
            'Origin': 'http://192.168.0.167',
            'Connection': 'keep-alive',
            'Host': '192.168.0.202:21120'

        }
        add_case_file_f ={
            "fieldNameHere": ("006.ppt",open(r"c:\006.ppt", "rb"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        }
        add_case_file_r = requests.post(add_case_file_url,headers=add_case_file_h, files=add_case_file_f)
        return add_case_file_r.json()
    def edit_case(self,CourseModuleID,CaseID,CaseAnswer,CaseQuestion,QuestionContent):
        edit_case_url = urljoin(self.base_url,"wcf/CaseService.svc/CreateOrUpdateCaseInfoTwo?v=1544429498142")

        edit_case_json={
                    "caseInfo": "{\"CourseModuleID\":\""+CourseModuleID+"\",\"CaseID\":\""+CaseID+"\",\"CaseAnswer\":\""+CaseAnswer+"\",\"CaseQuestion\":\""+CaseQuestion+"\",\"IsEnd\":1,\"QuestionContent\":\""+QuestionContent+"\",\"AuditState\":2}"

        }
        edit_case_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        edit_case_r = requests.post(edit_case_url, json=edit_case_json, headers=edit_case_h)
        return edit_case_r.json()
    def add_em(self,experimentName,courseModuleID,microLessonID,caseID,classIDs,addUser):
        add_em_url = urljoin(self.base_url,"wcf/ExperimentService.svc/SaveExperiment?v=1544434810397")

        add_em_json ={
                  "expEntity":"{\"experimentID\":\"00000000-0000-0000-0000-000000000000\",\"experimentName\":\""+experimentName+"\",\"courseModuleID\":\""+courseModuleID+"\",\"microLessonID\":\""+microLessonID+"\",\"caseID\":\""+caseID+"\",\"microLessonPercent\":5,\"questionsPercent\":15,\"questionsFiveStar\":10,\"questionsSysPercent\":5,\"discussionPercent\":15,\"discussionFiveStar\":5,\"discussionSysPercent\":15,\"interGroupPercent\":0,\"interGroupFiveStar\":0,\"interGroupSysPercent\":0,\"diagnosePercent\":30,\"diagnoseFiveStar\":30,\"diagnoseSysPercent\":0,\"groupPercent\":20,\"groupEvalPercent\":10,\"groupSysPercent\":10,\"personagePercent\":15,\"stuentEvalPercent\":5,\"personageSysPercent\":5,\"microCoursePercent\":20,\"courseDiscussionPercent\":45,\"coursePerformPercent\":35,\"classIDs\":\""+classIDs+"\",\"addUser\":\""+addUser+"\"}"
        }
        add_em_h={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
        add_em_r = requests.post(add_em_url, json=add_em_json, headers=add_em_h)
        return add_em_r.json()



    def tec_login(self,loginName,loginPWD):
        tec_login_url = urljoin(self.base_url,"wcf/TeacherInfoService.svc/LoginIn")
        tec_login_par = {
            "v":"1534812768392",
            "loginName":loginName,
            "loginPWD":loginPWD
        }
        tec_login_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        tec_login_r = requests.get(tec_login_url, params=tec_login_par, headers=tec_login_h)
        res = tec_login_r.json()
        return res

    def gettecid(self,res):
        dict1 = json.loads(res)
        useid = dict1["UserID"]
        return useid
    def add_class(self,TeacherID,ClassName):
        add_class_url = urljoin(self.base_url,"wcf/TeacherInfoService.svc/CreateOrUpdateClass?v=1534813216483")
        #add_class_url= "http://123.206.230.41:8080/kesgo.Service/wcf/TeacherInfoService.svc/CreateOrUpdateClass?v=1534813216483"
        add_class_json ={
            "classInfo": "{\"ClassID\":\"00000000-0000-0000-0000-000000000000\","
                         "\"TeacherID\":\""+TeacherID+"\","
                         "\"ClassName\":\""+ClassName+"\"}"

        }
        add_class_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        add_class_r = requests.post(add_class_url, json=add_class_json, headers=add_class_h)
        a = add_class_r.text
        return a

    def get_all_classid(self,teachId):
        get_all_classid_url = urljoin(self.base_url,"wcf/TeacherInfoService.svc/GetClassInfoByID")

        #get_all_classid_url = "http://123.206.230.41:8080/kesgo.Service/wcf/TeacherInfoService.svc/GetClassInfoByID"
        get_all_classid_par={
            "v":"1534813217520",
            "teachId":teachId
        }
        get_all_classid_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        get_all_classid_r = requests.get(get_all_classid_url, params=get_all_classid_par, headers=get_all_classid_h)
        result3 = get_all_classid_r.content.decode("utf-8")
        return get_all_classid_r.json()
    def get_add_class_classId(self,allclassId,ClassName):
        str1=allclassId
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            print(type(dict1))
            print(dict1)
            if dict1["ClassName"]==ClassName:
                return (dict1["ClassID"])
    def add_stu(self,adduser,realname,password,phone,classId):
        add_stu_url = urljoin(self.base_url,"wcf/StudentInfoService.svc/AddorUpdateStudentInfo?v=1534814126452")
        #add_stu_url = "http://123.206.230.41:8080/kesgo.Service/wcf/StudentInfoService.svc/AddorUpdateStudentInfo?v=1534814126452"
        add_stu_json ={
            "stuInfo": "{\"adduser\":\""+adduser+"\",\"adduserrole\":1,\"realname\":\""+realname+"\",\"password\":\""+password+"\",\"phone\":\""+phone+"\",\"classId\":\""+classId+"\"}",
	        "classId": classId

        }
        add_stu_h={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        add_stu_r=requests.post(add_stu_url, json=add_stu_json, headers=add_stu_h)
        b = add_stu_r.text
        return b
    def get_all_stu(self,classID):
        get_all_stu_url = urljoin(self.base_url,"wcf/TeacherInfoService.svc/PageStuInfos")
        #get_all_stu_url = "http://123.206.230.41:8080/kesgo.Service/wcf/TeacherInfoService.svc/PageStuInfos"
        get_all_stu_par = {
            "v":"1534814127566",
            "searchText":"",
            "classID":classID,
            "pageIndex":"1",
            "pageSize":"10"
        }
        get_all_stu_h ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        get_all_stu_r=requests.get(get_all_stu_url, params=get_all_stu_par, headers=get_all_stu_h)
        return get_all_stu_r.json()
    def get_add_StudentID(self,allsutdentid,realname):
        str1=allsutdentid
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            print(type(dict1))
            print(dict1)
            if dict1["RealName"] == realname:
                return (dict1["StudentID"])
    def edit_add_stu(self,adduser,realname,password,phone,studentnumber,qq,birthday,classId,studentID):
        edit_add_stu_url = urljoin(self.base_url,"wcf/StudentInfoService.svc/AddorUpdateStudentInfo?v=1534815539827")
        #edit_add_stu_url="http://123.206.230.41:8080/kesgo.Service/wcf/StudentInfoService.svc/AddorUpdateStudentInfo?v=1534815539827"
        edit_add_stu_json={
            	"stuInfo": "{\"adduser\":\""+adduser+"\",\"adduserrole\":1,\"realname\":\""+realname+"\",\"password\":\""+password+"\",\"phone\":\""+phone+"\",\"studentnumber\":\""+studentnumber+"\",\"qq\":\""+qq+"\",\"birthday\":\""+birthday+"\",\"classId\":\""+classId+"\",\"studentID\":\""+studentID+"\"}",
            	"classId": classId
        }
        edit_add_stu_h={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        edit_add_stu_r=requests.post(edit_add_stu_url, json=edit_add_stu_json, headers=edit_add_stu_h)
    def phone_num(self):
        num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187', '188',
             '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits,7))
        res = start+end
        return res
    def name(self):
        name = ['一','二','三','四','五','六','七','八','九','十']
        start = random.choice(name)
        return start
    def stu_num(self):
        num_start = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
             '15', '16', '17', '18', '19', '20']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits,1))
        res = start+end
        return res
    def QQ_num(self):
        num_start = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
             '15', '16', '17', '18', '19', '20']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits,3))
        res = start+end
        return res
    def birthday(self):
        for i in range(1,5):
            num_month = ['0']
            month = random.choice(num_month)+str(i)
            num_day = ['0']
            day = random.choice(num_day)+str(i)
            res = month+"-"+day
        return res
    def get_allallexperimentID(self,teacherid):
        url3 =urljoin(self.base_url,"wcf/ExperimentService.svc/GetExperimentList_Paged")
        body3 = {
            "v":"1532679665405",
            "pageIndex":"1",
            "pageSize":"20",
            "expName":"",
            "expCourseID":"00000000-0000-0000-0000-000000000000",
            "expState":"0",
            "UserID":teacherid

        }
        header3 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        r3 = requests.get(url3, params=body3, headers=header3)
        result3 = r3.content.decode("utf-8")
        return r3.json()
    def getexperimentID(self,allexperiment,experimentName):
        str1=allexperiment
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            print(type(dict1))
            print(dict1)
            if dict1["ExperimentName"]==experimentName:
                return (dict1["ExperimentID"])
    def starexperiment(self,experimentID):
        url4 = urljoin(self.base_url,"wcf/ExperimentService.svc/SetExperimentStatus")
        body4 = {
            "v":"1532936043573",
            "expID":experimentID,
            "expStatus":"1"

        }
        h4 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

        }
        r1 = requests.get(url4, params=body4, headers=h4)
        return r1



    def all_Technological_process(self,tcname,teachernum,experimentName):
        res = self.admin_login("apadmin","654321")
        #print(res)#登录
        adminId = self.getadminid(res)         #获取登录的管理员id
        #print (adminId)
        text = self.add_teacher(tcname,teachernum,"1",adminId) #添加教师
        #print(text)
        asd = self.get_all_add_teacher(adminId)      #获取所有教师id
        json.dumps(asd)
        #print(asd)
        str_pc = asd
        list1 = json.loads(str_pc)
        #print(type(list))
        b = self.get_add_teacherId(asd,tcname)
        #print(b)
        res1 = self.teacher_login(teachernum,"1")
        #print(res1)
        teacherid = self.get_tecid(res1)
        #print (teacherid)
        res_img = self.add_update("1.png")
        #print(res_img)#登录
        img_id = self.get_update(res_img)
        text1 = self.add_kecheng("头脑风暴一",teacherid,img_id)
        #print(text1)
        asd1 = self.get_all_kecheng(teacherid)
        json.dumps(asd1)
        #print(asd1)
        str1 = asd1
        list1 = json.loads(str1)
        #print(type(list1))
        b1 = self.get_add_kechengID(asd1,"头脑风暴一")
        #print(b1)#课程id
        #return b1
        c1 = self.add_zhangjie(teacherid,"章节一",b1)
        #print(c1)
        asd2 = self.get_all_zhangjie(b1,teacherid)
        json.dumps(asd2)
        #print(asd2)
        str2 = asd2
        list2 = json.loads(str2)
        #print(type(list2))
        b2 = self.get_add_zhangjieID(asd2,"章节一")
        #print(b2)#章节id
        Micro_lesson_file = self.add_Micro_lesson_file("005.docx")

        #print(Micro_lesson_file)
        update_file=self.get_update_file(Micro_lesson_file)
        #print(update_file)
        MicroImagePath=update_file.replace("docx","png")
        #print(MicroImagePath)
        ResourcePath=update_file.replace("docx","pdf")
        #print(ResourcePath)

        #print(ResourcePath)
        add_weike = self.add_Micro_lesson(b2,teacherid,teacherid,b1,MicroImagePath,"微课一","005.docx",ResourcePath,update_file) #添加教师
        #print(type(add_weike))
        asd3 = self.get_all_add_Micro_lessonID(b1,teacherid)
        json.dumps(asd3)
        #print(asd1)
        str3 = asd3
        list1 = json.loads(str3)
        #print(type(list1))
        b3 = self.get_add_Micro_lessonID(asd3,"微课一")
        #print(b3)#微课id
        #return b3
        add_case = self.add_case("思考题一","思考题二","选项A","选项B","选项C","选项D",teacherid,"案例正文",img_id,"1.png","案例简介","案例一",b2,b1,b3,teacherid)
        #print (add_case)#案例的id
        Tool = self.add_Diagnostic_tools("诊断工具一",img_id,teacherid,teacherid,"模块一","模块二","模块三")
        add_case_file = self.add_case_file("006.ppt")
        ppt_id = self.get_update(add_case_file)#ppt文件id
        edit_case = self.edit_case(b1,add_case,"诊断指导","诊断总结问题","头脑风暴问题")
        #print (teacherid)
        a_tc = self.add_class(teacherid,"班级一")
        #print(a)
        b_tc = self.get_all_classid(teacherid)
        json.dumps(b_tc)
        #print(b)
        str_tc = b_tc
        list1 = json.loads(str_tc)
        #print(type(list1))
        b_tc = self.get_add_class_classId(b_tc,"班级一")
       # return b
        #班级id
        for ii in  range(0,2):
            for i in range(1,6):
                phone = self.phone_num()+str(i)
                name = Unicode(3)
                #print("手机号码是%s"%phone)
                c = self.add_stu(teacherid,name,"1",phone,b_tc)
                #print(c)
                d_tc = self.get_all_stu(b_tc)
                json.dumps(d_tc)
                #print(d)
                str2_tc = d_tc
                list2_tc = json.loads(str2_tc)
                #print(type(list2))
                e = self.get_add_StudentID(d_tc,name)
                #print(e)
                stunumber = self.stu_num()
                #print("学号是%s"%stunumber)
                QQnumber = self.QQ_num()+str(i)
                birthdaty = "2018"+"-"+'0'+str(i)+"-"+'0'+str(i)
                f = self.edit_add_stu(teacherid,name,"1",phone,stunumber,QQnumber,birthdaty,b_tc,e)
        #return b_tc
        self.add_em(experimentName,b1,b3,add_case,b_tc,teacherid)
        em_id = self.get_allallexperimentID(teacherid)
        json.dumps(em_id)
    #print(em_id)
        str1_em_id = em_id
        list1_em_id = json.loads(str1_em_id)
        #print(type(list1_em_id))
        b_em_id= self.getexperimentID(em_id,experimentName)       #获取添加的实验的id
    #print(b)
        c = self.starexperiment(b_em_id)  #开始添加的实验
class update():
    def up(self):
            res_img = Process.add_update("1.png")
        #print(res_img)#登录
            img_id = Process.get_update(res_img)
            print(img_id)

if __name__ == "__main__":
    base_url = "http://192.168.0.167/AllPassKesgo.Service/"
    abc = Process(base_url)
    # aaaaa = abc.all_Technological_process("siwuliu","13456456456","shiyanyi")
    # print (aaaaa)
    qwe = update.up
    print (qwe)
















