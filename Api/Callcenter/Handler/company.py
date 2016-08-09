#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import RESTfulHandler,BaseHandler
from tornado import web
from Right.Entity.CompanyModel import CompanyList
from Right.Entity.UserModel import UserList
from Right.Entity.DepartmentFunctionModel import DepartmentFunctionList
from Right.Entity.DepartmentModel import DepartmentList
import json,datetime
from sqlalchemy import desc,or_,and_


#公司管理
@urlmap(r'/company\/?([0-9]*)')
class CompanyHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        username = self.get_current_user()
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))

        totalquery = self.db.query(CompanyList.CompanyId)
        CompanyListObj = self.db.query(CompanyList)
        if searchKey:
            totalquery = totalquery.filter(or_(CompanyList.CompanyName.like('%%%s%%' % searchKey)))
            CompanyListObj = CompanyListObj.filter(or_(CompanyList.CompanyName.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = CompanyListObj.order_by(desc(CompanyList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.Result['username'] = username
        self.Result['success'] = True
        self.finish(self.Result)

    @web.asynchronous
    def post(self,ident=0):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            data = json.loads(self.request.body)
            objTask = CompanyList()
            objTask.ParentCompany = data['params'].get('ParentCompany', None)
            objTask.CompanyName = data['params'].get('CompanyName', None)
            objTask.Area = data['params'].get('Area', None)
            objTask.Address = data['params'].get('Address', None)
            objTask.Profession = data['params'].get('Profession', None)
            objTask.CompanyNature = data['params'].get('CompanyNature', None)
            objTask.Scale = data['params'].get('Scale', None)
            objTask.TelePhone = data['params'].get('TelePhone', None)
            objTask.Fax = data['params'].get('Fax', None)
            objTask.HomePage = data['params'].get('HomePage', None)
            objTask.Is_valid = data['params'].get('Is_valid', '是')
            objTask.Comment = data['params'].get('Comment', None)
            objTask.Create = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
            objTask.CreateTime = datetime.datetime.now()
            objDepart = DepartmentFunctionList()
            objDepart.DepartmentName = objTask.CompanyName
            objDepart.Level = 1
            objDepart.Parent = 0
            self.db.add(objTask)
            self.db.add(objDepart)
            self.db.commit()
            self.Result['info'] = u'创建公司成功'
            self.finish(self.Result)

    @web.asynchronous
    def put(self, ident):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            data = json.loads(self.request.body)
            objTask = self.db.query(CompanyList).get(ident)
            if ident and objTask:
                objTask.ParentCompany = data['params'].get('ParentCompany', None)
                objTask.CompanyName = data['params'].get('CompanyName', None)
                objTask.Area = data['params'].get('Area', None)
                objTask.Address = data['params'].get('Address', None)
                objTask.Profession = data['params'].get('Profession', None)
                objTask.CompanyNature = data['params'].get('CompanyNature', None)
                objTask.Scale = data['params'].get('Scale', None)
                objTask.TelePhone = data['params'].get('TelePhone', None)
                objTask.Fax = data['params'].get('Fax', None)
                objTask.HomePage = data['params'].get('HomePage', None)
                objTask.Is_valid = data['params'].get('Is_valid', '是')
                objTask.Comment = data['params'].get('Comment', None)
                objTask.Update = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
                objTask.UpdateTime = datetime.datetime.now()
                self.db.add(objTask)
                self.db.commit()
                self.Result['rows'] = 1
                self.Result['info'] = u'修改公司成功'
            else:
                self.Result['rows'] = 0
                self.Result['info'] = u'修改公司失败'
            self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            com = self.db.query(CompanyList).filter(CompanyList.CompanyId==ident).first()
            companyname = com.CompanyName
            depart = self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.DepartmentName==companyname).first()
            departid = depart.DepartmentFunctionId
            self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.Parent==departid).delete()
            self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.DepartmentName==companyname).delete()
            self.db.query(CompanyList).filter(CompanyList.CompanyId==ident).delete()
            self.db.query(DepartmentList).filter(DepartmentList.CompanyName==companyname).delete()
            self.db.commit()
            self.Result['info'] = u'删除公司成功'
            self.finish(self.Result)


#获取有效公司
@urlmap(r'/companyshow/')
class CompanyShowHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        director = self.db.query(CompanyList)
        directordict = [i.CompanyName for i in director]
        data = json.dumps(directordict,indent=2)
        self.finish(data)