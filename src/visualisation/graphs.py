import matplotlib.pyplot as plt
import numpy as np


def autolabel(rects):
    for rect in rects:
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2
        space = 5
        ha = 'left'
        if x_value < 0:
            space *= -1
            ha = 'right'

        label = "{:.1f}M".format(x_value)

        plt.annotate(
            label,
            (x_value, y_value),
            xytext=(space, 0),
            textcoords="offset points",
            va='center', ha=ha)


def autolabel_vertival(rects, ax, xpos='center'):
    xpos = xpos.lower()
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.6, 'right': 0.0, 'left': 0.982}

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                '{}'.format(height), ha=ha[xpos], va='bottom')


def convert(x):
    if x >= 1e6:
        s = x * 1e-6
    else:
        s = x * 1e-3
    return s


def visualize_top_entities(data, filename):
    names = []
    installs = []
    for d in data:
        names.append(d['name'])
        installs.append(convert(d['installs']))

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.rcdefaults()
    y_pos = np.arange(len(names))

    bar_plot = ax.barh(y_pos, installs, align='center')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.invert_yaxis()
    ax.set(xlabel='Installs, M', title='Top by installs')
    ax.set_xlim(0, 7000)

    autolabel(bar_plot)
    plt.savefig('../visuals/' + filename + '.png', bbox_inches='tight')
    plt.show()


def percentage(data):
    sum = 0
    p = []
    for d in data:
        sum += d

    for d in data:
        p.append(float(d) * 100 / float(sum))
    return p


def visualize_piechart(data, filename):
    names = []
    installs = []
    for d in data:
        names.append(d['name'])
        installs.append(d['installs'])
    sizes = percentage(installs)

    plt.figure()
    plt.pie(sizes, labels=names, autopct='%1.1f%%')
    plt.title('Types of apps')
    plt.axis('equal')
    plt.savefig('../visuals/' + filename + '.png', bbox_inches='tight')
    plt.show()


def visualize_dates(data, filename):
    dates = []
    times = []
    for d in data:
        dates.append(d['date'])
        times.append(d['number'])

    plt.figure()
    plt.plot(dates, times)
    plt.grid(True)
    plt.title('Dynamics of released apps')
    plt.savefig('../visuals/' + filename + '.png', bbox_inches='tight')
    plt.show()


def index_results(filename):
    old_means = (0.745, 0.867, 0.642, 0.434, 0.738)
    new_means = (0.389, 0.362, 0.335, 0.286, 0.328)

    ind = np.arange(len(old_means))
    width = 0.4

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width / 2, old_means, width,
                    color='SkyBlue', label='No BRIN')
    rects2 = ax.bar(ind + width / 2, new_means, width,
                    color='IndianRed', label='Using BRIN')

    ax.set_ylabel('Execution time, ms')
    ax.set_title('Results of BRIN index tests')
    ax.set_xticks(ind)
    ax.set_xticklabels(('Test 1', 'Test 2', 'Test 3', 'Test 4', 'Test 5'))
    ax.legend()

    autolabel_vertival(rects1, ax, "left")
    autolabel_vertival(rects2, ax, "right")

    plt.savefig('../visuals/' + filename + '.png', bbox_inches='tight')
    plt.show()
