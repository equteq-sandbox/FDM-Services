class User:
	"""docstring for User"""
	def __init__(self, user_name,first_name,last_name,email,phone_number):
		#super(ClassName, self).__init__()
		# self.user_id = user_id
		self.user_name = user_name
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.phone_number = phone_number
        # self.validated = validated
        
        # self.isValidated = validated
	def setUser(self, user_name,first_name,last_name,email,phone_number):
		# self.user_id = user_id
		self.user_name = user_name
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.phone_number = phone_number
	def setUserName(self):
		self.user_name = user_name