from manim import *
from manim_slides import Slide

class BasicExample(Slide):
	def construct(self):
		# 1. Create a Circle
		circle = Circle(color=BLUE)
		dot = Dot()

		self.play(Create(circle))
		self.add(dot)

		# This creates a pause until you press a key
		self.next_slide()

		# 2. Transform into a Square
		square = Square(color=RED)
		self.play(Transform(circle, square))

		self.next_slide()

		# 3. Fade everything out
		self.play(FadeOut(circle), FadeOut(dot))