#coding=utf-8

from lib.Route import db_session
from lib.RedisCache import RedisCache


class Kit(object):
	@classmethod
	def getCustomerLinkOprnoById(cls, ident):
		if ident:
			if RedisCache.hexists('Cache:CallCenter.BindTeam', ident):
				return RedisCache.hget('Cache:CallCenter.BindTeam', ident)
			else:
				result = db_session.execute("select name from ccs_team where id={0}".format(ident)).fetchone()
				db_session.close_all()
				if result:
					RedisCache.hset('Cache:CallCenter.BindTeam', ident, result[0])
					return result[0]
				else:
					RedisCache.hset('Cache:CallCenter.BindTeam', ident, '')
					return ''