from collections import UserDict
from collections.abc import Iterator
from datetime import date
from datetime import datetime
from random import randrange
import time

class Field:
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    
    def __init__(self, value):
        super().__init__(value)
        self.__value = value
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value


class Phone(Field):
    
    def __init__(self, value):
        self.__value = value
        self.check_phone(value)
        
    def check_phone(self, phone):
        if not phone.isdigit():
            raise ValueError(f'There is an invalid character in number "{phone}"')
        if len(phone) != 10:
            raise ValueError(f'Number "{phone}" must have 10 digits')
        return phone
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = self.check_phone(value)
        
        
class Birthday(Field):
    
    def __init__(self, value):
        super().__init__(value)
        self.__value = value
        self.check_birthday(value)
        
    def check_birthday(self, value):
        value = value.replace('.', '').replace('/','')
        try:
            self.__value = time.strptime(value, '%d%m%Y')
            return self.__value
        except:
            raise ValueError(f'Date format error {value}')
        
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = self.check_birthday(value)
        

class Record:
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def days_to_birthday(self):
        current_date = date.today()
        birthday = self.birthday.value
        year = current_date.year
        month = birthday.tm_mon
        day = birthday.tm_mday
        birthday = date(year, month, day)
        if birthday < current_date:
            birthday = date(year + 1, month, day)
        return (birthday - current_date).days
    
    def add_phone(self, phone, birthday=None):
        self.phone = Phone(phone)
        self.phones.append(self.phone)
        if birthday != None:
            self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        self.phone = Phone(phone)
        for p in self.phones:
            if p.value == self.phone.value:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        self.old_phone = Phone(old_phone)
        self.new_phone = Phone(new_phone)
        for p in self.phones:
            if p.value == self.old_phone.value:
                p.value = self.new_phone.value
                return True 
        raise ValueError       

    def find_phone(self, phone):
        self.phone = Phone(phone)
        for p in self.phones:
            if p.value == self.phone.value:
                return p
    
    def __str__(self):
        if hasattr(self, 'birthday'):
            birthday_date = time.strftime('%d.%m.%Y', self.birthday.value)
            birthday_txt = f'Birthday: {birthday_date} days left: {self.days_to_birthday()}'
        else:
            birthday_txt = ''
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)} {birthday_txt}"


class AddressBook(UserDict):
    
    def iterator(self, max_value):
        self.max_value = max_value
        self.tmp_book = {}
        self.count_str = 1
        for key, value in self.data.items():
            self.tmp_book[key] = self.data[key]
            if self.count_str == self.max_value:
                yield self.tmp_book
                self.count_str = 0
                self.tmp_book.clear()
            self.count_str += 1
            
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, user):
        self.user = user
        return self.data.setdefault(self.user)
    
    def delete(self, user):
        self.user = user
        self.data.pop(self.user, None)
    
    
try:
    # Creating a new address book
    book = AddressBook()
    nom_phone = 1234567000
    for i in range(50):
        name_record = 'Name' + '0' + str(i) if i < 10 else 'Name' + str(i)
        job_record  = Record(name_record)
        year = str(randrange(1980, 2000))
        month = str(randrange(1, 12))
        day = str(randrange(1, 28))
        for j in range(3):
            nom_phone += 1
            if j == 2 and i % 2 == 0:
                job_record.add_phone(str(nom_phone), day+'.'+month+'.'+year)
            else:
                job_record.add_phone(str(nom_phone))
        book.add_record(job_record)
    print('---------------------------------------------------------------------------')
    
    # Output of all entries in the book page by page
    
    print_part = book.iterator(10)
    for page in print_part:
        for name, record in page.items():
           print(record)
        print('---------------------------------------------------------------------------')
        
except ValueError:
     raise
