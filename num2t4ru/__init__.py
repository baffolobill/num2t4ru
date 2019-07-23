# -*- coding: utf-8 -*-
"""
Created on 04.07.2011
Changed on 13.03.2016 by Artem Tiumentcev

@author: Sergey Prokhorov <me@seriyps.ru>
"""
import decimal


UNITS = (
    'ноль',

    ('один', 'одна'),
    ('два', 'две'),

    'три', 'четыре', 'пять',
    'шесть', 'семь', 'восемь', 'девять'
)

TEENS = (
    'десять', 'одиннадцать',
    'двенадцать', 'тринадцать',
    'четырнадцать', 'пятнадцать',
    'шестнадцать', 'семнадцать',
    'восемнадцать', 'девятнадцать'
)

TENS = (
    TEENS,
    'двадцать', 'тридцать',
    'сорок', 'пятьдесят',
    'шестьдесят', 'семьдесят',
    'восемьдесят', 'девяносто'
)

HUNDREDS = (
    'сто', 'двести',
    'триста', 'четыреста',
    'пятьсот', 'шестьсот',
    'семьсот', 'восемьсот',
    'девятьсот'
)

ORDERS = (  # plural forms and gender
    # (('', '', ''), 'm'), # (('рубль', 'рубля', 'рублей'), 'm'), # (('копейка', 'копейки', 'копеек'), 'f')
    (('тысяча', 'тысячи', 'тысяч'), 'f'),
    (('миллион', 'миллиона', 'миллионов'), 'm'),
    (('миллиард', 'миллиарда', 'миллиардов'), 'm'),
)

MINUS = 'минус'


def thousand(rest, sex):
    """Converts numbers from 19 to 999"""
    prev = 0
    plural = 2
    name = []
    use_teens = 10 <= rest % 100 <= 19
    if not use_teens:
        data = ((UNITS, 10), (TENS, 100), (HUNDREDS, 1000))
    else:
        data = ((TEENS, 10), (HUNDREDS, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(TEENS[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if 2 <= cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


def num2text(num, main_units=(('', '', ''), 'm'), do_not_replace_number=False):
    """
    http://ru.wikipedia.org/wiki/Gettext#.D0.9C.D0.BD.D0.BE.D0.B6.D0.B5.D1.81.\
    D1.82.D0.B2.D0.B5.D0.BD.D0.BD.D1.8B.D0.B5_.D1.87.D0.B8.D1.81.D0.BB.D0.B0_2
    """
    _orders = (main_units,) + ORDERS
    if do_not_replace_number and isinstance(num, str) and num in {'00', '0'}:
        return ' '.join((num, _orders[0][0][2])).strip()  # ноль
    
    if num == 0:
        return ' '.join((UNITS[0], _orders[0][0][2])).strip()  # ноль
    
    rest = abs(num)
    ord_ = 0
    name = []
    while rest > 0:
        plural, nme = thousand(rest % 1000, _orders[ord_][1])
        if nme or ord_ == 0:
            name.append(_orders[ord_][0][plural])
        if do_not_replace_number:
            name += [str(num)]
            break
        name += nme
        rest = int(rest / 1000)
        ord_ += 1
    if num < 0:
        name.append(MINUS)
    name.reverse()
    return ' '.join(name).strip()


def decimal2text(value, places=2,
                 fractional_as_number=False,
                 int_units=(('', '', ''), 'm'),
                 exp_units=(('', '', ''), 'm')):
    value = decimal.Decimal(value)
    round_precision = decimal.Decimal(10) ** -places

    integral, exp = str(value.quantize(round_precision)).split('.')
    exp = int(exp)
    if fractional_as_number:
        exp = exp or '00'

    return '{} {}'.format(
        num2text(int(integral), int_units),
        num2text(exp, exp_units, do_not_replace_number=fractional_as_number))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        try:
            num = sys.argv[1]
            if '.' in num:
                print(decimal2text(
                    decimal.Decimal(num),
                    int_units=(('штука', 'штуки', 'штук'), 'f'),
                    exp_units=(('кусок', 'куска', 'кусков'), 'm')))
            else:
                print(num2text(
                    int(num),
                    main_units=(('штука', 'штуки', 'штук'), 'f')))
        except ValueError:
            print(sys.stderr, "Invalid argument {}".format(sys.argv[1]))
        sys.exit()
