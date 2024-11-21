class NoDataFoundError(Exception):
	"""Exception raised when no data is found in the database."""
	def __init__(self, message="No data found in the database."):
		super().__init__(message)