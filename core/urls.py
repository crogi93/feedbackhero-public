from django.urls import path

from core.views import *

urlpatterns = [
    path('boards', BoardListView.as_view()),
    path('boards/<int:id>', BoardDetailView.as_view()),
    path('status', StatusListView.as_view()),
    path('status/<int:id>', StatusDetailView.as_view()),
    path('suggestions', SuggestionListView.as_view()),
    path('suggestions/<int:id>', SuggestionDetailView.as_view()),
    path('suggestions/<int:id>/comments', CommentListView.as_view()),
    path('suggestions/<int:id>/comments/<int:cid>', CommentDetailView.as_view()),
    path('suggestions/<int:id>/votes', VoteListView.as_view()),
    path('suggestions/<int:id>/votes/<int:cid>', VoteDetailView.as_view()),
]
