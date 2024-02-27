from collections import UserDict
import re
import datetime as dt
from datetime import datetime as dtdt


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Номер телефону має містити 10 цифр.") 
        super().__init__(value)
        
class Birthday(Field):
    def __init__(self, value):
        try:
            patern=r'(\d{2})\.(\d{2})\.(\d{4})'
            if re.match(patern,value):
                self.value = dtdt.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
class Record:
    def __init__(self, name):
        self.name =Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self,phone):
        self.phones.append(Phone(phone))
        

    def remove_phone(self,phone):
        if phone in self.phones:
            self.phones.remove(phone)


    def edit_phone(self,phone_old,phone_new):
        for p in self.phones:
            if p.value == phone_old:
                p.value = phone_new
                break


    def find_phone(self,phone):
        if phone in self.phones:
            return phone
        
    def add_birthday(self,birthday):
        self.birthday=Birthday(birthday)
        

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    # реалізація класу
    book={}      
    def add_record(self,record):
        self.data[record.name.value]=record

    def find(self,name):
        return self.data.get(name)
		
    def delete(self,name):
        if name in self.data:
            del self.data[name]

    def birthdays(self):
        today_date=dtdt.today().date()
        birthdays=[]
        for user in self:
            user_record = self[user]
            birth_date=user_record.birthday.value
            birth_date = birth_date.replace(year=today_date.year)
            birth_date=birth_date.date()
            w_day=birth_date.isoweekday()
            days_difference=(birth_date-today_date).days
            if 0<=days_difference<7:
                if w_day<6:
                    birthdays.append({'name':user_record.name,'birthday':birth_date.strftime("%Y.%m.%d")})
                else:
                    if (birth_date+dt.timedelta(days=1)).weekday()==0:
                        birthdays.append({'name':user_record.name, 'birthday':(birth_date+dt.timedelta(days=1)).strftime("%Y.%m.%d")})
                    elif (birth_date+dt.timedelta(days=2)).weekday()==0: 
                        birthdays.append({'name':user_record.name, 'birthday':(birth_date+dt.timedelta(days=2)).strftime("%Y.%m.%d")})     
        return birthdays