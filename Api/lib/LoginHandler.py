# -*- coding: utf-8 -*-
__author__ = 'Hipeace86'
__datetime__ = '16-3-9'

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from lib.tools import md5hash
from tornado import web
import datetime
from Callcenter.Entity.AdmUser import AdmUser
from sqlalchemy import desc,or_,and_


@urlmap(r'/login')
class LoginHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        account = self.get_argument('user', '')
        password = self.get_argument('password', '')
        passwd = md5hash(password)
        try:
            user = self.db.query(AdmUser).filter(and_(AdmUser.Account == account,AdmUser.PassWord == passwd)).first()
            if user:
                self.set_cookie('user', str(user.Account), expires_days=0.5)
                self.Result['info'] = u'登陆成功'
                self.Result['status'] = 200
            else:
                self.Result['status'] = 404
                self.Result['info'] = u"用户名不存在"
        except Exception,e:
            self.Result['info'] = u'登陆失败,原因{0}'.format(e)
            self.Result['status'] = 400
        self.finish(self.Result)

@urlmap(r'/logout')
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect('/#/login')
