#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime,Date
from lib.Route import BaseModel,CallCenterMasterModel

class SoftPhone(BaseModel,CallCenterMasterModel):
    """
    软电话
    """
    __tablename__ = 'freess_softphone'

    Id = Column('ID', Integer, primary_key=True)                 #软电话ID
    Phone = Column('PHONE', String(20))                          #电话
    UserName = Column('USERNAME', String(20))                    #用户名
    PassWord = Column('PASSWRD', String(20))                    #
    InternetIp = Column('INTERNETIP', String(20))                #
    InternetPort = Column('INTERNETPORT', Integer)               #
    EthernetIp = Column('ETHERNETIP', String(20))                #
    EthernetPort = Column('ETHERNETPORT', Integer)               #
    Expires = Column('EXPIRES', Integer)                         #
    LastTime = Column('LASTTIME', DateTime)                      #
    LastTimet = Column('LASTTIMET', Integer)                     #
    GroupId = Column('GROUPID', Integer)                         #
    State = Column('STATE', Integer)                             #
    Remark = Column('REMARK', String(20))                        #

    def toDict(self):
        return {
            'Id': self.Id,
            'Phone': self.Phone,
            'UserName': self.UserName,
            'PassWord': self.PassWord,
            'InternetIp': self.InternetIp,
            'InternetPort': self.InternetPort,
            'EthernetIp': self.EthernetIp,
            'EthernetPort': self.EthernetPort,
            'Expires': self.Expires,
            'LastTime': self.LastTime.strftime('%Y-%m-%d %H:%M:%S') if self.LastTime else '',
            'LastTimet': self.LastTimet,
            'GroupId': self.GroupId,
            'State': self.State,
            'Remark': self.Remark
        }