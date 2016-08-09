#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.OutBilllog import OutBilllog
from Callcenter.Entity.AdmUser import AdmUser
import json,datetime
from sqlalchemy import desc,or_,and_


#呼出记录
@urlmap(r'/outbill\/?([0-9]*)')
class OutBillHandler(BaseHandler):
    @web.asynchronous
    def get(self,ident):
        phone = self.get_argument('agentoprno', None)
        page = int(self.get_argument('page', 1))
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        username = self.get_cookie('user')
        self.Result['username'] = username
        try:
            stime = datetime.datetime.strptime(self.get_argument('starttimeout', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            starttime = datetime.datetime.strptime(stime,"%Y-%m-%d") + datetime.timedelta(days=1)
            etime = datetime.datetime.strptime(self.get_argument('endtimeout', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            endtime = datetime.datetime.strptime(etime,"%Y-%m-%d") + datetime.timedelta(days=2)
            starttime = starttime.strftime("%Y-%m-%d")
            endtime = endtime.strftime("%Y-%m-%d")
            if starttime == endtime:
                etime = datetime.datetime.strptime(endtime, "%Y-%m-%d") + datetime.timedelta(days=2)
                endtime = etime.strftime("%Y-%m-%d")
                totalquery = self.db.query(OutBilllog.SeqId).filter(OutBilllog.BeginTime >= starttime, OutBilllog.EndTime <= endtime)
                OutBillObj = self.db.query(OutBilllog).filter(OutBilllog.BeginTime >= starttime, OutBilllog.EndTime <= endtime)
            else:
                totalquery = self.db.query(OutBilllog.SeqId).filter(OutBilllog.BeginTime>=starttime,OutBilllog.EndTime<=endtime)
                OutBillObj = self.db.query(OutBilllog).filter(OutBilllog.BeginTime >= starttime, OutBilllog.EndTime <= endtime)
        except Exception, e:
            totalquery = self.db.query(OutBilllog.SeqId)
            OutBillObj = self.db.query(OutBilllog)
        if str(username[-4:]).isdigit():
            phone = str(username[-4:])
            totalquery = totalquery.filter(OutBilllog.AgentOprno==phone)
            rows = OutBillObj.filter(OutBilllog.AgentOprno==phone).order_by(OutBilllog.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        if str(phone).isdigit():
            totalquery = totalquery.filter(or_(OutBilllog.AgentOprno==phone,OutBilllog.Called==phone,OutBilllog.Called=='0' + phone))
            rows = OutBillObj.filter(or_(OutBilllog.AgentOprno==phone,OutBilllog.Called==phone,OutBilllog.Called=='0' + phone)).order_by(OutBilllog.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        else:
            rows = OutBillObj.order_by(OutBilllog.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['total'] = totalquery.count()
        self.Result['rows'] = map(lambda row: row.toDict(), rows)
        self.finish(json.dumps(self.Result))