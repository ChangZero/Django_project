from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question
from django.urls import reverse
from django.views import generic
from django.utils import timezone


# def index(request):
# 1
# return HttpResponse("Hello, world. You're at the polls index.")

# 2. Actually do someting
# latest_question_list = Question.objects.order_by('-pub_date')[:5]
# output = ', '.join([q.question_text for q in latest_question_list])
# return HttpResponse(output)

# 3. Use the template
# latest_question_list = Question.objects.order_by('-pub_date')[:5]
# template = loader.get_template("polls/index.html")
# context = {
#     'latest_question_list': latest_question_list,
# }
# return HttpResponse(template.render(context, request))

# 4. Use the shortcut - render
# latest_question_list = Question.objects.order_by('-pub_date')[:5]
# context = {'latest_question_list': latest_question_list}
# return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     # 1
#     # return HttpResponse("You're looking at question %s." % question_id)

#     # 2
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exits")
#     # return render(request, 'polls/detail.html', {'question': question})

#     # 3
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))
        # HttpResponseRedirect은 request.POST와 한 세트임
