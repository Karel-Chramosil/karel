# -*- coding: utf-8 -*-

# This file is a copied implementation from my asciichart repository on GitHub
# https://github.com/kroitor/asciichart

from math import cos
# from math import sin
from math import pi
from math import floor
from math import ceil

from termcolor import colored

def pplot(series, series_ask, cfg={}):

    color1 = "red"
    color2 = "yellow"
    posun_ask_bid  = 1

    minimum = min(series)
    maximum = max(series) + posun_ask_bid

    interval = abs(float(maximum) - float(minimum))
    offset = cfg['offset'] if 'offset' in cfg else 3
    # padding = cfg['padding'] if 'padding' in cfg else '       '
    height = cfg['height'] if 'height' in cfg else interval
    ratio = height / interval
    # print(minimum,ratio,type(minimum))
    min2 = floor(float(minimum) * ratio)
    max2 = ceil(float(maximum) * ratio)

    intmin2 = int(min2)
    intmax2 = int(max2)

    rows = abs(intmax2 - intmin2)
    width = len(series) + offset
    # format = cfg['format'] if 'format' in cfg else lambda x: (padding + '{:.2f}'.format(x))[:-len(padding)]

    result = [[' '] * width for i in range(rows + 1)]

    # axis and labels
    for y in range(intmin2, intmax2 + 1):
        label = (colored('{:8.2f}', color2)).format(float(maximum) - ((y - intmin2) * interval / rows))
        result[y - intmin2][max(offset - len(label), 0)] = label
        result[y - intmin2][offset - 1] = (colored('┼', color2)) if y == 0 else (colored('┤', color2))

    y0 = int(series[0] * ratio - min2)
    result[rows - y0][offset - 1] = '┼'  # first value

    for x in range(0, len(series) - 1):  # plot the line
        y0 = int(round(series[x + 0] * ratio) - intmin2)
        y1 = int(round(series[x + 1] * ratio) - intmin2)
        if y0 == y1:
            result[rows - y0][x + offset] = (colored('─', color2))
        else:
            result[rows - y1][x + offset] = (colored('╰', color2)) if y0 > y1 else (colored('╭', color2))
            result[rows - y0][x + offset] = (colored('╮', color2)) if y0 > y1 else (colored('╯', color2))
            start = min(y0, y1) + 1
            end = max(y0, y1)
            for y in range(start, end):
                result[rows - y][x + offset] = (colored('│', color2))
        y0 = int(round(series_ask[x + 0] * ratio) - intmin2) + posun_ask_bid
        y1 = int(round(series_ask[x + 1] * ratio) - intmin2) + posun_ask_bid
        if y0 == y1:
            result[rows - y0][x + offset] = (colored('─', color1))
        else:
            result[rows - y1][x + offset] = (colored('╰', color1)) if y0 > y1 else (colored('╭', color1))
            result[rows - y0][x + offset] = (colored('╮', color1)) if y0 > y1 else (colored('╯', color1))
            start = min(y0, y1) + 1
            end = max(y0, y1)
            for y in range(start, end):
                result[rows - y][x + offset] = (colored('│', color1))


    return '\n'.join([''.join(row) for row in result])


if __name__ == '__main__':
    width = 60
    series = [10 * cos(i * ((pi * 3) / width)) for i in range(width)]
    print(pplot(series))
