from pyhive import hive

class Database():
	def __init__(self):
		self.cursor = self.get_cursor_for_hivedb()
	
	def get_cursor_for_hivedb(self):
		cursor = hive.connect(host='localhost', port=9000).cursor()
		return cursor

	def execute_query(self, query):
		return self.cursor.execute(query)

	def explain_analyze_query(self, query):
		explain_query = 'EXPLAIN ' + query
		return self.cursor.execute(explain_query)