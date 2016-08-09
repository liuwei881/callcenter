#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,FreectiMasterModel
from lib.Kit import Kit

class CcsOprno(BaseModel,FreectiMasterModel):
    """
    坐席列表
    """
    __tablename__ = 'ccs_oprno'

    Id = Column('id', Integer, primary_key=True)                 #坐席ID
    BindAccount = Column('bind_account', Integer)                #
    BindTeam = Column('bind_team', Integer)                      #
    Oprno = Column('oprno', String(10))                          #
    OrderId = Column('orderid', Integer)                         #
    ShowCaller = Column('showcaller', String(22))                #电话
    Sipphone = Column('sipphone', String(20))                    #Email
    Sipphonepwd = Column('sipphonepwd', String(20))              #
    Status = Column('status', Integer)                           #状态
    Fee = Column('fee', Integer)                                 #费用
    Is_settle = Column('is_settle', Integer)                     #
    Ctime = Column('ctime', Integer)                 #

    def toDict(self):
        return {
            'Id': self.Id,
            'BindAccount': self.BindAccount,
            'BindTeam': Kit.getCustomerLinkOprnoById(self.BindTeam),
            'Oprno': self.Oprno,
            'OrderId': self.OrderId,
            'ShowCaller': self.ShowCaller,
            'Sipphone': self.Sipphone,
            'Sipphonepwd': self.Sipphonepwd,
            'Status': self.Status,
            'Fee': self.Fee,
            'Is_settle': self.Is_settle,
            'Ctime':self.Ctime
        }
