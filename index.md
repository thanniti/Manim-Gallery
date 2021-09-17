# Welcome to my manim gallery

manim is python libary for creating math animation create by grant Sanderson founder of 3b1b channels

## TheMotionOfPlanets
![Orbitting](https://github.com/thanniti/Manim-Gallery/blob/main/Media/TheMotionOfPlanets_ManimCE_v0.10.0.gif)
```python

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

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/thanniti/Manim-Gallery/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
b