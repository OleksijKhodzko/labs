from manim import Scene, Rectangle, Write

class xd123(Scene):
    def construct(self):
        rect1 = Rectangle(height=0.5, width=0.5)
        self.play(Write(rect1))
