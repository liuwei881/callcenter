#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web
from Right.Entity.DepartmentFunctionModel import DepartmentFunctionList
import json

#部门管理，二级联动
@urlmap(r'/departfunc/')
class DepartFuncHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        depart = self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.Level==1)
        depart_list = []
        for i in depart:
            d = {}
            d["id"] = i.DepartmentFunctionId
            d["name"] = i.DepartmentName
            d["code"] = i.DepartmentFunctionId
            d["child"] = []
            child = self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.Level==2,DepartmentFunctionList.Parent==i.DepartmentFunctionId)
            for c in child:
                k = {}
                childthree = self.db.query(DepartmentFunctionList).filter(DepartmentFunctionList.Level==3,DepartmentFunctionList.Parent==c.DepartmentFunctionId)
                k["child"] = []
                for j in childthree:
                    k["child"].append({"username":j.DepartmentName})
                d["child"].append({"id":c.DepartmentFunctionId,"name":c.DepartmentName,"child":k["child"]})
                depart_list.append(d)
        rows = []
        [rows.append(i) for i in depart_list if i not in rows]
        data = json.dumps(rows,indent=2)
        self.finish(data)
