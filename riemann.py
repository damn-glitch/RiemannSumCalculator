import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

GREEN_RGB = '#99FF99'
RED_RGB = '#F88379'


def compute_nth_riemann_sum(n: int, func: str, a: float, b: float, endpoint_method: str) -> tuple:
    delta_x = (b - a) / n  # Used as a step value, defined as commonly used in class
    sum = 0  # Tracks total value of the sum
    rectangles = []  # Keeps a history of the area we've summed. This is used purely for visualization

    # Python's range isn't inclusive of the end variable so add one (so the last value is n)
    # (This is an implementation of the sigma notation used)
    for i in range(1, n + 1):
        # xᵢ = a + iΔx
        x_i_minus_1 = a + ((i - 1) * delta_x)
        x_i = a + (i * delta_x)

        # Determine what point to evaluate f at
        if endpoint_method == "Left":
            sample_point = x_i_minus_1
        elif endpoint_method == "Right":
            sample_point = x_i
        elif endpoint_method == "Middle":
            sample_point = (x_i_minus_1 + x_i) / 2
        else:
            raise ArithmeticError("Unknown sampling method " + endpoint_method)

        # Evaluate f(xᵢ*) (where xᵢ* = sample_point as chosen above)
        # (We use the fact Python is a dynamic language to simply treat the function as an expression)
        f_at_sample = eval(func, {"x": sample_point})

        # Multiply by Δx and then sum (doing this in a loop is equal to sigma notation)
        sum += f_at_sample * delta_x

        # Store the coordinates of the rectangle we calculated the area of to visualize later
        # (The data is ordered like this so it can be passed directly into matplotlib)
        rectangles.append((
            (x_i_minus_1, 0),
            delta_x,
            f_at_sample
        ))

    return sum, delta_x, rectangles


def plot_riemann_sum(tk_canvas, n: int, func: str, a: float, b: float, sum: float, delta_x: float, rectangles: list):
    # Reset pyplot (so we can plot more than one Riemann sum per program run)
    plt.clf()

    # Plot the "actual" function (so we can see how it lines up with the rectangles used
    # for approximation) by evenly distributing 500 points between a and b and evaluating
    # func at each point
    x = np.linspace(a, b, num=500)
    y = eval(func)

    plt.plot(x, y)

    # Plot the rectangles (whose areas we summed to produce the Riemann sum)
    for rectangle in rectangles:
        plt.gca().add_patch(
            patches.Rectangle(
                *rectangle,
                # Positive area is green, negative area is red
                # rectangle[1] = Δx, rectangle[2] = f(xᵢ*)
                # If Δx * f(xᵢ*) > 0 then the area is above the curve and "moving"
                # in the positive direction. If Δx were negative then area above
                # the x axis should be counted as negative.
                color=GREEN_RGB if rectangle[1] * rectangle[2] > 0 else RED_RGB
            )
        )

    # Draw a box at the top left showing the actual sum and the value of delta x
    plt.gca().text(
        0.05,
        0.95,
        r"$S_{" + str(n) + "} = " + str(round(sum, 3)) + "$"  # Some nice LaTeX to subscript
        "\n"
        "Δx = " + str(round(delta_x, 3)),
        transform=plt.gca().transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox={
            "boxstyle": "round",
            "facecolor": "wheat",
            "alpha": 0.7
        }
    )

    plt.xlim(a, b)  # Sometimes the auto scaling axis feature behaves oddly so we manually set it

    # Draw onto the Tkinter canvas
    fig_canvas = FigureCanvasTkAgg(plt.gcf(), master=tk_canvas)
    fig_canvas.draw()
    fig_canvas.get_tk_widget().pack()
