import matplotlib.pyplot as plt
import sys
import ast


path1 = sys.argv[1]
path2 = sys.argv[2]
with open(path1) as f:
    data = f.read()
dag_n = ast.literal_eval(data)
with open(path2) as f:
    data = f.read()
d = ast.literal_eval(data)


assert_fail = []
ign = []
tl = {}
x = []
x_not_opt_rhomb = []
x_not_opt = []
x_und_rhomb = []
x_und = []
y = []
y_not_opt_rhomb = []
y_not_opt = []
y_und_rhomb = []
y_und = []
x_set = set()
other = {}
x_vert_n = {}
max_n_opt = 0
max_dag = ''
for dag in d:
    fl_assert_fail = False
    fl_tl = False
    fl_opt = False
    fl_non_opt = False
    fl_und = False
    opt = {}
    non_opt = {}
    und = {}
    if dag_n[dag] not in tl:
        x_vert_n[dag_n[dag]] = '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')'
        tl[dag_n[dag]] = 0
    for sort in d[dag]:
        tm = -100
        if d[dag][sort]['status'] == 'IGNORED':
            ign.append(dag)
            break
        elif d[dag][sort]['status'] == 'assertion failed':
            assert_fail.append(dag)
            fl_assert_fail = True
            continue
        elif d[dag][sort]['status'] == 'TIMELIMIT':
            if fl_tl:
                continue
            fl_tl = True
            tl[dag_n[dag]] += 1
            x_set.add(str(dag_n[dag]) + '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')')
            continue
        else:
            tm = d[dag][sort]['tm']
        if d[dag][sort]['status'] == 'INT_OPT':
            fl_opt = True
            opt[sort] = tm
            #x.append(str(dag_n[dag]) + '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')')
            #y.append(tm)
            #break
        elif d[dag][sort]['status'] == 'INT_NON_OPT':
            fl_non_opt = True
            non_opt[sort] = [d[dag][sort]['f'], tm]
        elif d[dag][sort]['status'] == 'INT_UND':
            fl_und = True
            und[sort] = tm
        else:
            other[dag][sort] = d[dag][sort]
    #x_set.add(dag_n[dag])
    x_set.add(str(dag_n[dag]) + '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')')
    if fl_opt:
        if dag_n[dag] > max_n_opt:
            max_n_opt = dag_n[dag]
            max_dag = dag
        if fl_tl:
            tl[dag_n[dag]] -= 1
        min_tm = -1
        for sort in opt:
            if min_tm == -1 or min_tm > opt[sort]:
                min_tm = opt[sort]
        x.append(str(dag_n[dag]) + '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')')
        y.append(min_tm)
        continue
    elif fl_non_opt:
        min_f = -1
        for sort in non_opt:
            if min_f == -1 or min_f > non_opt[sort][0]:
                min_f = non_opt[sort][0]
        min_tm = -1
        for sort in non_opt:
            if non_opt[sort][0] >= min_f and (min_tm == -1 or min_tm > non_opt[sort][1]):
                min_tm = non_opt[sort][1]
        if fl_tl:
            x_not_opt_rhomb.append(str(dag_n[dag]) + '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')')
            y_not_opt_rhomb.append(min_tm)
        else:
            x_not_opt.append(str(dag_n[dag]) + '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')')
            y_not_opt.append(min_tm)
    elif fl_und:
        min_tm = -1
        for sort in und:
            if min_tm == -1 or min_tm > und[sort]:
                min_tm = und[sort]
        if fl_tl:
            x_und_rhomb.append(str(dag_n[dag]) + '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')')
            y_und_rhomb.append(min_tm)
        else:
            x_und.append(str(dag_n[dag]) + '\n(' + str(list(dag_n.values()).count(dag_n[dag])) + ')')
            y_und.append(min_tm)


x_set = list(x_set)

new_x, new_y, new_x_not_opt, new_y_not_opt, new_x_und, new_y_und, new_x_not_opt_rhomb, new_y_not_opt_rhomb, new_x_und_rhomb, new_y_und_rhomb = [], [], [], [], [], [], [], [], [], []
if len(x) != 0 and len(y) != 0:
    new_x, new_y = zip(*[(b, a) for b, a in sorted(zip(x, y))])
if len(x_not_opt) != 0 and len(y_not_opt) != 0:
    new_x_not_opt, new_y_not_opt = zip(*[(b, a) for b, a in sorted(zip(x_not_opt, y_not_opt))])
if len(x_und) != 0 and len(y_und) != 0:
    new_x_und, new_y_und = zip(*[(b, a) for b, a in sorted(zip(x_und, y_und))])
if len(x_not_opt_rhomb) != 0 and len(y_not_opt_rhomb) != 0:
    new_x_not_opt_rhomb, new_y_not_opt_rhomb = zip(*[(b, a) for b, a in sorted(zip(x_not_opt_rhomb, y_not_opt_rhomb))])
if len(x_und_rhomb) != 0 and len(y_und_rhomb) != 0:
    new_x_und_rhomb, new_y_und_rhomb = zip(*[(b, a) for b, a in sorted(zip(x_und_rhomb, y_und_rhomb))])


plt.figsize = (5, 10)
plt.grid(axis='x', linestyle='--', linewidth=0.5)
timel = 0
for i in sorted(tl.keys()):
    if tl[i] > 0:
        timel = plt.scatter(str(i) + x_vert_n[i], 1800, color='red')
    else:
        timel = plt.scatter(str(i) + x_vert_n[i], 1800, s=0, color='red')
    plt.text(str(i) + x_vert_n[i], 1820, f'{tl[i]}')
opt = plt.scatter(new_x, new_y)
non_opt = plt.scatter(new_x_not_opt, new_y_not_opt, color='purple')
non_opt_rhomb = plt.scatter(new_x_not_opt_rhomb, new_y_not_opt_rhomb, color='purple', marker='d')
undef = plt.scatter(new_x_und, new_y_und, color='black')
undef_rhomb = plt.scatter(new_x_und_rhomb, new_y_und_rhomb, color='black', marker='d')
plt.ylabel('время, с')
plt.xlabel('количество вершин, (количество графов)')
plt.xticks(x_set)
plt.yticks(rotation=90)
plt.axhline(y=1800, color='r', linestyle='-')
plt.title('Случайные графы')
leg = plt.legend((opt, non_opt, undef, timel), ('INTEGER OPTIMAL', 'INTEGER NON-OPTIMAL', 'INTEGER UNDEFINED', 'TIMELIMIT'), loc='center right', markerscale=0, handlelength=0, handletextpad=0, fontsize=9.1)
count = 0
for text in leg.get_texts():
    if count == 0:
        text.set_color("b")
    elif count == 1:
        text.set_color("purple")
    elif count == 2:
        text.set_color("black")
    elif count == 3:
        text.set_color("red")
    count += 1
plt.show()


