from django.urls import path

from frontend.views import *

urlpatterns = [
    path("board", SuggestionListView.as_view(), name="suggestionslistview"),
    path(
        "board/suggestions",
        SuggestionCreateView.as_view(),
        name="suggestionscreateview",
    ),
    path(
        "board/suggestions/<int:id>",
        SuggestionDetailView.as_view(),
        name="suggestionsdetailview",
    ),
    path("board/suggestion/<int:id>/votes", voteup_suggestion, name="voteupsuggestion"),
]
