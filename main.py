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
from mail_sender import *

SM = None
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
        psw_query = f"select Password, IsVerified from students where email = '{email}'"
        c.execute(psw_query)
        psw_records =  c.fetchone() 
        print(psw_records)
        mydb.commit()
        if password == psw_records['Password']:
            if psw_records['IsVerified'] == 1:
                SM.current = "home_page"
                SM.transition.direction = "up"
                toast("Login Successful!")
                return True
            else:
                toast("Please verify your email first!")
                SM.current = "verification"
                return False
        else:
            toast("Wrong email or password!")
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
        global SM
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

        # self.manager.current = "login"
        
        if self.email not in email_lst:
            print("Password is valid 1, continue...")
            if self.username != "" and self.email != "" and self.email.count("@") == 1 and self.email.count(".") > 0:
                print("Password is valid 2, continue...")
                if self.password != "" and self.confirm_password != "" and self.password == self.confirm_password and len(self.password) >= 6 and re.search(r"\d", self.password)  and re.search(r"[A-Z]", self.password) and re.search(r"[a-z]", self.password) :
                    verification_code = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(6))
                    info_quary = "insert into students (StudentName, Email, Password, VerifyCode, IsVerified) values (%s, %s, %s, %s, %s)"
                    c.execute(info_quary, (self.username, self.email, self.password, verification_code, 0)) 
                    course_quary = "insert into courses (Email, CanCourse_1, CanCourse_2, CanCourse_3, NeedCourse_1, NeedCourse_2 ) values (%s, %s, %s, %s, %s, %s)"
                    c.execute(course_quary, (self.email, self.courses_g1, self.courses_g2, self.courses_g3, self.courses_b1, self.courses_b2)) 
                    mydb.commit()
                    mydb.close()
                    print("\n\n" + str(self.email))
                    sendEmailVerification(verification_code, str(self.email))
                    toast("Everything is OK so far!")
                    SM.current = "verification"
                    toast("Verification Code has been sent to your email.")
                else: 
                    if self.password != self.confirm_password: 
                        toast("Password doesnt match")
                    else: 
                        toast("Please check password")
        elif self.email in email_lst:
            c = mydb.cursor()
            email_quary = f"select email from students"
            c.execute(email_quary)
            email_records =  c.fetchall() 
            mydb.commit()
            toast("Email already exists")
            toast("Invalid user")

class VerificationPage(Screen):
    pass

class ProfilePage(Screen): 
    
    def get_student_id(self, email):
        mydb = mysql.connect(
			host = db_host, 
			user = db_user,
			passwd = db_password,
			database = db_name,
            )

		# Create A Cursor
        c = mydb.cursor()
        """Hämtar användarens ID från databasen"""
        studnet_id = f"select StudentId from students where Email = '{email}'"
        c.execute(studnet_id)
        result = c.fetchone()
        mydb.commit()
        result2 = result[0]

        return result2

    def update_profile_info(self, id, new_name, password):
        mydb = mysql.connect(
			host = db_host, 
			user = db_user,
			passwd = db_password,
			database = db_name,
            )

		# Create A Cursor
        c = mydb.cursor()
        """Uppdaterar användarens profil vid begäran"""
        c.execute(f"SET SQL_SAFE_UPDATES = 0")
        update = f"UPDATE  Students SET StudentName = '{new_name}', Password ='{password}' where StudentID = {id}"

        
        c.execute(update)
        mydb.commit()
        print(id, new_name, password)

    def update_profile_courses(self, email, good_c1, good_c2, good_c3, bad_c1, bad_c2):
        mydb = mysql.connect(
			host = db_host, 
			user = db_user,
			passwd = db_password,
			database = db_name,
            )

		# Create A Cursor
        c = mydb.cursor()
        """Uppdaterar användarens profil vid begäran"""
        c.execute(f"SET SQL_SAFE_UPDATES = 0")
    
        update_course = f"UPDATE  courses SET CanCourse_1 = '{good_c1}', CanCourse_2 = '{good_c2}', CanCourse_3 = '{good_c3}', NeedCourse_1 = '{bad_c1}', NeedCourse_2 = '{bad_c2}' where Email = '{email}'"
        c.execute(update_course)
        mydb.commit()
        print(good_c1, good_c2, good_c3, bad_c1, bad_c2 )


class MainApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Builder.load_file('login-page.kv'))
        self.sm.add_widget(Builder.load_file('sign_up2.kv'))
        self.sm.add_widget(Builder.load_file('verification.kv'))
        #self.sm.add_widget(Builder.load_file('navbar.kv'))
        self.sm.add_widget(Builder.load_file('navbar2.kv'))
        global SM
        SM = self.sm
        return self.sm
    

    def created_account(self):
        name = str(self.sm.get_screen("create_an_account").ids.new_user.text).strip()
        email = self.sm.get_screen("create_an_account").ids.new_email.text
        
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
        
    
    def verify_code(self):
        email = str(self.sm.get_screen('create_an_account').ids.new_email.text).strip()
        if email == "":
            email = str(self.sm.get_screen('login').ids.user_email.text).strip()
        mydb = mysql.connect(
			host = db_host, 
			user = db_user,
			passwd = db_password,
			database = db_name,
            )

        c = mydb.cursor(dictionary=True) 
        vc_query = f"select VerifyCode from students where email = '{email}'"
        c.execute(vc_query)
        vc_records =  c.fetchone() 
        print(vc_records)
        mydb.commit()
        inputted_verfication_code = self.sm.get_screen('verification').ids.user_verification_code.text
        if vc_records['VerifyCode'] == inputted_verfication_code:
            verified_query = f"update students set IsVerified = 1 where Email = '{email}'"
            print(verified_query)
            c = mydb.cursor()
            c.execute(verified_query)
            mydb.commit()
            toast("Verification Successful")
            self.sm.current = "login"

    def update_profile(self):
        """Funktion som skickar den nya profil informationen till update_profile_info som sedan updaterar databasen"""
        student_email = self.sm.get_screen('login').ids.user_email.text
        name = self.sm.get_screen('home_page').ids.edit_user.text
        password = self.sm.get_screen('home_page').ids.profile_password.text
        #conf_password = self.sm.get_screen('home_page').ids.conf_password.text
        good_course1 = self.sm.get_screen('home_page').ids.good_c1.text
        good_course2 = self.sm.get_screen('home_page').ids.good_c2.text
        good_course3 = self.sm.get_screen('home_page').ids.good_c3.text
        bad_course1 = self.sm.get_screen('home_page').ids.bad_b1.text
        bad_course2 = self.sm.get_screen('home_page').ids.bad_b2.text

        user_id = ProfilePage().get_student_id(student_email) 
        ProfilePage().update_profile_info(user_id, name, password)
        ProfilePage().update_profile_courses(student_email, good_course1, good_course2, good_course3, bad_course1, bad_course2)


if __name__ == '__main__':
    MainApp().run()
    # print(LoginWindow().validate('ssarwar@pm.me', 'AaAa12'))
