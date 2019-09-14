from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', second=1)
def timed_job():
    print('cron This job is run every three minutes.')

@sched.scheduled_job('cron', hour=16)
def scheduled_job():
    print('This job is run every weekday at 4pm.')

sched.start()