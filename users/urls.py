from django.urls import path

from users.views import *

urlpatterns = [
    path("board/<int:id>", SuggestionListView.as_view(), name="suggestionslistview"),
    path(
        "board/<int:id>/suggestions",
        SuggestionCreateView.as_view(),
        name="suggestionscreateview",
    ),
    path(
        "board/<int:bid>/suggestions/<int:id>",
        SuggestionDetailView.as_view(),
        name="suggestionsdetailview",
    ),
    path(
        "board/<int:bid>/suggestion/<int:id>/votes",
        voteup_suggestion,
        name="voteupsuggestion",
    ),
]
