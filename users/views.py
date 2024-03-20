from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.views.generic.base import View

from core.models import *
from core.serializers import *
from users.filters import *


class SuggestionListView(View):
    template_name = "users/suggestion_list_view.html"

    def get(self, request, id):
        board = get_object_or_404(Board, id=id, deleted_at__isnull=True, is_active=True)
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

    def get(self, request, bid, id):
        board = get_object_or_404(
            Board, id=bid, deleted_at__isnull=True, is_active=True
        )
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

    def post(self, request, bid, id):
        suggestion = get_object_or_404(Suggestion, id=id)
        data = {**request.POST.dict()}
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(suggestion=suggestion)
            messages.success(request, "Your comment have been created.")
            return redirect("suggestionsdetailview", bid=bid, id=id)

        [messages.warning(request, errors[0]) for errors in serializer.errors.values()]
        return redirect("suggestionsdetailview", bid=bid, id=id)


class SuggestionCreateView(View):
    template_name = "users/suggestion_create_view.html"

    def get(self, request, id):
        board = get_object_or_404(Board, id=id, deleted_at__isnull=True, is_active=True)
        context = {
            "board": board,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        board = get_object_or_404(Board, id=id, is_active=True)
        data = {
            **request.POST.dict(),
            **request.FILES.dict(),
            "status": board.status_default.id if board.status_default else None,
        }
        serializer = SuggestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(board=board)
            messages.success(request, "Your suggestion have been submited.")
            return redirect("suggestionslistview", id=id)

        [messages.warning(request, errors[0]) for errors in serializer.errors.values()]
        return redirect("suggestionscreateview", id=id)


def voteup_suggestion(request, bid, id):
    suggestion = get_object_or_404(Suggestion, id=id)
    serializer = VoteSerializer(data={"suggestion": suggestion})
    if serializer.is_valid():
        serializer.save(suggestion=suggestion)
        messages.success(request, "Your suggestion have been counted.")
        return redirect("suggestionsdetailview", bid=bid, id=id)

    [messages.warning(request, errors[0]) for errors in serializer.errors.values()]
    return redirect("suggestionsdetailview", bid=bid, id=id)
