#!/usr/bin/python3
from datetime import datetime
from chinese_calendar import is_workday
import pandas as pd
import calendar, sys


def get_attendance(df:pd.DataFrame, beginning:datetime, ending:datetime, times=1):
    df = df[df['日期时间'] >= beginning]
    df = df[df['日期时间'] <= ending]
    df = df.groupby('姓名').count()
    df = df[df['日期时间'] >= times]
    return set(df.index)


def print_noshow(name: str, day, period: str):
    print('{}缺{}日{}打卡记录。\r'.format(name, day, period))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        filename = sys.argv[1]
    except IndexError:
        print('需要将考勤记录文件转成csv拖到程序上！')
        input('按任意键退出。')

    df = pd.read_csv(filename)
    df['日期时间'] = pd.to_datetime(df['日期时间'], infer_datetime_format=True)
    year = df.loc[0,'日期时间'].year
    month = df.loc[0,'日期时间'].month
    names = set(df['姓名'].unique())

    for name in names:

        days = calendar.monthrange(year, month)[1]
        for i in range(days):
            day = i+1

            # check if is workday
            if is_workday(datetime(year, month, day)):
                # 上班
                attendance = get_attendance(df, beginning=datetime(year, month, day, 0, 0, 0),
                                            ending=datetime(year, month, day, 9, 10, 0))
                # noshow = name - attendance
                if name not in attendance:
                    print_noshow(name, day, '上午签到')

                # 中午
                attendance = get_attendance(df, beginning=datetime(year, month, day, 11, 50, 0),
                                            ending=datetime(year, month, day, 14, 10, 0), times=2)
                attendance1 = get_attendance(df, beginning=datetime(year, month, day, 11, 50, 0),
                                            ending=datetime(year, month, day, 14, 10, 0))
                # noshow = name - attendance1  # 一次打卡都没有
                # noshow1 = name - attendance - noshow  # 有一次打卡
                if name not in attendance1:
                    print_noshow(name, day, '上午签退')
                    print_noshow(name, day, '下午签到')
                if name not in attendance:  # 有一次打卡的记为缺下午签到
                    print_noshow(name, day, '下午签到')

                # 下班
                attendance = get_attendance(df, beginning=datetime(year, month, day, 17, 50, 0),
                                            ending=datetime(year, month, day, 23, 59, 59))
                # noshow = name - attendance
                if name not in attendance:
                    print_noshow(name, day, '下午签退')
            else:
                pass
    input('统计结束，按任意键退出。')