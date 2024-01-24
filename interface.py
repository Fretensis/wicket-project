import customtkinter as ctk
import CardUser as cu
import datetime as dt
import threading
import time
import log
from tkinter import IntVar
from PIL import Image

class App(ctk.CTk):

	user_arr = cu.CardUser.user_arr
	defaultUser = user_arr[0]

	logs_new = open('logs.txt', 'w+')
	logs_new.close()

	def __init__(self):
		super().__init__()

		self.radio_var = IntVar(value=0)
		self.check_radioButton = 0

		self.geometry("600x450")
		self.title("Wicket Project")
		self.resizable(False, False)

		# Logo
		self.main_text = ctk.CTkFrame(self, 580, 50, bg_color='transparent')
		self.main_text.pack(padx=(10, 10), pady=(10, 10))

		# W O R K S P A C E
		self.menu_sidebar_up = ctk.CTkFrame(self, 200, 181, 10, bg_color='transparent')
		self.menu_sidebar_up.place(x=390, y=70)

		self.menu_sidebar_down = ctk.CTkFrame(self, 200, 181, 10, bg_color='transparent')
		self.menu_sidebar_down.place(x=390, y=259)

		self.wicket = ctk.CTkFrame(self, 370, 370, 10, bg_color='transparent')
		self.wicket.place(x=10, y=70)

		self.text = ctk.CTkTextbox(self.wicket, 351, 61)
		self.text.place(x=10, y=300)

		# картинки
		self.logo = ctk.CTkImage(dark_image=Image.open('WhicketProject.png'), size=(500, 48))
		self.logo_label = ctk.CTkLabel(self.main_text, 500, 50, text='', image=self.logo)
		self.logo_label.place(x=40, y=0)

		self.wicket_open_png = ctk.CTkImage(dark_image=Image.open('wicket_open.png'), size=(241, 280))
		self.wicket_close_png = ctk.CTkImage(dark_image=Image.open('wicket.png'), size=(241, 280))


		#  Данные с карты
		self.info_wicket_1 = ctk.CTkLabel(self.menu_sidebar_up, 100, 10, 10,
		                                  text=(f"Баланс карты: {self.user_arr[0].coins}\n"))
		self.info_wicket_1.place(x=20, y=25)
		self.info_wicket_2 = ctk.CTkLabel(self.menu_sidebar_up, 100, 10, 10,
		                                  text=(f"Срок годности: {self.user_arr[0].date} дней"))
		self.info_wicket_2.place(x=20, y=50)
		self.info_wicket_3 = ctk.CTkLabel(self.menu_sidebar_up, 100, 10, 10,
		                                  text=(f"Блокировка: {self.user_arr[0].block}"))
		self.info_wicket_3.place(x=20, y=75)

		# картинки
		self.wicket_label = ctk.CTkLabel(self.wicket, 241, 280, text='', image=self.wicket_close_png)
		self.wicket_label.place(x=10, y=20)

		# интерактив
		self.btn_put_card = ctk.CTkButton(self.menu_sidebar_down, 120, 30, 5,
		                                  text='Put Card', command=self.put_card_event)
		self.btn_put_card.place(x=40, y=143)

		self.btn_open_db = ctk.CTkButton(self.menu_sidebar_down, 120, 30, 5,
		                                 text='Open ACS Logs', command=self.open_window)
		self.btn_open_db.place(x=40, y=103)

		self.user_var = ctk.CTkOptionMenu(self.menu_sidebar_up, 120, 30, 5,
		                                  values=[self.user_arr[0].name, self.user_arr[1].name, self.user_arr[2].name,
		                                          self.user_arr[3].name], command=self.info_user_event)
		self.user_var.place(x=20, y=140)

		self.btn_restart = ctk.CTkButton(self.menu_sidebar_down, 120, 30, text='Add Coins',
		                                 command=self.add_event)
		self.btn_restart.place(x=40, y=63)

	    # сенсоры
		self.sensor_1 = ctk.CTkRadioButton(self.wicket, variable=self.radio_var,
		                                   value=1, text='Sensor_1', command=self.sensor_event)
		self.sensor_1.place(x=270, y=20)

		self.sensor_2 = ctk.CTkRadioButton(self.wicket, variable=self.radio_var,
		                                   value=2, text='Sensor_2', command=self.sensor_event)
		self.sensor_2.place(x=270, y=50)

		self.sensor_3 = ctk.CTkRadioButton(self.wicket, variable=self.radio_var,
		                                   value=3, text='Sensor_3', command=self.sensor_event)
		self.sensor_3.place(x=270, y=80)
		self.sensor_4 = ctk.CTkRadioButton(self.wicket, variable=self.radio_var,
		                                   value=0, text='Closed', command=self.sensor_event)
		self.sensor_4.place(x=270, y=110)

	def info_user_event(self, values):
		if values == self.user_arr[0].name:
			self.defaultUser = self.user_arr[0]

		elif values == self.user_arr[1].name:
			self.defaultUser = self.user_arr[1]

		elif values == self.user_arr[2].name:
			self.defaultUser = self.user_arr[2]

		else:
			self.defaultUser = self.user_arr[3]

		self.info_wicket_1.configure(text=f"Баланс карты: {self.defaultUser.coins}\n")
		self.info_wicket_2.configure(text=f"Срок годности: {self.defaultUser.date} дней")
		self.info_wicket_3.configure(text=f"Блокировка: {self.defaultUser.block}")

	def put_card_event(self):
		if not (not (self.defaultUser.coins != 0 and self.defaultUser.date != 0) or not (self.defaultUser.block != True)):
			self.check_radioButton = 1
			self.defaultUser.coins = self.defaultUser.coins - 1
			self.info_wicket_1.configure(text=f"Баланс карты: {self.defaultUser.coins}\n")
			self.wicket_label.configure(image=self.wicket_open_png)
			self.text.insert('0.0',
			                 text=f"<{dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} ПРОХОД РАЗРЕШЁН>\n"
			                      f"Cостояние карты:\n" 
			                      f"Баланс карты: {self.defaultUser.coins}; "
			                      f"Cрок годности: {self.defaultUser.date}; "
			                      f"Блок: {self.defaultUser.block};\n"
			                      "-----------------------------------------------\n")
			self.write_logs(value=True)
		else:
			self.closer()#self.wicket_label.configure(image=self.wicket_close_png)
			self.text.insert('0.0',
			                 text=f"<{dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} ПРОХОД ЗАБЛОКИРОВАН>\n"
			                      f"Cостояние карты:\n"
			                      f"Баланс карты: {self.defaultUser.coins}; "
			                      f"Cрок годности: {self.defaultUser.date}; "
			                      f"Блок: {self.defaultUser.block};\n"
			                      "-----------------------------------------------\n")
			self.write_logs(value=False)

	def closer(self):
		if (self.radio_var.get() == 1) or (self.radio_var.get() == 2) or (self.radio_var.get() == 3):
			self.check_radioButton = 0
			self.radio_var.set(0)
			self.wicket_label.configure(image=self.wicket_close_png)
		else:
			self.wicket_label.configure(image=self.wicket_close_png)

	def add_event(self):
		for i in range(10):
			self.defaultUser.coins += 1

		self.info_wicket_1.configure(text=f"Баланс карты: {self.defaultUser.coins}\n")

	def open_window(self):
		logWindow = log.LogsWindow(self)
		logWindow.grab_set()

	def write_logs(self, value: bool):
		if value == False:
			with open('logs.txt', 'r+') as logs:
				old_logs = logs.read()
				logs.seek(0, 0)
				logs.write(f"<{dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} ПРОХОД ЗАБЛОКИРОВАН>\n"
			                f"Cостояние карты:\n" 
						    f"Баланс карты: {self.defaultUser.coins}; "
			                f"Cрок годности: {self.defaultUser.date}; "
			                f"Блок: {self.defaultUser.block};\n"
			                "-----------------------------------------------\n")
				logs.write(old_logs)
		else:
			with open('logs.txt', 'r+') as logs:
				old_logs = logs.read()
				logs.seek(0, 0)
				logs.write(f"<{dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} ПРОХОД РАЗРЕШЁН>\n"
				                f"Cостояние карты:\n"
				                f"Баланс карты: {self.defaultUser.coins}; "
				                f"Cрок годности: {self.defaultUser.date}; "
				                f"Блок: {self.defaultUser.block};\n"
				                "-----------------------------------------------\n")
				logs.write(old_logs)

	def sensor_event(self):
		if self.check_radioButton != 0:
			timer_thread_wicket = threading.Timer(5, self.closer)
			timer_thread_wicket.start()

		else:
			self.closer()