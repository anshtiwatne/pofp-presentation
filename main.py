from pathlib import Path

import numpy as np

from manim import *
from manim_slides import Slide
from lambda_creature import ExpressionLambda


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
		reveal_origin = LEFT * 5.0 - DOWN * 0.25

		for page in page_stack:
			self.add(page)

		self.wait(0.01)
		self.next_slide()

		title = Text("All Sorts of Permutations", font_size=44)
		subtitle = Text("(functional pearl)", font_size=29, color=BLUE_B)
		authors = Text(
			"J. Christiansen, N. Danilenko, S. Dylus", font_size=26, color=GREY_B
		)
		title.next_to(subtitle, UP, buff=0.22)
		authors.next_to(subtitle, DOWN, buff=0.34)
		title_block = VGroup(title, subtitle, authors)
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

		# Voiceover/Intent: Transition into an insertion sort demo after the title card.
		self.play(
			AnimationGroup(*[FadeOut(page) for page in page_stack], lag_ratio=0.0),
			FadeOut(title_block, shift=0.15 * LEFT),
			run_time=1.0,
		)

		insert_values = [5, 2, 4, 1, 3]
		insert_expr = MathTex(
			r"\mathrm{insertSort}(\mathrm{cmp}, [5, 2, 4, 1, 3])",
			font_size=40,
			color=WHITE,
			substrings_to_isolate=[r"[5, 2, 4, 1, 3]", r"\mathrm{cmp}"],
		)
		insert_expr.move_to(ORIGIN)

		self.play(FadeIn(insert_expr, shift=0.1 * UP), run_time=0.8)

		self.next_slide()

		insert_expr_target = ORIGIN + UP * 1.2
		array_center = ORIGIN + DOWN * 0.3

		cells = VGroup()
		cell_groups = []
		for value in insert_values:
			box = Square(side_length=0.95, color=GREY_B, stroke_width=2)
			box.set_fill(color=GREY_D, opacity=0.2)
			label = Text(str(value), font_size=34, color=WHITE)
			label.move_to(box.get_center())
			cell = VGroup(box, label)
			cells.add(cell)
			cell_groups.append(cell)

		cells.arrange(RIGHT, buff=0.0)
		cells.move_to(array_center)
		slot_positions = [cell.get_center() for cell in cell_groups]
		cell_height = cell_groups[0][0].height
		sorted_fill = GREEN_C
		unsorted_fill = RED_C
		key_fill = YELLOW_C
		key_label_color = BLACK
		default_label_color = WHITE

		def set_insert_colors(sorted_cells, key_cell=None):
			for cell in cell_groups:
				box = cell[0]
				if cell is key_cell:
					box.set_fill(color=key_fill, opacity=0.5)
					cell[1].set_color(key_label_color)
				elif cell in sorted_cells:
					box.set_fill(color=sorted_fill, opacity=0.35)
					cell[1].set_color(default_label_color)
				else:
					box.set_fill(color=unsorted_fill, opacity=0.25)
					cell[1].set_color(default_label_color)

		set_insert_colors({cell_groups[0]})

		self.play(
			insert_expr.animate.move_to(insert_expr_target),
			FadeIn(cells, shift=0.08 * UP),
			run_time=1.1,
		)

		self.next_slide()

		cells_order = list(cell_groups)
		values_order = list(insert_values)
		key_offset = DOWN * cell_height

		for i in range(1, len(values_order)):
			key_cell = cells_order[i]
			key_value = values_order[i]

			# Voiceover/Intent: Drop the key below the row and step through comparisons.
			sorted_cells = set(cells_order[:i])
			set_insert_colors(sorted_cells, key_cell=key_cell)

			key_cell.set_z_index(10)
			self.play(
				key_cell.animate.move_to(slot_positions[i] + key_offset),
				run_time=0.45,
			)
			self.next_slide()

			cells_order[i] = None
			values_order[i] = None

			scan_idx = i - 1
			while scan_idx >= 0 and values_order[scan_idx] > key_value:
				self.play(
					Indicate(cells_order[scan_idx], color=YELLOW_C),
					run_time=0.3,
				)
				self.next_slide()
				self.play(
					cells_order[scan_idx].animate.move_to(slot_positions[scan_idx + 1]),
					key_cell.animate.move_to(slot_positions[scan_idx] + key_offset),
					run_time=0.4,
				)
				self.next_slide()
				cells_order[scan_idx + 1] = cells_order[scan_idx]
				values_order[scan_idx + 1] = values_order[scan_idx]
				cells_order[scan_idx] = None
				values_order[scan_idx] = None
				scan_idx -= 1

			insert_idx = scan_idx + 1
			self.play(
				key_cell.animate.move_to(slot_positions[insert_idx]),
				run_time=0.35,
			)
			self.next_slide()
			key_cell.set_z_index(0)

			cells_order[insert_idx] = key_cell
			values_order[insert_idx] = key_value

			sorted_cells.add(key_cell)
			set_insert_colors(sorted_cells)
			if i == len(values_order) - 1:
				# Ensure final color updates are flushed before the next slide pause.
				self.wait(0.01)

		self.next_slide()

		self.play(FadeOut(cells, shift=0.08 * DOWN), run_time=0.8)

		insert_expr_target = ORIGIN + UP * 1.55
		self.play(insert_expr.animate.move_to(insert_expr_target), run_time=0.5)

		tree_top_y = -0.35
		tree_root = np.array([0.0, 1.1, 0.0])
		leaf_specs = [
			(r"[1, 2, 3, 4, 5]", LEFT * 4.8 + UP * tree_top_y + DOWN * 1.35),
			(r"[5, 4, 3, 2, 1]", LEFT * 2.4 + UP * tree_top_y + DOWN * 1.35),
			(r"[2, 1, 4, 5, 3]", RIGHT * 2.4 + UP * tree_top_y + DOWN * 1.35),
			(r"[1, 3, 5, 2, 4]", RIGHT * 4.8 + UP * tree_top_y + DOWN * 1.35),
		]
		leaf_labels = VGroup()
		branch_lines = VGroup()
		branch_ellipsis = MathTex(r"\cdots", font_size=42, color=GREY_B)
		branch_ellipsis.move_to(UP * tree_top_y)
		for perm_tex, target in leaf_specs:
			leaf = MathTex(perm_tex, font_size=26, color=WHITE)
			leaf.move_to(target)
			leaf_labels.add(leaf)
			branch_end = leaf.get_top() + UP * 0.18
			branch_lines.add(
				Line(tree_root, branch_end, color=GREY_B, stroke_width=2)
			)
		branch_question = MathTex(r"?", font_size=62, color=WHITE)
		branch_question.move_to(DOWN * 1.95)
		branch_group = VGroup(branch_lines, branch_ellipsis, branch_question, leaf_labels)

		self.play(
			LaggedStart(*[Create(line) for line in branch_lines], lag_ratio=0.12),
			LaggedStart(*[FadeIn(leaf, shift=0.08 * DOWN) for leaf in leaf_labels], lag_ratio=0.08),
			FadeIn(branch_ellipsis, shift=0.08 * DOWN),
			FadeIn(branch_question, shift=0.08 * DOWN),
			run_time=1.6,
		)

		self.next_slide()

		question = MathTex(
			r"\mathrm{cmp}(a,b): \text{ Is } a \le b\ ?",
			font_size=58,
			color=WHITE,
			tex_to_color_map={r"\mathrm{cmp}": BLUE_B, r"(a,b)": BLUE_B},
		)
		question.to_edge(UP, buff=0.55)
		question.set_z_index(10)

		cmp_part = insert_expr.get_part_by_tex(r"\mathrm{cmp}")

		# Detach cmp_part from insert_expr so it doesn't get faded out or removed
		insert_expr.remove(cmp_part)
		self.add(cmp_part)

		self.play(
			FadeOut(insert_expr, shift=0.1 * DOWN),
			FadeOut(branch_group, shift=0.1 * DOWN),
			cmp_part.animate.move_to(
				question.get_part_by_tex(r"\mathrm{cmp}").get_center()
			)
			.scale(58 / 40)
			.set_color(BLUE_B),
			run_time=1.2,
		)

		target_cmp = question.get_part_by_tex(r"\mathrm{cmp}")
		question_rest = VGroup(*[m for m in question if m != target_cmp])

		self.play(
			FadeIn(question_rest),
			Transform(cmp_part, target_cmp),
			run_time=0.8,
		)

		self.remove(cmp_part, question_rest)
		self.add(question)

		self.next_slide()

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

		coin_cmp_text = MathTex(
			r"\mathrm{coin}\mathrm{Cmp}(a,b): \text{ Is } a \le b\ ?",
			font_size=58,
			color=WHITE,
			tex_to_color_map={
				r"\mathrm{coin}": BLUE_B,
				r"\mathrm{Cmp}": BLUE_B,
				r"(a,b)": BLUE_B,
			},
		)
		coin_cmp_text.to_edge(UP, buff=0.55)

		divider = Line(UP * 2.6, DOWN * 2.2, color=GREY_B, stroke_width=2)

		bottom_text = Text(
			"We explore both possibilities and put our results together!",
			font_size=32,
			color=WHITE,
		)
		bottom_text.to_edge(DOWN, buff=0.55)
		bottom_text.set_max_width(11.0)

		self.play(
			FadeIn(divider),
			FadeIn(head_block, shift=0.2 * RIGHT),
			FadeIn(tail_block, shift=0.2 * LEFT),
			run_time=1.2,
		)

		self.next_slide()

		self.play(
			TransformMatchingTex(question, coin_cmp_text),
			run_time=1.2,
		)

		self.play(
			FadeIn(bottom_text, shift=0.15 * UP),
			run_time=0.9,
		)

		self.next_slide()

		self.play(
			FadeOut(coin_cmp_text, shift=0.1 * UP),
			FadeOut(divider),
			FadeOut(head_block, shift=0.1 * LEFT),
			FadeOut(tail_block, shift=0.1 * RIGHT),
			FadeOut(bottom_text, shift=0.1 * DOWN),
			run_time=0.8,
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

		# Voiceover/Intent: Build the output list from individual MathTex
		# entries so we can animate each leaf flying down to its slot.
		# Order follows the tree's left-to-right layout.
		leaves_in_order = [
			(leaf_321, r"[3, 2, 1]"),
			(leaf_312, r"[3, 1, 2]"),
			(leaf_132, r"[1, 3, 2]"),
			(leaf_231, r"[2, 3, 1]"),
			(leaf_213, r"[2, 1, 3]"),
			(leaf_123, r"[1, 2, 3]"),
		]

		# Build individual MathTex pieces for the output list.
		output_open = MathTex(r"\big[", font_size=34, color=WHITE)
		output_close = MathTex(r"\big]", font_size=34, color=WHITE)
		output_entries = []
		output_commas = []
		for i, (_, perm_str) in enumerate(leaves_in_order):
			entry = MathTex(perm_str, font_size=34, color=WHITE)
			output_entries.append(entry)
			if i < len(leaves_in_order) - 1:
				comma = MathTex(r",", font_size=34, color=WHITE)
				output_commas.append(comma)

		# Assemble into a VGroup: [ entry, entry, ... entry ]
		all_parts = [output_open]
		for i, entry in enumerate(output_entries):
			all_parts.append(entry)
			if i < len(output_entries) - 1:
				all_parts.append(output_commas[i])
		all_parts.append(output_close)

		output_list = VGroup(*all_parts).arrange(RIGHT, buff=0.08)
		output_list.to_edge(DOWN, buff=0.35)
		if output_list.width > 10.2:
			output_list.scale_to_fit_width(10.2)

		output_list_shift = LEFT * 1.4
		output_tail = MathTex(r"= P([2, 3, 1]) !", font_size=34, color=WHITE)
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

		self.next_slide()

		# Voiceover/Intent: Rewrite the specific coinCmp calls into the shared
		# comparison predicate before we show the output permutation list.
		cmp_rewrite_sources = [
			cmp_23,
			cmp_13_left,
			cmp_12_right,
			cmp_12_left,
			cmp_13_right,
		]
		cmp_rewrite_targets = [
			MathTex(r"2 \le 3", font_size=36, color=WHITE).move_to(cmp_23),
			MathTex(r"1 \le 3", font_size=34, color=WHITE).move_to(cmp_13_left),
			MathTex(r"1 \le 2", font_size=34, color=WHITE).move_to(cmp_12_right),
			MathTex(r"1 \le 2", font_size=34, color=WHITE).move_to(cmp_12_left),
			MathTex(r"1 \le 3", font_size=34, color=WHITE).move_to(cmp_13_right),
		]
		self.play(
			AnimationGroup(
				*[
					TransformMatchingTex(source, target)
					for source, target in zip(cmp_rewrite_sources, cmp_rewrite_targets)
				],
				lag_ratio=0.0,
			),
			run_time=1.2,
		)
		cmp_23, cmp_13_left, cmp_12_right, cmp_12_left, cmp_13_right = (
			cmp_rewrite_targets
		)

		# --- Beautiful leaf-copy animation ---
		# Voiceover/Intent: Copies of each leaf glow and then fly down from
		# the tree to assemble the output permutation list at the bottom.

		self.next_slide()

		# Step 1: Highlight every leaf to draw attention.
		leaf_mobjects = [pair[0] for pair in leaves_in_order]
		self.play(
			LaggedStart(
				*[
					Indicate(lf, color=YELLOW_C, scale_factor=1.15)
					for lf in leaf_mobjects
				],
				lag_ratio=0.12,
			),
			run_time=1.0,
		)

		# Step 2: Fade in the bracket / comma scaffold (no entries yet).
		scaffold = VGroup(output_open, output_close, *output_commas)
		self.play(FadeIn(scaffold, shift=0.08 * UP), run_time=0.5)

		# Step 3: Animate copies of each leaf flying down to their slot
		# using TransformFromCopy (original stays in tree, copy morphs
		# into the target entry).
		self.play(
			LaggedStart(
				*[
					TransformFromCopy(leaf, entry)
					for (leaf, _), entry in zip(leaves_in_order, output_entries)
				],
				lag_ratio=0.15,
			),
			run_time=1.8,
		)

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

		quote_creature = ExpressionLambda(
			body_color="#5e5086", eye_color=WHITE, pupil_color=BLACK, height=1.7
		)
		quote_creature.move_to(ORIGIN + RIGHT * 0.7 + DOWN * 0.2)
		quote_creature.set_z_index(12)

		self.play(
			FadeIn(quote_creature, shift=0.15 * LEFT),
			run_time=0.9,
		)

		self.next_slide()

		speech_text = Paragraph(
			"Lets try giving coinCmp to other",
			"sorting algorithms",
			alignment="center",
			font_size=20,
			color=WHITE,
		)
		speech_text.set_max_width(3.3)
		speech_bubble = Ellipse(
			width=speech_text.width + 1.0,
			height=speech_text.height + 0.5,
			color=WHITE,
			stroke_width=2,
			fill_opacity=0,
		)
		speech_bubble.next_to(quote_creature, UP + LEFT, buff=0.02)
		speech_bubble.shift(UP * 0.06 + LEFT * 0.03)
		speech_text.move_to(speech_bubble.get_center())
		speech_bubble_group = VGroup(speech_bubble, speech_text)
		speech_bubble_group.set_z_index(11)

		self.play(
			creature_look_at_animation(quote_creature, speech_bubble_group.get_center()),
			FadeIn(speech_bubble_group, shift=0.1 * DOWN),
			run_time=1.0,
		)

		self.next_slide()

		self.play(
			FadeOut(quote_creature, shift=0.1 * DOWN),
			FadeOut(speech_bubble_group, shift=0.1 * DOWN),
			run_time=0.8,
		)

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
		selection_block.move_to(ORIGIN + UP * 0.1)

		# Reveal selection explanation sequentially (top-down): title, step1, arrow, step2, arrow, step3
		self.play(FadeIn(selection_title, shift=0.08 * DOWN), run_time=0.6)
		self.play(FadeIn(selection_step1, shift=0.06 * DOWN), run_time=0.45)
		self.play(FadeIn(selection_arrow1, shift=0.03 * DOWN), run_time=0.35)
		self.play(FadeIn(selection_step2, shift=0.06 * DOWN), run_time=0.45)
		self.play(FadeIn(selection_arrow2, shift=0.03 * DOWN), run_time=0.35)
		self.play(FadeIn(selection_step3, shift=0.06 * DOWN), run_time=0.45)

		self.next_slide()

		self.play(
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

		# Voiceover/Intent: Call out duplicate leaves, then replace that
		# statement with the final permutation-set expression after pruning.
		sel_duplicates_text = Text("We get duplicates!", font_size=34, color=WHITE)
		sel_duplicates_text.to_edge(DOWN, buff=0.35)
		sel_output_suffix = MathTex(r"= P([2, 3, 1])", font_size=34, color=WHITE)
		sel_output_suffix.move_to(sel_duplicates_text.get_center())

		sel_yellow_duplicate_color = YELLOW_C
		sel_blue_duplicate_color = BLUE_C
		sel_underline_123_a = Underline(
			sel_leaf_123_a, color=sel_yellow_duplicate_color, buff=0.06
		)
		sel_underline_123_b = Underline(
			sel_leaf_123_b, color=sel_yellow_duplicate_color, buff=0.06
		)
		sel_underline_132_a = Underline(
			sel_leaf_132_a, color=sel_blue_duplicate_color, buff=0.06
		)
		sel_underline_132_b = Underline(
			sel_leaf_132_b, color=sel_blue_duplicate_color, buff=0.06
		)

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
			sel_underline_123_a,
			sel_underline_123_b,
			sel_underline_132_a,
			sel_underline_132_b,
		)
		sel_jiggle_targets = VGroup(sel_leaf_123_a, sel_leaf_123_b)
		sel_jiggle_targets.add(sel_leaf_132_a, sel_leaf_132_b)
		sel_focus_targets = {
			sel_title,
			sel_cmp_23,
			sel_trunk,
			sel_line_23_left,
			sel_line_23_right,
			sel_cmp_13_left,
			sel_line_13_left_right,
			sel_cmp_12_right,
			sel_line_12_right_right,
			sel_cmp_23_left,
			sel_line_23_left_right,
			sel_cmp_23_right,
			sel_line_23_right_left,
			sel_leaf_123_a,
			sel_leaf_132_b,
			sel_underline_123_a,
			sel_underline_132_b,
		}
		sel_dim_group = VGroup(
			*[
				m
				for m in sel_tree_group
				if m not in sel_focus_targets
			]
		)
		sel_consistency_cross_left = Cross(
			Square(side_length=0.24, stroke_width=0, fill_opacity=0), color=RED_C
		)
		sel_consistency_cross_left.move_to(sel_line_23_left_right.get_center())
		sel_consistency_cross_right = Cross(
			Square(side_length=0.24, stroke_width=0, fill_opacity=0), color=RED_C
		)
		sel_consistency_cross_right.move_to(sel_line_23_right_left.get_center())
		sel_consistency_label = Text("Enforce consistency", font_size=22, color=WHITE)
		sel_consistency_label.move_to(
			0.5
			* (
				sel_consistency_cross_left.get_center()
				+ sel_consistency_cross_right.get_center()
			)
			+ DOWN * 0.12
		)
		sel_tree_group.add(
			sel_consistency_cross_left,
			sel_consistency_cross_right,
			sel_consistency_label,
		)

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
		self.next_slide()

		self.play(
			Create(sel_underline_123_a),
			Create(sel_underline_123_b),
			Create(sel_underline_132_a),
			Create(sel_underline_132_b),
			FadeIn(sel_duplicates_text, shift=0.1 * UP),
			run_time=0.9,
		)

		self.next_slide()

		self.play(
			LaggedStart(
				*[m.animate.set_color(GREY_B).set_opacity(0.18) for m in sel_dim_group],
				lag_ratio=0.01,
			),
			run_time=0.9,
		)

		self.next_slide()

		self.play(
			Create(sel_consistency_cross_left),
			Create(sel_consistency_cross_right),
			FadeIn(sel_consistency_label, shift=0.08 * UP),
			run_time=0.7,
		)

		self.next_slide()

		self.play(
			LaggedStart(
				*[
					m.animate.set_color(WHITE).set_opacity(1.0)
					for m in [
						sel_cmp_12_left,
						sel_cmp_13_right,
						sel_cmp_23_left,
						sel_cmp_13_left,
						sel_leaf_321,
						sel_leaf_312,
						sel_leaf_132_a,
						sel_leaf_231,
						sel_leaf_213,
						sel_leaf_123_b,
					]
				],
				lag_ratio=0.01,
			),
			*[
				m.animate.set_color(color).set_opacity(opacity)
				for m, color, opacity in [
					(sel_trunk, GREY_B, 1.0),
					(sel_line_23_left, sel_false_color, 1.0),
					(sel_line_23_right, sel_true_color, 1.0),
					(sel_line_13_left_left, sel_false_color, 1.0),
					(sel_line_13_left_right, sel_true_color, 1.0),
					(sel_line_12_right_left, sel_false_color, 1.0),
					(sel_line_12_right_right, sel_true_color, 1.0),
					(sel_line_12_left_left, sel_false_color, 1.0),
					(sel_line_12_left_right, sel_true_color, 1.0),
					(sel_line_23_left_left, sel_false_color, 1.0),
					(sel_line_23_left_right, GREY_B, 0.18),
					(sel_line_13_right_left, sel_false_color, 1.0),
					(sel_line_13_right_right, sel_true_color, 1.0),
					(sel_line_23_right_left, GREY_B, 0.18),
					(sel_line_23_right_right, sel_true_color, 1.0),
					(sel_leaf_123_a, GREY_B, 0.18),
					(sel_leaf_132_b, GREY_B, 0.18),
				]
			],
			FadeOut(sel_underline_123_a, shift=0.06 * DOWN),
			FadeOut(sel_underline_123_b, shift=0.06 * DOWN),
			FadeOut(sel_underline_132_a, shift=0.06 * DOWN),
			FadeOut(sel_underline_132_b, shift=0.06 * DOWN),
			FadeOut(sel_consistency_cross_left, scale=0.8),
			FadeOut(sel_consistency_cross_right, scale=0.8),
			FadeOut(sel_consistency_label, shift=0.05 * UP),
			ReplacementTransform(sel_duplicates_text, sel_output_suffix),
			run_time=1.1,
		)
		sel_tree_group.add(sel_output_suffix)
		sel_tree_group.remove(
			sel_underline_123_a,
			sel_underline_123_b,
			sel_underline_132_a,
			sel_underline_132_b,
			sel_consistency_cross_left,
			sel_consistency_cross_right,
			sel_consistency_label,
		)

		self.next_slide()

		self.play(FadeOut(sel_tree_group, shift=0.1 * DOWN), run_time=0.6)
		self.remove(
			sel_output_suffix,
			sel_underline_123_a,
			sel_underline_123_b,
			sel_underline_132_a,
			sel_underline_132_b,
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

		# Reveal bubble explanation sequentially (top-down): title, step1, arrow, step2, arrow, step3, arrow, step4
		self.play(FadeIn(bubble_title, shift=0.08 * DOWN), run_time=0.6)
		self.play(FadeIn(bubble_step1, shift=0.06 * DOWN), run_time=0.45)
		self.play(FadeIn(bubble_arrow1, shift=0.03 * DOWN), run_time=0.35)
		self.play(FadeIn(bubble_step2, shift=0.06 * DOWN), run_time=0.45)
		self.play(FadeIn(bubble_arrow2, shift=0.03 * DOWN), run_time=0.35)
		self.play(FadeIn(bubble_step3, shift=0.06 * DOWN), run_time=0.45)
		self.play(FadeIn(bubble_arrow3, shift=0.03 * DOWN), run_time=0.35)
		self.play(FadeIn(bubble_step4, shift=0.06 * DOWN), run_time=0.45)

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
		bubble_line_23_left_right.set_color(GREY_B).set_opacity(0.18)
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
		bubble_leaf_132_a.set_color(GREY_B).set_opacity(0.18)

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
			run_time=1.0,
		)
		bubble_tree_group = VGroup(
			bubble_tree_title,
			bubble_trunk,
			bubble_cmp_23,
			bubble_cmp_12_left,
			bubble_cmp_13_right,
			bubble_cmp_23_left,
			bubble_cmp_13_left,
			bubble_cmp_32_right,
			bubble_cmp_12_right,
			bubble_leaf_123_a,
			bubble_leaf_132_a,
			bubble_leaf_213,
			bubble_leaf_231,
			bubble_leaf_132_b,
			bubble_leaf_123_b,
			bubble_leaf_312,
			bubble_leaf_321,
			bubble_line_23_left,
			bubble_line_23_right,
			bubble_line_12_left_left,
			bubble_line_12_left_right,
			bubble_line_13_right_left,
			bubble_line_13_right_right,
			bubble_line_23_left_left,
			bubble_line_23_left_right,
			bubble_line_13_left_left,
			bubble_line_13_left_right,
			bubble_line_32_right_left,
			bubble_line_32_right_right,
			bubble_line_12_right_left,
			bubble_line_12_right_right,
		)

		self.next_slide()

		bubble_note = Text(
			"We get [1, 2, 3] twice (even with consistency)",
			font_size=28,
			color=WHITE,
		)
		bubble_note.to_edge(DOWN, buff=0.4)
		bubble_note.set_max_width(11.0)
		bubble_underline_123_a = Underline(bubble_leaf_123_a, color=RED_C, buff=0.06)
		bubble_underline_123_b = Underline(bubble_leaf_123_b, color=RED_C, buff=0.06)
		bubble_callout_group = VGroup(
			bubble_note,
			bubble_underline_123_a,
			bubble_underline_123_b,
		)
		bubble_focus_targets = {
			bubble_tree_title,
			bubble_trunk,
			bubble_cmp_23,
			bubble_line_23_right,
			bubble_cmp_13_right,
			bubble_line_13_right_left,
			bubble_cmp_32_right,
			bubble_line_32_right_right,
			bubble_leaf_123_b,
		}
		bubble_dim_group = VGroup(
			*[m for m in bubble_tree_group if m not in bubble_focus_targets]
		)

		self.play(
			FadeIn(bubble_note, shift=0.1 * UP),
			Create(bubble_underline_123_a),
			Create(bubble_underline_123_b),
			run_time=0.9,
		)

		self.next_slide()

		self.play(
			LaggedStart(
				*[
					m.animate.set_color(GREY_B).set_opacity(0.18)
					for m in bubble_dim_group
				],
				lag_ratio=0.01,
			),
			bubble_underline_123_a.animate.set_color(GREY_B).set_opacity(0.18),
			run_time=0.9,
		)

		self.next_slide()

		bubble_cmp_32_right_slashed = MathTex(r"2 \nless 3", font_size=32)
		bubble_cmp_32_right_slashed.move_to(bubble_cmp_32_right.get_center())
		self.play(
			ReplacementTransform(bubble_cmp_32_right, bubble_cmp_32_right_slashed),
			# At this moment the left branch is intentionally still dimmed/gray.
			# Flip the visible branch color semantics on the right branch now.
			bubble_line_32_right_right.animate.set_color(bubble_false_color),
			run_time=0.8,
		)
		bubble_tree_group.remove(bubble_cmp_32_right)
		bubble_tree_group.add(bubble_cmp_32_right_slashed)
		bubble_cmp_32_right = bubble_cmp_32_right_slashed

		self.next_slide()

		bubble_totality_cross = Cross(
			Square(side_length=0.24, stroke_width=0, fill_opacity=0), color=RED_C
		)
		bubble_totality_cross.move_to(bubble_line_32_right_right.get_center())
		bubble_totality_label = Text("Enforce totality", font_size=22, color=WHITE)
		bubble_totality_label.next_to(bubble_totality_cross, LEFT, buff=0.18)

		self.play(
			Create(bubble_totality_cross),
			FadeIn(bubble_totality_label, shift=0.08 * LEFT),
			run_time=0.7,
		)
		bubble_callout_group.remove(bubble_underline_123_a, bubble_underline_123_b)
		bubble_tree_group.add(bubble_totality_cross, bubble_totality_label)

		self.next_slide()

		bubble_note_final = Text(
			"= P([1, 2, 3])",
			font_size=28,
			color=WHITE,
		)
		bubble_note_final.move_to(bubble_note)

		self.play(
			LaggedStart(
				*[
					m.animate.set_color(color).set_opacity(opacity)
					for m, color, opacity in [
						(bubble_tree_title, WHITE, 1.0),
						(bubble_trunk, GREY_B, 1.0),
						(bubble_cmp_23, WHITE, 1.0),
						(bubble_line_23_left, bubble_false_color, 1.0),
						(bubble_line_23_right, bubble_true_color, 1.0),
						(bubble_cmp_12_left, WHITE, 1.0),
						(bubble_cmp_13_right, WHITE, 1.0),
						(bubble_cmp_23_left, WHITE, 1.0),
						(bubble_cmp_13_left, WHITE, 1.0),
						(bubble_cmp_12_right, WHITE, 1.0),
						(bubble_cmp_32_right, WHITE, 1.0),
						(bubble_leaf_123_a, WHITE, 1.0),
						(bubble_leaf_132_a, GREY_B, 0.18),
						(bubble_leaf_213, WHITE, 1.0),
						(bubble_leaf_231, WHITE, 1.0),
						(bubble_leaf_132_b, WHITE, 1.0),
						(bubble_leaf_312, WHITE, 1.0),
						(bubble_leaf_321, WHITE, 1.0),
						(bubble_leaf_123_b, GREY_B, 0.18),
						(bubble_line_23_left_left, bubble_false_color, 1.0),
						(bubble_line_12_left_left, bubble_false_color, 1.0),
						(bubble_line_12_left_right, bubble_true_color, 1.0),
						(bubble_line_13_left_left, bubble_false_color, 1.0),
						(bubble_line_13_left_right, bubble_true_color, 1.0),
						(bubble_line_32_right_left, bubble_true_color, 1.0),
						(bubble_line_12_right_left, bubble_false_color, 1.0),
						(bubble_line_12_right_right, bubble_true_color, 1.0),
						(bubble_line_13_right_left, bubble_false_color, 1.0),
						(bubble_line_13_right_right, bubble_true_color, 1.0),
						(bubble_line_32_right_right, GREY_B, 0.18),
						(bubble_line_23_left_right, GREY_B, 0.18),
					]
				],
				lag_ratio=0.01,
			),
			FadeOut(bubble_underline_123_a, shift=0.06 * DOWN),
			FadeOut(bubble_underline_123_b, shift=0.06 * DOWN),
			FadeOut(bubble_totality_cross, scale=0.8),
			FadeOut(bubble_totality_label, shift=0.05 * UP),
			Transform(bubble_note, bubble_note_final),
			run_time=1.0,
		)
		bubble_tree_group.remove(bubble_totality_cross, bubble_totality_label)
		self.remove(bubble_totality_cross, bubble_totality_label)

		self.next_slide()

		self.play(
			FadeOut(bubble_tree_group, shift=0.1 * DOWN),
			FadeOut(bubble_callout_group, shift=0.1 * DOWN),
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

		# Reveal patience explanation sequentially (top-down): title, step1, arrow, step2, arrow, step3
		self.play(FadeIn(patience_title, shift=0.08 * DOWN), run_time=0.6)
		self.play(FadeIn(patience_step1, shift=0.06 * DOWN), run_time=0.45)
		self.play(FadeIn(patience_arrow1, shift=0.03 * DOWN), run_time=0.35)
		self.play(FadeIn(patience_step2, shift=0.06 * DOWN), run_time=0.45)
		self.play(FadeIn(patience_arrow2, shift=0.03 * DOWN), run_time=0.35)
		self.play(FadeIn(patience_step3, shift=0.06 * DOWN), run_time=0.45)

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
			# Slightly larger cards for clarity
			card.scale_to_fit_height(1.9)
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
		stack_offset = 0.24
		moves = []
		for card, pile_index, depth in placements:
			target = np.array(
				[
					np.linspace(-3.2, 3.2, pile_count)[pile_index],
					cards_group.get_center()[1] - stack_offset * depth,
					0,
				]
			)
			card.set_z_index(10 + depth)
			moves.append(card.animate.move_to(target))
		self.play(LaggedStart(*moves, lag_ratio=0.2), run_time=2.5)

		# Compute piles mapping (pile_index -> list of (card, depth))
		piles = {}
		for card, pile_index, depth in placements:
			piles.setdefault(pile_index, []).append((card, depth))

		# Identify top cards for each pile (not used visually here but kept for clarity)
		top_cards = []
		for i in range(pile_count):
			group = piles.get(i, [])
			if not group:
				continue
			top = min(group, key=lambda t: t[1])[0]
			top_cards.append(top)

		# Show the final merged output by moving the existing cards into
		# increasing numeric order from left to right.
		sorted_cards = sorted(cards, key=lambda cv: cv[1])
		final_row_y = cards_group.get_center()[1]
		final_spacing = sorted_cards[0][0].width + 0.2
		first_x = -0.5 * final_spacing * (len(sorted_cards) - 1)
		final_row_positions = [
			np.array([first_x + i * final_spacing, final_row_y, 0])
			for i in range(len(sorted_cards))
		]

		# Animate the actual cards from the piles into the sorted row.
		transforms = [
			card.animate.move_to(pos).set_z_index(12)
			for (card, _), pos in zip(sorted_cards, final_row_positions)
		]
		if transforms:
			self.play(LaggedStart(*transforms, lag_ratio=0.12), run_time=1.6)

		self.wait(0.2)
		self.next_slide()
		patience_fade_group = Group(patience_block, cards_group)
		self.play(
			FadeOut(patience_fade_group, shift=0.1 * DOWN),
			run_time=0.7,
		)

		a_le_b = MathTex(r"a \le b", font_size=40, color=WHITE)
		b_le_c = MathTex(r"b \le c", font_size=40, color=WHITE)
		a_le_c = MathTex(r"a \le c", font_size=40, color=WHITE)
		duplicate_text = Text("!!!", font_size=24, color=WHITE)
		left_ellipsis_1 = MathTex(r"\cdots", font_size=46, color=GREY_B)
		left_ellipsis_2 = MathTex(r"\cdots", font_size=46, color=GREY_B)
		dot_leaf = Dot(radius=0.07, color=WHITE)

		a_le_b.move_to(LEFT * 0.65 + UP * 2.2)
		left_ellipsis_1.move_to(LEFT * 2.2 + UP * 0.9)
		b_le_c.move_to(RIGHT * 0.9 + UP * 0.9)
		left_ellipsis_2.move_to(LEFT * 0.65 + DOWN * 0.4)
		a_le_c.move_to(RIGHT * 2.45 + DOWN * 0.4)
		duplicate_text.move_to(RIGHT * 0.9 + DOWN * 1.7)
		dot_leaf.move_to(RIGHT * 4.0 + DOWN * 1.7)

		line_1_left = Line(
			a_le_b.get_bottom(), left_ellipsis_1.get_top(), color=RED_C, stroke_width=3
		)
		line_1_right = Line(
			a_le_b.get_bottom(), b_le_c.get_top(), color=GREEN_B, stroke_width=3
		)
		line_2_left = Line(
			b_le_c.get_bottom(), left_ellipsis_2.get_top(), color=RED_C, stroke_width=3
		)
		line_2_right = Line(
			b_le_c.get_bottom(), a_le_c.get_top(), color=GREEN_B, stroke_width=3
		)
		line_3_left = Line(
			a_le_c.get_bottom(), duplicate_text.get_top(), color=RED_C, stroke_width=3
		)
		line_3_right = Line(
			a_le_c.get_bottom(), dot_leaf.get_top(), color=GREEN_B, stroke_width=3
		)

		cross = Cross(
			Square(side_length=0.26, stroke_width=0, fill_opacity=0), color=RED_C
		)
		cross.move_to(line_3_left.get_center())
		enforce_label = Text("Enforce transitivity", font_size=24, color=WHITE)
		enforce_label.next_to(cross, LEFT, buff=0.08)

		bottom_text = Text(
			"Log all transitive implications of new comparisions",
			font_size=28,
			color=WHITE,
		)
		bottom_text.set_max_width(11.0)
		bottom_text.to_edge(DOWN, buff=0.65)

		transitivity_group = VGroup(
			a_le_b,
			b_le_c,
			a_le_c,
			duplicate_text,
			left_ellipsis_1,
			left_ellipsis_2,
			dot_leaf,
			line_1_left,
			line_1_right,
			line_2_left,
			line_2_right,
			line_3_left,
			line_3_right,
			bottom_text,
		)

		self.play(FadeIn(a_le_b, shift=0.06 * DOWN), run_time=0.45)
		self.play(
			Create(line_1_left),
			Create(line_1_right),
			FadeIn(left_ellipsis_1, shift=0.05 * DOWN),
			FadeIn(b_le_c, shift=0.06 * DOWN),
			run_time=0.6,
		)
		self.play(
			Create(line_2_left),
			Create(line_2_right),
			FadeIn(left_ellipsis_2, shift=0.05 * DOWN),
			FadeIn(a_le_c, shift=0.06 * DOWN),
			run_time=0.6,
		)
		self.play(
			Create(line_3_left),
			Create(line_3_right),
			FadeIn(duplicate_text, shift=0.06 * DOWN),
			FadeIn(dot_leaf, shift=0.04 * DOWN),
			run_time=0.6,
		)

		self.next_slide()

		self.play(FadeIn(enforce_label, shift=0.08 * LEFT), FadeIn(cross), run_time=0.8)

		self.next_slide()

		self.play(
			FadeOut(enforce_label, shift=0.05 * LEFT),
			FadeOut(cross),
			line_3_left.animate.set_color(GREY_B).set_opacity(0.18),
			duplicate_text.animate.set_color(GREY_B).set_opacity(0.18),
			run_time=0.8,
		)

		self.next_slide()

		self.play(FadeIn(bottom_text, shift=0.12 * UP), run_time=0.9)

		self.next_slide()

		self.play(FadeOut(transitivity_group, shift=0.08 * DOWN), run_time=0.7)

		property_headers = [
			Text("sorting algorithm", font_size=24, color=WHITE),
			Text("consistency", font_size=24, color=WHITE),
			Text("totality", font_size=24, color=WHITE),
			Text("transitivity", font_size=24, color=WHITE),
		]
		property_rows = [
			[Text("insertion sort", font_size=24, color=WHITE), Text("", font_size=24), Text("", font_size=24), Text("", font_size=24)],
			[Text("selection sort", font_size=24, color=WHITE), Text("✓", font_size=26, color=GREEN_B), Text("", font_size=24), Text("", font_size=24)],
			[Text("bubble sort", font_size=24, color=WHITE), Text("✓", font_size=26, color=GREEN_B), Text("✓", font_size=26, color=GREEN_B), Text("", font_size=24)],
			[Text("patience sort", font_size=24, color=WHITE), Text("", font_size=24), Text("", font_size=24), Text("✓", font_size=26, color=GREEN_B)],
		]

		col_widths = [3.4, 2.3, 2.0, 2.3]
		row_heights = [0.72, 0.68, 0.68, 0.68, 0.68]
		table_width = sum(col_widths)
		table_height = sum(row_heights)
		table_left = -table_width / 2
		table_top = table_height / 2

		table_cells = VGroup()
		table_grid = VGroup()

		for row_index, row in enumerate([property_headers] + property_rows):
			y_center = table_top - sum(row_heights[:row_index]) - row_heights[row_index] / 2
			for col_index, item in enumerate(row):
				x_center = table_left + sum(col_widths[:col_index]) + col_widths[col_index] / 2
				cell_box = Rectangle(
					width=col_widths[col_index],
					height=row_heights[row_index],
					stroke_color=GREY_B,
					stroke_width=2,
					fill_opacity=0,
				)
				cell_box.move_to(np.array([x_center, y_center, 0]))
				if row_index == 0:
					if col_index == 0:
						cell_box.set_fill(color=BLUE_C, opacity=0.18)
					else:
						cell_box.set_fill(color=YELLOW_C, opacity=0.18)
				elif col_index == 0:
					cell_box.set_fill(color=BLUE_C, opacity=0.12)
				else:
					cell_box.set_fill(color=YELLOW_C, opacity=0.12)
				item.move_to(cell_box.get_center())
				table_cells.add(cell_box, item)

		for row_edge in range(1, len(row_heights)):
			y = table_top - sum(row_heights[:row_edge])
			table_grid.add(
				Line(
					np.array([table_left, y, 0]),
					np.array([table_left + table_width, y, 0]),
					color=GREY_B,
					stroke_width=2,
				)
			)
		for col_edge in range(1, len(col_widths)):
			x = table_left + sum(col_widths[:col_edge])
			table_grid.add(
				Line(
					np.array([x, table_top, 0]),
					np.array([x, table_top - table_height, 0]),
					color=GREY_B,
					stroke_width=2,
				)
			)

		properties_table = VGroup(table_grid, table_cells)
		properties_table.move_to(ORIGIN + DOWN * 0.05)

		self.play(Create(table_grid), run_time=0.7)
		self.play(FadeIn(table_cells, shift=0.04 * UP), run_time=0.8)

		self.next_slide()

		self.play(
			FadeOut(properties_table, shift=0.08 * DOWN),
			run_time=0.7,
		)


		quote_formula = MathTex(
			r"\mathrm{sortM}(\mathrm{coinCmp}, xs) \to \mathrm{Perm}(xs)",
			font_size=44,
			color=WHITE,
		)
		quote_formula.move_to(ORIGIN + UP * 0.4)
		quote_formula_target = MathTex(
			r"\mathrm{Perm}(xs) \subseteq \mathrm{sortM}(\mathrm{coinCmp}, xs)",
			font_size=44,
			color=WHITE,
		)
		quote_formula_target.move_to(quote_formula.get_center())

		self.play(Write(quote_formula), run_time=1.0)

		self.next_slide()

		self.play(
			TransformMatchingTex(quote_formula, quote_formula_target),
			run_time=1.0,
		)

		self.next_slide()

		final_quote_text = Paragraph(
			'"Every sorting algorithm that actually sorts can describe every',
			"possible permutation (if there is a permutation that cannot be",
			"realized by the sorting algorithm then there is an input list",
			'that cannot be sorted)"',
			alignment="center",
			font_size=24,
			color=WHITE,
		)
		final_quote_text.set_max_width(10.6)
		final_quote_author = Text("Sebastian Fischer", font_size=21, color=BLUE_B)
		final_quote_block = VGroup(final_quote_text, final_quote_author).arrange(
			DOWN, buff=0.16
		)

		self.play(
			quote_formula_target.animate.shift(UP * 0.45),
			run_time=0.7,
		)
		final_quote_block.next_to(quote_formula_target, DOWN, buff=0.8)
		self.play(Write(final_quote_block), run_time=1.3)

		# Clear the final quote before appending the proof slide
		self.next_slide()
		self.play(
			FadeOut(final_quote_block, shift=0.08 * DOWN),
			FadeOut(quote_formula_target, shift=0.08 * UP),
			run_time=0.7,
		)


		# --- Inserted: Commutative Square (from proof.py, slide 2) ---

		# Colors used in the proof slide
		COLOR_INDEX = BLUE_C
		COLOR_DATA = RED_C
		COLOR_RELATION = GOLD_C
		COLOR_MULTIVERSE = PURPLE_C

		# Helper to create small arrays (copied from proof.py)
		def create_array(elements, box_color=WHITE, text_color=BLACK, scale=1.0):
			arr = VGroup()
			for el in elements:
				box = Square(side_length=0.8, fill_color=box_color, fill_opacity=0.9, stroke_color=WHITE)
				text = Tex(str(el), color=text_color).scale(1.2)
				node = VGroup(box, text)
				arr.add(node)
			arr.arrange(RIGHT, buff=0.1).scale(scale)
			return arr

		# Positions for the square corners
		TL = UP * 1.5 + LEFT * 3.8
		TR = UP * 1.5 + RIGHT * 3.8
		BL = DOWN * 1.7 + LEFT * 3.8
		BR = DOWN * 1.7 + RIGHT * 3.8

		# Top-left: Permuted indices
		pis = create_array([2, 0, 1], COLOR_INDEX, WHITE, scale=0.8)
		pis.move_to(TL)
		label_pis = Tex("Permuted Indices", font_size=28).next_to(pis, UP, buff=0.2)
		self.play(FadeIn(VGroup(pis, label_pis)))

		self.next_slide()

		# Top-right: Sorted indices
		iss = create_array([0, 1, 2], COLOR_INDEX, WHITE, scale=0.8)
		iss.move_to(TR)
		label_iss = Tex("Sorted Indices", font_size=28).next_to(iss, UP, buff=0.2)

		arrow_sort = Arrow(pis.get_right(), iss.get_left(), buff=0.4, color=WHITE)
		label_sort = Tex("Deterministic Sort", font_size=30).next_to(arrow_sort, UP, buff=0.2)

		self.play(GrowArrow(arrow_sort), FadeIn(label_sort))
		self.play(FadeIn(VGroup(iss, label_iss)))

		self.next_slide()

		# Bottom-left: input data xs
		xs = create_array(['C', 'A', 'B'], COLOR_DATA, WHITE, scale=0.8)
		xs.move_to(BL)
		label_xs = Tex("Input Data ($xs$)", font_size=28).next_to(xs, DOWN, buff=0.2)

		arrow_rel_L = Arrow(pis.get_bottom(), xs.get_top(), buff=0.4, color=COLOR_RELATION)
		label_rel_L = Tex("Map to Data", color=COLOR_RELATION, font_size=28).next_to(arrow_rel_L, RIGHT, buff=0.2)

		self.play(GrowArrow(arrow_rel_L), FadeIn(label_rel_L))
		self.play(FadeIn(VGroup(xs, label_xs)))

		self.next_slide()

		# Bottom-right: branching outcomes cloud
		cloud = Ellipse(width=4.8, height=2.8, color=COLOR_MULTIVERSE, fill_opacity=0.15)
		cloud.move_to(BR)
		label_cloud = Tex("Branching Outcomes", color=COLOR_MULTIVERSE, font_size=28).next_to(cloud, DOWN, buff=0.15)

		mini_1 = create_array(['C', 'A', 'B'], COLOR_DATA, WHITE, scale=0.35).move_to(cloud.get_center() + UP * 0.6 + LEFT * 1.0)
		mini_2 = create_array(['B', 'C', 'A'], COLOR_DATA, WHITE, scale=0.35).move_to(cloud.get_center() + DOWN * 0.6 + RIGHT * 0.8)
		mini_dots = Tex("...", font_size=48, color=WHITE).move_to(cloud.get_center() + UP * 0.5 + RIGHT * 1.1)

		arrow_permute = Arrow(xs.get_right(), cloud.get_left(), buff=0.4, color=WHITE)
		label_permute = Tex("Non-Deterministic Sort", font_size=30).next_to(arrow_permute, UP, buff=0.2)

		self.play(GrowArrow(arrow_permute), FadeIn(label_permute))
		self.play(FadeIn(cloud), FadeIn(label_cloud), FadeIn(mini_1, mini_2, mini_dots))

		self.next_slide()

		# === SCENE 3: Wadler's Free Theorem Climax ===
		free_theorem_text = Tex(
			"Parametric Polymorphism (Free Theorem)", font_size=36, color=YELLOW
		)
		free_theorem_text.to_edge(UP, buff=0.3)
		self.play(Write(free_theorem_text))

		# Highlight the three existing edges
		self.play(
			arrow_sort.animate.set_color(YELLOW),
			arrow_rel_L.animate.set_color(YELLOW),
			arrow_permute.animate.set_color(YELLOW),
			run_time=1,
		)

		self.next_slide()

		# Right Edge: reveal mapping back to the cloud
		arrow_rel_R = Arrow(
			iss.get_bottom(),
			cloud.get_top(),
			buff=0.4,
			color=COLOR_RELATION,
			stroke_width=arrow_sort.stroke_width,
		)
		label_rel_R = Tex("Map to Data", color=COLOR_RELATION, font_size=28).next_to(arrow_rel_R, LEFT, buff=0.2)

		self.play(GrowArrow(arrow_rel_R), FadeIn(label_rel_R))

		self.next_slide()

		# Reveal the Target Array inside the smaller ellipse
		ys = create_array(['A', 'B', 'C'], COLOR_DATA, WHITE, scale=0.7)
		ys.move_to(cloud.get_center() + DOWN * 0.1)

		# Dim background options and bring in the target
		self.play(
			mini_1.animate.set_opacity(0.15),
			mini_2.animate.set_opacity(0.15),
			mini_dots.animate.set_opacity(0.15),
			FadeIn(ys, shift=DOWN),
		)

		# Highlight Box and Label
		highlight_box = SurroundingRectangle(ys, color=YELLOW, buff=0.15)
		self.play(Create(highlight_box))

		self.next_slide()

		# Final blank slide: clear everything and capture an empty frame on next.
		# Fade out any remaining mobjects, wait briefly, then emit a slide boundary
		# so the presentation ends on a blank slide.
		self.play(FadeOut(Group(*self.mobjects), shift=0.08 * DOWN), run_time=0.6)
		self.wait(0.01)
		self.next_slide()

