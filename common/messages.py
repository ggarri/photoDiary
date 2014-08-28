import simplejson

class MessageGlobal():
	_001 = "Incorrect request type"

class MessageVO():
	def __init__(self, _type=False, msg=None, exception=None):
		self.type = _type
		if msg != None:
			self.description = msg
		elif exception != None:
			if exception.__class__ in dict.__subclasses__():
				self.description = exception

	def getJSON(self):
		return simplejson.dumps({"type" : self.type, "description": self.description })
