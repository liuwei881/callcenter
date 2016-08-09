#coding=utf-8

from lib.urlmap import urlmap
from lib.Route import db_session
from lib.basehandler import BaseHandler
from tornado import web,gen
from Callcenter.Entity.FreeSoftphone import SoftPhone
from Callcenter.Entity.FreeOprno import FreeOprno
from Callcenter.Entity.CcsOprno import CcsOprno
import json
from sqlalchemy import desc,or_,and_,engine


#坐席
@urlmap(r'/softphone\/?([0-9]*)')
class SoftPhoneHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        page = int(self.get_argument('page', 1))
        searchKey = self.get_argument('searchKey', None)
        pagesize = int(self.get_argument('pagesize', self._PageSize))
        totalquery = self.db.query(SoftPhone.Id)
        SoftPhoneObj = self.db.query(SoftPhone)
        if searchKey:
            totalquery = totalquery.filter(SoftPhone.Phone==searchKey)
            SoftPhoneObj = SoftPhoneObj.filter(SoftPhone.Phone==searchKey)
        self.Result['total'] = totalquery.count()
        serverTask = SoftPhoneObj.order_by(desc(SoftPhone.Id)).limit(pagesize).offset((page - 1) * pagesize).all()
        self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)

    @web.asynchronous
    def post(self,ident=0):
        data = json.loads(self.request.body)
        Phone = data['params'].get('Phone', None)
        Phone1 = data['params'].get('Phone1',None)
        if Phone < Phone1:
            for i in xrange(int(Phone),int(Phone1)+1):
                softphone = SoftPhone(Phone = str(i),UserName=str(i),PassWord="ceshi",GroupId=100,State=1)
                self.db.add(softphone)
                self.db.commit()
            self.db.execute("call Make_Account_Cursor()")
            self.db.commit()
        else:
            self.write(json.dumps("范围从小到大排序"))
        self.Result['info'] = u'创建软电话成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self,ident):
        phone = self.db.query(SoftPhone).filter(SoftPhone.Id==ident).first().Phone
        self.db.query(FreeOprno).filter(FreeOprno.Oprno==phone).delete()
        self.db.query(CcsOprno).filter(CcsOprno.Oprno==phone).delete()
        self.db.query(SoftPhone).filter(SoftPhone.Id == ident).delete()
        self.db.commit()
        self.Result['info'] = u'删除软电话成功'
        self.finish(self.Result)