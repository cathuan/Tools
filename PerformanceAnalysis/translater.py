class PlotFormat(object):

    # color support for matplotlib
    colors = {"b": "blue", "r": "red", "k": "black", "g": "green", "c": "cyan", "y": "yellow", "m": "magenta",
              "w": "white"}

    # marker format
    markers = {"o": "circle", "v": "triangle-down", "^": "triangle-up", "<": "triangle-left", ">": "triangle-right",
               "*": "star", "x": "x", "d": "diamond"}

    # style format: solid_line (None), dashed line, or dash dot line, or dotted line style
    styles = {"-": None, "--": "dash", ":": "dot", "-.": "dashdot"}

    def __init__(self, x, y, format_string, label=None, linewidth=None):

        self.mode = None
        self._color_format = self._get_color_format(format_string)
        self._marker_format = self._get_marker_format(format_string)
        self._style_format = self._get_style_format(format_string)

    def _get_color_format(self, format_string):
        color_format = None
        for matplotlib_format in PlotFormat.colors.keys():
            if matplotlib_format in format_string:
                assert color_format is None
                color_format = PlotFormat.colors[matplotlib_format]
        return color_format

    def _get_marker_format(self, format_string):
        marker_format = None
        for matplotlib_format in PlotFormat.markers.keys():
            if matplotlib_format in format_string:
                assert marker_format is None
                marker_format = PlotFormat.markers[matplotlib_format]
        return marker_format

    def _get_style_format(self, format_string):
        style_format = None
        for matplotlib_format in PlotFormat.styles.keys():
            if matplotlib_format in format_string:
                # matplotlib style format has "-" as line, but it has "--" and "-." as well..
                # so need to add an extra logic in case we can find "-" in both "--" and "-." case.
                if matplotlib_format == "-" and style_format is not None:
                    continue
                assert style_format is not None or style_format == "-"
                style_format = PlotFormat.styles[matplotlib_format]
        return style_format

    def get_argument(self):
        has_line = (self._style_format is not None)
        has_marker = (self._marker_format is not None)
        if has_marker and has_line:
            self.mode = "lines+markers"
        elif not has_marker and has_line:
            self.mode = "lines"
        elif has_marker and not has_line:
            self.mode = "markers"
        else:
            self.mode = "lines"  # if no style nor marker is supplied, defaulted as lines

    def get_color(self):
        if self._color_format is None:
            return "blue"  # default color is blue
        else:
            return self._color_format

    def get_line_argument(self):

        assert self.mode == "lines" or self.mode == "lines+markers"
        color = self.get_color()
        style = self._style_format
        return {"color": color, "dash": style}

    def get_marker_argument(self):

        assert self.mode == "markers" or self.mode == "lines+markers"
        color = self.get_color()
        symbol = self._marker_format
        assert symbol is not None
        return {"color": color, "symbol": symbol}


def example():
    html_plotter = HTMLPlotter("test html interactive plots")
    date1 = datetime.date(2014, 1, 1)

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "cyan", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "red", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "yellow", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "black", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "value", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "value", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "task", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "task", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "user", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "user", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "position", "red", "abs delta")

    f = open("test3.html", "w")
    print(html_plotter.generate_html(), file=f)
    f.close()


def example():
    html_plotter = HTMLPlotter("test html interactive plots")
    date1 = datetime.date(2014, 1, 1)

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "cyan", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "red", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "yellow", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "black", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "value", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "value", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "task", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "task", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "user", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "user", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "position", "red", "abs delta")

    f = open("test3.html", "w")
    print(html_plotter.generate_html(), file=f)
    f.close()

def example():
    html_plotter = HTMLPlotter("test html interactive plots")
    date1 = datetime.date(2014, 1, 1)

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "cyan", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "red", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "yellow", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "black", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "value", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "value", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "task", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "task", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "user", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "user", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "position", "red", "abs delta")

    f = open("test3.html", "w")
    print(html_plotter.generate_html(), file=f)
    f.close()
