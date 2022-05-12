import param
import panel as pn
from datetime import datetime
from dashboard_tutorial.views import SeriesView
from bokeh.models import CrosshairTool, Span


class AnalysisView(param.Parameterized):

    action_update_analysis = param.Action(lambda x: x.param.trigger('action_update_analysis'), label='Update')
    action_save_analysis = param.Action(lambda x: x.param.trigger('action_save_analysis'), label='Save')

    chart_forms = param.List([], item_type=SeriesView)

    def __init__(self, parent, **kwargs):
        assert kwargs.get('analysis', None), "Debe suministrar un objeto analysis"

        self.analysis = kwargs.pop('analysis', None)
        self.manager = kwargs.pop('manager', [])

        #self.analysis_name = kwargs.pop('analysis_name', "Default{}".format(str(random.randint(0, 1000))))

        self.ncols = kwargs.pop('ncols', 3)

        super().__init__(**kwargs)

        self.parent = parent

        self.crosshair = CrosshairTool(dimensions="both")
        self.current_time = Span(location=datetime.now().date(), dimension='height', line_color='red', line_width=2, line_dash='dashed', line_alpha=0.3)

        self.param.watch(self.save_analysis, 'action_save_analysis')

        self._load()

    def _load(self):
        list_chart_form = []
        for s in self.analysis.series:
            chart_form = SeriesView(parent=self, serie=s)
            chart_form.select_processing_2.param.watch(self.update_view, 'value', precedence=1)
            list_chart_form.append(chart_form)

        self.chart_forms = list_chart_form

    def save_analysis(self, event):
        self.analysis.save()

    def add_chart(self, **kwargs):
        #serie_id = kwargs.get('serie_id')

        # Update DataSource
        new_serie = self.analysis.add_serie(**kwargs)

        self.analysis.update_data_source()

        chart_form = SeriesView(parent=self, serie=new_serie)
        chart_form.select_processing_2.param.watch(self.update_view, 'value', precedence=1)

        self.chart_forms = [*self.chart_forms, chart_form]

        return chart_form

    def get_data_source(self):
        # print("**** Analysis Update Data Source *****")
        self.analysis.update_data_source()

    def update_view(self, event):
        self.param.trigger('action_update_analysis')

    @param.depends('action_update_analysis', 'chart_forms')
    def view(self):
        # print("***** Analysis View *********")
        # Arreglar esto aqui ya que al traer el dato modifica el datasource
        #self.data_source = self.get_data_source()
        #self.get_data_source()
        self.analysis.update_data_source()
        return pn.GridBox(*[c.panel() for c in self.chart_forms], ncols=self.parent.plot_by_row)

    def panel(self):
        # print("********** Analysis Panel ****************")
        return pn.Column(pn.Row(self.param.action_update_analysis, self.param.action_save_analysis), self.view)

    def __repr__(self, *_):
        return "Value"
