task_days = {}
base_sorted_days = []


def ordering_days(base, tasks_days, days):

    num_task_days = []
    new_base = []

    for i in range(days):
        num_task_days.append(tasks_days['day' + str(i + 1)])
    max_tasks = max(num_task_days)
    for i in range(days):
        if tasks_days['day' + str(base[i])] == max_tasks:
            new_base.append(base[i])
    for n in base:
        if n not in new_base:
            new_base.append(n)
    return new_base





def sort_days(days):
    global base_sorted_days

    if days % 2 == 0:
        sort_base = [1, 0, 2, -1, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6]

        for i in range(days):
            base = sort_base[i]
            x = (days / 2) + base
            x = int(x)
            base_sorted_days.append(x)


def chain(days, tasks):
    global task_days
    for i in range(days):
        task_days['day' + str(i + 1)] = int((tasks - (tasks % days)) / days)
    for n in range(tasks % days):
        task_days['day' + str(base_sorted_days[n])] += 1


def chain_tasks(days, tasks):
    global task_days
    base = ordering_days(base_sorted_days, task_days, days)
    print(base)
    for i in range(days):
        task_days['day' + str(i + 1)] -= int((tasks - (tasks % days)) / days)
    for n in range(tasks % days):
        task_days['day' + str(base[n])] -= 1

