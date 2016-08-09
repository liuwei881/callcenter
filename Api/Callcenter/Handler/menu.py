#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Right.Entity.MenuModel import MenuList
import json

#用户管理
@urlmap(r'/menu/')
class MenuHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        director = self.db.query(MenuList)
        directordict = map(lambda obj: obj.toDict(), director)
        data = json.dumps(directordict,indent=2)
        self.finish(data)
