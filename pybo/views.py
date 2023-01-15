from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm
from pybo.models import Question


def index(request):
    question_list = Question.objects.order_by('-created_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), created_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})
