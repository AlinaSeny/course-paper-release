import os
import sys
from re import findall


def read_pars_input(file_path):
    f = open(file_path, "r")
    nodes = []
    lines = f.readlines()
    for line in lines:
        nums = findall(r'\d+', line)
        if not nums:
            continue
        nodes.append(nums[0])
    f.close()
    return len(nodes)


d = {}
path = sys.argv[1]
dags = os.listdir(path)
names = []
dag_n = {}
for dag in dags:
    n = read_pars_input(path + '/' + dag)
    dag_n[dag] = n
    dag = dag[0:dag.find('.')]
    names.append(dag)
times = os.listdir('times')
slv_outs = os.listdir('solver_outputs')
outs = os.listdir('outputs')
for slv_out in slv_outs:
    dag = slv_out[0:slv_out.find('_')]
    if dag not in names:
        continue
    sort = slv_out[slv_out.find('_') + 1:-11]
    if sort not in 'default down_left up_right tiers reverse_tiers':
        continue
    if dag not in d:
        d[dag] = {'default': {'status': '', 'tm': -10}, 'down_left': {'status': '', 'tm': -10},
                  'up_right': {'status': '', 'tm': -10}, 'tiers': {'status': '', 'tm': -10},
                  'reverse_tiers': {'status': '', 'tm': -10}}
    slv_out = open('solver_outputs/' + slv_out, 'r')
    lines = slv_out.readlines()
    for line in lines:
        if 'Status:' in line:
            if 'INTEGER OPTIMAL' in line:
                d[dag][sort]['status'] = 'INT_OPT'
            elif 'INTEGER NON-OPTIMAL' in line:
                d[dag][sort]['status'] = 'INT_NON_OPT'
            elif 'INTEGER UNDEFINED' in line:
                d[dag][sort]['status'] = 'INT_UND'
            else:
                d[dag][sort]['status'] = ' '.join(line.split()[1:])
        if 'Objective:' in line:
            tmp = findall(r'\d+', line)
            d[dag][sort]['f'] = tmp[0]
            break

for time in times:
    dag = time[0:time.find('_')]
    if dag not in names:
        continue
    sort = time[time.find('_') + 1:-5]
    if sort not in 'default down_left up_right tiers reverse_tiers':
        continue
    if dag not in d:
        d[dag] = {'default': {'status': '', 'tm': -10}, 'down_left': {'status': '', 'tm': -10},
                  'up_right': {'status': '', 'tm': -10}, 'tiers': {'status': '', 'tm': -10},
                  'reverse_tiers': {'status': '', 'tm': -10}}
    time = open('times/' + time, 'r')
    lines = time.readlines()
    for line in lines:
        if 'timeout: the monitored command dumped core' in line:
            d[dag][sort]['status'] = 'assertion failed'
        elif 'real' in line:
            line = line.split()
            rl = line[1]
            m = rl.find('m')
            dot = rl.find('.')
            rl_t = int(rl[:m]) * 60 + int(rl[m + 1:dot])
            if rl_t >= 1800:
                d[dag][sort]['status'] = 'TIMELIMIT'
                d[dag][sort]['tm'] = 1800
                break
        elif 'user' in line:
            line = line.split()
            tm = line[1]
            m = tm.find('m')
            dot = tm.find('.')
            tm = int(tm[:m]) * 60 + int(tm[m + 1:dot])
            d[dag][sort]['tm'] = tm
            break

for dag in d:
    fl_ign = True
    for sort in d[dag]:
        if d[dag][sort]['tm'] != -10 or len(d[dag][sort]['status']) != 0:
            fl_ign = False
    if fl_ign:
        for sort in d[dag]:
            d[dag][sort]['status'] = 'IGNORED'

for out in outs:
    if 'reverse_tiers' in out:
        dag = out[0:out.find('r')]
        sort = 'reverse_tiers'
    else:
        dag = out[0:out.find('_')]
        sort = out[out.find('_') + 1:-11]
    if dag not in names:
        continue
    if sort not in 'default down_left up_right tiers reverse_tiers':
        continue
    if dag not in d:
        d[dag] = {'default': {'status': '', 'tm': -10}, 'down_left': {'status': '', 'tm': -10},
                  'up_right': {'status': '', 'tm': -10}, 'tiers': {'status': '', 'tm': -10},
                  'reverse_tiers': {'status': '', 'tm': -10}}
    out = open('outputs/' + out, 'r')
    lines = out.readlines()
    i = len(lines) - 1
    bound = len(lines)
    if len(d[dag][sort]['status']) == 0:
        d[dag][sort]['status'] = 'TIMELIMIT'
        d[dag][sort]['tm'] = 1800
        continue
    if (d[dag][sort]['status'] == 'INT_OPT' or d[dag][sort]['status'] == 'INT_NON_OPT' or d[dag][sort]['status'] == 'INT_UND') and d[dag][sort]['tm'] == -10:
        bound = len(lines) - 4
    while i >= bound:
        if 'Time used:' in lines[i]:
            tm = lines[i].split()[2]
            tm = round(float(tm))
            d[dag][sort]['tm'] = tm
            break
        i -= 1

for dag in sorted(d.keys()):
    print(dag)
    print('default', d[dag]['default'])
    print('down_left', d[dag]['down_left'])
    print('tiers', d[dag]['tiers'])
    print('reverse_tiers', d[dag]['reverse_tiers'])
    print('up_right', d[dag]['up_right'])
    print()

print(dag_n)
print(d)
