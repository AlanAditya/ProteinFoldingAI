from manim import *
import numpy as np


class ManimTester(Scene):
    def construct(self):
        box = Cube(side_length=2, color=BLUE)
        box.set_fill(BLUE, opacity=0.5)
        self.play(Create(box))
        self.wait(1)
        self.play(box.animate.rotate(PI / 4, axis=UP))
    