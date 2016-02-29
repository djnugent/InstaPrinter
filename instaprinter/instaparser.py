from PIL import Image
from urllib.error import URLError
from urllib.request import urlopen
from instarender import InstagramTheme
from instauser import User
import datetime
import json
import io

class InstagramPost():
	def __init__(self):
		self.id = None
		self.photo = None
		self.photo_url = None
		self.profile_pic = None
		self.profile_pic_url = None
		self.caption = None
		self.date = None
		self.user = None
		self.location = None
		self.post = None

	# grab most recent post meta data
	def poll_feed(self,user):
		try:
			url = "https://api.instagram.com/v1/users/self/media/recent/?access_token={0}&count=1".format(user.access_token)
			response = urlopen(url)
			meta = json.loads(response.read().decode('utf8'))['data'][0]
			typ = meta['type']
			if typ == 'image':
				self.id = meta['id']
				self.photo_url = meta['images']['standard_resolution']['url']
				self.profile_pic_url = meta['user']['profile_picture']
				self.caption = meta['caption']['text']
				self.date = datetime.date.fromtimestamp(int(meta['created_time'])).strftime('%m/%d/%y')
				self.user = meta['user']['username']
				try:
					self.location = meta['location']['name']
				except TypeError:
					self.location = None
				return True
			return False
		except URLError:
			print("[ Error ] Unable to poll server for", user.username)
			return False

	# compare current to last printed photo
	def is_new(self,last_id):
		if self.id is None:
			raise RuntimeError("photo id is unknown")
		return last_id != self.id

	# download photo and profile picture
	def download_post(self):
		if self.photo_url is None or self.profile_pic_url is None:
			raise RuntimeError("Meta data not downloaded")
		#photo
		raw_photo = urlopen(self.photo_url)
		photo_file = io.BytesIO(raw_photo.read())
		self.photo = Image.open(photo_file)

		#profile pic
		raw_prof_pic = urlopen(self.profile_pic_url)
		prof_pic_file = io.BytesIO(raw_prof_pic.read())
		self.profile_pic = Image.open(prof_pic_file)


	#render the photo to look like an instagram post
	def render_post(self):
		if self.photo is None or self.profile_pic is None:
			raise RuntimeError("Content not downloaded")
		self.post = InstagramTheme.renderTheme(self)
		return self.post

	def info(self):
		print("user:",self.user)
		print("location:", self.location)
		print("date:", self.date)
		print("caption:", self.caption)
