from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone="Asia/Bangkok")


@sched.scheduled_job('cron', hour=17, minute=17)
def scheduled_job():
    print('This job is run every day at 5pm 17.')

sched.start()