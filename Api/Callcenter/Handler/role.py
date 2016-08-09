#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import RESTfulHandler,BaseHandler
from tornado import web,gen
from Right.Entity.RoleModel import RoleList
from Right.Entity.UserModel import UserList
import json,datetime
from sqlalchemy import desc,or_,and_


#角色管理
@urlmap(r'/roles\/?([0-9]*)')
class RoleHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        username = self.get_current_user()
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))

        totalquery = self.db.query(RoleList.RoleId)
        RolelistObj = self.db.query(RoleList)
        if searchKey:
            totalquery = totalquery.filter(or_(RoleList.RoleName.like('%%%s%%' % searchKey)))
            RolelistObj = RolelistObj.filter(or_(RoleList.RoleName.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = RolelistObj.order_by(desc(RoleList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
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
            objTask = RoleList()
            objTask.RoleName = data['params'].get('RoleName', None)
            if objTask.RoleName and len(str(objTask.RoleName)) <= 30:
                try:
                    self.db.query(RoleList).filter(RoleList.RoleName==objTask.RoleName).first().RoleName
                except Exception, e:
                    objTask.Desc = data['params'].get('Desc', None)
                    objTask.Create = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
                    objTask.CreateTime = datetime.datetime.now()
                    self.db.add(objTask)
                    self.db.commit()
                    self.Result['info'] = u'创建角色成功'
                else:
                    self.Result['info'] = u'角色重复'
            else:
                self.Result['info'] = u'角色不能为空'
            self.finish(self.Result)
    @web.asynchronous
    def put(self, ident=0):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            data = json.loads(self.request.body)
            objTask = self.db.query(RoleList).get(ident)
            if ident and objTask:
                objTask.RoleName = data['params'].get('RoleName', None)
                objTask.Desc = data['params'].get('Desc', None)
                objTask.Update = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
                objTask.UpdateTime = datetime.datetime.now()
                self.db.add(objTask)
                self.db.commit()
                self.Result['rows'] = 1
                self.Result['info'] = u'修改角色成功'
            else:
                self.Result['rows'] = 0
                self.Result['info'] = u'修改角色失败'
            self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.Result['status'] = 400
            self.finish(self.Result)
        else:
            self.db.query(RoleList).filter(RoleList.RoleId==ident).delete()
            self.db.commit()
            self.Result['info'] = u'删除角色成功'
            self.finish(self.Result)

#判断角色的唯一性
@urlmap(r'/rolecheck\/?(.*)')
class CheckRoleHandler(BaseHandler):
    @web.asynchronous
    def post(self,ident):
        data = json.loads(self.request.body)
        proname = data['rolename']
        try:
            pro = self.db.query(RoleList).filter(RoleList.RoleName==proname).first().RoleName
        except Exception,e:
            self.write(json.dumps({"status":200,"msg":u"角色正常"}))
            self.finish()
        else:
            return
