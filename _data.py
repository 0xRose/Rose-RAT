import sqlite3


class DatabaseX():

    def __init__(self):
        self.conn = sqlite3.connect('sessions.db')
        self.c = self.conn.cursor()

    def get_webhook(self, sid):
        self.c.execute("SELECT webhook FROM ses WHERE sid=?", (sid, ))
        return self.c.fetchone()[0]

    def get_ip(self, sid):
        self.c.execute("SELECT ip FROM ses WHERE sid=?", (sid, ))
        return self.c.fetchone()[0]

    def enter_values(self, sid, ip, username, server, webhook, avatar, footer):
        self.c.execute("INSERT INTO ses VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (sid, ip, username, server, webhook, avatar, footer))
        self.conn.commit()
        return

    def get_all(self, sid):
        self.c.execute("SELECT * FROM ses WHERE sid=?", (sid, ))
        return self.c.fetchone()

    def delete_sid(self, sid):
        self.c.execute("DELETE FROM ses WHERE sid=?", (sid, ))
        self.conn.commit()
        return
    
    def get_sessions(self):
        self.c.execute("SELECT * FROM ses")
        return len(self.c.fetchall())


db = DatabaseX()