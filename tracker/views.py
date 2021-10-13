import plotly.graph_objs as go
import plotly.offline as opy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import *


@login_required
def home(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        progress_form = ProgressForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user=request.user, title=request.POST['title'], score=request.POST['score'], is_finished=finished)
            todos.save()
            messages.success(
                request, f'Todo Added from {request.user.username}!')
    else:
        form = TodoForm()
        progress_form = ProgressForm()
    todos = Todo.objects.filter(user=request.user)
    print("here", todos)
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    todos = zip(todos, range(1, len(todos)+1))
    context = {'form': form, 'todos': todos,
               'todos_done': todos_done, 'progress_form': progress_form}
    return render(request, 'home.html', context)


def register(request):
    if request.method == "POST":
        u_form = UserRegisterForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect('login')
    else:
        u_form = UserRegisterForm()
    return render(request, 'register.html', {'u_form': u_form})

@login_required
def profile(request):
    progresses = Progress.objects.filter(user=request.user).order_by('date')
    date_axis = []
    score_axis = []
    for progress in progresses:
        date_axis.append(progress.date)
        score_axis.append(progress.final_score)
    count = 0
    i = 0

    max_count = 0
    prev_count = 0
    print(score_axis)
    count_list = []

    while i < len(score_axis) - 1: #[10,20,30,40]
        while i < len(score_axis)-1 and score_axis[i] <= score_axis[i+1]:
            i += 1
            count += 1
        prev_count = count
        count_list.append(count)
        if count > max_count:
            print(count)
            max_count = count
            count = 0
        i += 1
    count_list.append(count)
    count_range = list(range(1, len(count_list)+1))
    print(count_list)

    trace1 = go.Scatter(x=date_axis, y=score_axis, marker={'color': 'red', 'symbol': 104},
                        mode="lines",  name='1st Trace')
    data = go.Data([trace1])
    layout = go.Layout(title="Progress Level", xaxis={
        'title': 'Date'}, yaxis={'title': 'Score'})
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         step="day",
                         stepmode="backward"),
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        )
    )
    div1 = opy.plot(figure, auto_open=False, output_type='div')

    trace1 = go.Bar(x=date_axis, y=score_axis, marker={'color': 'blue'},
                    name='1st Trace')
    data = go.Data([trace1])
    layout = go.Layout(title="Progress Level", xaxis={
        'title': 'Date'}, yaxis={'title': 'Score'})
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         step="day",
                         stepmode="backward"),
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        )
    )
    div2 = opy.plot(figure, auto_open=False, output_type='div')

    trace1 = go.Scatter(x=count_range, y=count_list, marker={'color': 'red', 'symbol': 104},
                        mode="lines",  name='1st Trace')

    data = go.Data([trace1])
    layout = go.Layout(title="Streak Progress", xaxis={
        'title': 'Number of streaks'}, yaxis={'title': 'Days'})
    figure = go.Figure(data=data, layout=layout)
    figure.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         step="day",
                         stepmode="backward"),
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        )
    )

    div3 = opy.plot(figure, auto_open=False, output_type='div')

    avg = round(sum(score_axis)/len(progresses), 2)
    context = {
        'progresses': progresses,
        'maxi': max(score_axis),
        'total': len(progresses),
        'avg': avg,
        'scatter': div1,
        'bar': div2,
        'streak_graph': div3,
        'current_streak': count_list[-1],
        'highest_streak': max_count,
    }
    return render(request, 'profile.html', context)


def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('home')


def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('home')

def reset_todo(request):
    todos = Todo.objects.filter(user=request.user)
    for todo in todos:
        todo.is_finished = False
        todo.save()
    return redirect('home')

def submit_todo(request):
    day_score = Todo.objects.filter(
        user=request.user, is_finished=True).aggregate(Sum('score'))['score__sum']
    progress, created = Progress.objects.update_or_create(user=request.user,
                                                          date=request.POST['date'],
                                                          defaults={'final_score': day_score})
    progress.save()

    return redirect('home')
