from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone="Asia/Bangkok")


@sched.scheduled_job('cron', hour=16, minute=30)
def scheduled_job():
    print('This job is run every day at 16pm 30.')

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

sched.start()