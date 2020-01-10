# MLCM
Machine Learning in Crowd Modelling // Exercise 2 onwards

## Running
The scenario files are included in the project, where the user can use specific ones for the specific problems. It can be edited to get desired outcome. The task 1 to 4 is in the folder Task1_4 and CahngeScenario folder. Last task is in Test5 folder.

### Running python file for task 5
```
python editScenario_task5.py --scenarioFile Task5_GNM.scenario --remove True
```

### Running python file for task 3
```
python editScenario_task3.py --scenarioFile Test6.scenario --outputFile Test6_editedpython.scenario
```
### Running Vadere
```
java -jar vadere-gui.jar
```
### Running Vadere console
```
java -jar vadere-console.jar scenario-run
--scenario-file "/path/to/the/file/scenariofilename.scenario"
--output-dir="/path/to/output/folders"
```