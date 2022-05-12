import logging
import param
import panel as pn
from datetime import datetime
from dashboard_tutorial.views import AnalysisView
from bokeh.models.callbacks import CustomJS
from bokeh.models import Span, Toggle, CrosshairTool


class DashboardView(param.Parameterized):
    # Parameters
    plot_by_row = param.Integer(3, bounds=(1, 4))

    autocomplete_search_serie = pn.widgets.TextInput(name='Search Serie', placeholder='Ticker or Serie Name')
    search_source = pn.widgets.Select(name='Source', value='fred', options=['fred', 'quandl', 'file'])

    button_add_serie = pn.widgets.Button(name='Add Serie', width_policy='fit', height_policy='fit', button_type='primary')

    action_open_modal = param.Action(lambda x: x.param.trigger('action_open_modal'), label='Add Serie')

    selected_analysis_name = param.String(default="", label="Analysis Name")
    action_new_analysis = param.Action(lambda x: x.param.trigger('action_new_analysis'), label='New Analysis')

    action_update_tabs = param.Action(lambda x: x.param.trigger('action_update_tabs'), label='Update Tabs')
    action_update_alerts = param.Action(lambda x: x.param.trigger('action_update_alerts'), label='Update Alerts')
    action_update_search_results = param.Action(lambda x: x.param.trigger('action_update_search_results'), label='Update Search Result')

    analysis_list = param.List([], item_type=AnalysisView)


    def __init__(self, **kwargs):
        assert kwargs.get('manager', None), "Definir el manager para la vista"
        manager = kwargs.pop('manager')
        title = kwargs.pop('title')

        super().__init__(**kwargs)

        self.button_add_serie.param.watch(self.add_serie_buttom, 'value')
        #self.button_create_analisis.param.watch(self.create_analysis, 'value')

        self.autocomplete_search_serie.param.watch(self.do_search, 'value')

        self.alerts = []
        self.search_result = []

        self.manager = manager

        self._load()

        # Create Dashboard View
        pn.extension(template='bootstrap')

        pn.extension(loading_spinner='dots', loading_color='#00aa41', sizing_mode="stretch_width")
        pn.param.ParamMethod.loading_indicator = True

        self.bootstrap = pn.template.BootstrapTemplate(title=title)
        self.bootstrap.sidebar.append(self.param.selected_analysis_name)
        self.bootstrap.sidebar.append(self.param.action_new_analysis)
        self.bootstrap.sidebar.append(self.param.action_open_modal)
        self.bootstrap.sidebar.append(self.param.plot_by_row)

        self.bootstrap.modal.append(pn.Column(pn.Row(self.autocomplete_search_serie, self.search_source), self.get_search_results))

        alerts = pn.Row(pn.panel(self.get_alerts, width=300))
        container = pn.Row(pn.panel(self.get_tabs, width=300))

        self.bootstrap.main.append(alerts)
        self.bootstrap.main.append(container)

    @param.depends('action_open_modal', watch=True)
    def open_modal(self):
        self.bootstrap.open_modal()

    def _load(self):
        logging.info("[+] Loading Analysis")
        list_form_analysis = []
        for k in self.manager.analysis.get_names():
            analysis = self.manager.analysis.get_by_name(k)
            form_analysis = AnalysisView(parent=self, analysis=analysis)
            list_form_analysis.append(form_analysis)
        self.analysis_list = list_form_analysis

    def _get_selected_data_source(self):
        return self.manager.sources.get_by_name(self.search_source.value)

    def add_analysis(self, **kwargs):
        new_analysis = self.manager.add_analysis(**kwargs)
        form_analysis = AnalysisView(parent=self, analysis=new_analysis)
        self.analysis_list = [*self.analysis_list, form_analysis]
        return form_analysis

    def do_search(self, event):
        logging.info("[+] Obteniendo resultados de busqueda ...")
        if event.new != "":
            self._get_selected_data_source().do_search(event.new)
            self.param.trigger('action_update_search_results')

    def _get_current_analysis_form(self):
        return self.analysis_list[self.tabs.active]

    def add_serie_buttom(self, event):
        logging.info("[+] Agregando nueva serie de tiempo ...")
        serie_id = event.obj.name

        # Serie Information
        serie_data = None

        for s in self._get_selected_data_source().get_search_results():
            if s['id'] == serie_id:
                serie_data = {"serie_id": s['id'], "source": self.search_source.value, 'units': s['units'], 'freq': s['frequency'], 'serie_name': s['name'], 'column': s['id']}
                break

        analysis_form = self._get_current_analysis_form()

        analysis_form.add_chart(**serie_data)

        self.bootstrap.close_modal()

    @param.depends('action_update_alerts', watch=False)
    def get_alerts(self):
        list_alerts = []

        for a in self.alerts:
            list_alerts.append(pn.pane.Alert('## Alert\n{}'.format(a)))

        self.alerts = []

        return list_alerts[0] if len(list_alerts) > 0 else None

    def tabinfo(self, event):
        print("TAB: ", self.tabs.active)

    @param.depends('action_update_tabs', 'plot_by_row', 'analysis_list', watch=False)
    def get_tabs(self):
        tabs = None
        tuplas = []

        for a in self.analysis_list:
            panel = a.panel()
            tuplas.append((a.analysis.name, panel))

        self.tabs = pn.Tabs(*tuplas, closable=True)

        self.tabs.param.watch(self.tabinfo, 'active')

        return self.tabs

    @param.depends('action_update_search_results', watch=False)
    def get_search_results(self):
        logging.info("[+] Renderizando resultados de busqueda ...")

        rows = []
        description = """
        **{}**\n
        {} to {}\n
        {}\n
        {}
        """

        selected_source = self._get_selected_data_source()

        for r in selected_source.get_search_results():
            button_select = pn.widgets.Button(name=r['id'])
            button_select.param.watch(self.add_serie_buttom, 'value')

            rows.append(pn.Card(
                    pn.Column(description.format(r['name'], r['observation_start'], r['observation_end'], r['frequency'], r['notes']), button_select),
                    header=pn.panel(selected_source.logo, height=40), header_color=selected_source.header_color, header_background=selected_source.header_background)
            )

        return pn.Column("**Search Results:**", pn.GridBox(*rows, ncols=4)) if len(rows) > 0 else None

    @param.depends('action_new_analysis', watch=True)
    def create_analysis(self):
        logging.debug("[+] Creando nuevo analisis: {}".format(self.selected_analysis_name))

        if self.selected_analysis_name == "":
            self.alerts.append("Digite un nombre para el nuevo analisis.")
            self.param.trigger('action_update_alerts')
        else:
            self.add_analysis(analysis_name=self.selected_analysis_name)
            self.param.trigger('action_update_tabs')

    def show(self):
        self.bootstrap.show()

    def __repr__(self, *_):
        return "Value"
