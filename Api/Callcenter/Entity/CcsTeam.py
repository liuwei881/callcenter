#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime,Date
from lib.Route import BaseModel,FreectiMasterModel

class CcsTeam(BaseModel,FreectiMasterModel):
    """
    坐席组
    """
    __tablename__ = 'ccs_team'

    Id = Column('id', Integer, primary_key=True)                 #坐席ID
    Name = Column('name', String(100))
    BindAccount = Column('bind_account', Integer)                #
    TimeId = Column('timeid', Integer)                           #
    Isrecord = Column('isrecord', Integer)                        #
    RecordPath = Column('recordpath', String(255))                         #登录IP
    AgentCount = Column('agentcount', Integer)
    ShowcallerTag = Column('showcallertag', Integer)
    ShowCaller = Column('showcaller', String(22))
    AudioCode = Column('audiocode', Integer)
    BlackTag = Column('blacktag', Integer)
    BillTag = Column('billtag', Integer)
    FeeType = Column('feetype', Integer)
    CallRule = Column('callrule', Integer)
    PlayOprno = Column('playoprno', Integer)
    PlayQueue = Column('playqueue', Integer)
    Memo = Column('memo', String(50))
    Ctime = Column('ctime', Integer)
    ServerIp = Column('server_ip', Integer)

    def toDict(self):
        return {
            'Id': self.Id,
            'Name': self.Name,
            'BindAccount': self.BindAccount,
            'TimeId': self.TimeId,
            'Isrecord': self.Isrecord,
            'RecordPath': self.RecordPath,
            'AgentCount': self.AgentCount,
            'ShowcallerTag': self.ShowcallerTag,
            'ShowCaller': self.ShowCaller,
            'AudioCode': self.AudioCode,
            'BlackTag': self.BlackTag,
            'BillTag': self.BillTag,
            'FeeType': self.FeeType,
            'CallRule': self.CallRule,
            'PlayOprno': self.PlayOprno,
            'PlayQueue': self.PlayQueue,
            'Memo': self.Memo,
            'Ctime': self.Ctime,
            'ServerIp': self.ServerIp
        }