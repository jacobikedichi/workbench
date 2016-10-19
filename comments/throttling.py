import time, models, datetime, pytz

from rest_framework import throttling

FIVE_MINUTES = 60*2
ONE_MINUTE = 60
    
class CommentCreateRateThrottle(throttling.ScopedRateThrottle):
    scope = 'create_comment'
    
    def __init__(self, *args, **kwargs):
        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)
        self.one_min_block = None
        self.five_min_block = None
        super(CommentCreateRateThrottle, self).__init__(*args, **kwargs)

    def allow_request(self, request, view):        
        self.scope = getattr(view, self.scope_attr, None)
        if not self.scope:
            return True   
        if self.rate is None:
            return True
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True
        self.history = self.cache.get(self.key, [])
        self.now = time.time()
        if request.method != 'POST':
            #We are only concerned with comment CREATion (POST)
            return True
        self.five_min_block = self.cache.get(self.get_five_min_block_key(request, view))
        if self.five_min_block:
            if self.now < self.five_min_block + (FIVE_MINUTES): 
                #This block of code should always execute, assuming our cache expiration works as expected 
                print "Blocked for 5 minutes"
                return False #They are on a five minute block
            else:
                #this should not really happen. Just being extra cautious.
                self.cache.delete(self.get_five_min_block_key(request, view))
        
        self.one_min_block = self.cache.get(self.get_one_min_block_key(request, view))
        if self.one_min_block:
            if self.now < self.one_min_block + (ONE_MINUTE):
                #This block of code should always execute if self.one_min_block is not None. Assuming cache
                #expiration is working as expected
                print "Blocked for 1 minute"
                return False #They are on a one minute block
            else:
                #this should not really happen. Just being extra cautious.
                self.cache.delete(self.get_one_min_block_key(request, view))
        # Drop any requests from the history which have now passed the throttle duration)
        while self.history and self.history[-1] <= self.now - self.duration:
            print str(self.now - self.history[-1]) + " apart. Deleting..."
            self.history.pop()
        
        if len(self.history) >= self.num_requests:
            print "Initial block for 5 minutes"
            self.cache.set(self.get_five_min_block_key(request, view), self.now, FIVE_MINUTES) #block for 5 minutes
            #Used for calculating wait/retry time
            self.five_min_block = self.cache.get(self.get_five_min_block_key(request, view))
            return False #They've maxed their allowed comments create rate
        request_data = request.data
        comment = request.data.get('comment')
        if comment:
            comment_obj = models.Comment.objects.filter(comment=comment).order_by('-date_created')
            if comment_obj.exists():
                date_created = comment_obj[0].date_created
                if date_created + datetime.timedelta(hours=24) > pytz.utc.localize(datetime.datetime.now()):
                    self.cache.set(self.get_one_min_block_key(request, view), self.now, ONE_MINUTE) #block for one minute
                    print "Initial block for 1 minute"
                    #Used for calculating wait/retry time
                    self.one_min_block = self.cache.get(self.get_one_min_block_key(request, view))
                    return False
            else:
                self.history.insert(0, self.now)
                self.cache.set(self.key, self.history, FIVE_MINUTES) #cache for 5 minutes
                return True
        return None
    
    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        five_min_retry = None
        one_min_retry = None
        if self.five_min_block is not None:
            five_min_retry = FIVE_MINUTES - (self.now - self.five_min_block)
        if self.one_min_block is not None:
            one_min_retry = ONE_MINUTE - (self.now - self.one_min_block)
        return max(one_min_retry, five_min_retry)
    
    def get_five_min_block_key(self, request, view):
        """
        returns cache key for five minute block (IP based)
        """
        return self.get_cache_key(request, view) + "_block_five_min"
    
    def get_one_min_block_key(self, request, view):
        """
        returns cache key for one minute block (IP based)
        """
        return self.get_cache_key(request, view) + "_block_one_min"
    
    def get_cache_key(self, request, view):
        """
        returns cache key (IP based)
        """
        ip_address = request.data.get('ip_address')
        return self.cache_format % {
            'scope': self.scope,
            'ident': ip_address or self.get_ident(request)
        }