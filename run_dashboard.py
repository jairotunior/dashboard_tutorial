import os
import logging
from pathlib import Path
from dashboard_tutorial.sources import FREDSource, QuandlSource, FileSource
from dashboard_tutorial.transformers import FractionalDifferentiationEW, FractionalDifferentiationFFD, Differentiation, PercentageChange
from dashboard_tutorial.managers import ManagerDashboard
from dashboard_tutorial.views import DashboardView


if __name__ == '__main__':
    # Config Logging
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    BASE_DIR = Path(__file__).resolve().parent

    ANALYSIS_PATH = os.path.join(BASE_DIR, 'dashboards')

    if not os.path.exists(ANALYSIS_PATH):
        logging.info("[+] Se ha creado directorio de archivos.")
        os.mkdir(ANALYSIS_PATH)

    # Define Manager
    manager = ManagerDashboard(path=ANALYSIS_PATH)

    # **************** Register Transformers ***************************
    differentiation_transform = Differentiation(units_show='Returns')
    fractional_diff_transform = FractionalDifferentiationEW(units_show='Fractional Return')
    fractional_diff_ffd_transform = FractionalDifferentiationFFD(units_show='FFD Return')
    percentage_change_transform = PercentageChange(units_show='Percentage Change')
    percentage_change_from_year_transform = PercentageChange(name="Percentage Change from Year Ago", units_show='Percentage Change from Year Ago', periods=12)

    manager.transformers.register(fractional_diff_transform)
    manager.transformers.register(fractional_diff_ffd_transform)
    manager.transformers.register(differentiation_transform)
    manager.transformers.register(percentage_change_transform)
    manager.transformers.register(percentage_change_from_year_transform)


    # ******************* Create Source Managers ******************************
    fred_credentials = os.path.join(BASE_DIR, "api_fred.txt")
    fred_source = FREDSource(fred_credentials=fred_credentials)

    quandl_api_key = 'API_KEY'
    quandl_source = QuandlSource(api_key=quandl_api_key)

    # File source
    file_source_dir = os.path.join(BASE_DIR, "datasets", 'yields')
    file_source = FileSource(dir=file_source_dir)

    manager.sources.register(fred_source)
    manager.sources.register(quandl_source)
    manager.sources.register(file_source)

    manager.load()

    # ******************************************** Create Figures *************************************
    logging.info("[+] Render dashboards...")

    dashboard_view = DashboardView(title="Dashboard", manager=manager)

    dashboard_view.show()

