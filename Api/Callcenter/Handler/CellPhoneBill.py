#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Callcenter.Entity.CellPhone import CellPhone
import json,datetime


#呼入手机搜索
@urlmap(r'/cellphonebill')
class OutBillHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        phone = self.get_argument('cellphone', None)
        if phone is None:
            self.Result['status'] = 500
            self.Result['info'] = u'请输入分机号'
        else:
            rows = self.db.query(CellPhone). \
                filter(CellPhone.Called == phone). \
                order_by(CellPhone.BeginTime.desc()).all()
            self.Result['rows'] = map(lambda row: row.toDict(), rows)
        self.finish(json.dumps(self.Result))