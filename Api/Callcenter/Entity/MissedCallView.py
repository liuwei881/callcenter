#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel

class MissedCallView(BaseModel):
    """
    查询视图
    """
    __tablename__ = 'missed_calls_view'

    Id = Column('id', Integer,primary_key=True)
    Caller = Column('CALLER', String(20))
    Called = Column('CALLED', String(20))
    BeginTime = Column('BEGINTIME', DateTime)
    AgentOprno = Column('AGENTOPRNO', String(5))
    Wtype = Column('WTYPE',String(3))


    def toDict(self):
        return {
            'Id': self.Id,
            'Caller':self.Caller,
            'Called': self.Called,
            'BeginTime': self.BeginTime.strftime('%Y-%m-%d %H:%M:%S') if self.BeginTime else '',
            'AgentOprno': self.AgentOprno,
            'Wtype': {"DL":"队列","ZX":"坐席","IVR":"IVR"}.get(self.Wtype,None)


        }
