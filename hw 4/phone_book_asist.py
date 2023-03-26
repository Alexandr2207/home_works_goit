import re
users = {}

def input_error(func):
    def inner(*args):
        try: 
            return func(*args)
        except KeyError:
            return f"Параметр не знайдено {' '.join(args)}"
        except ValueError:
            return "Параметр повинен бути у відповідному форматі.\
                Щоб дізнатися більше напишіть 'допомогти' ."
        except IndexError:
            return "Введіть усі параметри для команди. Для допомоги напишіть 'допомогти'."
    return inner

def cmd_hello_func(): 
    return "Чим я можу бути корисним?"

@input_error
def cmd_add_func(*args):
    name = args[0]
    phone = args[1]

    if not re.match(r"^\+[\d]{12}$", phone):
        raise ValueError

    if name in users:
        return f"Ім'я ' {name} ' уже зареєстроване в телефонній книзі.\
            Надайте інше ім'я, або змініть номер телефону командою 'змінити'."
    elif phone in users.values():
        return f"Наданий вами номер телефону: {phone}, уже зареєстровний в телефонній книзі."
    else:
        users.update({name: phone})
        return f"{name} {phone} успішно зареєстровано в телефонну книгу."

@input_error
def cmd_change_func(*args):
    name = args[0]
    phone = args[1]

    if name not in users:
        return f"Ім'я ' {name} ' не зареєстроване в телефонній книзі."
    elif phone in users.values():
        return f"Наданий вами номер телефону: ' {phone} ', уже зареєстровний в телефонній книзі."
    else:
        users[name] = phone    
    return f"Номер телефону для ім'я '{name}' успішно змінено на: '{phone}'."

@input_error
def cmd_phone_func(*args):
    name = args[0]
    phone = users[name]
    return f"Номер телефону для '{name}' : '{phone}'."

def cmd_show_all_func(*args):
    all = ""
    if len(users) == 0:
        return "Телефонна книга пуста"
    else:
        for name, phone in users.items():
            all += name + ": " + phone + "\n"
        return all

def cmd_help(*args):
    return """Ви можете керувати телефонною книгою за допомоги наступних команд:
          привіт
          додати - щоб додати контакт введіть 'Ім'я' та номер телефону у такому форматі '+380123456789' 
          змінити - щоб змінити контакт введіть 'Ім'я' та номер телефону у такому форматі '+380123456789'
          номер - для перевірки номеру введіть 'Ім'я'
          показати всі - показує усі контакти у телефонній книзі
          бувай
          закрити
          вийти"""

def cmd_exit_func(*args): 
    return "До побачення!\n"

COMMANDS = {
    'привіт': cmd_hello_func,
    'додати': cmd_add_func,
    'змінити': cmd_change_func,
    'номер': cmd_phone_func,
    'показати всі': cmd_show_all_func,
    'бувай': cmd_exit_func,
    'закрити': cmd_exit_func,
    'вийти': cmd_exit_func,
    'допомогти': cmd_help,
}

def cmd_parser(command_line: str):
    for cmd in COMMANDS:
        if command_line.startswith(cmd):
            return COMMANDS[cmd], command_line.replace(cmd, '').strip().split()
    return None, []

def main():
    command_line = ""
    print("\nПривіт!")
    print(cmd_help())
    while True:
        command_line = input("\nВведіть команду: ")

        command, data = cmd_parser(command_line)

        if not command:
            print("Немає такої команди. Спрбуйте ще раз, або напишіть 'допомогти'!")
            continue

        print(command(*data))

        if command == cmd_exit_func:
            break

if __name__ == "__main__":
    main()