from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np


def get_month_dict(orders_month):
    current_date = datetime.today()
    month_list = [current_date - timedelta(days=x) for x in range(30)]
    my_month_dict = {}
    for i in range(30):
        new_day = {str(month_list[29-i].date()).split("-")[-1]:0}
        my_month_dict.update(new_day)

    for order in orders_month:
        create_day = str(order.create_at).split("-")[-1]
        my_month_dict[create_day] += 1

    keys = my_month_dict.keys()
    values = my_month_dict.values()

    return keys, values


def get_sum_values(dict_value):
    sum = 0
    for x in dict_value:
        sum += int(x)

    return sum


def draw_order_barchart(values, values_finish, values_cancle, keys):
    f, ax = plt.subplots()
    f.set_figwidth(9)
    f.set_figheight(5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)
    
    plt.title(_("Order statistics in 30 days"))
    plt.ylabel(_("Number of orders"))
    plt.xlabel(_("Day"))
    
    ind = np.arange(30)
    width = 0.25 
    my_bar1 = ax.bar(ind, values, width, color='#EE7AE9')
    my_bar2 = ax.bar(ind+width, values_finish, width, color='#00FA9A')
    my_bar3 = ax.bar(ind+2*width, values_cancle, width, color='#FF7256')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(keys)
    ax.legend((my_bar1[0], my_bar2[0], my_bar3[0]), (_('All orders'), _('Finished order'), _('Canceled order')))
    plt.savefig('./shop/static/img/my_order_chart.png', bbox_inches='tight')


def draw_order_circlechart(cancel_order, all_order):
    labels = _('Canceled order'), _('Finished orders')
    percent = cancel_order/all_order
    sizes = [percent, 1-percent]
    explode = (0, 0.1)
    f1, ax1 = plt.subplots()
    f1.set_figwidth(9)
    f1.set_figheight(5.25)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=['#FF7256', '#00FA9A'])
    ax1.axis('equal')
    plt.title(_("Order statistics in 30 days"))
    plt.savefig('./shop/static/img/my_order_circle.png', bbox_inches='tight')


def draw_reviews_barchart(list_star):
    f2, ax2 = plt.subplots()
    f2.set_figwidth(9)
    f2.set_figheight(5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_color('#DDDDDD')
    ax2.tick_params(bottom=False, left=False)
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(True, color='#EEEEEE')
    ax2.xaxis.grid(False)
    plt.title(_("Review statistics in 30 days"))
    plt.ylabel(_("Number times"))
    plt.xlabel(_("User rating"))
    plt.bar(range(len(list_star)), list(list_star.values()), align='center', width=0.4, color='#FFFF5C')
    plt.xticks(range(len(list_star)), list(list_star.keys()))   
    plt.savefig('./shop/static/img/my_star_chart.png', bbox_inches='tight')
