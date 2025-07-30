from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from .models import Todo, Comment
from .forms import CommentForm


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    queryset = Todo.objects.all().prefetch_related("comments", "comments__user")
    template_name = "todo/todo_info.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 조회할 권한이 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        comments = self.object.comments.order_by("-created_at")
        paginator = Paginator(comments, 5)
        context = {
            "todo": self.object.__dict__,
            "comment_form": CommentForm(),
            "page_obj": paginator.get_page(self.request.GET.get("page")),
        }
        return context

...

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["message"]
    pk_url_kwarg = "todo_id"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = Todo.objects.get(id=self.kwargs["todo_id"])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.kwargs["todo_id"]})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["message"]

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 댓글을 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.todo.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 댓글을 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.todo.id})