import customtkinter as ctk
import time


class LogsWindow(ctk.CTkToplevel):
	def __init__(self, parent):
		super().__init__(parent)

		self.geometry('350x450')
		self.title('Wicket ASC Logs')
		self.resizable(False, False)

		self.log_frame = ctk.CTkTextbox(self, 350, 400, 0)
		self.log_frame.place(x=0, y=0)

		self.btn_close = ctk.CTkButton(self, 350, 50, text='close', command=self.closer, corner_radius=0)
		self.btn_close.place(x=0, y=400)

		with open('logs.txt') as logs:
			self.log_frame.insert('0.0', logs.read())

	def closer(self):
		self.destroy()


