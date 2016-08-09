#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,CallCenterSlaveModel

class IvrBilllog(BaseModel,CallCenterSlaveModel):
    """
    ivrbilllog
    """
    __tablename__ = 'freecti_ivr_billlog'

    SeqId = Column('SEQID', Integer, primary_key=True)
    BillId = Column('BILLID', String(21))
    Caller = Column('CALLER', String(20))
    Called = Column('CALLED', String(20))
    BeginTime = Column('BEGINTIME', DateTime)
    EndTime = Column('ENDTIME', DateTime)
    FromTag = Column('FROMTAG', Integer)
    ToTag = Column('TOTAG', Integer)
    TooPrno = Column('TOOPRNO', String(5))
    OrgCalled = Column('ORGCALLED', String(20))

    def toDict(self):
        return {
            'SeqId': self.SeqId,
            'BillId':self.BillId,
            'Caller': self.Caller,
            'Called': self.Called,
            'BeginTime': self.BeginTime.strftime('%Y-%m-%d %H:%M:%S') if self.BeginTime else '',
            'EndTime': self.EndTime.strftime('%Y-%m-%d %H:%M:%S') if self.EndTime else '',
            'FromTag': self.FromTag,
            'ToTag': self.ToTag,
            'TooPrno':self.TooPrno,
            'OrgCalled':self.OrgCalled

        }
