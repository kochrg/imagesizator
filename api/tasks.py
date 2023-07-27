# from imagesizator.celery import app
# from api.common.functions.delete_expired_files import delete_expired_files
# from celery.schedules import crontab
# from celery import shared_task


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls to delete expired files every 30 seconds.
#     sender.add_periodic_task(30.0, test().s('hello'), name='add every 30')

# @app.task
# def test(arg):
#     print("Deleting files:", arg)
#     # delete_expired_files()
