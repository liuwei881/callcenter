#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.AdmUser import AdmUser
import json


#获取登录用户
@urlmap(r'/username\/?([0-9]*)')
class UserNameHandler(BaseHandler):
    @web.asynchronous
    def get(self,ident):
        username = self.get_cookie('user')
        serverTask = self.db.query(AdmUser).filter(AdmUser.Account==username).all()
        self.Result['username'] = username
        self.Result['rows'] = map(lambda row:row.toDict(),serverTask)
        self.finish(self.Result)

    @web.asynchronous
    def put(self, ident=0):
        data = json.loads(self.request.body)
        objTask = self.db.query(AdmUser).get(ident)
        if ident and objTask:
            objTask.TelePhone = data['params'].get('TelePhone', None)
            objTask.NickName = data['params'].get('NickName', None)
            self.db.add(objTask)
            self.db.commit()
            self.Result['rows'] = 1
            self.Result['info'] = u'修改用户成功'
        else:
            self.Result['rows'] = 0
            self.Result['info'] = u'修改用户失败'
        self.finish(self.Result)
