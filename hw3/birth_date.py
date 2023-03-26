from datetime import datetime, timedelta
from collections import defaultdict
from pprint import pprint

# початок наступного тижня
def get_next_week(d: datetime):
    diff_days = 7 - d.weekday()
    return d + timedelta(days=diff_days)

def prepare_birthday(text: str):
    bd = datetime.strptime(text, '%Y-%m-%d')
    return bd.replace(year=datetime.now().year).date()

def get_birthdays_per_week(users):

    birthdays = defaultdict(list)

    today = datetime.now().date()

    next_week = get_next_week(today)
    start_period = next_week - timedelta(2)
    end_period = next_week + timedelta(4)
    print(f"Дні народження в період з {start_period} по {end_period} : \n" )

    happy_users = [user for user in users if start_period <= prepare_birthday(user['birthday']) <= end_period]
    
    for user in happy_users:
        curr_bd = prepare_birthday(user['birthday'])
        if curr_bd.weekday() in (5,6):
            birthdays['Monday'].append(user['name'])
        else:
            birthdays[curr_bd.strftime('%A')].append(user['name'])


    for day, users in birthdays.items():
        if users:
            print(f"Вітаємо іменинників в '{day}' >>> '{', '.join(users)}' \n")

    return birthdays
   
if __name__ == '__main__':
    
    users =[
            {'name': 'Luffi', 'birthday': '2005-03-20'},
            {'name': 'Zoro', 'birthday': '2004-03-21'},
            {'name': 'Nami', 'birthday': '2005-03-21'},
            {'name': 'Ussopp', 'birthday': '2007-03-18'},
            {'name': 'Sanji', 'birthday': '2005-03-19'},
            {'name': 'Chopper', 'birthday': '2010-03-20'},
            {'name': 'Robin', 'birthday': '1998-03-21'},
            {'name': 'Franky', 'birthday': '1999-03-22'},
            {'name': 'Brook', 'birthday': '1989-03-25'},
            {'name': 'Jimbey', 'birthday': '1980-03-26'}
        ]
    
    result = get_birthdays_per_week(users)
    
    # pprint(result)