from daemon import Daemon
from db_executor import init_base
from queue import Queue


events = Queue(maxsize=16)
connection, tablenames = init_base("DB.db")
threads = []


def out():
    print(events.queue)


def stop():
    if not threads:
        return

    for thread in threads:
        thread.stop()


def main():
    while 1:
        keyword = input("enter keyword->")
        if keyword:
            break

    for tablename in tablenames:
        print(tablename['name'].lower())
        thread = Daemon(connection, tablename['name'].lower(), events)
        thread.init_keyword(keyword)
        thread.start()


def interface():
    while 1:
        print("1. start\n2.stop\n3. show")
        cmd = input(">")
        if cmd and cmd == "1":
            main()
        if cmd and cmd == "2":
            stop()
        if cmd and cmd == "3":
            out()


if __name__ == "__main__":
    interface()