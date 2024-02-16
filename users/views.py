from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.base import View

from core.serializers import *
from core.models import *

from users.filters import *


class SuggestionListView(View):
    template_name = "users/suggestion_list_view.html"

    def get(self, request):
        board = get_object_or_404(Board, id=2)
        statuses = Status.objects.filter(board=board).annotate(
            sum_suggestions=Count(
                "suggestion", filter=Q(suggestion__board=board), distinct=True
            )
        )

        suggestions = Suggestion.objects.filter(board=board).annotate(
            sum_votes=Count("votes", distinct=True),
            sum_comments=Count("comments", distinct=True),
        )

        filter = SuggestionFilter(request.GET, queryset=suggestions)
        paginator = Paginator(filter.qs, per_page=settings.PAGINATION_LIMIT_SUGGESTIONS)

        page_number = request.GET.get("page")
        page_suggestions = paginator.get_page(page_number)
        context = {
            "board": board,
            "suggestions": page_suggestions,
            "suggestions_count": suggestions.count(),
            "statuses": statuses,
        }
        return render(request, self.template_name, context)


class SuggestionDetailView(View):
    template_name = "users/suggestion_detail_view.html"

    def get(self, request, id):
        board = get_object_or_404(Board, id=2)
        suggestion = (
            Suggestion.objects.filter(id=id).annotate(
                sum_votes=Count("votes", distinct=True),
                sum_comments=Count("comments", distinct=True),
            )
        ).first()

        comments = Comment.objects.filter(suggestion=suggestion)
        paginator = Paginator(comments, per_page=settings.PAGINATION_LIMIT_COMMENTS)

        page_number = request.GET.get("page")
        page_comments = paginator.get_page(page_number)
        context = {
            "board": board,
            "comments": page_comments,
            "suggestion": suggestion,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        suggestion = get_object_or_404(Suggestion, id=id)
        data = {**request.POST.dict()}
        comment = CommentSerializer(data=data)
        if comment.is_valid():
            comment.save(suggestion=suggestion)
            messages.success(request, "Your comment have been created.")
            return redirect("suggestionsdetailview", id=id)

        messages.warning(request, "Something went wrong. Please try again!")
        return redirect("suggestionsdetailview", id=id)


class SuggestionCreateView(View):
    template_name = "users/suggestion_create_view.html"

    def get(self, request):
        board = get_object_or_404(Board, id=1)
        context = {
            "board": board,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        board = get_object_or_404(Board, id=2)
        data = {**request.POST.dict(), **request.FILES.dict()}
        suggestion = SuggestionSerializer(data=data)
        if suggestion.is_valid():
            suggestion.save(board=board)
            messages.success(request, "Your suggestion have been submited.")
            return redirect("suggestionslistview")

        messages.warning(request, "Something went wrong. Please try again!")
        return redirect("suggestionscreateview")


def voteup_suggestion(request, id):
    suggestion = get_object_or_404(Suggestion, id=id)
    serializer = VoteSerializer(data={"suggestion": suggestion})
    if serializer.is_valid():
        serializer.save(suggestion=suggestion)
        messages.success(request, "Your suggestion have been counted.")
        return redirect("suggestionsdetailview", id=id)

    messages.warning(request, "Something went wrong. Please try again!")
    return redirect("suggestionsdetailview", id=id)
