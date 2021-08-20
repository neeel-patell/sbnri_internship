from scrapper import Scrapper
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=1) # will executed after an hour
def main():
    call_me()

def call_me():
    # sample function which have block of code
    print("Executing . . . ")
    scrap = Scrapper()
    # object created and refresh() method called to refresh the content in database from webpage
    scrap.refresh()
    print("Executed . . . ")
    
if __name__ == '__main__':
    call_me() # called first time for when executed directly from command prompt after that will executed after 1 hour 
    sched.start()
