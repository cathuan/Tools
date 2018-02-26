from __future__ import print_function
from matplotlib import pyplot as plt

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        print('mode', "(%s)" % (plt.get_current_fig_manager().toolbar.mode), "[%s]" % (type(plt.get_current_fig_manager().toolbar.mode)))
        print('pan/zoom?', plt.get_current_fig_manager().toolbar.mode == "pan/zoom")
        print('zoom rect?', plt.get_current_fig_manager().toolbar.mode == "zoom rect")
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build line segments')
line, = ax.plot(range(100000), range(100000))  # empty line
linebuilder = LineBuilder(line)

plt.show()