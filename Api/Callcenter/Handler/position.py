#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import RESTfulHandler,BaseHandler
from tornado import web,gen
from Right.Entity.PositionModel import PositionList
from Right.Entity.UserModel import UserList
import json,datetime
from sqlalchemy import desc,or_,and_


#职位管理
@urlmap(r'/position\/?([0-9]*)')
class PositionHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        username = self.get_current_user()
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))

        totalquery = self.db.query(PositionList.PositionId)
        PositionlistObj = self.db.query(PositionList)
        if searchKey:
            totalquery = totalquery.filter(or_(PositionList.PositionName.like('%%%s%%' % searchKey)))
            PositionlistObj = PositionlistObj.filter(or_(PositionList.PositionName.like('%%%s%%' % searchKey)))
        self.Result['total'] = totalquery.count()
        serverTask = PositionlistObj.order_by(desc(PositionList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
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
            objTask = PositionList()
            objTask.PositionName = data['params'].get('PositionName', None)
            objTask.Desc = data['params'].get('Desc', None)
            objTask.ReportTo = data['params'].get('ReportTo', None)
            objTask.Is_management = data['params'].get('Is_management', '0')
            objTask.Create = self.db.query(UserList).filter(UserList.UserId==self.get_current_user()).first().UserName
            objTask.CreateTime = datetime.datetime.now()
            self.db.add(objTask)
            self.db.commit()
            self.Result['info'] = u'创建职位成功'
            self.finish(self.Result)

    @web.asynchronous
    def put(self, ident):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            data = json.loads(self.request.body)
            objTask = self.db.query(PositionList).get(ident)
            if ident and objTask:
                objTask.PositionName = data['params'].get('PositionName', None)
                objTask.Desc = data['params'].get('Desc', None)
                objTask.ReportTo = data['params'].get('ReportTo', None)
                objTask.Is_management = data['params'].get('Is_management', '否')
                objTask.Update = self.db.query(UserList).filter(UserList.UserId == self.get_current_user()).first().UserName
                objTask.UpdateTime = datetime.datetime.now()
                self.db.add(objTask)
                self.db.commit()
                self.Result['rows'] = 1
                self.Result['info'] = u'修改职位成功'
            else:
                self.Result['rows'] = 0
                self.Result['info'] = u'修改职位失败'
            self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        if self.RightEnable == False:
            self.Result['success'] = False
            self.finish(self.Result)
        else:
            self.db.query(PositionList).filter(PositionList.PositionId==ident).delete()
            self.db.commit()
            self.Result['info'] = u'删除职位成功'
            self.finish(self.Result)

#获取有效职位
@urlmap(r'/positionshow/')
class PositionShowHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        director = self.db.query(PositionList)
        directordict = [i.PositionName for i in director]
        data = json.dumps(directordict,indent=2)
        self.finish(data)