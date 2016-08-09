#coding=utf-8

from lib.basehandler import BaseHandler
from lib.urlmap import urlmap
import time
import json
import copy
from datetime import datetime
from datetime import timedelta
from sqlalchemy import func
from Callcenter.Entity.OutBilllog import OutBilllog
from Callcenter.Entity.FreeOprno import FreeOprno
import numpy as np


@urlmap(r'/callcenter/weekly')
class WeeklyReportApiHandler(BaseHandler):

    def get(self):
        st = self.get_argument('st', None)
        et = self.get_argument('et', None)
        if st is None:
            st = time.strftime('%Y-%m-01')
        if et is None:
            et = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            et = datetime.strptime(et, '%Y-%m-%d') + \
                timedelta(days=1).strftime('%Y-%m-%d')
        series = []

        # 全部通话数量
        weekAll = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(OutBilllog.SeqId)).\
            filter(OutBilllog.BeginTime > st).filter(OutBilllog.BeginTime < et).\
            group_by(func.weekofyear(OutBilllog.BeginTime)).limit(60).all()
        xAxis = dict((k[0], 0) for k in weekAll)
        allData = dict(copy.deepcopy(xAxis), **dict(weekAll))
        series.append({'name': u'呼叫总量', 'data': [
                      value for (key, value) in sorted(allData.items())]})
        # 未接听数量
        noReceiver = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(OutBilllog.SeqId)).\
            filter(OutBilllog.BeginTime > st).filter(OutBilllog.BeginTime < et).\
            filter(func.timediff(OutBilllog.EndTime, OutBilllog.BeginTime) == 46).\
            filter(OutBilllog.State > 0).\
            group_by(func.weekofyear(OutBilllog.BeginTime)).limit(60).all()
        noReceiverData = dict(copy.deepcopy(xAxis), **dict(noReceiver))
        series.append({'name': u'未接听量', 'data': [value for (
            key, value) in sorted(noReceiverData.items())]})
        # 接听数量
        hasReceiver = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(OutBilllog.SeqId)).\
            filter(OutBilllog.BeginTime > st).filter(OutBilllog.BeginTime < et).\
            filter(OutBilllog.State == 0).\
            group_by(func.weekofyear(OutBilllog.BeginTime)).limit(60).all()
        hasReceiverData = dict(copy.deepcopy(xAxis), **dict(hasReceiver))
        series.append({'name': u'接听量', 'data': [value for (
            key, value) in sorted(hasReceiverData.items())]})
        self.Result['rows'] = series
        self.Result['xAxis'] = sorted(xAxis.keys())
        self.finish(json.dumps(self.Result))


@urlmap(r'/callcenter/monthly')
class MonthlyReportApiHandler(BaseHandler):

    def get(self):
        st = self.get_argument('st', None)
        et = self.get_argument('et', None)
        if st is None:
            st = (datetime.now() + timedelta(days=-330)).strftime('%Y-%m-01')
        if et is None:
            et = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            et = datetime.strptime(et, '%Y-%m-%d') + \
                timedelta(days=1).strftime('%Y-%m-%d')
        series = []

        # 全部通话数量
        monthAll = self.db.query(func.left(OutBilllog.BeginTime, 7), func.count(OutBilllog.SeqId)).\
            filter(OutBilllog.BeginTime > st).filter(OutBilllog.BeginTime < et).\
            group_by(func.left(OutBilllog.BeginTime, 7)).limit(100).all()
        xAxis = dict((u'{0}'.format(k[0]), 0) for k in monthAll)
        allData = dict(copy.deepcopy(xAxis), **dict(monthAll))
        series.append({'name': u'呼叫总量', 'data': [
                      value for (key, value) in sorted(allData.items())]})
        # 未接听数量
        noReceiver = self.db.query(func.left(OutBilllog.BeginTime, 7), func.count(OutBilllog.SeqId)).\
            filter(OutBilllog.BeginTime > st).filter(OutBilllog.BeginTime < et).\
            filter(func.timediff(OutBilllog.EndTime, OutBilllog.BeginTime) == 46).\
            filter(OutBilllog.State > 0).\
            group_by(func.left(OutBilllog.BeginTime, 7)).limit(100).all()
        noReceiverData = dict(copy.deepcopy(xAxis), **dict(noReceiver))
        series.append({'name': u'未接听量', 'data': [value for (
            key, value) in sorted(noReceiverData.items())]})
        # 接听数量
        hasReceiver = self.db.query(func.left(OutBilllog.BeginTime, 7), func.count(OutBilllog.SeqId)).\
            filter(OutBilllog.BeginTime > st).filter(OutBilllog.BeginTime < et).\
            filter(OutBilllog.State == 0).\
            group_by(func.left(OutBilllog.BeginTime, 7)).limit(100).all()
        hasReceiverData = dict(copy.deepcopy(xAxis), **dict(hasReceiver))
        series.append({'name': u'接听量', 'data': [value for (
            key, value) in sorted(hasReceiverData.items())]})
        self.Result['rows'] = series
        self.Result['xAxis'] = sorted(xAxis.keys())
        self.finish(json.dumps(self.Result))


