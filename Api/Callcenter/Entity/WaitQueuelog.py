#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,CallCenterSlaveModel

class WaitQueuelog(BaseModel,CallCenterSlaveModel):
    """
    等待队列
    """
    __tablename__ = 'freecti_waitqueue_log'

    SeqId = Column('SEQID', Integer, primary_key=True)
    BillId = Column('BILLID', String(21))
    Caller = Column('CALLER', String(20))
    Called = Column('CALLED', String(20))
    BeginTime = Column('BEGINTIME', DateTime)
    EndTime = Column('ENDTIME', DateTime)
    State = Column('STATE', Integer)
    Revisit = Column('REVISIT', Integer)

    def toDict(self):
        return {
            'SeqId': self.SeqId,
            'BillId':self.BillId,
            'Caller': self.Caller,
            'Called': self.Called,
            'BeginTime': self.BeginTime.strftime('%Y-%m-%d %H:%M:%S') if self.BeginTime else '',
            'EndTime': self.EndTime.strftime('%Y-%m-%d %H:%M:%S') if self.EndTime else '',
            'State': self.State,
            'Revisit': self.Revisit
        }
