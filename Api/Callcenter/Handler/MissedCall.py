#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.MissedCallView import MissedCallView
from Callcenter.Entity.AdmUser import AdmUser
import json,datetime,tablib,os
from sqlalchemy import desc,or_,and_


#未接来电查询
@urlmap(r'/missedcall\/?([0-9]*)')
class MissedCallHandler(BaseHandler):
    @web.asynchronous
    def get(self,ident):
        phone = self.get_argument('agentoprno', None)
        #if phone == "":
        #    phone = "all"
        page = int(self.get_argument('page', 1))
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        username = self.get_cookie('user')
        self.Result['username'] = username
        try:
            stime = datetime.datetime.strptime(self.get_argument('starttime', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            starttime = datetime.datetime.strptime(stime, "%Y-%m-%d") + datetime.timedelta(days=1)
            etime = datetime.datetime.strptime(self.get_argument('endtime', None), '%Y-%m-%dT%H:%M:%S.000Z').strftime("%Y-%m-%d")
            endtime = datetime.datetime.strptime(etime, "%Y-%m-%d") + datetime.timedelta(days=2)
            starttime = starttime.strftime("%Y-%m-%d")
            endtime = endtime.strftime("%Y-%m-%d")
            if starttime == endtime:
                etime = datetime.datetime.strptime(endtime, "%Y-%m-%d") + datetime.timedelta(days=2)
                endtime = etime.strftime("%Y-%m-%d")
                totalquery = self.db.query(MissedCallView.Id).filter(MissedCallView.BeginTime >= starttime,MissedCallView.BeginTime < endtime)
                MissedCallObj = self.db.query(MissedCallView).filter(MissedCallView.BeginTime >= starttime,MissedCallView.BeginTime < endtime)
            else:
                totalquery = self.db.query(MissedCallView.Id).filter(MissedCallView.BeginTime>=starttime)
                MissedCallObj = self.db.query(MissedCallView).filter(MissedCallView.BeginTime >= starttime)
        except Exception, e:
            MissedCallObj = self.db.query(MissedCallView)
            totalquery = self.db.query(MissedCallView.Id)
        if str(username[-4:]).isdigit():
            phone = str(username[-4:])
            totalquery = totalquery.filter(MissedCallView.AgentOprno==phone)
            rows = MissedCallObj.filter(MissedCallView.AgentOprno==phone).order_by(MissedCallView.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        #    allrows = MissedCallObj.filter(or_(MissedCallView.Caller==phone,MissedCallView.Caller=='0' + phone)).order_by(MissedCallView.BeginTime.desc()).all()
        elif str(phone).isdigit():
            totalquery = totalquery.filter(or_(MissedCallView.Caller==phone,MissedCallView.Caller=='0' + phone))
            rows = MissedCallObj.filter(or_(MissedCallView.Caller==phone,MissedCallView.Caller=='0' + phone)).order_by(MissedCallView.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        #    allrows = MissedCallObj.filter(or_(MissedCallView.Caller == phone, MissedCallView.Caller == '0' + phone)).order_by(MissedCallView.BeginTime.desc()).all()
        else:
            rows = MissedCallObj.order_by(MissedCallView.BeginTime.desc()).limit(pagesize).offset((page - 1) * pagesize).all()
        #    allrows = MissedCallObj.order_by(MissedCallView.BeginTime.desc()).all()
        self.Result['total'] = totalquery.count()
        self.Result['oprno'] = phone
        self.Result['rows'] = map(lambda row: row.toDict(), rows)
        # allrows = map(lambda row: row.toDict(), allrows)
        # headers = ('呼损类型', '坐席号码', '开始时间', '主叫号码')
        # oprnolist = []
        # for i in allrows:
        #     del i['Called']
        #     del i['Id']
        #     n = dict(sorted(i.iteritems(), key=lambda key: key[0], reverse=False))
        #     oprnolist.append(tuple(n.values()))
        # oprnolist = tablib.Dataset(*oprnolist, headers=headers)
        # doc = os.path.join(os.path.dirname(__file__), 'missedcaller/{0}.xlsx'.format(phone))
        # with open(doc, 'wb') as oprnotable:
        #     oprnotable.writelines(oprnolist.xlsx)
        self.finish(json.dumps(self.Result))