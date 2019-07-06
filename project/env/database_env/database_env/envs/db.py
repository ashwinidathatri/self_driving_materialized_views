from pyhive import hive

class Database():
	def __init__(self):
		self.cursor = self.get_cursor_for_hivedb()
		self.cursor.execute('USE dbse')

	def get_cursor_for_hivedb(self):
		cursor = hive.connect(host='localhost', port=10000).cursor()
		return cursor

	def execute_query(self, query):
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def explain_analyze_query(self, query):
		explain_query = 'EXPLAIN ' + query
		self.cursor.execute(explain_query)
		return self.cursor.fetchall()

	def get_table_names_from_hive(self):
		self.cursor.execute('SHOW TABLES')
		return self.cursor.fetchall()