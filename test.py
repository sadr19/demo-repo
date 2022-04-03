import email
from kivymd.app import MDApp
from kivy.lang import Builder
import kivy
from matplotlib.pyplot import text
kivy.require('1.0.8')
from kivymd.uix.list import IconRightWidget, ThreeLineAvatarIconListItem
import mysql.connector as mysql
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivymd.toast import toast
from  kivy.uix.floatlayout import FloatLayout
import re
import random, string

from db_creds import *

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self, email, password):
        mydb = mysql.connect(
			host = db_host, 
			user = db_user,
			passwd = db_password,
			database = db_name,
            )

        c = mydb.cursor(dictionary=True) 
        psw_query = f"select Password from students where email = '{email}'"
        c.execute(psw_query)
        psw_records =  c.fetchone() 
        mydb.commit()
        print("psw_records", psw_records)
        if password == psw_records:
            return True

        else:
            return False 
    
class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm_password= ObjectProperty(None)
    courses_g1 = StringProperty(None)
    courses_g2 = StringProperty(None)
    courses_g3 = StringProperty(None)
    courses_b1 = StringProperty(None)
    courses_b2 = StringProperty(None)
    
    def __init__(self, username, email, password, confirm_password, courses_g1,  courses_g2, courses_g3, courses_b1, courses_b2): 
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.courses_g1 = courses_g1
        self.courses_g2 = courses_g2
        self.courses_g3 = courses_g3
        self.courses_b1 = courses_b1
        self.courses_b2 = courses_b2

    
    def register(self): 
        
		# Define DB Stuff
        mydb = mysql.connect(
			host = db_host, 
			user = db_user,
			passwd = db_password,
			database = db_name,
            )

		# Create A Cursor
        c = mydb.cursor()
        email_quary = f"select email from students"
        c.execute(email_quary)
        email_records =  c.fetchall() 
        mydb.commit()
        email_lst = list(email_records)
        print(email_lst)
         
        if self.email not in email_lst:   
            if self.username != "" and self.email != "" and self.email.count("@") == 1 and self.email.count(".") > 0:
                if self.password != "" and self.confirm_password != "" and self.password != self.confirm_password and len(self.password) >= 6 and re.search(r"\d", self.password)  and re.search(r"[A-Z]", self.password) and re.search(r"[a-z]", self.password) :
                    verification_code = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(6))
                    info_quary = "insert into students (StudentName, Email, Password, VerifyCode) values (%s, %s, %s)"
                    c.execute(info_quary, (self.username, self.email, self.password, verification_code)) 
                    course_quary = "insert into courses (Email, CanCourse_1, CanCourse_2, CanCourse_3, NeedCourse_1, NeedCourse_2 ) values (%s, %s, %s, %s, %s, %s)"
                    c.execute(course_quary, (self.email, self.courses_g1, self.courses_g2, self.courses_g3, self.courses_b1, self.courses_b2)) 
                    mydb.commit()
                    mydb.close()
                    toast("Account Created Successfully")
                else: 
                    if self.password != self.confirm_password: 
                        toast("Password doesnt match")
                    else: 
                        toast("Please check password")
        elif self.email in email_lst:
            toast("Invalid user")
    
    




class MainApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Builder.load_file('login-page.kv'))
        self.sm.add_widget(Builder.load_file('sign_up2.kv'))
        self.sm.add_widget(Builder.load_file('navbar.kv'))
        self.sm.add_widget(Builder.load_file('navbar2.kv'))


        return self.sm

    def created_account(self):
        name = self.sm.get_screen("create_an_account").ids.new_user.text
        email = self.sm.get_screen("§create_an_account").ids.new_email.text
        
        password = self.sm.get_screen("create_an_account").ids.new_password.text
        confirm_password = self.sm.get_screen("create_an_account").ids.new_conf_password.text
        courses_g1 = self.sm.get_screen("create_an_account").ids.good_c1.text
        courses_g2 = self.sm.get_screen("create_an_account").ids.good_c2.text
        courses_g3 = self.sm.get_screen("create_an_account").ids.good_c3.text
        courses_b1 = self.sm.get_screen("create_an_account").ids.bad_b1.text
        courses_b2 = self.sm.get_screen("create_an_account").ids.bad_b2.text

        CreateAccountWindow(name, email, password, confirm_password, courses_g1, courses_g2, courses_g3, courses_b1, courses_b2).register()

    def login_valid(self):
        email = self.sm.get_screen("login").ids.user_email.text
        psw = self.sm.get_screen("login").ids.user_password.text
        validation_status = LoginWindow().validate(email, psw)
        if validation_status:
            toast("success")
        else: 
            toast("invalid")

    
