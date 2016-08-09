#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from sqlalchemy import func
from Callcenter.Entity.AdmUser import AdmUser
from Callcenter.Entity.OutBilllog import OutBilllog
import json,datetime


#每日统计
@urlmap(r'/dailyreport\/?([0-9]*)')
class DailyReportHandler(BaseHandler):

    def get(self, agentphone):
        username = self.get_cookie('user')
        if str(username[-4:]).isdigit():
            agentphone = str(username[-4:])
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            total = self.db.query(OutBilllog.SeqId).filter(OutBilllog.AgentOprno == agentphone,OutBilllog.BeginTime > today).count()
            state0 = self.db.query(OutBilllog.SeqId).filter(OutBilllog.AgentOprno == agentphone,OutBilllog.BeginTime > today, OutBilllog.State == 0).count()
            timeTotal = self.db.query(func.sec_to_time(func.sum(func.time_to_sec(func.timediff(OutBilllog.EndTime, OutBilllog.ConnectTime))))).filter(OutBilllog.AgentOprno == agentphone,OutBilllog.BeginTime > today).first()
            countgt60 = self.db.query(OutBilllog.SeqId).filter(OutBilllog.AgentOprno == agentphone,OutBilllog.BeginTime > today,OutBilllog.State == 0,func.time_to_sec(func.timediff(OutBilllog.EndTime, OutBilllog.ConnectTime)) < 60).count()
            countgt180 = self.db.query(OutBilllog.SeqId).filter(OutBilllog.AgentOprno == agentphone,OutBilllog.BeginTime > today,OutBilllog.State == 0,func.time_to_sec(func.timediff(OutBilllog.EndTime, OutBilllog.ConnectTime)) >= 60,func.time_to_sec(func.timediff(OutBilllog.EndTime, OutBilllog.ConnectTime)) < 180).count()
            self.Result['rows'] = {'total': total, 'state0': state0,
                                   'timeTotal': str(timeTotal[0]), 'c60': countgt60, 'c180': countgt180}
            self.Result['username'] = username
            self.write(self.Result)
        else:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            total = self.db.query(OutBilllog.SeqId).filter(OutBilllog.AgentOprno == agentphone, OutBilllog.BeginTime > today).count()
            state0 = self.db.query(OutBilllog.SeqId).filter(OutBilllog.AgentOprno == agentphone, OutBilllog.BeginTime > today, OutBilllog.State == 0).count()
            timeTotal = self.db.query(func.sec_to_time(func.sum(func.time_to_sec(func.timediff(OutBilllog.EndTime, OutBilllog.ConnectTime))))).filter(OutBilllog.AgentOprno == agentphone,OutBilllog.BeginTime > today).first()
            countgt60 = self.db.query(OutBilllog.SeqId).filter(OutBilllog.AgentOprno == agentphone, OutBilllog.BeginTime > today, OutBilllog.State == 0,func.time_to_sec(func.timediff(OutBilllog.EndTime, OutBilllog.ConnectTime)) < 60).count()
            countgt180 = self.db.query(OutBilllog.SeqId).filter(OutBilllog.AgentOprno == agentphone, OutBilllog.BeginTime > today, OutBilllog.State == 0,func.time_to_sec(func.timediff(OutBilllog.EndTime, OutBilllog.ConnectTime)) >= 60,func.time_to_sec(func.timediff(OutBilllog.EndTime, OutBilllog.ConnectTime)) < 180).count()
            self.Result['rows'] = {'total': total, 'state0': state0,
                                   'timeTotal': str(timeTotal[0]), 'c60': countgt60, 'c180': countgt180}
            self.Result['admin'] = True
            self.Result['username'] = username
            self.write(self.Result)
