import rumps
import cv2
from mss import mss
import numpy as np

from os.path import join, expanduser

CONFIG = {
	'name': 'TimeLapse',
	'start': 'Start time lapse',
	'end': 'End time lapse',
	'pause': 'Pause time lapse',
	'resume': 'Resume time lapse',
	'help': 'Help',
	'about': 'About',
	'quit': 'Quit',
	'shots_per_min': 25,
	'set_shots_per_min': 'Set shots per minute',  
	'frame_rate': 24,  # 24 fps video output
	'set_frame_rate': 'Set frame rate',
	'dest': 'Desktop',
	'output': 'output.mp4',
	'codec': 'avc1',  # the one which works for macos
}

class TimeLapse(rumps.App):
	def __init__(self):
		super(TimeLapse, self).__init__(CONFIG['name'], quit_button=None)

		# timer setup
		self.timer = rumps.Timer(
			self.take_photo, 1./CONFIG['shots_per_min'] * 60)

		# screenshot setup
		self.sct = mss()

		self.forcc = cv2.VideoWriter_fourcc(*CONFIG['codec'])
		self.dir = join(expanduser('~'), CONFIG['dest'])

		self.trailing_menu = [
			rumps.MenuItem(CONFIG['set_frame_rate'], callback=self.set),
			rumps.MenuItem(CONFIG['set_shots_per_min'], callback=self.set),
			None,  # separator
			CONFIG['help'],
			rumps.MenuItem(CONFIG['about'], callback=lambda _: rumps.alert(
				'Timelapse by @wkaisertexas')),
			rumps.MenuItem(CONFIG['quit'], callback=self.quit, key='q')
		]

		self.reset_menu()

	# Callbacks
	def reset_menu(self):
		self.timer.stop()
		self.timer.count = 0

		# creates the menu
		if self.menu:  # clears the menu if it already exists
			self.menu.clear()

		self.devices = self.get_devices_menu()
		self.menu = [  # for some reason, the other menu items are trailing
			# command key shift R
			rumps.MenuItem(CONFIG['start'], callback=self.start, key='R'),
			None,
			# self.devices,
			*self.trailing_menu
		]

		self.title = '🎥'

	def start(self, sender):
		self.title = '⏸'

		self.menu.clear()
		self.menu = [
			rumps.MenuItem(CONFIG['pause'], callback=self.pause, key='R'),
			rumps.MenuItem(CONFIG['end'], callback=self.end, key='e'),
			None,
			self.devices,
			*self.trailing_menu
		]

		# starts the timer -> note: does not reset the recorder
		self.timer.start()

	def end(self, sender):
		i = 0
		for recorder in self.webcam_recorders + self.mon_recorders:
			if recorder:
				recorder.release()
				i += 1

		if i == 0:
			rumps.alert('No recording devices were found')
		elif i == 1:
			rumps.alert(f"Video saved to {self.dir}")
		else:
			rumps.alert(f"{i} videos saved to {self.dir}")

		self.reset_menu()

	def quit(self, sender):	# TODO: troubleshoot the problems where the app was not quitting

		"""
		Releases (saves) all recording devices and quits the app
		"""

		for recorder in self.webcam_recorders + self.mon_recorders:
			if recorder:
				recorder.release()		
		
		rumps.quit_application()
		exit()

	def pause(self, sender):
		"""
		Pauses the video recording and sets the menu to the play arrow
		"""
		self.title = '▶️'
		self.timer.stop()  # stops adding new frames to the video

		self.menu.clear()
		self.menu = [
			rumps.MenuItem(CONFIG['resume'], callback=self.resume, key='R'),
			rumps.MenuItem(CONFIG['end'], callback=self.end, key='e'),
			None,
			self.devices,
			* self.trailing_menu
		]

	def resume(self, sender):
		self.title = '⏸'
		self.timer.start()

		self.menu.clear()
		self.menu = [
			rumps.MenuItem(CONFIG['pause'], callback=self.pause, key='R'),
			rumps.MenuItem(CONFIG['end'], callback=self.end, key='e'),
			None,
			self.devices,
			*self.trailing_menu
		]

	@rumps.clicked(CONFIG['help'])
	def help(self, sender):
		"""
		Displays the help menu
		"""
		rumps.alert('Created by @wkaisertexas with documenation at github.com/wkaisertexas/timelapse')  # kind fo a filler function ig

	def take_photo(self, timer):
		"""
		Takes a screenshot for each selected device and saves it to a video writer object
		"""

		# records the monitor(s)
		for i, monitor in enumerate(self.monitors):
			if monitor:  # if the monitor is selected
				mon = self.sct.monitors[i]  # gets the monitor
				img = self.sct.grab(mon)  # grabs the monitor
				# gets rid of the alpha channel
				img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
				# saves the image using the video writer object
				self.mon_recorders[i].write(img)

		# records the webcam(s)
		for i, webcam in enumerate(self.webcams):
			if webcam:  # if the webcam is selected
				_, img = self.webcam_readers[i].read()  # reads the webcam
				# saves the image using the video writer object
				self.webcam_recorders[i].write(img)

	def set(self, sender):
		# creates a window to set the frame rate
		res = rumps.Window(sender.title, 'What value would you like to select?',
						   default_text='25', dimensions=(200, 100)).run()
		if not res.clicked:
			return

		res = int(res.text)
		# frame rate of output videos
		if sender.title == CONFIG['set_frame_rate']:
			CONFIG['frame_rate'] = res
			if self.timer.is_running():
				rumps.alert('Unable to change the frame rate while recording')
		elif sender.title == CONFIG['set_shots_per_min']:
			CONFIG['shots_per_min'] = res
			# adjusts the interval adhoc
			self.timer.interval = 1./CONFIG['shots_per_min'] * 60

	def get_devices_menu(self):
		"""
		Returns a list of possible video recording devices (monitors or video input devices)
		"""
		# monitors
		menu = []
		for i in range(len(self.sct.monitors)):
			menu.append(rumps.MenuItem(
				f"Monitor {i}", callback=self.toggle_device))

		if len(menu) > 0:
			menu.append(None)  # seperator

		# video input devices
		num_cameras = self.get_num_cameras()
		for i in range(num_cameras):
			menu.append(rumps.MenuItem(
				f"Video Input {i}", callback=self.toggle_device))

		# video device status trackers
		if not hasattr(self, 'montiors') or len(self.monitors) != len(self.sct.monitors):
			self.monitors = [False for _ in range(len(self.sct.monitors))]
			self.mon_recorders = [None for _ in range(len(self.sct.monitors))]

		if not hasattr(self, 'cameras') or len(self.cameras) != num_cameras:
			self.cameras = [False for _ in range(num_cameras)]
			self.webcam_recorders = [None for _ in range(num_cameras)]
			self.webcam_readers = [None for _ in range(num_cameras)]

		# toggles on the first monitor by default
		first_mon = menu[0]
		first_mon.title = 'Monitor 0 (Default)'
		
		self.toggle_device(first_mon)
		
		return ('Recording Devices', menu)

	def toggle_device(self, sender):
		"""
		Toggles the recording device
		"""
		sender.state = not sender.state  # toggles the menu item's checkmark

		if sender.title.startswith('Monitor'):
			index = int(sender.title.split(' ')[1])
			self.monitors[index] = sender.state

			if sender.state:  # monitor is being selected -> create a video writer
				self.mon_recorders[index] = cv2.VideoWriter(
					f'{self.dir}/monitor_{index}.mp4', self.forcc, CONFIG['frame_rate'], (self.sct.monitors[index]['width'] * 2, self.sct.monitors[index]['height'] * 2))
			else:  # monitor is being unselected -> close the video writer
				self.mon_recorders[index].release()
				# removes the video writer object
				self.mon_recorders[index] = None
			
			return

		index = int(sender.title.split(' ')[2])
		self.cameras[index] = sender.state
		if sender.state:
			self.webcam_readers[index] = cv2.VideoCapture(index)
			self.webcam_recorders[index] = cv2.VideoWriter(f'{self.dir}/webcam_{index}.mp4', self.forcc, CONFIG['frame_rate'], (int(self.webcam_readers[index].get(
				cv2.CAP_PROP_FRAME_WIDTH)), int(self.webcam_readers[index].get(cv2.CAP_PROP_FRAME_HEIGHT))))  # TODO: check if I have to double this

	def get_num_cameras(self):
		"""
		Gets the number of cameras attached to the computer
		"""
		# tries to make a video recorder device for each webcam
		return sum([1 if cv2.VideoCapture(i).read()[0] else 0 for i in range(10)])


if __name__ == '__main__':
	TimeLapse().run()
