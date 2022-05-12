import panel as pn
import param
import re
from dashboard_tutorial.utils import create_ts
from bokeh.models.callbacks import CustomJS


class SeriesView(param.Parameterized):

    def __init__(self, **kwargs):
        assert kwargs.get('serie', None), "Debe suministrar un objeto serie"
        assert kwargs.get('parent', None), "Debe suministrar un objeto AnalysisView"

        self.parent = kwargs.pop('parent', None)
        self.serie = kwargs.pop('serie', None)

        self.analysis = self.serie.analysis
        self.manager = self.analysis.manager

        super().__init__(**kwargs)

        option_transforms = self.manager.transformers.get_names()

        select_value = 'Normal'

        for ot in self.manager.transformers.all():
            if re.search("{}$".format(ot.suffix), self.serie.column):
                select_value = ot.name
                break

        #self.select_processing_2 = pn.widgets.Select(name='Transform', value=select_value, options=['Normal', 'Percentage Change', 'Percentage Change from Year Ago'])
        self.select_processing_2 = pn.widgets.Select(name='Transform', value=select_value, options=['Normal', *option_transforms])
        self.select_processing_2.param.watch(self.set_column, 'value', onlychanged=True, precedence=0)

        self.fig, self.h_hovertool, self.v_hovertool = create_ts(source=self.analysis.data_source, x_data_range=self.analysis.x_data_range,
                                                 column=self.serie.column, serie_name=self.serie.serie_name, freq=self.serie.freq,
                                                 units=self.serie.units_show)

        # Sync Crosshair tools with the other graphs
        self.fig.add_tools(self.parent.crosshair)

        self.callback_figs = CustomJS(args=dict(span=self.parent.current_time), code="""
        span.location = cb_obj.x;
        console.log(new Date(cb_obj.x));
        """)

        # Syncc the Span mark with the other graphs
        self._add_current_time_span()

    def _add_current_time_span(self):
        self.fig.renderers.extend([self.parent.current_time])
        self.fig.js_on_event('tap', self.callback_figs)

    def set_column(self, event):
        transformation_name = event.new

        self.serie.update(transformation_name)

        self.update_plot()

    def update_plot(self):
        line = self.fig.select_one({'name': 'line'})
        cr = self.fig.select_one({'name': 'cr'})

        line.glyph.y = self.serie.column
        cr.glyph.y = self.serie.column

        self.fig.yaxis[0].axis_label = self.serie.units_show

        # Set Name of legent
        self.fig.legend[0].name = self.serie.column

    #@param.depends('select_processing')
    def view(self):
        #data_source = self.output()
        # print("******** Chart Form View**************")
        # print("************ Chart Form - Set column **************")
        return self.fig

    def panel(self):
        return pn.Card(pn.Column(self.view, self.select_processing_2), title=self.serie.serie_name)

    def __repr__(self, *_):
        return "Value"
