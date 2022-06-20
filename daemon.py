from threading import Thread
from pymorphy2 import MorphAnalyzer
import winsound


morph = MorphAnalyzer()


def find_keyword(sequence, keyword):
    sequence = str(sequence)
    try:
        for word in sequence.lower().split():
            if morph.normal_forms(word)[0] == keyword.lower():
                return True
    except:
        return False


class Daemon(Thread):
    def __init__(self, connection, tablename, event_pool):
        Thread.__init__(self)
        self.connection = connection
        self.tablename = tablename
        self.keyword = None
        self.event_back = event_pool
        self.flag = True

    def init_keyword(self, keyword: str):
        self.keyword = keyword

    def stop(self):
        self.flag = False

    def run(self):
        cursor = self.connection.cursor()
        if not self.keyword:
            return
        while self.flag:
            for row in cursor.execute(f"SELECT * FROM {self.tablename}").fetchall():
                for attribute in row.keys():
                    result = find_keyword(row[attribute], self.keyword)
                    if result:
                        data = (self.tablename, attribute, row[attribute])
                        #  print(data)
                        if data not in self.event_back.queue:
                            self.event_back.put(data)
                            duration = 1000  # milliseconds
                            freq = 440  # Hz
                            winsound.Beep(freq, duration)
