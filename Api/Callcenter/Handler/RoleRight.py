#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Right.Entity.RoleModel import RoleList
from Right.Entity.RoleRightModel import RoleRightList
import json


#角色权限管理
@urlmap(r'/role/member\/?([0-9]*)')
class RoleMemberHandler(BaseHandler):
    @web.asynchronous
    def get(self, ident):
        if ident:
            try:
                objServer = self.db.query(RoleRightList).filter(RoleRightList.RoleId==ident).all()
                d = {}
                d['RoleId'] = ident
                d['RoleName'] = self.db.query(RoleList).filter(RoleList.RoleId==ident).first().RoleName
                objs = [obj.toDict() for obj in objServer]
                if objs:
                    countlist = [i.get("MenuId",None) for i in objs]
                    c = {}
                    for i in countlist:
                        c[i] = {}
                        menu = self.db.query(RoleRightList).filter(RoleRightList.MenuId==i,RoleRightList.RoleId==ident).first()
                        menupost = menu.MenuPost
                        menuget = menu.MenuGet
                        menuput = menu.MenuPut
                        menudel = menu.MenuDel
                        if menupost:
                            c[i][menupost] = True
                        if menuget:
                            c[i][menuget] = True
                        if menuput:
                            c[i][menuput] = True
                        if menudel:
                            c[i][menudel] = True
                    objs[0]["MenuId"] = c
                    objs[0].update(d)
                else:
                    objs.append(d)
                self.Result['rows'] = objs[0]
            except Exception,e:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found,{0}'.format(e)
        else:
            totalquery = self.db.query(RoleRightList.MenuId)
            memberlistObj = self.db.query(RoleRightList)
            self.Result['total'] = totalquery.count()
            self.Result['rows'] = map(lambda obj: obj.toDict(), memberlistObj)
        self.finish(self.Result)

    @web.asynchronous
    def post(self,ident=0):
        data = json.loads(self.request.body)
        self.db.query(RoleRightList).filter(RoleRightList.RoleId==ident).delete()
        self.db.commit()
        menudict = data['params'].get('MenuId',None)
        if menudict:
            for k, v in menudict.iteritems():
                if menudict[k].get('post',False):
                    MenuPost = 'post'
                else:
                    MenuPost = ''
                if menudict[k].get('put',False):
                    MenuPut = 'put'
                else:
                    MenuPut = ''
                if menudict[k].get('get',False):
                    MenuGet = 'get'
                else:
                    MenuGet = ''
                if menudict[k].get('delete',False):
                    MenuDel = 'delete'
                else:
                    MenuDel = ''
                pro = RoleRightList(MenuId=int(k), RoleId=ident,
                                    MenuPost=MenuPost,MenuPut=MenuPut,
                                    MenuGet=MenuGet,MenuDel=MenuDel)
                self.db.add(pro)
                self.db.query(RoleRightList).filter(RoleRightList.MenuPost=='',RoleRightList.MenuPut=='',
                                                    RoleRightList.MenuGet=='',RoleRightList.MenuDel=='').delete()
                self.db.commit()
        else:
            pass
        self.Result['rows'] = 1
        self.Result['info'] = u'修改角色成员成功'
        self.finish(self.Result)
