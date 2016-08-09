#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,CallCenterMasterModel

class FreeOprno(BaseModel,CallCenterMasterModel):
    """
    坐席列表
    """
    __tablename__ = 'freecti_oprno'

    Id = Column('ID', Integer, primary_key=True)
    DepId = Column('DEPID', Integer)
    Oprno = Column('OPRNO', String(10))
    OrderId = Column('ORDERID', Integer)
    SysTime = Column('SYSTIME', DateTime)
    ShowCaller = Column('SHOWCALLER', String(22))
    Sipphone = Column('SIPPHONE', String(20))
    Sipphonepwd = Column('SIPPHONEPWD', String(20))
    State = Column('STATE', Integer)

    def toDict(self):
        return {
            'Id': self.Id,
            'DepId':self.DepId,
            'Oprno': self.Oprno,
            'OrderId': self.OrderId,
            'SysTime': self.SysTime.strftime('%Y-%m-%d %H:%M:%S') if self.SysTime else '',
            'ShowCaller': self.ShowCaller,
            'Sipphone': self.Sipphone,
            'Sipphonepwd': self.Sipphonepwd,
            'State':self.State

        }
