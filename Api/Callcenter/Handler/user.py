#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import RESTfulHandler,BaseHandler
from tornado import web,gen
from Right.Entity.UserModel import UserList
from lib.tools import md5hash
from Right.Entity.DepartmentFunctionModel import DepartmentFunctionList
import json,datetime
from sqlalchemy import desc,or_,and_


#用户管理
@urlmap(r'/user\/?([0-9]*)')
class UserHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        username = self.get_current_user()
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(UserList.UserId)
        UserlistObj = self.db.query(UserList)
        if searchKey:
            totalquery = totalquery.filter(UserList.UserName.like('%%%s%%' % searchKey))
            UserlistObj = UserlistObj.filter(UserList.UserName.like('%%%s%%' % searchKey))
        self.Result['total'] = totalquery.count()
        serverTask = UserlistObj.order_by(desc(UserList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
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
            objTask = UserList()
            objTask.UserName = data['params'].get('UserName', None)
            objTask.UserAccount = data['params'].get('UserAccount', None)
            objTask.PassWord = md5hash("".join(["iprun", md5hash('{0}'.format(data['params'].get('PassWord', None))), "admin"]))
            if objTask.UserName and objTask.UserAccount and objTask.PassWord:
                try:
                    self.db.query(UserList).filter(UserList.UserName==objTask.UserName).first().UserName
                except Exception, e:
                    objTask.CompanyName = data['params'].get('CompanyName', None).get('name', None)
                    objTask.Department = data['params'].get('Department', None).get('name', None)
                    objTask.Position = data['params'].get('Position', None)
                    objTask.Sex = data['params'].get('Sex', None)
                    objTask.TelePhone = data['params'].get('TelePhone', None)
                    objTask.Area = data['params'].get('Area', None)
                    objTask.Address = data['params'].get('Address', None)
                    objTask.Phone = data['params'].get('Phone', None)
                    objTask.Email = data['params'].get('Email', None)
                    objTask.Postcode = data['params'].get('Postcode', None)
                    objTask.OutsideLogin = data['params'].get('OutsideLogin', '1')
                    objTask.BirthDay = data['params'].get('BirthDay', None)
                    objTask.Is_valid = data['params'].get('Is_valid', '1')
                    objTask.Comment = data['params'].get('Comment', None)
                    objTask.Create = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
                    objTask.CreateTime = datetime.datetime.now()
                    objDepart = DepartmentFunctionList()
                    objDepart.DepartmentName = objTask.UserName
                    objDepart.Level = 3
                    objDepart.Parent = self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.DepartmentName==objTask.Department).first().DepartmentFunctionId
                    self.db.add(objDepart)
                    self.db.add(objTask)
                    self.db.commit()
                    self.Result['info'] = u'创建用户成功'
                else:
                    self.Result['info'] = u'用户重复'
            else:
                self.Result['info'] = u'用户不能为空'
            self.finish(self.Result)

    @web.asynchronous
    def put(self, ident=0):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            data = json.loads(self.request.body)
            objTask = self.db.query(UserList).get(ident)
            if ident and objTask:
                objTask.Department = data['params'].get('Department', None)
                objTask.CompanyName = data['params'].get('CompanyName', None)
                objTask.Position = data['params'].get('Position', None)
                objTask.UserName = data['params'].get('UserName', None)
                objTask.Sex = data['params'].get('Sex', None)
                objTask.UserAccount = data['params'].get('UserAccount', None)
                objTask.TelePhone = data['params'].get('TelePhone', None)
                objTask.Area = data['params'].get('Area', None)
                objTask.Address = data['params'].get('Address', None)
                objTask.Phone = data['params'].get('Phone', None)
                objTask.Email = data['params'].get('Email', None)
                objTask.Postcode = data['params'].get('Postcode', None)
                objTask.OutsideLogin = data['params'].get('OutsideLogin', '1')
                objTask.BirthDay = data['params'].get('BirthDay', None)
                if data['params'].get('Is_valid',None) == "是":
                    objTask.Is_valid = 1
                else:
                    objTask.Is_valid = 0
                objTask.Update = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
                objTask.UpdateTime = datetime.datetime.now()
                self.db.add(objTask)
                self.db.commit()
                self.Result['rows'] = 1
                self.Result['info'] = u'修改用户成功'
            else:
                self.Result['rows'] = 0
                self.Result['info'] = u'修改用户失败'
            self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            user = self.db.query(UserList).filter(UserList.UserId==ident).first()
            username = user.UserName
            depname = user.Department
            parent = self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.DepartmentName==depname).first().DepartmentFunctionId
            self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.DepartmentName==username,DepartmentFunctionList.Parent==parent).delete()
            self.db.query(UserList).filter(UserList.UserId==ident).delete()
            self.db.commit()
            self.Result['info'] = u'删除用户成功'
            self.finish(self.Result)

#获取用户成员字典
@urlmap(r'/userdict/')
class UserdictHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        director = self.db.query(UserList)
        userdict = map(lambda obj: obj.toDict(), director)
        data = json.dumps(userdict,indent=2)
        self.finish(data)

#判断用户的唯一性
@urlmap(r'/usernamecheck\/?(.*)')
class CheckUserHandler(BaseHandler):
    @web.asynchronous
    def post(self,ident):
        data = json.loads(self.request.body)
        proname = data['username']
        try:
            pro = self.db.query(UserList).filter(UserList.UserName==proname).first().UserName
        except Exception,e:
            self.write(json.dumps({"status":200,"msg":u"用户正常"}))
            self.finish()
        else:
            return

#判断用户账户的唯一性
@urlmap(r'/useraccountcheck\/?(.*)')
class CheckUserAccountHandler(BaseHandler):
    @web.asynchronous
    def post(self,ident):
        data = json.loads(self.request.body)
        proname = data['useraccount']
        try:
            pro = self.db.query(UserList).filter(UserList.UserAccount==proname).first().UserAccount
        except Exception,e:
            self.write(json.dumps({"status":200,"msg":u"用户账户正常"}))
            self.finish()
        else:
            return

#获取登录用户
@urlmap(r'/username\/?([0-9]*)')
class UserNameHandler(BaseHandler):
    @web.asynchronous
    def get(self,ident):
        userid = self.get_current_user()
        serverTask = self.db.query(UserList).get(userid)
        username = self.db.query(UserList).filter(UserList.UserId==userid).first().UserName
        self.Result['username'] = username
        self.Result['rows'] = serverTask.toDict()
        self.finish(self.Result)

    @web.asynchronous
    def put(self, ident=0):
        data = json.loads(self.request.body)
        objTask = self.db.query(UserList).get(ident)
        if ident and objTask:
            objTask.UserName = data['params'].get('UserName', None)
            objTask.Sex = data['params'].get('Sex', None)
            objTask.TelePhone = data['params'].get('TelePhone', None)
            objTask.Area = data['params'].get('Area', None)
            objTask.Address = data['params'].get('Address', None)
            objTask.Phone = data['params'].get('Phone', None)
            objTask.Email = data['params'].get('Email', None)
            objTask.BirthDay = data['params'].get('BirthDay', None)
            self.db.add(objTask)
            self.db.commit()
            self.Result['rows'] = 1
            self.Result['info'] = u'修改用户成功'
        else:
            self.Result['rows'] = 0
            self.Result['info'] = u'修改用户失败'
        self.finish(self.Result)



