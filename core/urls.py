from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import *

urlpatterns = [
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
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
        "boards/<int:bid>/suggestions/<int:id>/comments",
        CommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "boards/<int:bid>/suggestions/<int:id>/comments/<int:cid>",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
    path(
        "boards/<int:bid>/suggestions/<int:id>/votes",
        VoteListView.as_view(),
        name="vote-list",
    ),
    path(
        "boards/<int:bid>/suggestions/<int:id>/votes/<int:cid>",
        VoteDetailView.as_view(),
        name="vote-detail",
    ),
]
