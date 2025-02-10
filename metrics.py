import datetime

print(datetime.datetime.now()-datetime.datetime(2020,10,7))

def format_timedelta(timedelta):
    total_days = timedelta.days
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    return f"{years} años, {months} meses, {days} días"

def solvingTime(item : tuple):
    dif = item[5]-item[3]
    return format_timedelta(dif)

def attendingTime(item : tuple):
    dif = item[4]-item[3]
    return format_timedelta(dif)
