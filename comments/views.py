import models, serializers, throttling
from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class CommentList(generics.ListCreateAPIView):
    """
    Responsible for comment lists. Listing all comments or creating a new one
    """
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    throttle_scope = 'create_comment' #Applies CommentCreateRateThrottle to this view (For CREATE purposes)
    
    def get_queryset(self):
        comment_qs = models.Comment.objects.all()
        content_url = self.kwargs.get('content_url')
        if content_url:
            comment_qs = comment_qs.filter(content_url__url=content_url)
        return comment_qs
    
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Responsible for individual comments
    """
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
