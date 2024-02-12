''' The console bot assistant recognizes the following commands entered from the keyboard:
        "hello"    - responds to a greeting with a phrase: "How can I help you?"
        "add"      - Adds a new contact to the phone book
        "change"   - Replaces the phone number for an existing user
        "phone"    - Print the phone number of the specified user to the console
        "show all" - Output all saved contacts to the console
        "good bye", "close", "exit" - Finishing work '''
        
dict_user = dict()                               # Phonebook

''' Decorator. Exception Handling '''
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            return f'Error: Command not recognized "{args[0]}". \nPlease re-enter: '
        except IndexError:
            return f'Error: Invalid number of parameters "{args[0]}". \nPlease re-enter: '
        except ValueError:
            return f'Error: User "{args[0]}". Not in the phonebook\nPlease re-enter: '
        return result
    return wrapper

''' Decorator. Controlling command parameters '''
def check_param(from_func):
    def check(func):
        def wrapper(list_param):
            if from_func == 'add' or from_func == 'change':
                if len(list_param) != 2:
                    raise IndexError
                name_user, phone_user = list_param
            elif from_func == 'phone':
                if len(list_param) != 1:
                    raise IndexError
                name_user = list_param[0]
                phone_user = '0000000'
                
            if not name_user.isalnum():
                return f'Username "{name_user}" contains invalid characters'+\
                        ' \nPlease re-enter: '
    
            phone_nom = phone_user.replace('-','')
            if not phone_nom.isdigit():
                return f'Phone number "{phone_user}" contains invalid characters'+\
                        ' \nPlease re-enter: '
    
            if len(phone_nom) != 7:
                return f'Phone number "{phone_user}" must contain 7 digits'+\
                        ' \nPlease re-enter: '
    
            return func(list_param, dict_user)                 # Ошибок не обнаружено
        return wrapper
    return check

def hello(list_param):
    return 'How can I help you? '

''' Add a new user '''
@check_param('add')
def add(list_param, dict_user):
    name_user, phone_user = list_param
    if dict_user.get(name_user) == None:
        dict_user[name_user] = phone_user
        return f'User added: "{name_user}" phone: "{phone_user}"'+\
                '\nContinue typing: '
    else:
        return f'User "{name_user}" already in the phonebook '+\
                '\nContinue typing: '

''' Replacing a phone number '''
@check_param('change')
def change(list_param, dict_user):
    name_user, phone_user = list_param
    old_phone = dict_user.get(name_user)
    if old_phone != None:
        dict_user[name_user] = phone_user
        return f'For user: "{name_user}" phone number: "{old_phone}"' + \
               f' has been replaced by: "{phone_user}"' + \
                '\nContinue typing: '
    else:
        return f'User "{name_user}" not in phonebook ' + \
                '\nPlease re-enter: '
    
''' Show user's phone number '''
@check_param('phone')
def phone(list_param, dict_user):
    try:
        text_return = f'User "{list_param[0]}"  phone:  - "{dict_user[list_param[0]]}"' + \
                       '\nContinue typing: '
    except:
        raise ValueError
    return text_return

def exit(list_param):
    return 'exit'

''' Processing information entered from the console '''
@input_error
def handler(msg: str, dict_comand):
    ''' We convert the line from the console into a list, using a space as a separator.
        If there is more than one space between words, then the resulting empty lines are ignored '''    
    list_param = tuple(filter(lambda x: x, msg.split(' ')))
    func = dict_comand[list_param[0]]   # Name of the function for processing the list of parameters
    list_param = list_param[1:]         # Command Options
    return func(list_param)                      

''' Dictionary where: Key - command received from the console
                    Value - function to process this command '''
dict_command = {
    'hello'    : hello,
    'add'      : add,
    'change'   : change,
    'phone'    : phone,
    'close'    : exit,
    'exit'     : exit
}

if __name__ == "__main__":
    msg_bot = "The assistant bot welcomes you. I'm waiting for the command to be entered: "
    while msg_bot != 'exit':
        msg_user = input(msg_bot).lower().replace('good bye', 'exit')
        if 'show all' in msg_user:
            for user_name, user_phone in dict_user.items():
                print("|{:^12}|{:^10}|".format(user_name, user_phone))
            msg_bot = "I'm waiting for the command to be entered: "
        else:
            msg_bot  = handler(msg_user, dict_command)
        
    print('Good bye!')     
