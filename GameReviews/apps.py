from django.apps import AppConfig
import os

# class MainappConfig(AppConfig):
#     name = 'mainapp'

#     def ready(self):
#         from . import jobs

#         if os.environ.get('RUN_MAIN', None) != 'true':
#             jobs.start_scheduler()

class SubscribeConfig(AppConfig):
    name = 'subscribe'
    
    def ready(self):
        from . import jobs

        if os.environ.get('RUN_MAIN', None) != 'true':
            jobs.start_scheduler()
