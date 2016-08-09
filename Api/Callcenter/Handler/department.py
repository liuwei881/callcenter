#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import RESTfulHandler
from tornado import web,gen
from Right.Entity.DepartmentModel import DepartmentList
from Right.Entity.UserModel import UserList
from Right.Entity.DepartmentFunctionModel import DepartmentFunctionList
import json,datetime
from sqlalchemy import desc,or_,and_


#部门管理
@urlmap(r'/department\/?([0-9]*)')
class DepartmentHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        username = self.get_current_user()
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))

        totalquery = self.db.query(DepartmentList.DepartmentId)
        DepartmentlistObj = self.db.query(DepartmentList)
        if searchKey:
            totalquery = totalquery.filter(or_(DepartmentList.DepartmentName.like('%%%s%%' % searchKey)))
            DepartmentlistObj = DepartmentlistObj.filter(or_(DepartmentList.DepartmentName.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = DepartmentlistObj.order_by(desc(DepartmentList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
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
            objTask = DepartmentList()
            objTask.CompanyName = data['params'].get('CompanyName', None)
            objTask.ParentBusiness = data['params'].get('ParentBusiness', None)
            objTask.DepartmentName = data['params'].get('DepartmentName', None)
            objTask.Desc = data['params'].get('Desc', None)
            objTask.Is_management = data['params'].get('Is_management', '否')
            objTask.Create = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
            objTask.CreateTime = datetime.datetime.now()
            objDepart = DepartmentFunctionList()
            objDepart.DepartmentName = objTask.DepartmentName
            objDepart.Level = 2
            objDepart.Parent = self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.DepartmentName==objTask.CompanyName).first().DepartmentFunctionId
            self.db.add(objDepart)
            self.db.add(objTask)
            self.db.commit()
            self.Result['info'] = u'创建部门成功'
            self.finish(self.Result)

    @web.asynchronous
    def put(self, ident):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            data = json.loads(self.request.body)
            objTask = self.db.query(DepartmentList).get(ident)
            if ident and objTask:
                objTask.CompanyName = data['params'].get('CompanyName', None)
                objTask.ParentBusiness = data['params'].get('ParentBusiness', None)
                objTask.DepartmentName = data['params'].get('DepartmentName', None)
                objTask.Desc = data['params'].get('Desc', None)
                objTask.Is_management = data['params'].get('Is_management', '否')
                objTask.Update = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
                objTask.UpdateTime = datetime.datetime.now()
                self.db.add(objTask)
                self.db.commit()
                self.Result['rows'] = 1
                self.Result['info'] = u'修改部门成功'
            else:
                self.Result['rows'] = 0
                self.Result['info'] = u'修改部门失败'
            self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            departname = self.db.query(DepartmentList).filter(DepartmentList.DepartmentId==ident).first()
            dename = departname.DepartmentName
            companyname = departname.CompanyName
            parent = self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.DepartmentName==companyname).first().DepartmentFunctionId
            self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.DepartmentName==dename,DepartmentFunctionList.Parent==parent).delete()
            self.db.query(DepartmentList).filter(DepartmentList.DepartmentId==ident).delete()
            self.db.commit()
            self.Result['info'] = u'删除部门成功'
            self.finish(self.Result)
