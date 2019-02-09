import numpy as np
import matplotlib.pyplot as plt


def set_hider(ax):
    """Function set the plotted lines in axes hidable by clicking the legend.

    The hidable artists in the graph must be all lines (create by call ax.plot())
    and it must have a label, otherwise the program will crash."""

    def onpick(event):
        """Handler used to hide lines by hiding plotted lines."""

        # legendLine is the line in the legend
        legendLine = event.artist

        ax = legendLine.axes
        fig = ax.get_figure()

        # origLine is the line plotted on the graph canvas
        label = legendLine.get_label()
        origLine = None
        for line in ax.lines:
            if line.get_label() == label:
                assert origLine is None, "More than one line with label {}".format(label)
                origLine = line
                break
        else:
            assert False, "No line with label {} found".format(label)

        vis = not origLine.get_visible()
        origLine.set_visible(vis)
        legendLine.set_alpha(1.0 if vis else 0.2)

        fig.canvas.draw()

    fig = ax.get_figure()
    leg = ax.get_legend()
    leg.get_frame().set_alpha(0.4)
    for legendLine in leg.get_lines():
        legendLine.set_picker(5)
    fig.canvas.mpl_connect('pick_event', onpick)


def main():
    t = np.arange(0.0, 0.2, 0.1)
    y1 = 2*np.sin(2*np.pi*t)
    y2 = 4*np.sin(2*np.pi*t)
    y3 = 8*np.sin(2*np.pi*t)

    fig, ax = plt.subplots()
    ax.set_title('Click on legend line to toggle line on/off')
    ax.plot(t, y1, color='red', label='1 HZ')
    ax.plot(t, y2, color='blue', label='2 HZ')
    ax.plot(t, y3, color='green', label='4 HZ')
    ax.legend(loc='upper left', fancybox=True, shadow=True)

    set_hider(ax)
    plt.show()


if __name__ == "__main__":

    main()
