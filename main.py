from pathlib import Path

import numpy as np

from manim import *
from manim_slides import Slide
from lambda_creature import LambdaCreature, ExpressionLambda


def creature_look_at_animation(creature, point):
	eye_center = creature.eye_sclera.get_center()
	direction = point - eye_center
	norm = np.linalg.norm(direction)
	if norm == 0:
		direction = RIGHT
	else:
		direction = direction / norm

	pupil_radius = creature.pupil.radius
	sclera_radius = creature.eye_sclera.radius
	max_offset = sclera_radius - pupil_radius
	new_pupil_position = eye_center + direction * max_offset * 0.7

	tangent_distance = (pupil_radius - creature.highlight.radius) * 0.85
	direction_45 = np.array([-np.sqrt(2) / 2, np.sqrt(2) / 2, 0])
	new_highlight_position = new_pupil_position + tangent_distance * direction_45

	return AnimationGroup(
		creature.pupil.animate.move_to(new_pupil_position),
		creature.highlight.animate.move_to(new_highlight_position),
		lag_ratio=0.0,
	)


class Main(Slide):
	def construct(self):
		asset_dir = Path(__file__).resolve().parent / "assets"
		page_files = [
			asset_dir / "pages" / "1.jpg",
			asset_dir / "pages" / "2.jpg",
			asset_dir / "pages" / "3.jpg",
			asset_dir / "pages" / "4.jpg",
		]

		stack_origin = ORIGIN
		reveal_origin = LEFT * 5.0 + UP * 0.95
		page_stack = []
		for index, page_file in enumerate(page_files):
			page = ImageMobject(str(page_file))
			page.scale_to_fit_height(5.9)
			page.move_to(stack_origin)
			page.set_z_index(20 - index)
			page_stack.append(page)

		for page in page_stack:
			self.add(page)

		self.next_slide()

		title = Text("All Sorts of Permutations", font_size=44)
		subtitle = Text("(functional pearl)", font_size=26, color=GREY_B)
		authors = Text(
			"J. Christiansen, N. Danilenko, S. Dylus", font_size=26, color=GREY_B
		)
		title_block = VGroup(title, subtitle, authors).arrange(DOWN, buff=0.18)
		title_block.move_to(RIGHT * 3.2 + ORIGIN)
		for line in title_block:
			line.set_max_width(5.1)

		self.play(
			AnimationGroup(
				page_stack[0]
				.animate.move_to(reveal_origin + RIGHT * 0.06 + DOWN * 0.04)
				.scale(0.82),
				page_stack[1]
				.animate.move_to(reveal_origin + RIGHT * 0.82 + DOWN * 0.44)
				.scale(0.77),
				page_stack[2]
				.animate.move_to(reveal_origin + RIGHT * 1.64 + DOWN * 0.88)
				.scale(0.72),
				page_stack[3]
				.animate.move_to(reveal_origin + RIGHT * 2.46 + DOWN * 1.32)
				.scale(0.67),
				lag_ratio=0.0,
			),
			FadeIn(title_block, shift=0.2 * RIGHT),
			run_time=2.4,
		)

		self.next_slide()

		quote_source = Text(
			"Sebastian Fischer", font_size=24, color=GREY_B, slant=ITALIC
		)
		quote_text = Text(
			'"Every sorting algorithm that actually sorts\ncan describe every possible permutation\n(if there is a permutation that cannot be\nrealized by the sorting algorithm then there\nis an input list that cannot be sorted)."',
			font_size=38,
		)
		quote_block = VGroup(quote_source, quote_text).arrange(DOWN, buff=0.24)
		quote_block.scale_to_fit_width(8.0)
		quote_block.to_corner(UL, buff=0.55)
		quote_block.shift(RIGHT * 0.55 + DOWN * 0.1)
		quote_block.set_z_index(10)

		creature = LambdaCreature(
			body_color="#5e5086", eye_color=WHITE, pupil_color=BLACK, height=1.7
		)
		creature.move_to(RIGHT * 4.1 + DOWN * 2.35)
		creature.set_z_index(12)

		self.play(
			AnimationGroup(*[FadeOut(page) for page in page_stack], lag_ratio=0.0),
			FadeOut(title_block, shift=0.15 * LEFT),
			FadeIn(quote_block, shift=0.15 * RIGHT),
			FadeIn(creature, shift=0.2 * DOWN),
			run_time=2.2,
		)

		self.next_slide()

		bubble_text = Paragraph(
			"If insertion sort made random",
			"decisions while comparing items,",
			"could it eventually produce every",
			"possible ordering of a list?",
			alignment="center",
			font_size=18,
			color=WHITE,
		)
		bubble_text.scale_to_fit_width(5.9)
		bubble = Ellipse(
			width=bubble_text.width + 2.0,
			height=bubble_text.height + 1.0,
			color=WHITE,
			stroke_width=2,
			fill_opacity=0,
		)
		bubble.move_to(bubble_text.get_center())
		bubble_group = VGroup(bubble, bubble_text)
		bubble_group.set_z_index(11)
		bubble_group.move_to(RIGHT * -0.05 + DOWN * 1.35)

		self.play(
			FadeIn(bubble_group, shift=0.15 * UP),
			creature_look_at_animation(creature, quote_block.get_center()),
			run_time=1.8,
		)

		self.next_slide()

		self.play(
			AnimationGroup(
				FadeOut(bubble_group, shift=0.1 * DOWN),
				FadeOut(quote_block, shift=0.1 * LEFT),
				FadeOut(creature, shift=0.1 * DOWN),
				lag_ratio=0.0,
			),
			run_time=1.2,
		)

		question = MathTex(r"\text{Is } a \le b\ ?", font_size=64)
		question.to_edge(UP, buff=0.55)

		head_coin = Circle(radius=0.9, color=GREEN_B, fill_opacity=1.0, stroke_width=4)
		head_label = Text("H", font_size=52, color=WHITE)
		head_group = VGroup(head_coin, head_label)
		head_caption = Text("Yes", font_size=30, color=WHITE)
		head_block = VGroup(head_group, head_caption).arrange(DOWN, buff=0.25)
		head_block.move_to(LEFT * 3.2)

		tail_coin = Circle(radius=0.9, color=RED_B, fill_opacity=1.0, stroke_width=4)
		tail_label = Text("T", font_size=52, color=WHITE)
		tail_group = VGroup(tail_coin, tail_label)
		tail_caption = Text("No", font_size=30, color=WHITE)
		tail_block = VGroup(tail_group, tail_caption).arrange(DOWN, buff=0.25)
		tail_block.move_to(RIGHT * 3.2)

		divider = Line(UP * 2.6, DOWN * 2.2, color=GREY_B, stroke_width=2)

		bottom_text = Text(
			"We define a comparision function coinCmp that lets us explore\nboth possibilities and put our eventual results together",
			font_size=32,
			color=WHITE,
			t2c={"coinCmp": BLUE_B},
		)
		bottom_text.to_edge(DOWN, buff=0.55)
		bottom_text.set_max_width(11.0)

		self.play(
			FadeIn(question, shift=0.15 * DOWN),
			FadeIn(divider),
			FadeIn(head_block, shift=0.2 * RIGHT),
			FadeIn(tail_block, shift=0.2 * LEFT),
			FadeIn(bottom_text, shift=0.15 * UP),
			run_time=2.0,
		)

		self.next_slide()

		self.play(
			FadeOut(question, shift=0.1 * UP),
			FadeOut(divider),
			FadeOut(head_block, shift=0.1 * LEFT),
			FadeOut(tail_block, shift=0.1 * RIGHT),
			FadeOut(bottom_text, shift=0.1 * DOWN),
			run_time=1.0,
		)

		title = MathTex(
			r"\mathrm{insertSort}(\mathrm{coinCmp}, [2, 3, 1])", font_size=42
		)
		title.to_edge(UP, buff=0.45)

		level1_y = 2.0
		level2_y = 0.7
		level3_y = -0.7
		level4_y = -2.2
		x_level2 = 3.2
		x_level3 = 1.8
		x_level4 = 1.2

		x_left = -x_level2
		x_right = x_level2
		x_left_left = x_left - x_level3
		x_left_right = x_left + x_level3
		x_right_left = x_right - x_level3
		x_right_right = x_right + x_level3
		x_left_left_left = x_left_left - x_level4
		x_left_left_right = x_left_left + x_level4
		x_right_left_left = x_right_left - x_level4
		x_right_left_right = x_right_left + x_level4

		cmp_23 = MathTex(r"\mathrm{coinCmp}(2, 3)", font_size=36)
		cmp_23.move_to(UP * level1_y)

		cmp_13_left = MathTex(r"\mathrm{coinCmp}(1, 3)", font_size=34)
		cmp_13_left.move_to(RIGHT * x_left + UP * level2_y)

		cmp_12_right = MathTex(r"\mathrm{coinCmp}(1, 2)", font_size=34)
		cmp_12_right.move_to(RIGHT * x_right + UP * level2_y)

		leaf_132 = MathTex(r"[1, 3, 2]", font_size=32)
		leaf_132.move_to(RIGHT * x_left_right + UP * level3_y)

		cmp_12_left = MathTex(r"\mathrm{coinCmp}(1, 2)", font_size=34)
		cmp_12_left.move_to(RIGHT * x_left_left + UP * level3_y)

		leaf_123 = MathTex(r"[1, 2, 3]", font_size=32)
		leaf_123.move_to(RIGHT * x_right_right + UP * level3_y)

		cmp_13_right = MathTex(r"\mathrm{coinCmp}(1, 3)", font_size=34)
		cmp_13_right.move_to(RIGHT * x_right_left + UP * level3_y)

		leaf_312 = MathTex(r"[3, 1, 2]", font_size=32)
		leaf_312.move_to(RIGHT * x_left_left_right + UP * level4_y)

		leaf_321 = MathTex(r"[3, 2, 1]", font_size=32)
		leaf_321.move_to(RIGHT * x_left_left_left + UP * level4_y)

		leaf_213 = MathTex(r"[2, 1, 3]", font_size=32)
		leaf_213.move_to(RIGHT * x_right_left_right + UP * level4_y)

		leaf_231 = MathTex(r"[2, 3, 1]", font_size=32)
		leaf_231.move_to(RIGHT * x_right_left_left + UP * level4_y)

		true_color = GREEN_B
		false_color = RED_B

		trunk = Line(title.get_bottom(), cmp_23.get_top(), color=GREY_B, stroke_width=2)
		line_23_left = Line(
			cmp_23.get_bottom(),
			cmp_13_left.get_top(),
			color=false_color,
			stroke_width=3,
		)
		line_23_right = Line(
			cmp_23.get_bottom(),
			cmp_12_right.get_top(),
			color=true_color,
			stroke_width=3,
		)
		line_13_left_left = Line(
			cmp_13_left.get_bottom(),
			cmp_12_left.get_top(),
			color=false_color,
			stroke_width=3,
		)
		line_13_left_right = Line(
			cmp_13_left.get_bottom(),
			leaf_132.get_top(),
			color=true_color,
			stroke_width=3,
		)
		line_12_right_left = Line(
			cmp_12_right.get_bottom(),
			cmp_13_right.get_top(),
			color=false_color,
			stroke_width=3,
		)
		line_12_right_right = Line(
			cmp_12_right.get_bottom(),
			leaf_123.get_top(),
			color=true_color,
			stroke_width=3,
		)
		line_12_left_left = Line(
			cmp_12_left.get_bottom(),
			leaf_321.get_top(),
			color=false_color,
			stroke_width=3,
		)
		line_12_left_right = Line(
			cmp_12_left.get_bottom(),
			leaf_312.get_top(),
			color=true_color,
			stroke_width=3,
		)
		line_13_right_left = Line(
			cmp_13_right.get_bottom(),
			leaf_231.get_top(),
			color=false_color,
			stroke_width=3,
		)
		line_13_right_right = Line(
			cmp_13_right.get_bottom(),
			leaf_213.get_top(),
			color=true_color,
			stroke_width=3,
		)

		output_list = MathTex(
			r"\left[\,[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1] \,\right]",
			font_size=34,
			color=WHITE,
		)
		output_list.to_edge(DOWN, buff=0.35)
		output_list.set_max_width(10.2)

		output_list_shift = LEFT * 1.4
		output_tail = MathTex(r"= P([1, 2, 3]) !", font_size=34, color=WHITE)
		output_tail.next_to(output_list, RIGHT, buff=0.35)
		output_tail.align_to(output_list, DOWN)
		output_tail.shift(output_list_shift)

		self.play(FadeIn(title, shift=0.1 * DOWN), run_time=0.6)
		self.play(FadeIn(cmp_23, shift=0.1 * DOWN), FadeIn(trunk), run_time=0.6)
		self.play(
			Create(line_23_left),
			Create(line_23_right),
			FadeIn(cmp_13_left, shift=0.1 * DOWN),
			FadeIn(cmp_12_right, shift=0.1 * DOWN),
			run_time=0.9,
		)
		self.play(
			Create(line_13_left_left),
			Create(line_13_left_right),
			Create(line_12_right_left),
			Create(line_12_right_right),
			FadeIn(cmp_12_left, shift=0.1 * DOWN),
			FadeIn(leaf_132, shift=0.1 * DOWN),
			FadeIn(cmp_13_right, shift=0.1 * DOWN),
			FadeIn(leaf_123, shift=0.1 * DOWN),
			run_time=1.0,
		)
		self.play(
			Create(line_12_left_left),
			Create(line_12_left_right),
			Create(line_13_right_left),
			Create(line_13_right_right),
			FadeIn(leaf_321, shift=0.1 * DOWN),
			FadeIn(leaf_312, shift=0.1 * DOWN),
			FadeIn(leaf_231, shift=0.1 * DOWN),
			FadeIn(leaf_213, shift=0.1 * DOWN),
			run_time=1.0,
		)
		self.play(FadeIn(output_list, shift=0.1 * UP), run_time=0.7)

		self.next_slide()

		self.play(
			output_list.animate.shift(output_list_shift),
			FadeIn(output_tail, shift=0.1 * UP),
			run_time=0.8,
		)

		tree_group = VGroup(
			title,
			cmp_23,
			cmp_13_left,
			cmp_12_right,
			cmp_12_left,
			cmp_13_right,
			leaf_132,
			leaf_123,
			leaf_312,
			leaf_321,
			leaf_213,
			leaf_231,
			trunk,
			line_23_left,
			line_23_right,
			line_13_left_left,
			line_13_left_right,
			line_12_right_left,
			line_12_right_right,
			line_12_left_left,
			line_12_left_right,
			line_13_right_left,
			line_13_right_right,
			output_list,
			output_tail,
		)

		self.next_slide()

		self.play(FadeOut(tree_group, shift=0.1 * DOWN), run_time=0.8)

		selection_creature = LambdaCreature(
			body_color="#5e5086", eye_color=WHITE, pupil_color=BLACK, height=1.6
		)
		selection_creature.move_to(LEFT * 4.0 + DOWN * 0.55)
		selection_creature.set_z_index(12)

		selection_bubble_text = Paragraph(
			"What about",
			"selection sort?",
			alignment="center",
			font_size=24,
			color=WHITE,
		)
		selection_bubble_text.set_max_width(3.4)
		selection_bubble = Ellipse(
			width=selection_bubble_text.width + 0.8,
			height=selection_bubble_text.height + 0.45,
			color=WHITE,
			stroke_width=2,
			fill_opacity=0,
		)
		selection_bubble.move_to(selection_bubble_text.get_center())
		selection_bubble_group = VGroup(selection_bubble, selection_bubble_text)
		selection_bubble_group.next_to(selection_creature, UP, buff=0.28)
		selection_bubble_group.shift(RIGHT * 0.25 + UP * 0.2)
		selection_bubble_group.set_z_index(11)

		selection_title = Text("Selection Sort", font_size=38, color=BLUE_B)
		selection_step1 = Text("Scans unsorted part of list", font_size=24, color=WHITE)
		selection_step2 = Text(
			"Finds and places the minimum at the front", font_size=24, color=WHITE
		)
		selection_step3 = Text(
			"Repeats the scan until the entire list is sorted",
			font_size=24,
			color=WHITE,
		)
		selection_step1.set_max_width(5.6)
		selection_step2.set_max_width(5.6)
		selection_step3.set_max_width(5.6)
		selection_arrow1 = MathTex(r"\downarrow", font_size=30, color=WHITE)
		selection_arrow2 = MathTex(r"\downarrow", font_size=30, color=WHITE)
		selection_gap = Rectangle(
			width=0.1, height=0.2, stroke_opacity=0, fill_opacity=0
		)

		selection_block = VGroup(
			selection_title,
			selection_gap,
			selection_step1,
			selection_arrow1,
			selection_step2,
			selection_arrow2,
			selection_step3,
		).arrange(DOWN, buff=0.26)
		selection_block.to_edge(RIGHT, buff=0.95)
		selection_block.shift(UP * 0.2)

		self.play(
			FadeIn(selection_creature, shift=0.2 * RIGHT),
			FadeIn(selection_bubble_group, shift=0.1 * UP),
			run_time=1.2,
		)

		self.next_slide()

		self.play(
			FadeIn(selection_block, shift=0.2 * LEFT),
			run_time=1.2,
		)

		self.next_slide()

		self.play(
			FadeOut(selection_creature, shift=0.1 * DOWN),
			FadeOut(selection_bubble_group, shift=0.1 * DOWN),
			FadeOut(selection_block, shift=0.1 * DOWN),
			run_time=0.8,
		)

		sel_title = MathTex(
			r"\mathrm{selectSort}(\mathrm{coinCmp}, [2, 3, 1])", font_size=42
		)
		sel_title.to_edge(UP, buff=0.45)

		sel_level1_y = 2.0
		sel_level2_y = 0.7
		sel_level3_y = -0.7
		sel_level4_y = -2.2
		sel_x_level2 = 3.6
		sel_x_level3 = 1.8
		sel_x_level4 = 0.9

		sel_x_left = -sel_x_level2
		sel_x_right = sel_x_level2
		sel_x_left_left = sel_x_left - sel_x_level3
		sel_x_left_right = sel_x_left + sel_x_level3
		sel_x_right_left = sel_x_right - sel_x_level3
		sel_x_right_right = sel_x_right + sel_x_level3
		sel_x_left_left_left = sel_x_left_left - sel_x_level4
		sel_x_left_left_right = sel_x_left_left + sel_x_level4
		sel_x_left_right_left = sel_x_left_right - sel_x_level4
		sel_x_left_right_right = sel_x_left_right + sel_x_level4
		sel_x_right_left_left = sel_x_right_left - sel_x_level4
		sel_x_right_left_right = sel_x_right_left + sel_x_level4
		sel_x_right_right_left = sel_x_right_right - sel_x_level4
		sel_x_right_right_right = sel_x_right_right + sel_x_level4

		sel_cmp_23 = MathTex(r"2 \le 3", font_size=36)
		sel_cmp_23.move_to(UP * sel_level1_y)

		sel_cmp_13_left = MathTex(r"1 \le 3", font_size=34)
		sel_cmp_13_left.move_to(RIGHT * sel_x_left + UP * sel_level2_y)

		sel_cmp_12_right = MathTex(r"1 \le 2", font_size=34)
		sel_cmp_12_right.move_to(RIGHT * sel_x_right + UP * sel_level2_y)

		sel_cmp_12_left = MathTex(r"1 \le 2", font_size=32)
		sel_cmp_12_left.move_to(RIGHT * sel_x_left_left + UP * sel_level3_y)

		sel_cmp_23_left = MathTex(r"2 \le 3", font_size=32)
		sel_cmp_23_left.move_to(RIGHT * sel_x_left_right + UP * sel_level3_y)

		sel_cmp_13_right = MathTex(r"1 \le 3", font_size=32)
		sel_cmp_13_right.move_to(RIGHT * sel_x_right_left + UP * sel_level3_y)

		sel_cmp_23_right = MathTex(r"2 \le 3", font_size=32)
		sel_cmp_23_right.move_to(RIGHT * sel_x_right_right + UP * sel_level3_y)

		sel_leaf_321 = MathTex(r"[3, 2, 1]", font_size=28)
		sel_leaf_321.move_to(RIGHT * sel_x_left_left_left + UP * sel_level4_y)

		sel_leaf_312 = MathTex(r"[3, 1, 2]", font_size=28)
		sel_leaf_312.move_to(RIGHT * sel_x_left_left_right + UP * sel_level4_y)

		sel_leaf_132_a = MathTex(r"[1, 3, 2]", font_size=28)
		sel_leaf_132_a.move_to(RIGHT * sel_x_left_right_left + UP * sel_level4_y)

		sel_leaf_123_a = MathTex(r"[1, 2, 3]", font_size=28)
		sel_leaf_123_a.move_to(RIGHT * sel_x_left_right_right + UP * sel_level4_y)

		sel_leaf_231 = MathTex(r"[2, 3, 1]", font_size=28)
		sel_leaf_231.move_to(RIGHT * sel_x_right_left_left + UP * sel_level4_y)

		sel_leaf_213 = MathTex(r"[2, 1, 3]", font_size=28)
		sel_leaf_213.move_to(RIGHT * sel_x_right_left_right + UP * sel_level4_y)

		sel_leaf_132_b = MathTex(r"[1, 3, 2]", font_size=28)
		sel_leaf_132_b.move_to(RIGHT * sel_x_right_right_left + UP * sel_level4_y)

		sel_leaf_123_b = MathTex(r"[1, 2, 3]", font_size=28)
		sel_leaf_123_b.move_to(RIGHT * sel_x_right_right_right + UP * sel_level4_y)

		sel_true_color = GREEN_B
		sel_false_color = RED_B

		sel_trunk = Line(
			sel_title.get_bottom(), sel_cmp_23.get_top(), color=GREY_B, stroke_width=2
		)
		sel_line_23_left = Line(
			sel_cmp_23.get_bottom(),
			sel_cmp_13_left.get_top(),
			color=sel_false_color,
			stroke_width=3,
		)
		sel_line_23_right = Line(
			sel_cmp_23.get_bottom(),
			sel_cmp_12_right.get_top(),
			color=sel_true_color,
			stroke_width=3,
		)
		sel_line_13_left_left = Line(
			sel_cmp_13_left.get_bottom(),
			sel_cmp_12_left.get_top(),
			color=sel_false_color,
			stroke_width=3,
		)
		sel_line_13_left_right = Line(
			sel_cmp_13_left.get_bottom(),
			sel_cmp_23_left.get_top(),
			color=sel_true_color,
			stroke_width=3,
		)
		sel_line_12_right_left = Line(
			sel_cmp_12_right.get_bottom(),
			sel_cmp_13_right.get_top(),
			color=sel_false_color,
			stroke_width=3,
		)
		sel_line_12_right_right = Line(
			sel_cmp_12_right.get_bottom(),
			sel_cmp_23_right.get_top(),
			color=sel_true_color,
			stroke_width=3,
		)
		sel_line_12_left_left = Line(
			sel_cmp_12_left.get_bottom(),
			sel_leaf_321.get_top(),
			color=sel_false_color,
			stroke_width=3,
		)
		sel_line_12_left_right = Line(
			sel_cmp_12_left.get_bottom(),
			sel_leaf_312.get_top(),
			color=sel_true_color,
			stroke_width=3,
		)
		sel_line_23_left_left = Line(
			sel_cmp_23_left.get_bottom(),
			sel_leaf_132_a.get_top(),
			color=sel_false_color,
			stroke_width=3,
		)
		sel_line_23_left_right = Line(
			sel_cmp_23_left.get_bottom(),
			sel_leaf_123_a.get_top(),
			color=sel_true_color,
			stroke_width=3,
		)
		sel_line_13_right_left = Line(
			sel_cmp_13_right.get_bottom(),
			sel_leaf_231.get_top(),
			color=sel_false_color,
			stroke_width=3,
		)
		sel_line_13_right_right = Line(
			sel_cmp_13_right.get_bottom(),
			sel_leaf_213.get_top(),
			color=sel_true_color,
			stroke_width=3,
		)
		sel_line_23_right_left = Line(
			sel_cmp_23_right.get_bottom(),
			sel_leaf_132_b.get_top(),
			color=sel_false_color,
			stroke_width=3,
		)
		sel_line_23_right_right = Line(
			sel_cmp_23_right.get_bottom(),
			sel_leaf_123_b.get_top(),
			color=sel_true_color,
			stroke_width=3,
		)

		sel_output_list = MathTex(
			r"\left[\,[3, 2, 1], [3, 1, 2], [1, 3, 2], [1, 2, 3], [2, 3, 1], [2, 1, 3], [1, 3, 2], [1, 2, 3] \,\right]",
			font_size=28,
			color=WHITE,
			substrings_to_isolate=[r"[1, 2, 3]"],
		)
		sel_output_list.to_edge(DOWN, buff=0.35)
		sel_output_list.set_max_width(9.8)
		sel_output_list_matches = VGroup(
			*[
				submob
				for submob in sel_output_list
				if getattr(submob, "tex_string", None) == r"[1, 2, 3]"
			]
		)

		sel_output_tail = Text("We get [1, 2, 3] twice!", font_size=24, color=WHITE)
		sel_output_tail.next_to(sel_output_list, RIGHT, buff=0.3)
		sel_output_tail.align_to(sel_output_list, DOWN)
		sel_output_list_shift = LEFT * ((sel_output_tail.width + 0.3) / 2)
		sel_output_tail.shift(sel_output_list_shift)

		sel_tree_group = VGroup(
			sel_title,
			sel_cmp_23,
			sel_cmp_13_left,
			sel_cmp_12_right,
			sel_cmp_12_left,
			sel_cmp_23_left,
			sel_cmp_13_right,
			sel_cmp_23_right,
			sel_leaf_321,
			sel_leaf_312,
			sel_leaf_132_a,
			sel_leaf_123_a,
			sel_leaf_231,
			sel_leaf_213,
			sel_leaf_132_b,
			sel_leaf_123_b,
			sel_trunk,
			sel_line_23_left,
			sel_line_23_right,
			sel_line_13_left_left,
			sel_line_13_left_right,
			sel_line_12_right_left,
			sel_line_12_right_right,
			sel_line_12_left_left,
			sel_line_12_left_right,
			sel_line_23_left_left,
			sel_line_23_left_right,
			sel_line_13_right_left,
			sel_line_13_right_right,
			sel_line_23_right_left,
			sel_line_23_right_right,
			sel_output_list,
			sel_output_tail,
		)
		sel_jiggle_targets = VGroup(sel_leaf_123_a, sel_leaf_123_b)
		sel_jiggle_targets.add(*sel_output_list_matches)

		self.play(FadeIn(sel_title, shift=0.1 * DOWN), run_time=0.6)
		self.play(FadeIn(sel_cmp_23, shift=0.1 * DOWN), FadeIn(sel_trunk), run_time=0.6)
		self.play(
			Create(sel_line_23_left),
			Create(sel_line_23_right),
			FadeIn(sel_cmp_13_left, shift=0.1 * DOWN),
			FadeIn(sel_cmp_12_right, shift=0.1 * DOWN),
			run_time=0.9,
		)
		self.play(
			Create(sel_line_13_left_left),
			Create(sel_line_13_left_right),
			Create(sel_line_12_right_left),
			Create(sel_line_12_right_right),
			FadeIn(sel_cmp_12_left, shift=0.1 * DOWN),
			FadeIn(sel_cmp_23_left, shift=0.1 * DOWN),
			FadeIn(sel_cmp_13_right, shift=0.1 * DOWN),
			FadeIn(sel_cmp_23_right, shift=0.1 * DOWN),
			run_time=1.0,
		)
		self.play(
			Create(sel_line_12_left_left),
			Create(sel_line_12_left_right),
			Create(sel_line_23_left_left),
			Create(sel_line_23_left_right),
			Create(sel_line_13_right_left),
			Create(sel_line_13_right_right),
			Create(sel_line_23_right_left),
			Create(sel_line_23_right_right),
			FadeIn(sel_leaf_321, shift=0.1 * DOWN),
			FadeIn(sel_leaf_312, shift=0.1 * DOWN),
			FadeIn(sel_leaf_132_a, shift=0.1 * DOWN),
			FadeIn(sel_leaf_123_a, shift=0.1 * DOWN),
			FadeIn(sel_leaf_231, shift=0.1 * DOWN),
			FadeIn(sel_leaf_213, shift=0.1 * DOWN),
			FadeIn(sel_leaf_132_b, shift=0.1 * DOWN),
			FadeIn(sel_leaf_123_b, shift=0.1 * DOWN),
			run_time=1.2,
		)
		self.play(FadeIn(sel_output_list, shift=0.1 * UP), run_time=0.7)

		self.next_slide()

		self.play(
			sel_output_list.animate.shift(sel_output_list_shift).set_color_by_tex(
				r"[1, 2, 3]", BLUE_B
			),
			FadeIn(sel_output_tail, shift=0.1 * UP),
			sel_leaf_123_a.animate.set_color(BLUE_B),
			sel_leaf_123_b.animate.set_color(BLUE_B),
			run_time=0.8,
		)

		self.next_slide()

		self.play(FadeOut(sel_tree_group, shift=0.1 * DOWN), run_time=0.6)

		title_size = 38
		body_size = 36

		problem_title = Tex("Problem", font_size=title_size, color=BLUE_B)
		problem_line1 = MathTex(
			r"\text{Selection sort asks if } a \le b \text{ twice in the same branch,}",
			font_size=body_size,
			color=WHITE,
		)
		problem_line2 = MathTex(
			r"\text{different answers from coinCmp lead to duplicates}",
			font_size=body_size,
			color=WHITE,
		)
		problem_text = VGroup(problem_line1, problem_line2).arrange(DOWN, buff=0.12)
		problem_block = VGroup(problem_title, problem_text).arrange(DOWN, buff=0.18)
		problem_block.to_edge(UP, buff=0.45)

		left_text = MathTex(
			r"\begin{aligned}"
			r"&\text{in } [2, 3, 1]: 2 \nleq 3, 1 \le 3 \Rightarrow \text{min} = 1\\"
			r"&\text{in } [2, 3]: 2 \le 3 \Rightarrow \text{min} = 2\\"
			r"&\text{so the result} = [1, 2, 3]"
			r"\end{aligned}",
			font_size=body_size,
			color=WHITE,
		)
		right_text = MathTex(
			r"\begin{aligned}"
			r"&\text{in } [2, 3, 1]: 2 \le 3, 1 \le 2 \Rightarrow \text{min} = 1\\"
			r"&\text{then in } [2, 3]: 2 \le 3 \Rightarrow \text{min} = 2\\"
			r"&\text{so the result} = [1, 2, 3]"
			r"\end{aligned}",
			font_size=body_size,
			color=WHITE,
		)
		middle_group = VGroup(left_text, right_text).arrange(
			RIGHT, buff=1.1, aligned_edge=UP
		)
		middle_group.move_to(ORIGIN + DOWN * 0.1)

		divider = Line(UP, DOWN, color=GREY_B, stroke_width=2)
		divider.set_height(middle_group.height + 0.4)
		divider.move_to(middle_group.get_center())

		solution_title = Tex("Solution", font_size=title_size, color=BLUE_B)
		solution_text = Tex(
			r"The result of coinCmp(2, 3) should be consistent within the same branch\\"
			r"Make coinCmp remember its past decisions!",
			font_size=body_size,
			color=WHITE,
			tex_to_color_map={"consistent": BLUE_B},
		)
		solution_block = VGroup(solution_title, solution_text).arrange(DOWN, buff=0.18)
		solution_block.to_edge(DOWN, buff=0.45)

		self.play(
			FadeIn(problem_block, shift=0.1 * DOWN),
			run_time=0.9,
		)

		self.next_slide()

		self.play(
			FadeIn(middle_group, shift=0.1 * UP),
			FadeIn(divider),
			run_time=0.9,
		)

		self.next_slide()

		self.play(
			FadeIn(solution_block, shift=0.1 * UP),
			run_time=0.9,
		)

		self.next_slide()

		self.play(
			FadeOut(problem_block, shift=0.1 * DOWN),
			FadeOut(middle_group, shift=0.1 * DOWN),
			FadeOut(divider),
			FadeOut(solution_block, shift=0.1 * DOWN),
			run_time=0.6,
		)

		happy_creature = ExpressionLambda(
			body_color="#5e5086", eye_color=WHITE, pupil_color=BLACK, height=1.8
		)
		happy_creature.move_to(ORIGIN + DOWN * 0.35)
		happy_creature.set_z_index(12)

		happy_bubble_text = Paragraph(
			"Let's test a few more",
			"sorting algorithms!",
			alignment="center",
			font_size=24,
			color=WHITE,
		)
		happy_bubble = Ellipse(
			width=happy_bubble_text.width + 1.0,
			height=happy_bubble_text.height + 0.6,
			color=WHITE,
			stroke_width=2,
			fill_opacity=0,
		)
		happy_bubble.move_to(happy_bubble_text.get_center())
		happy_bubble_group = VGroup(happy_bubble, happy_bubble_text)
		happy_bubble_group.next_to(happy_creature, UP, buff=0.35)
		happy_bubble_group.set_z_index(11)

		self.play(
			FadeIn(happy_creature, shift=0.15 * UP),
			FadeIn(happy_bubble_group, shift=0.15 * UP),
			happy_creature.happy(),
			run_time=1.0,
		)

		self.next_slide()

		self.play(
			FadeOut(happy_creature, shift=0.1 * DOWN),
			FadeOut(happy_bubble_group, shift=0.1 * DOWN),
			run_time=0.6,
		)

		bubble_title = Text("Bubble Sort", font_size=38, color=BLUE_B)
		bubble_step1 = Text("Steps through the list", font_size=24, color=WHITE)
		bubble_step2 = Text("Compares adjacent elements", font_size=24, color=WHITE)
		bubble_step3 = Text(
			"Swaps them if they're in the wrong order", font_size=24, color=WHITE
		)
		bubble_step4 = Text(
			"Repeats until no swaps are needed", font_size=24, color=WHITE
		)
		bubble_arrow1 = MathTex(r"\downarrow", font_size=30, color=WHITE)
		bubble_arrow2 = MathTex(r"\downarrow", font_size=30, color=WHITE)
		bubble_arrow3 = MathTex(r"\downarrow", font_size=30, color=WHITE)
		bubble_gap = Rectangle(width=0.1, height=0.2, stroke_opacity=0, fill_opacity=0)

		bubble_block = VGroup(
			bubble_title,
			bubble_gap,
			bubble_step1,
			bubble_arrow1,
			bubble_step2,
			bubble_arrow2,
			bubble_step3,
			bubble_arrow3,
			bubble_step4,
		).arrange(DOWN, buff=0.26)
		bubble_block.move_to(ORIGIN)

		self.play(
			FadeIn(bubble_block, shift=0.1 * UP),
			run_time=1.0,
		)

		self.next_slide()

		self.play(FadeOut(bubble_block, shift=0.1 * DOWN), run_time=0.6)

		bubble_tree_title = MathTex(
			r"\mathrm{bubbleSort}(\mathrm{coinCmp}, [2, 3, 1])", font_size=42
		)
		bubble_tree_title.to_edge(UP, buff=0.45)

		bubble_level1_y = 2.0
		bubble_level2_y = 0.7
		bubble_level3_y = -0.7
		bubble_level4_y = -2.2
		bubble_x_level2 = 3.6
		bubble_x_level3 = 1.8
		bubble_x_level4 = 0.9

		bubble_x_left = -bubble_x_level2
		bubble_x_right = bubble_x_level2
		bubble_x_left_left = bubble_x_left - bubble_x_level3
		bubble_x_left_right = bubble_x_left + bubble_x_level3
		bubble_x_right_left = bubble_x_right - bubble_x_level3
		bubble_x_right_right = bubble_x_right + bubble_x_level3
		bubble_x_left_left_left = bubble_x_left_left - bubble_x_level4
		bubble_x_left_left_right = bubble_x_left_left + bubble_x_level4
		bubble_x_left_right_left = bubble_x_left_right - bubble_x_level4
		bubble_x_left_right_right = bubble_x_left_right + bubble_x_level4
		bubble_x_right_left_left = bubble_x_right_left - bubble_x_level4
		bubble_x_right_left_right = bubble_x_right_left + bubble_x_level4
		bubble_x_right_right_left = bubble_x_right_right - bubble_x_level4
		bubble_x_right_right_right = bubble_x_right_right + bubble_x_level4

		bubble_cmp_23 = MathTex(r"2 \le 3", font_size=36)
		bubble_cmp_23.move_to(UP * bubble_level1_y)

		bubble_cmp_12_left = MathTex(r"1 \le 2", font_size=34)
		bubble_cmp_12_left.move_to(RIGHT * bubble_x_left + UP * bubble_level2_y)

		bubble_cmp_13_right = MathTex(r"1 \le 3", font_size=34)
		bubble_cmp_13_right.move_to(RIGHT * bubble_x_right + UP * bubble_level2_y)

		bubble_cmp_23_left = MathTex(r"2 \le 3", font_size=32)
		bubble_cmp_23_left.move_to(RIGHT * bubble_x_left_left + UP * bubble_level3_y)

		bubble_cmp_13_left = MathTex(r"1 \le 3", font_size=32)
		bubble_cmp_13_left.move_to(RIGHT * bubble_x_left_right + UP * bubble_level3_y)

		bubble_cmp_32_right = MathTex(r"3 \le 2", font_size=32)
		bubble_cmp_32_right.move_to(RIGHT * bubble_x_right_left + UP * bubble_level3_y)

		bubble_cmp_12_right = MathTex(r"1 \le 2", font_size=32)
		bubble_cmp_12_right.move_to(RIGHT * bubble_x_right_right + UP * bubble_level3_y)

		bubble_leaf_123_a = MathTex(r"[1, 2, 3]", font_size=28)
		bubble_leaf_123_a.move_to(
			RIGHT * bubble_x_left_left_left + UP * bubble_level4_y
		)

		bubble_leaf_132_a = MathTex(r"[1, 3, 2]", font_size=28)
		bubble_leaf_132_a.move_to(
			RIGHT * bubble_x_left_left_right + UP * bubble_level4_y
		)

		bubble_leaf_213 = MathTex(r"[2, 1, 3]", font_size=28)
		bubble_leaf_213.move_to(RIGHT * bubble_x_left_right_left + UP * bubble_level4_y)

		bubble_leaf_231 = MathTex(r"[2, 3, 1]", font_size=28)
		bubble_leaf_231.move_to(
			RIGHT * bubble_x_left_right_right + UP * bubble_level4_y
		)

		bubble_leaf_132_b = MathTex(r"[1, 3, 2]", font_size=28)
		bubble_leaf_132_b.move_to(
			RIGHT * bubble_x_right_left_left + UP * bubble_level4_y
		)

		bubble_leaf_123_b = MathTex(r"[1, 2, 3]", font_size=28)
		bubble_leaf_123_b.move_to(
			RIGHT * bubble_x_right_left_right + UP * bubble_level4_y
		)

		bubble_leaf_312 = MathTex(r"[3, 1, 2]", font_size=28)
		bubble_leaf_312.move_to(
			RIGHT * bubble_x_right_right_left + UP * bubble_level4_y
		)

		bubble_leaf_321 = MathTex(r"[3, 2, 1]", font_size=28)
		bubble_leaf_321.move_to(
			RIGHT * bubble_x_right_right_right + UP * bubble_level4_y
		)

		bubble_true_color = GREEN_B
		bubble_false_color = RED_B

		bubble_trunk = Line(
			bubble_tree_title.get_bottom(),
			bubble_cmp_23.get_top(),
			color=GREY_B,
			stroke_width=2,
		)
		bubble_line_23_left = Line(
			bubble_cmp_23.get_bottom(),
			bubble_cmp_12_left.get_top(),
			color=bubble_false_color,
			stroke_width=3,
		)
		bubble_line_23_right = Line(
			bubble_cmp_23.get_bottom(),
			bubble_cmp_13_right.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)
		bubble_line_12_left_left = Line(
			bubble_cmp_12_left.get_bottom(),
			bubble_cmp_23_left.get_top(),
			color=bubble_false_color,
			stroke_width=3,
		)
		bubble_line_12_left_right = Line(
			bubble_cmp_12_left.get_bottom(),
			bubble_cmp_13_left.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)
		bubble_line_13_right_left = Line(
			bubble_cmp_13_right.get_bottom(),
			bubble_cmp_32_right.get_top(),
			color=bubble_false_color,
			stroke_width=3,
		)
		bubble_line_13_right_right = Line(
			bubble_cmp_13_right.get_bottom(),
			bubble_cmp_12_right.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)
		bubble_line_23_left_left = Line(
			bubble_cmp_23_left.get_bottom(),
			bubble_leaf_123_a.get_top(),
			color=bubble_false_color,
			stroke_width=3,
		)
		bubble_line_23_left_right = Line(
			bubble_cmp_23_left.get_bottom(),
			bubble_leaf_132_a.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)
		bubble_line_13_left_left = Line(
			bubble_cmp_13_left.get_bottom(),
			bubble_leaf_213.get_top(),
			color=bubble_false_color,
			stroke_width=3,
		)
		bubble_line_13_left_right = Line(
			bubble_cmp_13_left.get_bottom(),
			bubble_leaf_231.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)
		bubble_line_32_right_left = Line(
			bubble_cmp_32_right.get_bottom(),
			bubble_leaf_132_b.get_top(),
			color=bubble_false_color,
			stroke_width=3,
		)
		bubble_line_32_right_right = Line(
			bubble_cmp_32_right.get_bottom(),
			bubble_leaf_123_b.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)
		bubble_line_12_right_left = Line(
			bubble_cmp_12_right.get_bottom(),
			bubble_leaf_312.get_top(),
			color=bubble_false_color,
			stroke_width=3,
		)
		bubble_line_12_right_right = Line(
			bubble_cmp_12_right.get_bottom(),
			bubble_leaf_321.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)

		bubble_note = Text(
			"bubbleSort duplicates [1, 2, 3] even with a consistent coinCmp!",
			font_size=28,
			color=WHITE,
		)
		bubble_note.to_edge(DOWN, buff=0.4)
		bubble_note.set_max_width(11.0)

		bubble_simplified_x = LEFT * 5.4
		bubble_simplified_step = 1.75
		bubble_simplified_top = 1.5 * bubble_simplified_step
		bubble_cmp_23_target = bubble_cmp_23.copy().move_to(
			bubble_simplified_x + UP * bubble_simplified_top
		)
		bubble_cmp_13_target = bubble_cmp_13_right.copy().move_to(
			bubble_simplified_x + UP * (bubble_simplified_top - bubble_simplified_step)
		)
		bubble_cmp_32_target = bubble_cmp_32_right.copy().move_to(
			bubble_simplified_x
			+ UP * (bubble_simplified_top - 2 * bubble_simplified_step)
		)
		bubble_leaf_123_target = bubble_leaf_123_b.copy().move_to(
			bubble_simplified_x
			+ UP * (bubble_simplified_top - 3 * bubble_simplified_step)
		)

		bubble_line_23_simplified = Line(
			bubble_cmp_23_target.get_bottom(),
			bubble_cmp_13_target.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)
		bubble_line_13_simplified = Line(
			bubble_cmp_13_target.get_bottom(),
			bubble_cmp_32_target.get_top(),
			color=bubble_false_color,
			stroke_width=3,
		)
		bubble_line_32_simplified = Line(
			bubble_cmp_32_target.get_bottom(),
			bubble_leaf_123_target.get_top(),
			color=bubble_true_color,
			stroke_width=3,
		)

		bubble_problem_title = Tex("Problem", font_size=38, color=BLUE_B)
		bubble_problem_text = MathTex(
			r"\begin{aligned}"
			r"&\text{Bubble sort occasionally evaluates both } a \le b \text{ and } b \le a\\"
			r"&\text{within the same branch; both evaluating to true or to false}\\"
			r"&\text{can lead to duplicates}"
			r"\end{aligned}",
			font_size=36,
			color=WHITE,
		)
		bubble_problem_block = VGroup(
			bubble_problem_title, bubble_problem_text
		).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

		bubble_solution_title = Tex("Solution", font_size=38, color=BLUE_B)
		bubble_solution_text = MathTex(
			r"\begin{aligned}"
			r"&\text{Enforce totality on coinCmp; if it evaluates } \text{coinCmp}(a, b) \text{ as true}\\"
			r"&\text{it must also remember the inverse to be false}"
			r"\end{aligned}",
			font_size=36,
			color=WHITE,
			tex_to_color_map={"totality": BLUE_B},
		)
		bubble_solution_block = VGroup(
			bubble_solution_title, bubble_solution_text
		).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

		bubble_right_block = VGroup(
			bubble_problem_block, bubble_solution_block
		).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
		bubble_right_block.to_edge(RIGHT, buff=0.7)
		bubble_right_block.shift(UP * (-bubble_right_block.get_center()[1]))

		self.play(FadeIn(bubble_tree_title, shift=0.1 * DOWN), run_time=0.6)
		self.play(
			FadeIn(bubble_cmp_23, shift=0.1 * DOWN),
			FadeIn(bubble_trunk),
			run_time=0.6,
		)
		self.play(
			Create(bubble_line_23_left),
			Create(bubble_line_23_right),
			FadeIn(bubble_cmp_12_left, shift=0.1 * DOWN),
			FadeIn(bubble_cmp_13_right, shift=0.1 * DOWN),
			run_time=0.9,
		)
		self.play(
			Create(bubble_line_12_left_left),
			Create(bubble_line_12_left_right),
			Create(bubble_line_13_right_left),
			Create(bubble_line_13_right_right),
			FadeIn(bubble_cmp_23_left, shift=0.1 * DOWN),
			FadeIn(bubble_cmp_13_left, shift=0.1 * DOWN),
			FadeIn(bubble_cmp_32_right, shift=0.1 * DOWN),
			FadeIn(bubble_cmp_12_right, shift=0.1 * DOWN),
			run_time=1.0,
		)
		self.play(
			Create(bubble_line_23_left_left),
			Create(bubble_line_23_left_right),
			Create(bubble_line_13_left_left),
			Create(bubble_line_13_left_right),
			Create(bubble_line_32_right_left),
			Create(bubble_line_32_right_right),
			Create(bubble_line_12_right_left),
			Create(bubble_line_12_right_right),
			FadeIn(bubble_leaf_123_a, shift=0.1 * DOWN),
			FadeIn(bubble_leaf_132_a, shift=0.1 * DOWN),
			FadeIn(bubble_leaf_213, shift=0.1 * DOWN),
			FadeIn(bubble_leaf_231, shift=0.1 * DOWN),
			FadeIn(bubble_leaf_132_b, shift=0.1 * DOWN),
			FadeIn(bubble_leaf_123_b, shift=0.1 * DOWN),
			FadeIn(bubble_leaf_312, shift=0.1 * DOWN),
			FadeIn(bubble_leaf_321, shift=0.1 * DOWN),
			FadeIn(bubble_note, shift=0.1 * UP),
			run_time=1.2,
		)

		self.next_slide()

		bubble_fade_group = VGroup(
			bubble_tree_title,
			bubble_trunk,
			bubble_cmp_12_left,
			bubble_cmp_23_left,
			bubble_cmp_13_left,
			bubble_cmp_12_right,
			bubble_leaf_123_a,
			bubble_leaf_132_a,
			bubble_leaf_213,
			bubble_leaf_231,
			bubble_leaf_132_b,
			bubble_leaf_312,
			bubble_leaf_321,
			bubble_line_23_left,
			bubble_line_12_left_left,
			bubble_line_12_left_right,
			bubble_line_13_right_right,
			bubble_line_23_left_left,
			bubble_line_23_left_right,
			bubble_line_13_left_left,
			bubble_line_13_left_right,
			bubble_line_32_right_left,
			bubble_line_12_right_left,
			bubble_line_12_right_right,
			bubble_note,
		)

		self.play(
			FadeOut(bubble_fade_group, shift=0.1 * DOWN),
			bubble_cmp_23.animate.move_to(bubble_cmp_23_target.get_center()),
			bubble_cmp_13_right.animate.move_to(bubble_cmp_13_target.get_center()),
			bubble_cmp_32_right.animate.move_to(bubble_cmp_32_target.get_center()),
			bubble_leaf_123_b.animate.move_to(bubble_leaf_123_target.get_center()),
			ReplacementTransform(bubble_line_23_right, bubble_line_23_simplified),
			ReplacementTransform(bubble_line_13_right_left, bubble_line_13_simplified),
			ReplacementTransform(bubble_line_32_right_right, bubble_line_32_simplified),
			FadeIn(bubble_right_block, shift=0.1 * UP),
			run_time=1.2,
		)

		bubble_simplified_group = VGroup(
			bubble_cmp_23,
			bubble_cmp_13_right,
			bubble_cmp_32_right,
			bubble_leaf_123_b,
			bubble_line_23_simplified,
			bubble_line_13_simplified,
			bubble_line_32_simplified,
		)

		self.next_slide()

		self.play(
			FadeOut(bubble_simplified_group, shift=0.1 * DOWN),
			FadeOut(bubble_right_block, shift=0.1 * DOWN),
			run_time=0.6,
		)

		patience_title = Text("Patience Sort", font_size=38, color=BLUE_B)
		patience_step1 = Text("Iterates through the list", font_size=24, color=WHITE)
		patience_step2 = Text(
			"Divides elements into piles based on ascending values",
			font_size=24,
			color=WHITE,
		)
		patience_step3 = Text(
			"Systematically merges piles back together", font_size=24, color=WHITE
		)
		patience_step1.set_max_width(9.6)
		patience_step2.set_max_width(9.6)
		patience_step3.set_max_width(9.6)
		patience_arrow1 = MathTex(r"\downarrow", font_size=30, color=WHITE)
		patience_arrow2 = MathTex(r"\downarrow", font_size=30, color=WHITE)
		patience_gap = Rectangle(
			width=0.1, height=0.2, stroke_opacity=0, fill_opacity=0
		)

		patience_block = VGroup(
			patience_title,
			patience_gap,
			patience_step1,
			patience_arrow1,
			patience_step2,
			patience_arrow2,
			patience_step3,
		).arrange(DOWN, buff=0.26)
		patience_block.move_to(ORIGIN)

		self.play(FadeIn(patience_block, shift=0.1 * UP), run_time=1.0)

		self.next_slide()

		block_shift = UP * 1.2

		card_specs = [
			("7H", 7),
			("3D", 3),
			("9S", 9),
			("2C", 2),
			("8H", 8),
			("4S", 4),
			("6D", 6),
			("5C", 5),
		]
		cards = []
		for code, value in card_specs:
			card = ImageMobject(str(asset_dir / "cards" / f"{code}.png"))
			card.scale_to_fit_height(1.6)
			cards.append((card, value))

		cards_group = Group(*(card for card, _ in cards)).arrange(RIGHT, buff=0.2)
		cards_group.scale(1.0)
		cards_group.next_to(patience_block, DOWN, buff=0.7)
		cards_group.shift(block_shift + DOWN * 0.05)

		self.play(
			patience_block.animate.shift(block_shift),
			FadeIn(cards_group, shift=0.1 * UP),
			run_time=0.8,
		)

		pile_tops = []
		pile_counts = []
		placements = []
		for card, value in cards:
			chosen = None
			for index, top in enumerate(pile_tops):
				if top >= value:
					chosen = index
					break
			if chosen is None:
				pile_tops.append(value)
				pile_counts.append(0)
				chosen = len(pile_tops) - 1
			depth = pile_counts[chosen]
			pile_counts[chosen] += 1
			pile_tops[chosen] = value
			placements.append((card, chosen, depth))

		pile_count = len(pile_tops)
		pile_xs = np.linspace(-3.2, 3.2, pile_count)
		pile_top_y = cards_group.get_center()[1]
		stack_offset = 0.24
		moves = []
		for card, pile_index, depth in placements:
			target = np.array(
				[pile_xs[pile_index], pile_top_y - stack_offset * depth, 0]
			)
			card.set_z_index(10 + depth)
			moves.append(card.animate.move_to(target))

		self.play(LaggedStart(*moves, lag_ratio=0.2), run_time=2.5)

		self.next_slide()

		patience_fade_group = Group(patience_block, cards_group)
		self.play(
			FadeOut(patience_fade_group, shift=0.1 * DOWN),
			run_time=0.6,
		)

		title_size = 38
		body_size = 36

		patience_problem_title = Tex("Problem", font_size=title_size, color=BLUE_B)
		patience_problem_line1 = MathTex(
			r"\text{Even with a consistent and total coinCmp, patience sort generates duplicate permutations}",
			font_size=body_size,
			color=WHITE,
		)
		patience_problem_line2 = MathTex(
			r"\text{since it assumes transitivity to hold}",
			font_size=body_size,
			color=WHITE,
		)
		patience_problem_text = VGroup(
			patience_problem_line1, patience_problem_line2
		).arrange(DOWN, buff=0.12)
		patience_problem_block = VGroup(
			patience_problem_title, patience_problem_text
		).arrange(DOWN, buff=0.18)
		patience_problem_block.to_edge(UP, buff=0.45)

		patience_solution_title = Tex("Solution", font_size=title_size, color=BLUE_B)
		patience_solution_line1 = MathTex(
			r"\text{Every time a new comparision is made, use it and the history of all past comparisions}",
			font_size=body_size,
			color=WHITE,
		)
		patience_solution_line2 = MathTex(
			r"\text{to compute and log all transitive implications the new comparision has}",
			font_size=body_size,
			color=WHITE,
		)
		patience_solution_line3 = MathTex(
			r"\text{If } a \le b \text{ and } b \le c \text{ were true, then } a \le c \text{ is logged as true}",
			font_size=body_size,
			color=WHITE,
		)
		patience_solution_text = VGroup(
			patience_solution_line1,
			patience_solution_line2,
			patience_solution_line3,
		).arrange(DOWN, buff=0.12)
		patience_solution_block = VGroup(
			patience_solution_title, patience_solution_text
		).arrange(DOWN, buff=0.18)
		patience_solution_block.to_edge(DOWN, buff=0.45)

		for line in (
			patience_problem_line1,
			patience_problem_line2,
			patience_solution_line1,
			patience_solution_line2,
			patience_solution_line3,
		):
			line.set_max_width(11.0)

		self.play(
			FadeIn(patience_problem_block, shift=0.1 * DOWN),
			FadeIn(patience_solution_block, shift=0.1 * UP),
			run_time=0.9,
		)

		self.next_slide()
