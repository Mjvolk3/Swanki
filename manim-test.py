from manim import Scene, Axes, Text, MathTex, RED, BLUE, UP, RIGHT, LEFT, DOWN, ORIGIN, ValueTracker, always_redraw
import numpy as np

class ExponentialDistribution(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.2],
            axis_config={"color": BLUE},
            x_length=10,  # Increased size
            y_length=6    # Increased size
        )
        
        # #TODO: Adjust x and y label positions
        x_label = axes.get_x_axis_label("x").shift(DOWN * 0.5 + RIGHT * 0.5)
        y_label = axes.get_y_axis_label("f(x)").shift(LEFT * 1 + UP * 0.1)

        # Create title
        # #TODO: Adjust title position
        title = Text("Exponential Distribution", font_size=40).to_edge(UP).shift(DOWN * 0.5)
        
        self.add(axes, x_label, y_label, title)

        # Create formula and position it
        # #TODO: Adjust formula position
        formula = MathTex(r"f(x) = \lambda e^{-\lambda x}", font_size=36).move_to(axes.c2p(1.5, 0.8))
        self.add(formula)

        # Function to create the exponential distribution graph
        def exp_dist(x, lambda_val):
            return lambda_val * np.exp(-lambda_val * x)

        # Create ValueTracker for lambda
        lambda_tracker = ValueTracker(1)

        # Create graph
        graph = always_redraw(lambda: axes.plot(
            lambda x: exp_dist(x, lambda_tracker.get_value()),
            color=RED,
            x_range=[0, 5]
        ))

        # Create lambda value text
        # #TODO: Adjust lambda text position
        lambda_text = always_redraw(lambda: MathTex(r"\lambda = {:.2f}".format(lambda_tracker.get_value()), font_size=36)
                                    .move_to(axes.c2p(3.5, 0.5)))

        self.add(graph, lambda_text)

        # Initial wait
        self.wait(1)

        # Animate changes in lambda
        for new_lambda in [0.5, 1.5, 2, 1]:
            self.play(
                lambda_tracker.animate.set_value(new_lambda),
                run_time=3,
            )
            self.wait(1)

        # Final wait
        self.wait(2)

# Render the scene
if __name__ == "__main__":
    from manim import config
    config.output_file = "exponential_distribution.mp4"
    scene = ExponentialDistribution()
    scene.render()