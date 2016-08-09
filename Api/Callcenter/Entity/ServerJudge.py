#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime,Date
from lib.Route import BaseModel,CallCenterSlaveModel
from lib.Kit import Kit

class ServerJudge(BaseModel,CallCenterSlaveModel):
    """
    评价表
    """
    __tablename__ = 'freecti_serverjudge'

    Id = Column('ID', Integer, primary_key=True)
    BillId = Column('BILLID', String(21))
    DepId = Column('DEPID', Integer)
    Oprno = Column('OPRNO', String(5))
    Caller = Column('CALLER', String(20))
    Called = Column('CALLED', String(20))
    SkillId = Column('SKILLID', Integer)
    SysTime = Column('SYSTIME', DateTime)
    State = Column('STATE', Integer)

    def toDict(self):
        return {
            'Id': self.Id,
            'BillId': self.BillId,
            'DepId': Kit.getCustomerLinkOprnoById(self.DepId),
            'Oprno': self.Oprno,
            'Caller': self.Caller[0:-4],
            'Called': self.Called[0:-4],
            'SkillId': self.SkillId,
            'SysTime': self.SysTime.strftime('%Y-%m-%d %H:%M:%S') if self.SysTime else '',
            'State': {1:"非常满意",2:"满意",3:"不满意"}.get(self.State,"未评价")
        }