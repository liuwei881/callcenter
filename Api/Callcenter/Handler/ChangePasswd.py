#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.AdmUser import AdmUser
from lib.tools import md5hash
import json,datetime


#更改用户密码
@urlmap(r'/changepasswd\/?([0-9]*)')
class ChangePassHandler(BaseHandler):
    @web.asynchronous
    def put(self, ident=0):
        username = self.get_cookie('user')
        data = json.loads(self.request.body)
        objTask = self.db.query(AdmUser).get(ident)
        if username and objTask:
            oldpassword = data['params'].get('OldPassWord', None)
            oldpasswordhash = md5hash(oldpassword)
            try:
                self.db.query(AdmUser).filter(AdmUser.PassWord==oldpasswordhash,AdmUser.Account==username).all()
                newpassword = data['params'].get('NewPassWord', None)
                renewpassword = data['params'].get('ReNewPassWord', None)
                if newpassword == renewpassword and newpassword != oldpassword:
                    objTask.PassWord = md5hash(newpassword)
                    self.db.add(objTask)
                    self.db.commit()
                    self.Result['rows'] = 1
                    self.Result['info'] = u'修改用户密码成功'
                else:
                    self.Result['status'] = 500
                    self.Result['info'] = u'新密码不能重复或2次输入密码不同'
            except Exception,e:
                self.Result['status'] = 400
                self.Result['info'] = '{0}'.format(e)
        else:
            self.Result['info'] = u'修改用户密码失败'
        self.finish(self.Result)
