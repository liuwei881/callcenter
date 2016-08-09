#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.InBilllog import InBilllog
from Callcenter.Entity.AdmUser import AdmUser
import json,datetime
from sqlalchemy import desc,or_,and_

#呼入记录
@urlmap(r'/inbill\/?([0-9]*)')
class InBillHandler(BaseHandler):
    @web.asynchronous
    def get(self,ident):
        phone = self.get_argument('agentoprno', None)
        page = int(self.get_argument('page', 1))
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        username = self.get_cookie('user')
        self.Result['username'] = username
        try:
            stime = datetime.datetime.strptime(self.get_argument('starttimein', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            starttime = datetime.datetime.strptime(stime, "%Y-%m-%d") + datetime.timedelta(days=1)
            etime = datetime.datetime.strptime(self.get_argument('endtimein', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            endtime = datetime.datetime.strptime(etime, "%Y-%m-%d") + datetime.timedelta(days=2)
            starttime = starttime.strftime("%Y-%m-%d")
            endtime = endtime.strftime("%Y-%m-%d")
            if starttime == endtime:
                etime = datetime.datetime.strptime(endtime, "%Y-%m-%d") + datetime.timedelta(days=2)
                endtime = etime.strftime("%Y-%m-%d")
                totalquery = self.db.query(InBilllog.SeqId).filter(InBilllog.BeginTime >= starttime, InBilllog.EndTime <= endtime)
                InBillObj = self.db.query(InBilllog).filter(InBilllog.BeginTime >= starttime, InBilllog.EndTime <= endtime)
            else:
                totalquery = self.db.query(InBilllog.SeqId).filter(InBilllog.BeginTime >= starttime, InBilllog.EndTime <= endtime)
                InBillObj = self.db.query(InBilllog).filter(InBilllog.BeginTime >= starttime, InBilllog.EndTime <= endtime)
        except Exception, e:
            totalquery = self.db.query(InBilllog.SeqId)
            InBillObj = self.db.query(InBilllog)
        if str(username[-4:]).isdigit():
            phone = str(username[-4:])
            totalquery = totalquery.filter(InBilllog.AgentOprno==phone)
            rows = InBillObj.filter(InBilllog.AgentOprno==phone).order_by(InBilllog.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        if str(phone).isdigit():
            totalquery = totalquery.filter(or_(InBilllog.AgentOprno==phone,InBilllog.Caller==phone,InBilllog.Caller=='0' + phone))
            rows = InBillObj.filter(or_(InBilllog.AgentOprno==phone,InBilllog.Caller==phone,InBilllog.Caller=='0' + phone)).order_by(InBilllog.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        else:
            rows = InBillObj.order_by(InBilllog.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['total'] = totalquery.count()
        self.Result['rows'] = map(lambda row: row.toDict(), rows)
        self.finish(json.dumps(self.Result))

