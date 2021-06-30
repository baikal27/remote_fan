import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import RPi.GPIO as GPIO

fanUi = 'fan_gui.ui'

class MainDialog(QDialog):
	def __init__(self):
		QDialog.__init__(self, None)
		uic.loadUi(fanUi, self)

		self.start.clicked.connect(self.starting)
		self.stop.clicked.connect(self.stopping)
		self.speed1.clicked.connect(lambda jjok, state=self.speed1 : self.speed(jjok, state))
		self.speed2.clicked.connect(lambda jjok, state=self.speed2 : self.speed(jjok, state))
		self.speed3.clicked.connect(lambda jjok, state=self.speed3 : self.speed(jjok, state))
		self.slide.valueChanged.connect(self.speedslide)
		self.left.clicked.connect(self.directing)
		self.right.clicked.connect(self.directing)

		self.initGPIO()
		self.activation = False
		self.grade = {'1':50, '2':70, '3':90}
		self.now_speed = 0

	def directing(self):
		try:
			if self.left.isChecked():
				self.direction = 'left'
				GPIO.output(self.in1_pin, False)
				GPIO.output(self.in2_pin, True)
				self.display.setText('Anti-clock direction')
				if self.activation:
					GPIO.output(self.yellow, True)
					GPIO.output(self.red, False)
					GPIO.output(self.green, False)
			elif self.right.isChecked():
				self.direction = 'right'
				GPIO.output(self.in1_pin, True)
				GPIO.output(self.in2_pin, False)
				self.display.setText('Clock direction')
				if self.activation:
					GPIO.output(self.yellow, False)
					GPIO.output(self.red, False)
					GPIO.output(self.green, True)
			else:
				self.display.setText("You should choice direction")
		except Exception as e:
			print(e)
		
	def initGPIO(self):
		GPIO.setmode(GPIO.BCM)
		self.init_freq = 50
		self.sig_pin = 13
		self.in1_pin = 5
		self.in2_pin = 6
		GPIO.setup(self.sig_pin, GPIO.OUT)
		GPIO.setup(self.in1_pin, GPIO.OUT)
		GPIO.setup(self.in2_pin, GPIO.OUT)

		self.yellow = 23
		self.red = 12
		self.green = 21
		GPIO.setup(self.yellow, GPIO.OUT)
		GPIO.setup(self.red, GPIO.OUT)
		GPIO.setup(self.green, GPIO.OUT)
		GPIO.output(self.yellow, False)
		GPIO.output(self.red, True)
		GPIO.output(self.green, False)
		self.direction = 'center'

		self.pwm_speed = GPIO.PWM(self.sig_pin, self.init_freq)
		self.pwm_speed.start(0)
		GPIO.output(self.in1_pin, True)
		GPIO.output(self.in2_pin, False)

	def starting(self):
		if self.direction == 'right':
			GPIO.output(self.yellow, False)
			GPIO.output(self.red, False)
			GPIO.output(self.green, True)
		elif self.direction == 'left':
			GPIO.output(self.yellow, True)
			GPIO.output(self.red, False)
			GPIO.output(self.green, False)
		else :
			GPIO.output(self.yellow, False)
			GPIO.output(self.red, True)
			GPIO.output(self.green, False)
			
		self.now_speed = 50
		self.slide.setValue(self.now_speed)
		self.pwm_speed.ChangeDutyCycle(self.now_speed)
		self.activation = True
		self.display.setText('Start Fan. The speed of the fan is {}'.format(self.now_speed))

	def stopping(self):
		try:
			if self.activation:
				self.now_speed = 0
				self.slide.setValue(self.now_speed)
				self.pwm_speed.ChangeDutyCycle(self.now_speed)
				self.activation = False
				self.display.setText('The fan is stopped.')
				GPIO.output(self.yellow, False)
				GPIO.output(self.red, True)
				GPIO.output(self.green, False)
			else:
				self.display.setText('First you should push the Start button.')
		except Exception as e:
			print(e)

	def speed(self, jjok, state):
		try:
			if self.activation:
				self.now_speed = self.grade[state.text()]
				self.slide.setValue(self.now_speed)
				self.pwm_speed.ChangeDutyCycle(self.now_speed)
				self.display.setText('The speed of the Fan is {}.'.format(self.now_speed))
			else:
				self.display.setText('First you should push the Start button.')
		except Exception as e:
			print(e)

	def speedslide(self):
		try:
			if self.activation:
				self.now_speed = self.slide.value()
				self.pwm_speed.ChangeDutyCycle(self.now_speed)
				self.display.setText('The speed of the Fan is {}.'.format(self.now_speed))
			else:
				self.display.setText('First you should push the Start button.')
		except Exception as e:
			print(e)

	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			self.pwm_speed.stop()
			GPIO.cleanup()
			event.accept()
			print('GPIO cleanup & Window closed')
		else:
			event.ignore()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	dialog = MainDialog()
	dialog.show()
	sys.exit(app.exec_())
