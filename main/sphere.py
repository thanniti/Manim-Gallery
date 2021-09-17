from manim import*
import numpy as np
import math
import scipy
import random
from sklearn import preprocessing

class SphereScene(ThreeDScene):

	def get_ghost_surface(self, surface):
		result = surface.copy()
		result.set_fill(BLUE_E, opacity=0)
		result.set_stroke(WHITE, width=0.5, opacity=0.5)
		return result

	def get_ax(self):
		ax = ThreeDAxes()
		return ax

	def get_smooth_sphere(self, color):
		sm_sphere = ParametricSurface(
			lambda u, v: np.array([
				1.5 * np.cos(u) * np.cos(v),
				1.5 * np.cos(u) * np.sin(v),
				1.5 * np.sin(u)
			]), v_range=[0, TAU], u_range=[-PI / 2, PI / 2],
			checkerboard_colors=[color, color], resolution=(150,150)
		)
		sm_sphere.set_opacity(0.8)
		sm_sphere.set_stroke(color, opacity=0.8)
		return sm_sphere

	def get_sphere(self, color_a, color_b, a, b):
		sphere = ParametricSurface(
			lambda u, v: np.array([
				1.5 * np.cos(u) * np.cos(v),
				1.5 * np.cos(u) * np.sin(v),
				1.5 * np.sin(u)
			]), v_range=[0, TAU], u_range=[-PI / 2, PI / 2],
			checkerboard_colors=[color_a, color_b], resolution=(a, b)
		)
		return sphere

	def get_rings(self, mob):
		u_values, v_values = mob.get_u_values_and_v_values()
		inv_rings = VGroup(*[VGroup() for u in u_values])
		for piece in mob:
			inv_rings[piece.u_index].add(piece.copy())
		rings = inv_rings[::-1]
		self.set_ring_colors_new(rings)
		self.rings = rings

		return rings

	def set_ring_colors_new(self, rings):
		a = len(rings)
		colors = [BLUE_E, BLUE_D]*a
		for i in range(0, a):
			rings[i].set_color(colors[i])

class RectangulatedSphere(SphereScene):
	#CONFIG
	uniform_color = False
	wait_time = 10
	a = 10
	b = 20

	def construct(self):
		sphere = self.get_sphere(BLUE_D, BLUE_C, self.a, self.b)
		if self.uniform_color:
			sphere.set_stroke(BLUE_E, width=0.5)
			sphere.set_fill(BLUE_E)
		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
		self.begin_ambient_camera_rotation(0.05)
		self.add(sphere)
		self.wait(self.wait_time)


class SmoothSphere(RectangulatedSphere):
	#CONFIG
	uniform_color = True
	wait_time = 0
	a = 150
	b = 250

class RotateAllPiecesWithExpansion(SphereScene):

	with_expansion = True
	a = 30
	b = 30

	def construct(self):
		#self.setup_shapes()
		self.rotate_all_pieces()

	#def setup_shapes(self):
		#self.sphere = self.get_sphere(BLUE_E, BLUE_C)
		#self.ghost_sphere = self.get_ghost_surface(sphere)

	def rotate_all_pieces(self):
		sphere = self.get_sphere(BLUE_E, BLUE_C, self.a, self.b)
		ghost_sphere = self.get_ghost_surface(sphere)
		
		ghost_sphere.scale(0.99)
		self.bring_to_back(ghost_sphere)

		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

		random.seed(0)
		random.shuffle(sphere.submobjects)

		sphere_target = VGroup()
		for piece in sphere:
			p0, p1, p2, p3 = piece.get_anchors()[:4]
			piece.set_points_as_corners([
				p3, p0, p1, p2, p3
			])
			piece.generate_target()
			sphere_target.add(piece.target)
			piece.target.move_to(
				(1 + random.random()) * piece.get_center()
			)

		self.add(ghost_sphere, sphere)
		self.wait()
		if self.with_expansion:
			self.play(LaggedStartMap(
				MoveToTarget, sphere
			))
		self.wait()
		self.play(*[
			Rotate(piece, 90 * DEGREES, axis=piece.get_center())
			for piece in sphere
		])
		self.wait(5)

class RotateAllPiecesWithoutExpansion(RotateAllPiecesWithExpansion):

	with_expansion = False

