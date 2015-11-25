from PIL import Image, ImageOps, ImageDraw,ImageFont
import textwrap

class InstagramTheme():
	HEADER_HEIGHT = 130
	FRAME_SIZE = (640,960)
	INSTA_BLUE = (18, 86, 136)
	INSTA_LIGHT_BLUE = (81, 127, 164)
	INSTA_BLACK = (60,60,60)
	BOLD_FONT = ImageFont.truetype("Roboto-Bold.ttf",24)
	REGULAR_FONT = ImageFont.truetype("Roboto-Regular.ttf",20)
	MEDIUM_FONT = ImageFont.truetype("Roboto-Medium.ttf",22)


	@classmethod
	def renderTheme(cls, post):
		photo = cls.crop_header_footer(post.photo)
		prof = cls.circular_crop(post.profile_pic)
		frame = InstagramTheme.create_frame(photo)
		cls.draw_header(frame,prof,post.user,post.location,post.date)
		cls.draw_footer(frame,post.user,post.caption,photo.size[1])
		return frame

	@classmethod
	def crop_header_footer(cls,photo):
		inv_photo = ImageOps.invert(photo)
		bounding_box = inv_photo.getbbox()
		left = 0
		upper = bounding_box[1] + 10
		right = photo.width
		lower = bounding_box[3] - 10
		return photo.crop(box=(left,upper,right,lower))


	@classmethod
	def circular_crop(cls,profile_pic):
		bigsize = (profile_pic.size[0] * 3, profile_pic.size[1] * 3)
		mask = Image.new('1', bigsize, 255)
		draw = ImageDraw.Draw(mask)
		draw.ellipse((0, 0) + bigsize, fill=0)
		mask = mask.resize(profile_pic.size, Image.ANTIALIAS)
		profile_pic.paste((255,255,255),mask=mask)
		return profile_pic

	@classmethod
	def create_frame(cls,photo):
		#add whitespace to photo
		frame = Image.new("RGB", cls.FRAME_SIZE, "white")
		frame.paste(photo, (0,cls.HEADER_HEIGHT))
		return frame

	@classmethod
	def draw_header(cls,frame,profile_pic, username, location, date):
		#add profile picture
		profile_pic = profile_pic.resize((65,65), Image.ANTIALIAS)
		frame.paste(profile_pic,(15,45))

		draw = ImageDraw.Draw(frame)
		x_loc = profile_pic.size[0] + 30
		if location is not None:
			#location and username
			y_loc = 50
			draw.text((x_loc, y_loc), username, fill=cls.INSTA_BLUE, font=cls.BOLD_FONT)
			y_loc = 80
			draw.text((x_loc, y_loc), location, fill=cls.INSTA_LIGHT_BLUE, font=cls.MEDIUM_FONT)
		else:
			#add username
			y_loc = 65
			draw.text((x_loc, y_loc), username, fill=cls.INSTA_BLUE, font=cls.BOLD_FONT)

		#add date
		x_loc = frame.size[0] - 100
		y_loc = 67
		draw.text((x_loc, y_loc), date, fill=cls.INSTA_BLACK, font=cls.REGULAR_FONT)

	@classmethod
	def draw_footer(cls, frame, username, caption,img_height):
		draw = ImageDraw.Draw(frame)
		#add username
		margin = 20
		y_offset = img_height + cls.HEADER_HEIGHT + 30
		draw.text((margin, y_offset), username, fill=cls.INSTA_BLUE, font=cls.BOLD_FONT)

		#add caption
		user_length = cls.BOLD_FONT.getsize(username)[0] + 10
		y_loc = y_offset + 2
		line_length = 0
		for word in caption.split():
			word = word + ' '
			word_length = cls.MEDIUM_FONT.getsize(word)[0]
			#see if word will fit on current line
			#line 1 has to start after username
			if y_loc == y_offset + 2:
				if margin + user_length + line_length + word_length > 640 - margin:
					y_loc += cls.MEDIUM_FONT.getsize(word)[1] + 10
					line_length = 0

			#line 2+ wraps under username
			else:
				if margin + line_length + word_length > 640 - margin:
					y_loc += cls.MEDIUM_FONT.getsize(word)[1] + 10
					line_length = 0
			#add word to line one
			if y_loc == y_offset + 2:
				x_loc = margin + user_length + line_length
				if word[0] == '#':
					color = cls.INSTA_BLUE
				else:
					color = cls.INSTA_BLACK
				draw.text((x_loc, y_loc), word, font=cls.MEDIUM_FONT, fill=color)
				line_length += word_length
			#add word to line 2+
			else:
				x_loc = margin + line_length
				if word[0] == '#':
					color = cls.INSTA_BLUE
				else:
					color = cls.INSTA_BLACK
				draw.text((x_loc, y_loc), word, font=cls.MEDIUM_FONT, fill=color)
				line_length += word_length
