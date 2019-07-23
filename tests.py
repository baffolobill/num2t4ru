# -*- coding: utf-8 -*-
'''
Created on 13.03.2016 by Artem Tiumentcev

@author: Sergey Prokhorov <me@seriyps.ru>
'''
import unittest

from num2t4ru import num2text, decimal2text


class TestStrToText(unittest.TestCase):

    def test_units(self):
        self.assertEqual(num2text(0), 'ноль')
        self.assertEqual(num2text(1), 'один')
        self.assertEqual(num2text(9), 'девять')

    def test_gender(self):
        self.assertEqual(num2text(1000), 'одна тысяча')
        self.assertEqual(num2text(2000), 'две тысячи')
        self.assertEqual(num2text(1000000), 'один миллион')
        self.assertEqual(num2text(2000000), 'два миллиона')

    def test_teens(self):
        self.assertEqual(num2text(10), 'десять')
        self.assertEqual(num2text(11), 'одиннадцать')
        self.assertEqual(num2text(19), 'девятнадцать')

    def test_tens(self):
        self.assertEqual(num2text(20), 'двадцать')
        self.assertEqual(num2text(90), 'девяносто')

    def test_hundreeds(self):
        self.assertEqual(num2text(100), 'сто')
        self.assertEqual(num2text(900), 'девятьсот')

    def test_orders(self):
        self.assertEqual(num2text(1000), 'одна тысяча')
        self.assertEqual(num2text(2000), 'две тысячи')
        self.assertEqual(num2text(5000), 'пять тысяч')
        self.assertEqual(num2text(1000000), 'один миллион')
        self.assertEqual(num2text(2000000), 'два миллиона')
        self.assertEqual(num2text(5000000), 'пять миллионов')
        self.assertEqual(num2text(1000000000), 'один миллиард')
        self.assertEqual(num2text(2000000000), 'два миллиарда')
        self.assertEqual(num2text(5000000000), 'пять миллиардов')

    def test_inter_oreders(self):
        self.assertEqual(num2text(1100), 'одна тысяча сто')
        self.assertEqual(num2text(2001), 'две тысячи один')
        self.assertEqual(num2text(5011), 'пять тысяч одиннадцать')
        self.assertEqual(num2text(1002000), 'один миллион две тысячи')
        self.assertEqual(num2text(2020000), 'два миллиона двадцать тысяч')
        self.assertEqual(num2text(5300600), 'пять миллионов триста тысяч шестьсот')
        self.assertEqual(num2text(1002000000), 'один миллиард два миллиона')
        self.assertEqual(num2text(2030000000), 'два миллиарда тридцать миллионов')
        self.assertEqual(num2text(1234567891),
                         'один миллиард двести тридцать четыре миллиона '
                         'пятьсот шестьдесят семь тысяч '
                         'восемьсот девяносто один')

    def test_main_units(self):
        male_units = (('рубль', 'рубля', 'рублей'), 'm')
        female_units = (('копейка', 'копейки', 'копеек'), 'f')
        self.assertEqual(num2text(101, male_units), 'сто один рубль')
        self.assertEqual(num2text(102, male_units), 'сто два рубля')
        self.assertEqual(num2text(105, male_units), 'сто пять рублей')

        self.assertEqual(num2text(101, female_units), 'сто одна копейка')
        self.assertEqual(num2text(102, female_units), 'сто две копейки')
        self.assertEqual(num2text(105, female_units), 'сто пять копеек')

        self.assertEqual(num2text(0, male_units), 'ноль рублей')
        self.assertEqual(num2text(0, female_units), 'ноль копеек')

        self.assertEqual(num2text(3000, male_units), 'три тысячи рублей')

    def test_decimal2text(self):
        int_units = (('рубль', 'рубля', 'рублей'), 'm')
        exp_units = (('копейка', 'копейки', 'копеек'), 'f')
        self.assertEqual(
            decimal2text(
                '105.245',
                int_units=int_units,
                exp_units=exp_units),
            'сто пять рублей двадцать четыре копейки')
        self.assertEqual(
            decimal2text(
                '101.26',
                int_units=int_units,
                exp_units=exp_units),
            'сто один рубль двадцать шесть копеек')
        self.assertEqual(
            decimal2text(
                '102.2450',
                places=4,
                int_units=int_units,
                exp_units=exp_units),
            'сто два рубля две тысячи четыреста пятьдесят копеек')  # xD
        self.assertEqual(
            decimal2text(
                '111',
                int_units=int_units,
                exp_units=exp_units),
            'сто одиннадцать рублей ноль копеек')
        self.assertEqual(
            decimal2text(
                '3000.00',
                int_units=int_units,
                exp_units=exp_units),
            'три тысячи рублей ноль копеек')

    def test_decimal2text_with_fractional_as_number(self):
        int_units = (('рубль', 'рубля', 'рублей'), 'm')
        exp_units = (('копейка', 'копейки', 'копеек'), 'f')
        self.assertEqual(
            decimal2text(
                '105.245',
                fractional_as_number=True,
                int_units=int_units,
                exp_units=exp_units),
            'сто пять рублей 24 копейки')
        self.assertEqual(
            decimal2text(
                '101.26',
                fractional_as_number=True,
                int_units=int_units,
                exp_units=exp_units),
            'сто один рубль 26 копеек')
        self.assertEqual(
            decimal2text(
                '102.2450',
                places=4,
                fractional_as_number=True,
                int_units=int_units,
                exp_units=exp_units),
            'сто два рубля 2450 копеек')  # xD
        self.assertEqual(
            decimal2text(
                '111',
                fractional_as_number=True,
                int_units=int_units,
                exp_units=exp_units),
            'сто одиннадцать рублей 00 копеек')
        self.assertEqual(
            decimal2text(
                '3000.00',
                fractional_as_number=True,
                int_units=int_units,
                exp_units=exp_units),
            'три тысячи рублей 00 копеек')

    def test_negative(self):
        self.assertEqual(num2text(-12345),
                         "минус двенадцать тысяч триста сорок пять")
        self.assertEqual(
            decimal2text('-123.45'),
            'минус сто двадцать три сорок пять')


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        try:
            num = sys.argv[1]
            if '.' in num:
                print(decimal2text(
                    num,
                    int_units=(('штука', 'штуки', 'штук'), 'f'),
                    exp_units=(('кусок', 'куска', 'кусков'), 'm')))
            else:
                print(num2text(
                    int(num),
                    main_units=(('штука', 'штуки', 'штук'), 'f')))
        except ValueError:
            print (sys.stderr, "Invalid argument {}".format(sys.argv[1]))
        sys.exit()
    unittest.main()
