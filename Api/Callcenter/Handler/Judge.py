#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.ServerJudge import ServerJudge
import json,tablib,os,datetime
from sqlalchemy import desc,or_,and_


#用户评价
@urlmap(r'/serverjudge\/?([0-9]*)')
class JudgeHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        page = int(self.get_argument('page', 1))
        Oprno = self.get_argument('agentoprno', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        try:
            stime = datetime.datetime.strptime(self.get_argument('starttimejudge', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            starttime = datetime.datetime.strptime(stime, "%Y-%m-%d") + datetime.timedelta(days=1)
            etime = datetime.datetime.strptime(self.get_argument('endtimejudge', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            endtime = datetime.datetime.strptime(etime, "%Y-%m-%d") + datetime.timedelta(days=2)
            starttime = starttime.strftime("%Y-%m-%d")
            endtime = endtime.strftime("%Y-%m-%d")
            if starttime == endtime:
                etime = datetime.datetime.strptime(endtime, "%Y-%m-%d") + datetime.timedelta(days=2)
                endtime = etime.strftime("%Y-%m-%d")
                totalquery = self.db.query(ServerJudge.Id).filter(ServerJudge.SysTime >= starttime,ServerJudge.SysTime < endtime)
                ServerJudgeObj = self.db.query(ServerJudge).filter(ServerJudge.SysTime >= starttime,ServerJudge.SysTime < endtime)
            else:
                totalquery = self.db.query(ServerJudge.Id).filter(ServerJudge.SysTime >= starttime)
                ServerJudgeObj = self.db.query(ServerJudge).filter(ServerJudge.SysTime >= starttime)
        except Exception, e:
            totalquery = self.db.query(ServerJudge.Id)
            ServerJudgeObj = self.db.query(ServerJudge)
        if Oprno:
            totalquery = totalquery.filter(or_(ServerJudge.Oprno==Oprno,ServerJudge.Caller==Oprno,ServerJudge.Called==Oprno,ServerJudge.Caller=='0'+Oprno,ServerJudge.Called=='0'+Oprno))
            ServerJudgeObj = ServerJudgeObj.filter(or_(ServerJudge.Oprno==Oprno,ServerJudge.Caller==Oprno,ServerJudge.Called==Oprno,ServerJudge.Caller=='0'+Oprno,ServerJudge.Called=='0'+Oprno))
        elif Oprno == '':
            Oprno = "all"
        serverTask = ServerJudgeObj.order_by(desc(ServerJudge.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        allserverTask = ServerJudgeObj.order_by(desc(ServerJudge.Id)).all()
        allserverTask = map(lambda obj: obj.toDict(), allserverTask)
        self.Result['total'] = totalquery.count()
        self.Result['oprno'] = Oprno
        self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        headers = ('坐席号', '主叫电话', '状态', '系统时间', '坐席组','被叫电话')
        oprnolist = []
        for i in allserverTask:
            del i['SkillId']
            del i['BillId']
            del i['Id']
            n = dict(sorted(i.iteritems(), key=lambda key:key[0], reverse=False))
            oprnolist.append(tuple(n.values()))
        oprnolist = tablib.Dataset(*oprnolist, headers=headers)
        doc = os.path.join(os.path.dirname(__file__), 'download/{0}.xlsx'.format(Oprno))
        with open(doc,'wb') as oprnotable:
            oprnotable.writelines(oprnolist.xlsx)
        self.finish(self.Result)