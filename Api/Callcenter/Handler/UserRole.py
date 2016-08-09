#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Right.Entity.UserModel import UserList
from Right.Entity.RoleModel import RoleList
from Right.Entity.UserRoleModel import UserRoleList
import json


#用户角色分配
@urlmap(r'/user/role\/?([0-9]*)')
class UserRoleHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        if ident:
            try:
                objServer = self.db.query(UserRoleList).filter(UserRoleList.RoleId==ident).all()
                d = {}
                d["RoleId"] = ident
                d["RoleName"] = self.db.query(RoleList).filter(RoleList.RoleId==ident).first().RoleName
                objs = [obj.toDict() for obj in objServer]
                if objs:
                    countlist = [i.get("UserId",None) for i in objs]
                    c = {}
                    for i in countlist:
                        username = self.db.query(UserList).filter(UserList.UserId==i).first().UserName
                        c[username] = True
                    objs[0]["UserName"] = c
                    objs[0].update(d)
                else:
                    objs.append(d)
                self.Result['rows'] = objs[0]
            except Exception,e:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found,{0}'.format(e)
        else:
            totalquery = self.db.query(UserRoleList.UserId)
            memberlistObj = self.db.query(UserRoleList)
            self.Result['total'] = totalquery.count()
            self.Result['rows'] = map(lambda obj: obj.toDict(), memberlistObj)
        self.finish(self.Result)

    @web.asynchronous
    def post(self,ident=0):
        data = json.loads(self.request.body)
        userdict = data['params'].get('UserName',None)
        if userdict:
            usernamenot = []
            username = []
            for k,v in userdict.iteritems():
                if not v:
                    usernamenot.append(k)
                else:
                    username.append(k)
            if usernamenot:
                for u in usernamenot:
                    userid = self.db.query(UserList).filter(UserList.UserName==u).first().UserId
                    self.db.query(UserRoleList).filter(UserRoleList.UserId==userid).delete()
            if username:
                for u in username:
                    userid = self.db.query(UserList).filter(UserList.UserName==u).first().UserId
                    if not self.db.query(UserRoleList).filter(UserRoleList.UserId==userid,UserRoleList.RoleId==ident).all():
                        pro = UserRoleList(UserId=userid,RoleId=ident)
                        self.db.add(pro)
        self.db.commit()
        self.Result['rows'] = 1
        self.Result['info'] = u'修改用户角色成功'
        self.finish(self.Result)
