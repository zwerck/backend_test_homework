from __future__ import annotations
import datetime


class Calculator:
    def __init__(self, limit, records=None):
        if records is None:
            records = []
        self.limit = limit
        self.records = records

    def add_record(self, obj: Record):
        self.records.append(obj)
        return self.records

    def get_today_stats(self):
        now = datetime.datetime.now()
        today_date = now.date()
        wasted = 0
        for item in self.records:
            if item.date == today_date:
                wasted += abs(item.amount)
        return wasted

    def get_week_stats(self):
        now = datetime.datetime.now()
        today_date = now.date()
        week_ago_date = today_date - datetime.timedelta(days=7)
        week_wasted = 0
        for item in self.records:
            if week_ago_date <= item.date <= today_date:
                week_wasted += item.amount
        return week_wasted


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            now = datetime.datetime.now()
            self.date = now.date()
        else:
            date_format = '%d.%m.%Y'
            moment = datetime.datetime.strptime(date, date_format)
            moment = moment.date()
            self.date = moment


class CashCalculator(Calculator):
    USD_RATE = 73.78
    EURO_RATE = 89.78

    def get_today_cash_remained(self, currency):
        if currency != 'rub' and currency != 'usd' and currency != 'eur':
            return f'Извините, мы не работаем с валютой {currency} =('
        difference = self.limit - Calculator.get_today_stats(self)
        if difference > 0:
            if currency == 'usd':
                difference = round(difference / self.USD_RATE, 2)
                return f'На сегодня осталось {difference} USD'
            elif currency == 'eur':
                difference = round(difference / self.EURO_RATE, 2)
                return f'На сегодня осталось {difference} Euro'
            else:
                return f'На сегодня осталось {difference} руб'
        elif Calculator.get_today_stats(self) == self.limit:
            return 'Денег нет, держись'
        elif difference < 0:
            difference = abs(difference)
            if currency == 'usd':
                difference = round(difference / self.USD_RATE, 2)
                return f'Денег нет, держись: твой долг - {difference} USD'
            elif currency == 'eur':
                difference = round(difference / self.EURO_RATE, 2)
                return f'Денег нет, держись: твой долг - {difference} Euro'
            else:
                return f'Денег нет, держись: твой долг - {difference} руб'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if Calculator.get_today_stats(self) < self.limit:
            difference = self.limit - Calculator.get_today_stats(self)
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {difference} кКал'
        if Calculator.get_today_stats(self) >= self.limit:
            return 'Хватит есть!'
