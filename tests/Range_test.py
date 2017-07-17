import os
import time
import unittest
from datetime import datetime, date, timedelta
from math import floor

from timestring import Range


def add_months(d, x):
    new_month = ((d.month - 1 + x) % 12) + 1
    new_year = d.year + floor((((d.month - 1) + x) / 12))
    return datetime(new_year, new_month, d.day)


def add_years(d, x):
    return date(d.year + x, d.month, d.day)


class RangeTest(unittest.TestCase):
    def assert_range(self, _range, expected_start, expected_end,
                     hours=False, minutes=False, seconds=False):
        self.assertEqual(_range.start.month, expected_start.month)
        self.assertEqual(_range.end.month, expected_end.month)
        self.assertEqual(_range.start.day, expected_start.day)
        self.assertEqual(_range.end.day, expected_end.day)
        self.assertEqual(_range.start.year, expected_start.year)
        self.assertEqual(_range.end.year, expected_end.year)
        if hours:
            self.assertEqual(_range.start.hour, expected_start.hour)
            self.assertEqual(_range.end.hour, expected_end.hour)
        if minutes:
            self.assertEqual(_range.start.minute, expected_start.minute)
            self.assertEqual(_range.end.minute, expected_end.minute)
        if seconds:
            self.assertEqual(_range.start.second, expected_start.second)
            self.assertEqual(_range.end.second, expected_end.second)

    def test_months(self):
        start = datetime.now().replace(day=1, month=12)
        end = datetime(start.year + 1, 1, 1)
        self.assert_range(Range('December'),
                          start,
                          end)

        start = datetime(2017, 1, 1)
        end = datetime(2017, 2, 1)
        self.assert_range(Range('January 2017'),
                          start,
                          end)

        start = datetime.now().replace(day=1)
        end = add_months(start, 1)
        self.assert_range(Range('this month'),
                          start,
                          end)

        start = datetime.now()
        end = add_months(start, 2)
        self.assert_range(Range('next 2 months'),
                          start,
                          end)

        start = add_months(datetime.now(), -24)
        end = datetime.now()
        self.assert_range(Range('last 24 months'),
                          start,
                          end)

        start = datetime.now()
        end = add_months(start, 1)
        self.assert_range(Range('upcoming month'),
                          start,
                          end)

    def test_dates(self):
        self.assert_range(Range('2016 25 December'),
                          datetime(2016, 12, 25),
                          datetime(2016, 12, 26))

        start = datetime.now().replace(day=25, month=12)
        end = datetime.now().replace(day=26, month=12)
        self.assert_range(Range('December 25th'),
                          start,
                          end)

        start = datetime(2010, 1, 10)
        end = datetime(2010, 1, 20)
        self.assert_range(Range('from january 10th 2010 to jan 20th 2010'),
                          start,
                          end)

    def test_week(self):
        start = datetime.now() + timedelta(days=-7)
        end = datetime.now()
        self.assert_range(Range('last week'),
                          start,
                          end)

        start = datetime.now()
        end = datetime.now() + timedelta(days=7)
        self.assert_range(Range('next week'),
                          start,
                          end)

    def test_year(self):
        start = add_years(datetime.now(), -1)
        end = datetime.now()
        self.assert_range(Range('last year'),
                          start,
                          end)

        start = datetime.now()
        end = add_years(datetime.now(), 1)
        self.assert_range(Range('next year'),
                          start,
                          end)

    def test_days(self):
        start = datetime.now()
        end = datetime.now() + timedelta(days=2)
        self.assert_range(Range('next 2 days'),
                          start,
                          end)

        start = datetime.now() + timedelta(days=1)
        end = datetime.now() + timedelta(days=2)
        self.assert_range(Range('tomorrow'),
                          start,
                          end)

        start = datetime.now() + timedelta(days=2)
        end = datetime.now() + timedelta(days=3)

        self.assert_range(Range('day after tomorrow'),
                          start,
                          end)

        start = datetime.now() + timedelta(days=-1)
        end = datetime.now()
        self.assert_range(Range('yesterday'),
                          start,
                          end)

        start = datetime.now() + timedelta(days=-2)
        end = datetime.now() + timedelta(days=-1)
        self.assert_range(Range('day before yesterday'),
                          start,
                          end)

    def test_weekday_today(self):
        # for past days of week
        # if today is Wednesday, 'Wednesday' = 'this Wednesday'
        # 'next Wednesday' = Wednesday of next week
        # 'last Wednesday' = Wednesday of last week
        today = datetime.now().strftime('%A')

        start = datetime.now()
        end = datetime.now() + timedelta(days=1)
        self.assert_range(Range(today),
                          start,
                          end)

        self.assert_range(Range('this ' + today),
                          start,
                          end)

        start = datetime.now() + timedelta(days=7)
        end = datetime.now() + timedelta(days=7 + 1)
        self.assert_range(Range('next ' + today),
                          start,
                          end)

        start = datetime.now() + timedelta(days=-7)
        end = datetime.now() + timedelta(days=-7 + 1)
        self.assert_range(Range('last ' + today),
                          start,
                          end)

    def test_prev_weekday(self):
        # for past days of week
        # if today is Wednesday, 'Tuesday' = 'this Tuesday' = 'next Tuesday'
        yesterday = datetime.now() + timedelta(days=-1)
        day_text = yesterday.strftime('%A')

        start = datetime.now() + timedelta(days=-1 + 7)
        end = datetime.now() + timedelta(days=-1 + 7 + 1)
        self.assert_range(Range(day_text),
                          start,
                          end)

        self.assert_range(Range('this ' + day_text),
                          start,
                          end)

        self.assert_range(Range('next ' + day_text),
                          start,
                          end)

        start = datetime.now() + timedelta(days=-1)
        end = datetime.now()
        self.assert_range(Range('last ' + day_text),
                          start,
                          end)

    def test_next_weekday(self):
        # for future days of week
        # if today is Wednesday, 'Thursday' = 'this thursday' = 'next thursday'
        tomorrow = datetime.now() + timedelta(days=1)
        day_text = tomorrow.strftime('%A')

        start = datetime.now() + timedelta(days=1)
        end = datetime.now() + timedelta(days=2)
        self.assert_range(Range(day_text),
                          start,
                          end)

        self.assert_range(Range('this ' + day_text),
                          start,
                          end)

        self.assert_range(Range('next ' + day_text),
                          start,
                          end)

        start = datetime.now() + timedelta(days=1 - 7)
        end = datetime.now() + timedelta(days=1 - 7 + 1)
        self.assert_range(Range('last ' + day_text),
                          start,
                          end)

    def test_range_with_time(self):
        start = datetime.now().replace(hour=14, minute=0, second=0)
        end = datetime.now().replace(hour=16, minute=0, second=0)
        self.assert_range(Range('from 2 PM to 4PM'),
                          start, end,
                          hours=True, minutes=True, seconds=True)

        start = datetime.now() + timedelta(hours=-5)
        end = datetime.now()
        self.assert_range(Range('last 5 hours'),
                          start, end,
                          hours=True, minutes=True, seconds=True)

        start = datetime.now()
        end = datetime.now() + timedelta(hours=4)
        self.assert_range(Range('next 4 hours'),
                          start, end,
                          hours=True, minutes=True, seconds=True)

        start = datetime(2016, 1, 10, 5)
        end = datetime(2016, 1, 10, 9)
        self.assert_range(Range('from jan 10 2016 5 am to jan 10, 2016 9 am'),
                          start,
                          end,
                          hours=True, minutes=True, seconds=True)

    @unittest.skip("skipping failing tests")
    def failing_tests(self):
        start = datetime(2016, 1, 10, 5)
        end = datetime(2016, 1, 10, 9)
        self.assert_range(Range('from jan 10 2016 5 am to 9 am'),
                          start,
                          end,
                          hours=True, minutes=True, seconds=True)

        start = datetime.now() + timedelta(days=-2)
        end = datetime.now()
        self.assert_range(Range('last 2 days'),
                          start,
                          end)

        start = add_months(datetime.now(), -5)
        end = datetime.now()
        self.assert_range(Range('last 5 months'),
                          start,
                          end)


def main():
    os.environ['TZ'] = 'UTC'
    time.tzset()
    unittest.main()


if __name__ == '__main__':
    main()