@urlmap('/callcenter/BaseHandler')
class CompareGraphHandler(BaseHandler):

    def get(self):
        series = []
        percentSeries = []
        # 全部呼出记录
        allRecord = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(1)).\
            join(FreeOprno, FreeOprno.Oprno == OutBilllog.AgentOprno).filter(func.left(FreeOprno.ShowCaller, 3) == '105').\
            filter(OutBilllog.BeginTime >
                   '2016-03-14').group_by(func.weekofyear(OutBilllog.BeginTime)).limit(100).all()
        xAxis = dict((k[0], 0) for k in allRecord)
        allData = dict(copy.deepcopy(xAxis), **dict(allRecord))
        allDataValues = [value for (key, value) in sorted(allData.items())]

        companyRecord = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(1)).\
            filter(OutBilllog.BeginTime > '2016-03-14').group_by(
                func.weekofyear(OutBilllog.BeginTime)).limit(100).all()
        companyData = dict(copy.deepcopy(xAxis), **dict(companyRecord))
        companyValues = [value for (key, value) in sorted(companyData.items())]

        # 未接听量
        noReceiver = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(1)).\
            join(FreeOprno, FreeOprno.Oprno == OutBilllog.AgentOprno).filter(func.left(FreeOprno.ShowCaller, 3) == '105').\
            filter(OutBilllog.BeginTime >
                   '2016-03-14').filter(func.timediff(OutBilllog.EndTime, OutBilllog.BeginTime) == 46).\
            filter(OutBilllog.State > 0).group_by(
                func.weekofyear(OutBilllog.BeginTime)).limit(100).all()
        noReceiverData = dict(copy.deepcopy(xAxis), **dict(noReceiver))
        noReceiverDataValues = [value for (
            key, value) in sorted(noReceiverData.items())]
        series.append({'name': u'测试组未接听量', 'data': noReceiverDataValues})
        percentSeries.append({'name': u'测试组未接听量占比', 'data': np.around(np.divide(
            np.array(noReceiverDataValues), np.array(allDataValues, dtype=float)).tolist(), decimals=3).tolist()})
        # 全公司呼出未接听量
        noReceiver = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(1)).\
            filter(OutBilllog.BeginTime >
                   '2016-03-14').filter(func.timediff(OutBilllog.EndTime, OutBilllog.BeginTime) == 46).\
            filter(OutBilllog.State > 0).group_by(
                func.weekofyear(OutBilllog.BeginTime)).limit(100).all()
        noReceiverData = dict(copy.deepcopy(xAxis), **dict(noReceiver))
        noReceiverDataValues = [value for (
            key, value) in sorted(noReceiverData.items())]
        series.append({'name': u'公司未接听量', 'data': noReceiverDataValues})
        percentSeries.append({'name': u'公司未接听量占比', 'data': np.around(np.divide(
            np.array(noReceiverDataValues), np.array(companyValues, dtype=float)).tolist(), decimals=3).tolist()})

        # 接听量
        hasReceiver = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(1)).\
            join(FreeOprno, FreeOprno.Oprno == OutBilllog.AgentOprno).filter(func.left(FreeOprno.ShowCaller, 3) == '105').\
            filter(OutBilllog.BeginTime > '2016-03-14').\
            filter(OutBilllog.ConnectTime != None).group_by(
                func.weekofyear(OutBilllog.BeginTime)).limit(100).all()
        hasReceiverData = dict(copy.deepcopy(xAxis), **dict(hasReceiver))
        hasReceiverDataValues = [value for (
            key, value) in sorted(hasReceiverData.items())]
        series.append({'name': u'测试组接听量', 'data': hasReceiverDataValues})
        percentSeries.append({'name': u'测试组接听量占比', 'data': np.around(np.divide(
            np.array(hasReceiverDataValues), np.array(allDataValues, dtype=float)).tolist(), decimals=3).tolist()})
        # 公司接听量
        hasReceiver = self.db.query(func.weekofyear(OutBilllog.BeginTime), func.count(1)).\
            filter(OutBilllog.BeginTime > '2016-03-14').\
            filter(OutBilllog.ConnectTime != None).group_by(
                func.weekofyear(OutBilllog.BeginTime)).limit(100).all()
        hasReceiverData = dict(copy.deepcopy(xAxis), **dict(hasReceiver))
        hasReceiverDataValues = [value for (
            key, value) in sorted(hasReceiverData.items())]
        series.append({'name': u'公司接听量', 'data': hasReceiverDataValues})
        percentSeries.append({'name': u'公司接听量占比', 'data': np.around(np.divide(
            np.array(hasReceiverDataValues), np.array(companyValues, dtype=float)).tolist(), decimals=3).tolist()})

        series.append({'name': u'测试组呼叫总量', 'data': allDataValues})
        series.append({'name': u'公司呼叫总量', 'data': companyValues})

        self.Result['rows'] = series
        self.Result['percentRows'] = percentSeries
        self.Result['xAxis'] = sorted(xAxis.keys())
        self.finish(json.dumps(self.Result))
