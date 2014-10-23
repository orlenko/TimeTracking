import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def mkgraph(data, filename):
    fig, ax = plt.subplots()
    dates = []
    productive = []
    wasted = []
    optimizable = []
    for rec in data:
        dates.append(rec['date'])
        productive.append(rec['billable_true'])
        wasted.append(rec['lost'])
        optimizable.append(rec['optimizable'])
    ax.plot(dates, productive, 'g*-')
    ax.plot(dates, wasted, 'rx-')
    ax.plot(dates, optimizable, 'yo-')

    days = mdates.DayLocator()
    day_fmt = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(day_fmt)

    ax.set_xlim(dates[0], dates[-1])

    # format the coords message box
    def hr(x): return '%1.2f' % x
    ax.format_xdata = mdates.DateFormatter('%m-%d')
    ax.format_ydata = hr
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    plt.savefig(filename)