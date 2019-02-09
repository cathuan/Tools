import numpy as np
import matplotlib.pyplot as plt


def onpick(event):

    legline = event.artist
    origline = lined[legline]
    vis = not origline.get_visible()
    origline.set_visible(vis)

    if vis:
        legline.set_alpha(1.0)
    else:
        legline.set_alpha(0.2)
    fig.canvas.draw()


if __name__ == "__main__":

    t = np.arange(0.0, 0.2, 0.1)
    y1 = 2*np.sin(2*np.pi*t)
    y2 = 4*np.sin(2*np.pi*t)

    fig, ax = plt.subplots()
    ax.set_title('Click on legend line to toggle line on/off')
    line1, = ax.plot(t, y1, color='red', label='1 HZ')
    line2, = ax.plot(t, y2, color='blue', label='2 HZ')
    leg = ax.legend(loc='upper left', fancybox=True, shadow=True)
    leg.get_frame().set_alpha(0.4)

    lines = [line1, line2]
    lined = dict()
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(5)
        lined[legline] = origline

    fig.canvas.mpl_connect('pick_event', onpick)
    plt.show()
