#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime,Date
from lib.Route import BaseModel,CallCenterSlaveModel

class CellPhone(BaseModel,CallCenterSlaveModel):
    """
    呼入手机搜索
    """
    __tablename__ = 'freecti_ivrcall_billlog'

    SeqId = Column('SEQID', Integer, primary_key=True)
    Caller = Column('CALLER', String(10))
    Called = Column('CALLED', String(10))
    BeginTime = Column('BEGINTIME', DateTime)
    EndTime = Column('ENDTIME', DateTime)
    RecordFile = Column('RECORDFILE', String(80))

    def toDict(self):
        return {
            'Caller': self.Caller,
            'Called': self.Called,
            'BeginTime': self.BeginTime.strftime('%Y-%m-%d %H:%M:%S') if self.BeginTime else '',
            'EndTime': self.EndTime.strftime('%Y-%m-%d %H:%M:%S') if self.EndTime else '',
            'RecordFile': self.RecordFile
        }
