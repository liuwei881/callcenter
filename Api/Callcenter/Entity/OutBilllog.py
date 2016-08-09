#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime,Date
from lib.Route import BaseModel,CallCenterSlaveModel

class OutBilllog(BaseModel,CallCenterSlaveModel):
    """
    呼出录音
    """
    __tablename__ = 'freecti_out_billlog'

    SeqId = Column('SEQID', Integer, primary_key=True)
    BillId = Column('BILLID', String(20))
    DepId = Column('DEPID', Integer)
    AgentOprno = Column('AGENTOPRNO', String(10))
    AgentPhone = Column('AGENTPHONE', String(20))
    Called = Column('CALLED', String(20))
    BeginTime = Column('BEGINTIME', DateTime)
    ConnectTime = Column('CONNECTTIME', DateTime)
    EndTime = Column('ENDTIME', DateTime)
    State = Column('STATE', Integer)
    AudioCode = Column('AUDIOCODE', Integer)
    RecordFile = Column('RECORDFILE', String(64))

    def toDict(self):
        return {
            'SeqId': self.SeqId,
            'BillId': self.BillId,
            'DepId': self.DepId,
            'AgentOprno': self.AgentOprno,
            'AgentPhone': self.AgentPhone,
            'Called': self.Called[0:-4],
            'BeginTime': self.BeginTime.strftime('%Y-%m-%d %H:%M:%S') if self.BeginTime else '',
            'ConnectTime': self.ConnectTime.strftime('%Y-%m-%d %H:%M:%S') if self.ConnectTime else '',
            'EndTime': self.EndTime.strftime('%Y-%m-%d %H:%M:%S') if self.EndTime else '',
            'AudioCode': self.AudioCode,
            'State': self.State,
            'RecordFile': self.RecordFile
        }