# coding:utf-8
import unittest
import ddt
import os
from Storming import readexcel
from Storming import excel
from Storming.test1 import MssqlUtil
from config import readConfig
# 获取write.xlsx路径
curpath = os.path.dirname(os.path.realpath(__file__))
testxlsx = os.path.join(curpath, "write.xlsx")
testdata = readexcel.Excelread(testxlsx).dict_data()
experimentname  = readConfig.exname
@ddt.ddt
class Test_api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.A = MssqlUtil()
        # sql = "select StudentID from dbo.AFCS_GroupStudents where StudentID ='"+!!+"'"
        # sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = 'cccttt'"
        # cls.list= cls.A.mssql_getrows(sql)

    @ddt.data(*testdata)
    def test_totalscore(self, data):
        stuid = data["学生id"]
        sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+experimentname+"' and StudentID = '"+stuid+"'"
        stulist= self.A.mssql_getrows(sql)
        print("总分是%s"%data["总分"],"库里总分是%s"%float(str(stulist[0][14])))
        self.assertTrue(abs(data["总分"] - float(str(stulist[0][14])))<0.01)

    @ddt.data(*testdata)
    def test_classdiscuss(self, data):
        stuid = data["学生id"]
        sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+experimentname+"' and StudentID = '"+stuid+"'"
        stulist= self.A.mssql_getrows(sql)
        print("个人表现是%s"%data["个人表现=学生互评+系统评分+组内互评"],"库里个人表现是%s"%float(str(stulist[0][10])))
        self.assertTrue(abs(data["个人表现=学生互评+系统评分+组内互评"] - float(str(stulist[0][10])))<0.01)

    @ddt.data(*testdata)
    def test_groupperform(self, data):
        stuid = data["学生id"]
        sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+experimentname+"' and StudentID = '"+stuid+"'"
        stulist= self.A.mssql_getrows(sql)
        print("头脑风暴是%s"%data["头脑风暴=头脑风暴+诊断总结"],"库里头脑风暴是%s"%float(str(stulist[0][6])))
        self.assertTrue(abs(data["头脑风暴=头脑风暴+诊断总结"] - float(str(stulist[0][6])))<0.01)

    @ddt.data(*testdata)
    def test_personalperform(self, data):
        stuid = data["学生id"]
        sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+experimentname+"' and StudentID = '"+stuid+"'"
        stulist= self.A.mssql_getrows(sql)
        print("小组表现是%s"%data["小组表现=小组互评+教师评分"],"库里小组表现是%s"%float(str(stulist[0][13])))
        self.assertTrue(abs(data["小组表现=小组互评+教师评分"] - float(str(stulist[0][13])))<0.01)
if __name__ == "__main__":
    unittest.main()
