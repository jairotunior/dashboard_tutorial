# Dashboard of Economic Data Analysis

This is a custom implementation of Trading environment in Gym Toolkit. The idea is create an environment in Gym that let implement any state-of-the-art algorithm of Deep Reinforcement Learning.
This dashboard integrate different economic sources letting you add the desired time serie to be analysis.

The data sources integrated are:

* [Federal Reserve](https://fred.stlouisfed.org) - Economic Research from Federal Reserve of St. Louis
* [Nasdaq Data Link](https://data.nasdaq.com) - A premier source for financial, economic and alternative datasets.

## Screenshots

![alt text](./screenshots/Screenshot1.png)

![alt text](./screenshots/Screenshot2.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

1. Create a new virtual environment with your prefered tools
```
python -m venv env
```
2. Copy the repositiory https://github.com/jairotunior/economic_data.git
3. Install the dependencies

```
pip install -r requirements.txt
```
4. Now run the dashboard with:
```
python another_layout.py
```


That's all for use.

## Built With

* [Pandas](https://pandas.pydata.org) - pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool
* [Numpy](http://www.numpy.org/) - Is the fundamental package for scientific computing with Python.
* [Python](https://www.python.org/) - The most amazing Programming Language.
* [Panel](https://panel.holoviz.org) - Panel is an open-source Python library that lets you create custom interactive web apps and dashboards

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
