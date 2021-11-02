# Welcome to my manim gallery

manim is python libary for creating math animation create by grant Sanderson founder of 3b1b channel

**some of the code are inherit form Grants ([see his code](https://github.com/3b1b/videos))

# to render
copy the code and run the command

`manim filename.py classname -p/-ql`
* *-p for height quality(1080p)* *
* *-ql for low quality(480p)* *
## TheMotionOfPlanets
> Orbiting of small mass object around large mass object
note that gravitational force is function of distance between two object
![Orbitting](https://github.com/thanniti/Manim-Gallery/blob/main/Media/TheMotionOfPlanets_ManimCE_v0.10.0.gif)
```python
from manim import*
import numpy as np
from numpy import random
from numpy import linalg as LA
import functools
import operator as op

class Orbiting(VGroup):

	rate = 7.5

	def __init__(self, planet, star, ellipse, rate, **kwargs):
		VGroup.__init__(self, **kwargs)
		self.add(planet)
		self.planet = planet
		self.star = star
		self.ellipse = ellipse
		self.rate = rate
		# Proportion of the way around the ellipse
		self.proportion = 0.75
		planet.move_to(ellipse.point_from_proportion(0.75))

		self.add_updater(lambda m, dt: m.update(dt))

	def update(self, dt):
        # time = self.internal_time

		planet = self.planet
		star = self.star
		ellipse = self.ellipse

		rate = self.rate
		radius_vector = planet.get_center() - star.get_center()
		rate *= 1.0 / LA.norm(radius_vector)

		prop = self.proportion
		d_prop = 0.001
		ds = LA.norm(op.add(
			ellipse.point_from_proportion((prop + d_prop) % 1),
			-ellipse.point_from_proportion(prop),
		))

		delta_prop = (d_prop / ds) * rate * dt

		self.proportion = (self.proportion + delta_prop) % 1
		planet.move_to(
			ellipse.point_from_proportion(self.proportion)
		)
class TheMotionOfPlanets(Scene):

	suncenter = ORIGIN+3*RIGHT
	sun_height = 0.5
	a = 3.5
	b = 2.0
	comet_height = 0.2
	ellipse_color = WHITE
	ellipse_stroke_width = 1

	def construct(self):
		self.setup_orbits()

	def setup_orbits(self):
		sun = Dot(color=RED)
		sun.set_height(self.sun_height)
		sun.move_to(self.suncenter)
		self.sun = sun
		comet = self.get_comet()
		ellipse = self.get_ellipse()
		orbit = Orbiting(comet, sun, ellipse, rate=5)

		self.add(sun)
		#self.add(comet)
		self.add(ellipse)
		#self.add_foreground_mobjects(comet)
		self.add(orbit)
		self.wait(30)
	
	def get_orbit(self):
		planet = Dot(color=GRAY)

	def get_comet(self):
		comet = Dot(color=GRAY)
		comet.set_height(self.comet_height)
		return comet

	def get_ellipse(self):
		sun = self.sun
		a = self.a
		b = self.b
		c = np.sqrt(a**2 - b**2)
		ellipse = Circle(radius=a)
		ellipse.set_stroke(
			self.ellipse_color,
			self.ellipse_stroke_width,
		)
		ellipse.stretch(fdiv(b, a), dim=1)
		ellipse.move_to(
			self.sun.get_center() + c * LEFT,
		)
		self.focus_points = [
			self.sun.get_center(),
			self.sun.get_center() + 2 * c * LEFT,
		]
		return ellipse
```
## InfiniteSumLine
![InfiniteSumLine](https://github.com/thanniti/Manim-Gallery/blob/main/Media/InfiniteSum_ManimCE_v0.10.0.gif)
```python
from manim import*
import numpy as np

class InfiniteSum(Scene):
	def construct(self):
	
		nl = NumberLine(
			x_range=[0,65,1.25],
			length=26,
			numbers_with_elongated_ticks=[0,5,10,15,20,25,30,35,40,45,50,55,60,65],
			include_numbers=True,
			numbers_to_include= [0,5,10,15,20,25,30,35,40,45,50,55,60,65],
			decimal_number_config={"num_decimal_places": 0},
			color = BLUE,
			).shift(2*DOWN)
		nl.to_edge(LEFT,buff=0)
		
		LINE_COLOR = [RED_A,RED]
		COLOR_bool = True
		sum_brace = []
		sum_line=[]
		SUM=[]
		a,b=0,3
		for i in range(0,3,1):
			COLOR_bool = int(not(COLOR_bool))
			sum_brace.append(BraceBetweenPoints(nl.n2p(a),nl.n2p(b),UP))
			sum_line.append(Line(nl.n2p(a),nl.n2p(b)).set_color(LINE_COLOR[COLOR_bool]))
			SUM.append(VGroup(sum_brace[i],sum_line[i]))
			a=a+3**(i+1)
			b=b+3**(i+2)

		sum_brace_group = Group(*[sum_brace[i] for i in range(3)])
		sum_line_group= Group(*[sum_line[i] for i in range(3)])
		
		sum_tex = Tex("3","9","27")

		sum_tex[0].next_to(sum_brace_group[0],UP)
		sum_tex[1].next_to(sum_brace_group[1],UP)
		sum_tex[2].next_to(sum_brace_group[2],UP)

		self.play(Create(nl))
		for i in range(0,3):
			self.play(AnimationGroup(
				GrowFromEdge(sum_brace_group[i], LEFT),
				GrowFromEdge(sum_line_group[i], LEFT),
				FadeIn(sum_tex[i]),
				lag_ratio = 0.5,
				run_time = 1.5,
				)
			)
```
## Many boxes
![Many boxes](https://github.com/thanniti/Manim-Gallery/blob/main/Media/StackRect_ManimCE_v0.10.0.png)
```python
from manim import*
import numpy as np

class StackRect(Scene):
	def construct(self):
		sequence = MathTex(r"1",r",",r"4",r",",r"9",r",",r"16",r",",r"?")
		sequence[0].shift(4*LEFT,1.5*DOWN),
		sequence[1].shift(3*LEFT,1.5*DOWN),
		sequence[2].shift(2*LEFT,1.5*DOWN),
		sequence[3].shift(1*LEFT,1.5*DOWN),
		sequence[4].shift(1.5*DOWN),
		sequence[5].shift(1*RIGHT,1.5*DOWN),
		sequence[6].shift(2*RIGHT,1.5*DOWN),
		sequence[7].shift(3*RIGHT,1.5*DOWN),
		sequence[8].shift(4*RIGHT,1.5*DOWN),

		rect = Rectangle(height=0.3, width=0.3, stroke_color = WHITE, stroke_opacity= 1)
		rect.set_fill(YELLOW, opacity=0.8)
		rect.set_stroke(width=0)

		rectgroup_1 = rect.copy().next_to(sequence[0],5*UP)

		rgroup_2 = VGroup(*[rect.copy() for i in range(2)])
		rgroup_2.arrange(RIGHT, buff = 0.1)
		rectgroup_2 = VGroup(*[rgroup_2.copy() for i in range(2)])
		rectgroup_2.arrange(DOWN, buff = 0.1)
		rectgroup_2.next_to(sequence[2],5*UP)

		rgroup_3 = VGroup(*[rect.copy() for i in range(3)])
		rgroup_3.arrange(RIGHT, buff = 0.1)
		rectgroup_3 = VGroup(*[rgroup_3.copy() for i in range(3)])
		rectgroup_3.arrange(DOWN, buff = 0.1)
		rectgroup_3.next_to(sequence[4],5*UP)

		rgroup_4 = VGroup(*[rect.copy() for i in range(4)])
		rgroup_4.arrange(RIGHT, buff = 0.1)
		rectgroup_4 = VGroup(*[rgroup_4.copy() for i in range(4)])
		rectgroup_4.arrange(DOWN, buff = 0.1)
		rectgroup_4.next_to(sequence[6],5*UP)
		
		rgroup_5 = VGroup(*[rect.copy() for i in range(5)])
		rgroup_5.arrange(RIGHT, buff = 0.1)
		rectgroup_5 = VGroup(*[rgroup_5.copy() for i in range(5)])
		rectgroup_5.arrange(DOWN, buff = 0.1)
		rectgroup_5.next_to(sequence[8],5*UP)

		self.add(rectgroup_1,rectgroup_2,rectgroup_3,rectgroup_4,rectgroup_5,sequence)
```
## SphereScene
this superclass are use to create the following sphere scene
```python
from manim import*
import numpy as np
from numpy import random

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
```
**Slicing Sphere**
![Slice To Rings](https://github.com/thanniti/Manim-Gallery/blob/main/Media/Ring_ManimCE_v0.10.0.gif)
```python
class Ring(SphereScene):

	n_random_subsets = 12
	a = 30
	b = 30

	def construct(self):
		self.setup_shapes()
		self.divide_into_rings()

	def setup_shapes(self):
		sphere = self.get_sphere(BLUE_E, BLUE_C, self.a, self.b)
		sphere.set_stroke(WHITE, width=0.25)
		self.add(sphere)
		self.sphere = sphere

		u_values, v_values = sphere.get_u_values_and_v_values()
		rings = VGroup(*[VGroup() for u in u_values])
		for piece in sphere:
			rings[piece.u_index].add(piece.copy())
		self.set_ring_colors(rings)
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

	def set_ring_colors(self, rings):
		a = len(rings)
		colors = [BLUE_E, BLUE_D]*a
		for i in range(0, a):
			rings[i].set_color(colors[i])
```
**Sphere Expansion**
![RotateAllPiecesWithExpansion](https://github.com/thanniti/Manim-Gallery/blob/main/Media/RotateAllPiecesWithExpansion_ManimCE_v0.10.0.gif)
```python
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
```
## ThreeBodySimulation
![ThreeBody](https://github.com/thanniti/Manim-Gallery/blob/main/Media/SimulateThreeBody_ManimCE_v0.10.0.gif)
```python
from manim import*
import numpy as np
from numpy import random
from numpy import linalg as LA
import functools
import operator as op

class SimulateThreeBody(ThreeDScene):

	masses = [1, 6, 3]
	colors = [RED_E, GREEN_E, BLUE_E]
	G = 1
	play_time = 60

	def construct(self):
		self.add_axes()
		self.add_bodies()
		self.add_trajectories()
		self.let_play()

	def add_bodies(self):
		masses = self.masses
		colors = self.colors

		bodies = self.bodies = VGroup()

		centers = self.get_initial_position()

		print(centers)

		for mass, color, center in zip(masses, colors, centers):
			body = Sphere(
				stroke_width=0.1,
			)
			body.set_color(color)
			body.set_opacity(0.75)
			body.mass = masses
			body.radius = 0.08 * np.sqrt(mass)
			body.set_width(2 * body.radius)

			body.point = center
			body.move_to(center)

			body.velocity = self.get_initial_velocity(
				center, centers, mass
			)

			bodies.add(body)

			#body.p = body.mass * vector(0,0,0)
		
		total_mass = np.sum([body.mass for body in bodies])
		center_of_mass = functools.reduce(op.add, [
			body.mass * body.get_center() / total_mass
			for body in bodies
		])
		average_momentum = functools.reduce(op.add, [
			body.mass * body.velocity / total_mass
			for body in bodies
		])
		for body in bodies:
			body.shift(-center_of_mass)
			body.velocity -= average_momentum

	def get_initial_position(self):
		return [
			np.array([random.randint(3),random.randint(3),random.randint(3)])
			for x in range(len(self.masses))
		]

	def get_initial_velocity(self, center, centers, mass):
		to_others = [
			center - center2
			for center2 in centers
		]
		velocity = 0.2 * mass * normalize(*filter(
			lambda diff: LA.norm(diff) > 0,
			to_others
		))
		return velocity

	def add_trajectories(self):
		def update_trajectory(traj, dt):
			new_point = traj.body.point
			if LA.norm(new_point - traj.get_points()[-1]) > 0.01:
				traj.add_smooth_curve_to(new_point)

		for body in self.bodies:
			traj = VMobject()
			traj.body = body
			traj.start_new_path(body.point)
			traj.set_stroke(body.color, 1, opacity=0.75)
			traj.add_updater(update_trajectory)
			self.add(traj, body)

	def let_play(self):
		bodies = self.bodies
		bodies.add_updater(self.update_bodies)
		# Break it up to see partial files as
		# it's rendered
		self.add(bodies)
		self.wait(10)
		#for x in range(int(self.play_time)):
		#	self.wait()

	def update_bodies(self, bodies, dt):
		G = self.G

		num_mid_steps = 1000
		for x in range(num_mid_steps):
			for body in bodies:
				acceleration = np.zeros(3)
				for body2 in bodies:
					if body2 is body:
						continue
					diff = body2.point - body.point
					m2 = body2.mass
					R = LA.norm(diff)
					acceleration = acceleration + (G * m2 * diff / (R**3))
				body.point = body.point + (body.velocity * dt / num_mid_steps)
				body.velocity = body.velocity + (acceleration * dt / num_mid_steps)
		for body in bodies:
			body.move_to(body.point)
		return bodies


	def add_axes(self):
		axes = ThreeDAxes()
		axes.set_stroke(width=0.5)
		self.add(axes)

		# Orient
		self.set_camera_orientation(
				phi=70 * DEGREES,
				theta=-110 * DEGREES,
		)
		self.begin_ambient_camera_rotation()
```
For more details see [Repository](https://github.com/thanniti/Manim-Gallery)

### Support or Contact
Thanniti Leelapattanaputichot
email: tunleela30547@gmail.com Ig:tunsza
