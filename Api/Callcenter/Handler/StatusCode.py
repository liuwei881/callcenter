#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.OutBilllog import OutBilllog
import json,datetime
from sqlalchemy import desc,or_,and_,func



#状态码统计
@urlmap(r'/statuscode/count')
class StatusCodeHandler(BaseHandler):
    def get(self):
        phone = self.get_argument('agentoprno', None)
        username = self.get_cookie('user')
        self.Result['username'] = username
        try:
            stime = datetime.datetime.strptime(self.get_argument('startcodetime', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            starttime = datetime.datetime.strptime(stime,"%Y-%m-%d") + datetime.timedelta(days=1)
            etime = datetime.datetime.strptime(self.get_argument('endcodetime', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            endtime = datetime.datetime.strptime(etime,"%Y-%m-%d") + datetime.timedelta(days=2)
            starttime = starttime.strftime("%Y-%m-%d")
            endtime = endtime.strftime("%Y-%m-%d")
            if starttime == endtime:
                etime = datetime.datetime.strptime(endtime, "%Y-%m-%d") + datetime.timedelta(days=2)
                endtime = etime.strftime("%Y-%m-%d")
                OutBillObj = self.db.query(OutBilllog.State,func.count(OutBilllog.State)).filter(OutBilllog.BeginTime >= starttime, OutBilllog.EndTime <= endtime)
            else:
                OutBillObj = self.db.query(OutBilllog.State,func.count(OutBilllog.State)).filter(OutBilllog.BeginTime >= starttime, OutBilllog.EndTime <= endtime)
        except Exception, e:
            OutBillObj = self.db.query(OutBilllog.State,func.count(OutBilllog.State))
        if str(username[-4:]).isdigit():
            phone = str(username[-4:])
            rows = OutBillObj.filter(OutBilllog.AgentOprno==phone).group_by(OutBilllog.State).all()
        elif str(phone).isdigit():
            rows = OutBillObj.filter(OutBilllog.AgentOprno==phone).group_by(OutBilllog.State).all()
        else:
            rows = OutBillObj.group_by(OutBilllog.State).all()
        self.Result['xAxis'] = sorted(dict(rows).keys())
        series = []
        seriespercent = []
        series.append({'name':u'状态码数量','data': [k[1] for k in sorted(rows)]})
        seriespercent.append({'name': u'状态码比例', 'data': [round(float(v) / sum(dict(rows).values())*100,2) for k, v in sorted(rows)]})
        self.Result['rows'] = series
        self.Result['rowspercent'] = seriespercent
        self.finish(json.dumps(self.Result))