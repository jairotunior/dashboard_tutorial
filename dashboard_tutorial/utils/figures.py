import pandas as pd
from datetime import date
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure
from bokeh.models.callbacks import CustomJS
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool, Span, Div, Toggle, BoxAnnotation, Slider, \
    CrosshairTool, Button, DataRange1d, Row, LinearColorMapper, Tabs, GroupFilter, CDSView, IndexFilter

def create_fig(title, legend_label, x_label, y_label, source, x, y, x_data_range, tooltip_format, vtooltip=False,
               htooltip=False, tools=None, view=None, secondary_plot=False):
    # create a new plot and share only one range
    fig = figure(plot_height=400, plot_width=600, tools=tools, active_scroll='xwheel_zoom',
                 title=title, x_axis_type='datetime', x_axis_label=x_label, x_range=x_data_range,
                 y_axis_label=y_label)

    line = fig.line(x=x, y=y, source=source, name="line", legend_label=legend_label, line_width=2)
    cr = fig.circle(x=x, y=y, source=source, name="cr", size=10,
                      fill_color="grey", hover_fill_color="firebrick",
                      fill_alpha=0.05, hover_alpha=0.3,
                      line_color=None, hover_line_color="white")

    #cr.visible = False

    horizontal_hovertool_fig = None
    vertical_hovertool_fig = None

    if htooltip:
        horizontal_hovertool_fig = HoverTool(tooltips=None, renderers=[cr], names=['cr'], mode='hline')
        fig.add_tools(horizontal_hovertool_fig)
    if vtooltip:
        #vertical_hovertool_fig = HoverTool(tooltips=tooltip_format, renderers=[line], names=['line'], formatters={'@date': 'datetime'}, mode='vline')
        vertical_hovertool_fig = HoverTool(tooltips=None, renderers=[cr], mode='vline')
        fig.add_tools(vertical_hovertool_fig)

    return fig, horizontal_hovertool_fig, vertical_hovertool_fig


def create_ts(source, x_data_range, **kwargs):
    tick = kwargs.get('column', None)
    serie_name = kwargs.get('serie_name', None)
    freq = kwargs.get('freq', None)
    units = kwargs.get('units', None)
    
    tools = kwargs.get('tools', ['pan', 'reset', 'save', 'xwheel_zoom', 'ywheel_zoom', 'box_select', 'lasso_select'])

    fig = h_hovertool = v_hovertool = None

    # Format the tooltip
    tooltip_format = [
        ('Date', '@date{%F}'),
        ('Rate', '@{}'.format(tick)),
    ]

    fig, h_hovertool, v_hovertool = create_fig(title=serie_name, legend_label=tick, x_label='date',
                                               y_label=units,
                                               source=source,
                                               x='date', y=tick, x_data_range=x_data_range,
                                               tooltip_format=tooltip_format, htooltip=True, vtooltip=True,
                                               tools=tools)

    return fig, h_hovertool, v_hovertool


# ************************************* Methods ***********************************

def add_auto_adjustment_y(fig, source, column):
    #source = ColumnDataSource(dict(index=df.date, x=df[column]))

    callback_rescale = CustomJS(args=dict(y_range=fig.y_range, source=source, column=column), code='''
        console.log(source.data[column]);
        clearTimeout(window._autoscale_timeout);
 
        var index = source.data.index,
            x = source.data[column],
            start = cb_obj.start,
            end = cb_obj.end,
            min = 1e10,
            max = -1;

        for (var i=0; i < index.length; ++i) {
            if (start <= index[i] && index[i] <= end) {
                max = Math.max(x[i], max);
                min = Math.min(x[i], min);
            }
        }
        var pad = (max - min) * .05;

        window._autoscale_timeout = setTimeout(function() {
            y_range.start = min - pad;
            y_range.end = max + pad;
        }, 50);
    ''')

    fig.x_range.js_on_change('start', callback_rescale)