class Ring(SphereScene):

	n_random_subsets = 12
	a = 30
	b = 30

	def construct(self):
		self.setup_shapes()
		self.divide_into_rings()
		self.show_shadows()
		self.correspond_to_every_other_ring()
		self.cut_cross_section()
		#self.show_theta()

	def setup_shapes(self):
		sphere = self.get_sphere(BLUE_E, BLUE_C, self.a, self.b)
		sphere.set_stroke(WHITE, width=0.25)
		self.add(sphere)
		self.sphere = sphere

		u_values, v_values = sphere.get_u_values_and_v_values()
		rings = VGroup(*[VGroup() for u in u_values])
		for piece in sphere:
			rings[piece.u_index].add(piece.copy())
		self.set_ring_colors_new(rings)
		self.rings = rings

		self.axes = self.get_ax()
		self.add(self.axes)

		#self.renderer.camera.light_source.move_to(3*IN)
		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
		self.begin_ambient_camera_rotation()

	def divide_into_rings(self):
		rings = self.rings

		self.play(FadeIn(rings), FadeOut(self.sphere))
		self.play(
			rings.animate.space_out_submobjects(1.5),
			rate_func=there_and_back_with_pause,
			run_time=3
		)
		self.wait(2)
		rings.save_state()

	def show_shadows(self):
		rings = self.rings
		north_rings = rings[:len(rings) // 2]
		ghost_rings = rings.copy()
		ghost_rings.set_fill(opacity=0.0)
		ghost_rings.set_stroke(WHITE, width=0.5, opacity=0.2)

		north_rings.submobjects.reverse()
		shadows = self.get_shadow(north_rings)
		for piece in shadows.family_members_with_points():
			piece.set_stroke(
				piece.get_fill_color(),
				width=0.5,
			)
		for shadow in shadows:
			shadow.save_state()
		shadows.become(north_rings)

		self.add(ghost_rings)
		self.play(FadeOut(rings), Animation(shadows))
		self.play(LaggedStartMap(Restore, shadows))
		self.wait()
		self.move_camera(phi=40 * DEGREES)
		self.wait(3)

		# Show circle
		radial_line = Line(ORIGIN, 1.5 * RIGHT)
		radial_line.set_stroke(RED)
		R_label = Tex("R")
		R_label.set_background_stroke(width=1)
		R_label.next_to(radial_line, DOWN)

		self.play(
			FadeIn(R_label, shift=UP),
			Create(radial_line)
		)
		self.play(Rotating(
			radial_line, angle=TAU,
			about_point=ORIGIN,
			rate_func=smooth,
			run_time=3,
		))
		self.wait()

		self.shadows = shadows
		self.R_label = R_label
		self.radial_line = radial_line
		self.ghost_rings = ghost_rings

		#self.get_attrs(
			#shadows, ghost_rings,
			#radial_line, R_label
		#)

	def correspond_to_every_other_ring(self):
		rings = self.rings
		shadows = self.shadows
		shadows.submobjects.reverse()

		rings.restore()
		self.set_ring_colors_new(rings)
		every_other_ring = rings[1::2]
		self.move_camera(
			phi=70 * DEGREES,
			theta=-135 * DEGREES,
			added_anims=[
				FadeOut(self.R_label),
				FadeOut(self.radial_line),
			],
			run_time=2,
		)
		shadows_copy = shadows.copy()
		shadows.fade(1)
		self.play(
			ReplacementTransform(
				shadows_copy, every_other_ring
			),
			FadeOut(self.ghost_rings),
			run_time=2,
		)
		self.wait(5)

		self.every_other_ring = every_other_ring

	def cut_cross_section(self):
		shadows = self.shadows
		every_other_ring = self.every_other_ring
		rings = self.rings

		back_half = self.get_hemisphere(rings, UP)
		front_half = self.get_hemisphere(rings, DOWN)
		front_half_ghost = front_half.copy()
		front_half_ghost.set_fill(opacity=0.2)
		front_half_ghost.set_stroke(opacity=0)

		# shaded_back_half = back_half.copy()
		# for piece in shaded_back_half.family_members_with_points():
		#     piece.set_points(piece.get_points()[::-1])
		# shaded_back_half.scale(0.999)
		# shaded_back_half.set_fill(opacity=0.5)

		circle = Circle(radius=1.5)
		circle.set_stroke(PINK, 2)
		circle.rotate(90 * DEGREES, RIGHT)

		every_other_ring_copy = every_other_ring.copy()
		self.add(every_other_ring_copy)
		self.remove(every_other_ring)
		rings.set_fill(opacity=0.8)
		rings.set_stroke(opacity=0.6)
		self.play(
			FadeIn(back_half),
			FadeIn(front_half_ghost),
			FadeIn(circle),
			FadeOut(shadows),
			FadeOut(every_other_ring_copy),
		)
		self.wait()

		self.back_half = back_half
		self.front_half = front_half
		self.front_half_ghost = front_half_ghost
		self.slice_circle = circle

		#self.set_variables_as_attrs(
			#back_half, front_half,
			#front_half_ghost,
			#slice_circle=circle
 		#)

	def show_theta(self):
		theta_tracker = ValueTracker(0)
		get_theta = theta_tracker.get_value
		theta_group = always_redraw(
			lambda: self.get_theta_group(get_theta())
		)
		theta_mob_opacity_tracker = ValueTracker(0)
		get_theta_mob_opacity = theta_mob_opacity_tracker.get_value
		theta_mob = theta_group[-1]
		theta_mob.add_updater(
			lambda m: m.set_fill(opacity=get_theta_mob_opacity())
		)
		theta_mob.add_updater(
			lambda m: m.set_background_stroke(
				width=get_theta_mob_opacity()
			)
		)

		lit_ring = always_redraw(
			lambda: self.get_ring_from_theta(
				self.rings, get_theta()
			).copy().set_color(YELLOW)
		)

		self.stop_ambient_camera_rotation()
		self.move_camera(theta=-60 * DEGREES)

		self.add(theta_group, lit_ring)
		n_rings = len(self.rings) - 1
		lit_ring_index = int((30 / 180) * n_rings)
		angle = PI * lit_ring_index / n_rings
		for alpha in [angle, 0, PI, angle]:
			self.play(
				theta_tracker.animate.set_value(alpha),
				theta_mob_opacity_tracker.animate.set_value(1),
				Animation(self.camera.phi_tracker),
				run_time=2,
			)
			self.wait()

		# Label d-theta
		radius = 1.5
		d_theta = PI / len(self.rings)
		alt_theta = get_theta() + d_theta
		alt_theta_group = self.get_theta_group(alt_theta)
		alt_R_line = alt_theta_group[1]
		# d_theta_arc = Arc(
		#     start_angle=get_theta(),
		#     angle=d_theta,
		#     radius=theta_group[0].radius,
		#     stroke_color=PINK,
		#     stroke_width=3,
		# )
		# d_theta_arc.rotate(90 * DEGREES, axis=RIGHT, about_point=ORIGIN)
		brace = Brace(Line(ORIGIN, radius * d_theta * RIGHT), UP)
		brace.rotate(90 * DEGREES, RIGHT)
		brace.next_to(self.sphere, OUT, buff=0)
		brace.add_to_back(brace.copy().set_stroke(BLACK, 3))
		brace.rotate(
			get_theta() + d_theta / 2,
			axis=UP,
			about_point=ORIGIN,
		)
		brace_label = MathTex(r"\theta ")
		brace_label.rotate(90 * DEGREES, RIGHT)
		brace_label.next_to(brace, OUT + RIGHT, buff=0)
		radial_line = self.radial_line
		R_label = self.R_label
		R_label.rotate(90 * DEGREES, RIGHT)
		R_label.next_to(radial_line, IN, SMALL_BUFF)

		self.play(
			TransformFromCopy(theta_group[1], alt_R_line),
			GrowFromCenter(brace),
			Animation(self.camera.phi_tracker),
		)
		self.wait()
		self.move_camera(
			phi=90 * DEGREES,
			theta=-90 * DEGREES,
		)
		self.wait()
		self.play(
			FadeIn(brace_label, direction=IN),
		)
		self.play(
			Create(radial_line),
			FadeIn(R_label),
		)
		self.wait()
		self.move_camera(
			phi=70 * DEGREES,
			theta=-70 * DEGREES,
		)
		self.wait(3)

		self.theta_tracker = theta_tracker
		self.lit_ring = lit_ring
		self.theta_group = theta_group
		self.brace = brace
		self.brace_label = brace_label
		self.d_theta = d_theta
		self.alt_R_line = alt_R_line
		self.theta_mob_opacity_tracker = theta_mob_opacity_tracker

		#self.set_variables_as_attrs(
			#theta_tracker, lit_ring, theta_group,
			#brace, brace_label, d_theta,
			#alt_R_line, theta_mob_opacity_tracker,
		#)

	def set_ring_colors(self, rings, colors=[BLUE_E, BLUE_D]):
		for i, ring in enumerate(rings):
			color = colors[i % len(colors)]
			ring.set_fill(color).set_opacity(1)
			ring.set_stroke(color, width=0.5, opacity=1)
			for piece in ring:
				piece.insert_n_curves(4)
				piece.on_sphere = True
				piece.set_points([
					*piece.get_points()[3:-1],
					*piece.get_points()[:3],
					piece.get_points()[3]
				])
		return rings

	def set_ring_colors_new(self, rings):
		a = len(rings)
		colors = [BLUE_E, BLUE_D]*a
		for i in range(0, a):
			rings[i].set_color(colors[i])

	def get_shadow(self, mobject):
		result = mobject.copy()
		result.apply_function(
			lambda p: np.array([*p[:2], 0])
		)
		return result

	def get_hemisphere(self, group, vect):
		if len(group.submobjects) == 0:
			if np.dot(group.get_center(), vect) > 0:
				return group
			else:
				return VMobject()
		else:
			return VGroup(*[
				self.get_hemisphere(submob, vect)
				for submob in group
			])

	def get_northern_hemisphere(self, group):
		return self.get_hemisphere(group, OUT)

	def get_theta(self, ring):
		piece = ring[0]
		point = piece.get_points()[3]
		return np.arccos(point[2] / get_norm(point))

	def get_theta_group(self, theta):
		arc = Arc(
			start_angle=90 * DEGREES,
			angle=-theta,
			radius=0.5,
		)
		arc.rotate(90 * DEGREES, RIGHT, about_point=ORIGIN)
		arc.set_stroke(YELLOW, 2)
		theta_mob = MathTex(r"\theta ")
		theta_mob.rotate(90 * DEGREES, RIGHT)
		vect = np.cos(theta / 2) * OUT + np.sin(theta / 2) * RIGHT
		theta_mob.move_to(
			(arc.radius + 0.25) * normalize(vect),
		)
		theta_mob.set_background_stroke(width=1)

		radius = 1.5
		point = arc.point_from_proportion(1)
		radial_line = Line(
			ORIGIN, radius * normalize(point)
		)
		radial_line.set_stroke(WHITE, 2)

		return Group(arc, radial_line, theta_mob)

	def get_ring_from_theta(self, rings, theta):
		n_rings = len(rings)
		index = min(int((theta / PI) * n_rings), n_rings - 1)
		return rings[index]


class SphereAnim(Ring):
	#CONFIG
	a = 30
	b = 30

	def construct(self):
		self.setup()
		self.play_setup()
		self.slice()
		#self.slice_to_discs()
		self.flash_through_rings()
		self.grow_rings()
		self.show_one_ring()
		self.show_radius()
		self.show_thickness()
		self.show_radial_line()
	
	def setup(self):
		ax = self.get_ax()
		sphere = self.get_sphere(BLUE_E, BLUE_D, self.a, self.b)
		ghost_sphere = self.get_ghost_surface(sphere)
		rings = self.get_rings(sphere)
		ghost_sphere.scale(0.99)
		discs = VGroup(*[
			Circle(fill_opacity=1)
			.set_width(rings[i].get_width())
			.move_to(rings[i].get_center()) 
			for i in range(len(rings))
			])
		self.set_ring_colors_new(discs)
		print (discs)
		#self.bring_to_back(ghost_sphere)

		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
		self.begin_ambient_camera_rotation()
		self.add(ax)
		#self.play(FadeIn(discs))

		self.sphere = sphere
		self.rings = rings
		self.ghost_sphere = ghost_sphere
		self.ax = ax
		self.discs = discs

	def play_setup(self):
		ghost_sphere = self.ghost_sphere
		rings = self.rings
		sphere = self.sphere
		self.play(Write(ghost_sphere))
		self.play(Create(sphere))

	def slice(self):
		rings = self.rings
		self.play(FadeIn(rings), FadeOut(self.sphere))
		self.wait(2)

	def slice_to_discs(self):
		discs = self.discs

		self.play(
			discs.animate.space_out_submobjects(1.5),
			rate_func=there_and_back_with_pause,
			run_time=3
		)
		self.wait(2)
		discs.save_state()
	
	def flash_through_rings(self):
		rings = self.rings
		#rings.fade(1)
		#rings.sort(lambda p: p[2])
		for x in range(1):
			self.play(LaggedStartMap(
				ApplyMethod, rings,
				lambda m: (m.set_fill, PINK, 1),
				rate_func=there_and_back,
				lag_ratio=0.5,
				run_time=2,
			))

	def grow_rings(self):
		sphere = self.sphere
		rings = self.rings
		ghost_sphere = self.ghost_sphere

		north_rings = rings[:len(rings) // 2]
		sphere.set_fill(opacity=0)
		sphere.set_stroke(WHITE, 0.5, opacity=0.5)
		southern_mesh = VGroup(*[
			face.copy() for face in sphere
			if face.get_center()[2] < 0
		])
		southern_mesh.set_stroke(WHITE, 0.1, 0.5)

		#self.play(Write(sphere))
		#self.wait()
		#self.play(
			#FadeOut(sphere),
			#FadeIn(southern_mesh),
			#FadeIn(north_rings),
		#)
		#self.wait(4)

		self.north_rings = north_rings
		self.southern_mesh = southern_mesh

	def show_one_ring(self):
		self.clear()
		
		ax = self.ax
		rings = self.rings
		southern_mesh = self.southern_mesh
		north_rings = rings[:len(rings) // 2]
		inv_rings = rings[::-1]
		southern_rings = inv_rings[:len(inv_rings) // 2]
		index = len(north_rings) // 2
		ring = north_rings[index]
		to_fade = VGroup(*[
			nr for nr in rings
			if nr is not ring
		])
		circle = Circle(stroke_opacity=0, fill_color=BLUE_D , fill_opacity=0.6)
		circle.move_to(ring, IN)
		self.bring_to_back(circle)

		self.add(ax, to_fade, ring)

		self.play(to_fade.animate.set_stroke(opacity=0))
		self.play(to_fade.animate.set_fill(opacity=0.1), FadeIn(circle))

		self.wait()

		self.ring = ring
		self.to_fade = to_fade
		self.circle = circle

	def show_radius(self):
		ax = self.ax
		self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
		radius = Line(ax.c2p(0,0,0),ax.c2p(1,0,0), color=RED, stroke_width=1.5)
		radius_label = Tex("R")
		radius_label.rotate(90 * DEGREES, RIGHT)
		radius_label.next_to(radius, RIGHT + OUT, buff=0)
		self.stop_ambient_camera_rotation()
		self.play(FadeIn(radius))
		self.begin_ambient_camera_rotation(0.02)

	def show_thickness(self):
		ring = self.ring

		thickness = ring.get_depth() * np.sqrt(2)
		brace = Brace(Line(ORIGIN, 0.2 * RIGHT), UP)
		brace.set_width(thickness)
		brace.rotate(90 * DEGREES, RIGHT)
		brace.rotate(45 * DEGREES, UP)
		brace.move_to(1.5 * (RIGHT + OUT))
		brace.set_stroke(WHITE, 1)
		word = MathTex(r"Rd\theta ")
		word.rotate(90 * DEGREES, RIGHT)
		word.next_to(brace, RIGHT + OUT, buff=0)

		self.play(
			GrowFromCenter(brace),
			Write(word),
		)
		self.wait(2)
		self.play(FadeOut(VGroup(brace, word)))

		self.thickness_label = VGroup(brace, word)

	def show_radial_line(self):
		ring = self.ring

		point = ring.get_corner(RIGHT + IN)
		R_line = Line(ORIGIN, point)
		theta = 45 * DEGREES
		arc = Arc(angle=theta, radius=0.5)
		arc.rotate(90 * DEGREES, RIGHT, about_point=ORIGIN)

		theta = MathTex(r"\theta")
		theta.rotate(90 * DEGREES, RIGHT)
		theta.next_to(arc, RIGHT)
		theta.shift(SMALL_BUFF * (LEFT + OUT))

		R_label = Tex("R")
		R_label.rotate(90 * DEGREES, RIGHT)
		R_label.next_to(
			R_line.get_center(), OUT + LEFT,
			buff=SMALL_BUFF
		)
		r_s = VGroup(R_label, R_line).set_color(YELLOW)

		z_axis_point = np.array(point)
		z_axis_point[:2] = 0
		r_line = DashedLine(z_axis_point, point)
		r_line.set_color(RED)
		r_label = MathTex(r"Rcos(\theta)")
		r_label.rotate(90 * DEGREES, RIGHT)
		r_label.scale(0.7).set_color(RED)
		r_label.set_stroke(width=0, background=True)
		r_label.next_to(r_line, OUT, 0.5 * SMALL_BUFF)

		self.wait()
		self.play(
			Create(arc),
			Write(theta),
		)
		self.wait()
		self.play(FadeIn(r_s))
		self.wait()
		self.move_camera(
			phi=70 * DEGREES,
			theta=-110 * DEGREES,
			run_time=3
		)
		self.wait(2)

		self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
		self.wait()


class ShowProof(SphereScene):

	a = 30
	b = 30
	
	def construct(self):
		self.setup()

	def setup(self):

		ax = self.get_ax()
		sphere = self.get_sphere(BLUE_E, BLUE_C, self.a, self.b)
		sphere_ghost = self.get_ghost_surface(sphere)

		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

		self.add(ax)
		self.play(FadeIn(sphere))
