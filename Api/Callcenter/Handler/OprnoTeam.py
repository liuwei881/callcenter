#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.CcsTeam import CcsTeam
from Callcenter.Entity.CcsOprno import CcsOprno
import json,time
from sqlalchemy import desc,or_,and_


#坐席组
@urlmap(r'/oprnoteam\/?([0-9]*)')
class OprnoTeamHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(CcsTeam.Id)
        CcsOprnoObj = self.db.query(CcsTeam)
        if searchKey:
            totalquery = totalquery.filter(CcsTeam.Name.like('%%%s%%' % searchKey))
            CcsOprnoObj = CcsOprnoObj.filter(CcsTeam.Name.like('%%%s%%' % searchKey))
        self.Result['total'] = totalquery.count()
        serverTask = CcsOprnoObj.order_by(desc(CcsTeam.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)

    @web.asynchronous
    def post(self,ident=0):
        data = json.loads(self.request.body)
        objTask = CcsTeam()
        objTask.Name = data['params'].get('Name', None)
        objTask.BindAccount = 1
        objTask.TimeId = 1
        objTask.Isrecord = 1
        objTask.RecordPath = "h:\\"
        objTask.ShowcallerTag = 1
        objTask.ShowCaller = "81377775"
        objTask.AudioCode = 18
        objTask.AgentCount = 100
        objTask.Ctime = int(time.time())
        self.db.add(objTask)
        self.db.commit()
        self.Result['info'] = u'创建坐席组成功'
        self.finish(self.Result)

    @web.asynchronous
    def put(self,ident=0):
        data = json.loads(self.request.body)
        objTask = self.db.query(CcsTeam).get(ident)
        if ident and objTask:
            objTask.Name = data['params'].get('Name', None)
            objTask.AgentCount = data['params'].get('AgentCount', None)
            self.db.add(objTask)
            self.db.commit()
            self.Result['rows'] = 1
            self.Result['info'] = u'修改坐席组成功'
        else:
            self.Result['rows'] = 0
            self.Result['info'] = u'修改坐席组失败'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self,ident=0):
        self.db.query(CcsTeam).filter(CcsTeam.Id==ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除坐席组成功'
        self.finish(self.Result)

#获取坐席组
@urlmap(r'/seatshow/')
class SeatShowHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        director = self.db.query(CcsTeam)
        seatdict = [i.Name for i in director]
        data = json.dumps(seatdict,indent=2)
        self.finish(data)