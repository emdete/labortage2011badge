#!/usr/bin/env -S python -u
from LaborUSBGadget import LaborUSBGadget
from time import sleep

class LaborBadge(LaborUSBGadget):
	"""
	Dies ist die klasse fuer das LaborTage 2011 Badge ein kleines blinkendevice
	"""
	commands = {
			'CUSTOM_RQ_SET_RED': 0x03,
			'CUSTOM_RQ_SET_GREEN': 0x04,
			'CUSTOM_RQ_SET_BLUE': 0x05,
			'CUSTOM_RQ_SET_RGB': 0x06,
			'CUSTOM_RQ_GET_RGB': 0x07,
			'CUSTOM_RQ_FADE_RGB': 0x08,
			'CUSTOM_RQ_READ_MEM': 0x10,
			'CUSTOM_RQ_WRITE_MEM': 0x11,
			'CUSTOM_RQ_READ_FLASH': 0x12,
			'CUSTOM_RQ_EXEC_SPM': 0x13,
			'CUSTOM_RQ_RESET': 0x14,
			'CUSTOM_RQ_READ_BUTTON': 0x15,
			'CUSTOM_RQ_READ_TMPSENS': 0x16,
			}


	def __init__(self):
		self.starttempUSB=230
		self.starttempHost=-40
		LaborUSBGadget.__init__(self, LaborUSBGadget.LABOR_BADGE_ID)

	def getTemprature(self):
		"""
		Das badge kann die raumtemperatur auswerten - lets have a look
		also im datenblatt vom attiny45 ist folgende tabelle abgebildet
		-40 +25 +85
		230 300 370
		und die Aussagen:
		* The measured voltage has a linear relationship to the temperature
		* The sensitivity is approximately 1 LSB / Grad C

		# linear
		a*(-40)+b = 230
		a*(25) + b = 300
		a*(85) + b = 370

		-40a+b-230=25a+b-300
		65a=70

		a=1.07692307692307692307

		-40a-230=85a-370
		a=1.12000000000000000000

		25a-300=85a-370
		a=1.16666666666666666666

		summe ueber alle a und dann druch drei ;)
		1.12119658119658119657 - das ist jetzt unser linearer korrekturfaktor k

		Bitte bitte selber justieren! das ding ist wirklich ungenau
		"""
		tmptemp=self.getCTLMsg(self.commands['CUSTOM_RQ_READ_TMPSENS'], 2)
		value=(tmptemp[1]<<8)+tmptemp[0]
		#a=1
		k=1.12119658119658119657
		return float(value-float(self.starttempUSB)+self.starttempHost)/k

	def getColor(self):
		"""
		die aktuell eingestellt farbe ausgeben
		"""
		ret = self.getCTLMsg(self.commands['CUSTOM_RQ_GET_RGB'], 6)
		return (
			ret[0] + ret[1] * 256,
			ret[2] + ret[3] * 256,
			ret[4] + ret[5] * 256,
			)


	def setColor(self, red=65535, green=65535, blue=65535):
		"""
		eine methode zum setzen aller farbwerte gleichzeitig die range ist
		dabei 16bit (0-65535 beide inklusivere)
		"""
		# check for range und an der stelle brauchen wir die byterepresentation
		# bigendien stream
		red &= 0xffff
		blue &= 0xffff
		green &= 0xffff
		return self.sendCTLMsg(self.commands['CUSTOM_RQ_SET_RGB'], (
			red % 256, red // 256,
			green % 256, green // 256,
			blue % 256, blue // 256,
			))


	def fadeToColor(self, count=100, red=0, green=0, blue=0):
		r,g,b = self.getColor()
		self.fadeDelta(count, (red-r) // count, (green-g) // count, (blue-b) // count)

	def fadeDelta(self, count=255, delta_red=255, delta_green=255, delta_blue=255):
		"""
		"""
		delta_red &= 0xffff
		delta_blue &= 0xffff
		delta_green &= 0xffff
		print("vals",
			count,
			delta_red % 256, delta_red // 256,
			delta_green % 256, delta_green // 256,
			delta_blue % 256, delta_blue // 256,
			)
		return self.sendCTLMsg(self.commands['CUSTOM_RQ_FADE_RGB'], (
			delta_red % 256, delta_red // 256,
			delta_green % 256, delta_green // 256,
			delta_blue % 256, delta_blue // 256,
			), count)


if __name__ == "__main__":
	blinkcolor={}
	blinkcolor2={}
	f=LaborBadge()
	print("temperature=", f.getTemprature())
	print("color=", f.getColor())
	print("setColor", f.setColor())
	for _ in range(4):
		print("fadeDelta", f.fadeDelta(255, -255, -255, -255))
		sleep(2)
		print("fadeDelta", f.fadeDelta())
		sleep(2)
	print("fadeDelta", f.fadeDelta(255, -255, -255, -255))

