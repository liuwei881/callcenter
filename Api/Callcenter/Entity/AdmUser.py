#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel,FreectiMasterModel

class AdmUser(BaseModel,FreectiMasterModel):
    """
    用户列表
    """
    __tablename__ = 'adm_user'

    Id = Column('id', Integer, primary_key=True)                 #用户ID
    Account = Column('account', String(64))                      #用户账户
    NickName = Column('nickname',String(50))                     #用户别名
    PassWord = Column('password', String(32))                    #用户密码
    BindAccount = Column('bind_account', Integer)                #
    BindPartner = Column('bind_partner', Integer)                #
    BindOprno = Column('bind_oprno', Integer)                    #
    BindBranch = Column('bind_branch', Integer)                  #
    LastLogin = Column('last_login_time', DateTime)                   #
    LastIp = Column('last_login_ip', String(40))                            #登录IP
    TelePhone = Column('tel', String(20))                  #电话
    Email = Column('email', String(50))                          #Email
    Remark = Column('remark', String(255))                       #
    CreateTime = Column('create_time', DateTime)                 #创建时间
    UpdateTime = Column('update_time', DateTime)                 #修改时间
    Status = Column('status', Integer)                           #
    Level = Column('level', Integer)                             #
    Rank = Column('rank', Integer)                               #
    Offline = Column('offline', Integer)                         #
    Info = Column('info', Text)                                  #
    LoginCount = Column('login_count', Text)

    def toDict(self):
        return {
            'Id': self.Id,
            'Account':self.Account,
            'NickName':self.NickName,
            'PassWord': self.PassWord,
            'BindAccount': self.BindAccount,
            'BindPartner': self.BindPartner,
            'BindOprno': self.BindOprno,
            'BindBranch': self.BindBranch,
            'LastLogin': self.LastLogin,
            'LastIp': self.LastIp,
            'TelePhone': self.TelePhone,
            'Email': self.Email,
            'Remark': self.Remark,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else '',
            'UpdateTime': self.UpdateTime.strftime('%Y-%m-%d %H:%M:%S') if self.UpdateTime else '',
            'Status':self.Status,
            'Level':self.Level,
            'Rank': self.Rank,
            'Offline': self.Offline,
            'Info': self.Info,
            'LoginCount':self.LoginCount
        }
