#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web,gen
from Callcenter.Entity.CcsOprno import CcsOprno
from Callcenter.Entity.CcsTeam import CcsTeam
import json
from sqlalchemy import desc,or_,and_


#坐席
@urlmap(r'/oprno\/?([0-9]*)')
class OprnoHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(CcsOprno.Id)
        CcsOprnoObj = self.db.query(CcsOprno)
        if searchKey:
            totalquery = totalquery.filter(CcsOprno.Oprno==searchKey)
            CcsOprnoObj = CcsOprnoObj.filter(CcsOprno.Oprno==searchKey)
        self.Result['total'] = totalquery.count()
        serverTask = CcsOprnoObj.order_by(desc(CcsOprno.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)

    @web.asynchronous
    def post(self,ident=0):
        data = json.loads(self.request.body)
        objTask = CcsOprno()
        objTask.BindAccount = data['params'].get('BindAccount', 1)
        BindTeam = data['params'].get('BindTeam',None)
        objTask.BindTeam = self.db.query(CcsTeam).filter(CcsTeam.Name==BindTeam).first().Id
        objTask.Oprno = data['params'].get('Oprno', None)
        objTask.OrderId = data['params'].get('OrderId', 0)
        objTask.ShowCaller = data['params'].get('ShowCaller', None)
        objTask.Sipphone = objTask.Oprno
        objTask.Sipphonepwd = data['params'].get('Sipphonepwd', 'ceshi')
        objTask.Status = data['params'].get('Status', 1)
        self.db.add(objTask)
        self.db.commit()
        self.Result['info'] = u'创建坐席成功'
        self.finish(self.Result)

    @web.asynchronous
    def put(self,ident=0):
        data = json.loads(self.request.body)
        objTask = self.db.query(CcsOprno).get(ident)
        if ident and objTask:
            BindTeam = data['params'].get('BindTeam', None)
            objTask.BindTeam = self.db.query(CcsTeam).filter(CcsTeam.Name == BindTeam).first().Id
            objTask.ShowCaller = data['params'].get('ShowCaller', None)
            objTask.Oprno = data['params'].get('Oprno', None)
            objTask.Status = data['params'].get('Status', 1)
            self.db.add(objTask)
            self.db.commit()
            self.Result['rows'] = 1
            self.Result['info'] = u'修改坐席成功'
        else:
            self.Result['rows'] = 0
            self.Result['info'] = u'修改坐席失败'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self,ident):
        self.db.query(CcsOprno).filter(CcsOprno.Id==ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除坐席成功'
        self.finish(self.Result)
