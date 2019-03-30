We consider a unit commitment problem definded by two **combined heat power units** (chp), a **heat plant** and a **heat storage** (store). 

In the input folder you will find
* technical data and the operating costs of every unit,
* prices for gas and power,
* heat demand for one day.

The projekt consists of 4 python files:
* model.py: Includes the objective function and constraints to descripe the problem.
* instance.py: The function run_optimization read the input timeseries, create the instance of the model, solve the problem and write the results into timeseries. A folder named output will be create to save the timeseries.
* analysis.py: Includes a short analysis and some plots of results. A subfolder named plots will be create to save the plots.
* main.py: Is to be execute.