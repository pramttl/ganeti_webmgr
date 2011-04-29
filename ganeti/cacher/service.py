from twisted.application.service import Service
from twisted.internet.defer import DeferredList
from twisted.internet.task import LoopingCall

from django.conf import settings

from ganeti.cacher.node import NodeCacheUpdater


class CacheService(Service):

    def __init__(self, *args, **kwargs):
        self.call = None
        self.node_updater = NodeCacheUpdater()

        #self.vm_updater = VirtualMachineCacheUpdater()
    
    def update_cache(self):
        """ a single run of all update classes """
        return DeferredList([self.node_updater.update_cache(),
                            #self.vm_updater.update_cache()
                            #
                            ])
    
    def startService(self):
        self.call = LoopingCall(self.update_cache)
        self.call.start(settings.PERIODIC_CACHE_REFRESH)
    
    def stopService(self):
        if self.call is not None:
            self.call.stop()
