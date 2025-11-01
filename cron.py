import schedule
import time
import main1 as m


def job():
    m.mainFunction()


schedule.every().day.at("7:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
