from django.urls import path

from core.views import *

urlpatterns = [
    path("boards", BoardListView.as_view(), name="board-list"),
    path("boards/<int:id>", BoardDetailView.as_view(), name="board-detail"),
    path("boards/<int:bid>/status", StatusListView.as_view(), name="status-list"),
    path(
        "boards/<int:bid>/status/<int:id>",
        StatusDetailView.as_view(),
        name="status-detail",
    ),
    path(
        "boards/<int:bid>/suggestions",
        SuggestionListView.as_view(),
        name="suggestion-list",
    ),
    path(
        "boards/<int:bid>/suggestions/<int:id>",
        SuggestionDetailView.as_view(),
        name="suggestion-detail",
    ),
    path(
        "suggestions/<int:id>/comments", CommentListView.as_view(), name="comment-list"
    ),
    path(
        "suggestions/<int:id>/comments/<int:cid>",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
    path("suggestions/<int:id>/votes", VoteListView.as_view(), name="vote-list"),
    path(
        "suggestions/<int:id>/votes/<int:cid>",
        VoteDetailView.as_view(),
        name="vote-detail",
    ),
]
