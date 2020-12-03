import mysql.connector

class DatabaseConnection:
    def __init__(self, dbConfig: dict):
        self.config = dbConfig
        self.connection = mysql.connector.connect(
            host = self.config['host'],
            user = self.config['user'],
            database = self.config['database'],
            password =self.config['password']
        )
        self.cursor = self.connection.cursor(prepared = True)
    
    def executeQuery(self, query, params = None):
        if not params : self.cursor.execute(query)
        else : self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        self.connection.commit()
        columnNames = [col[0] for col in self.cursor.description]
        return (result, columnNames)
    
    def kill(self):
        self.connection.close()