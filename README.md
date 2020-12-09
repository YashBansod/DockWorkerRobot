# Dock Worker Robot System (DWRS)

### Sample DWRS Configuration:

![DWRS image](./images/DWRS.svg)


### Setup Instructions
1. Open a command line interface in your system:  
    i. Terminal in Ubuntu (Linux)  
    ii. Powershell in Windows 10  
    
2. Make sure that a python 3.x interpreter is installed in your system by issuing the following command:
```shell script
python --version
```
Alternatively, you could activate a virtual python interpreter.  
Please make sure that you are using python interpreter version <=3.7.4 on windows.  

3. Install the required python libraries in your system by issuing the following command:
```shell script
pip install -r requirements.txt
```

### Run Instructions
1. Open the command line interface and browse to this project's directory:
```shell script
cd $project_dir
```
  
2. Edit the [parameters.py](./parameters.py) file for your desired simulation configuration.  
(See the example parameter files in the directory [example_parameters](./example_parameters/) for some examples.)

3. Run the simulation using the configured parameters by issuing the following command:
```shell script
python main_simulation.py -v -d
```
  
4. You can see the available simulation run options by issuing the following command:
```shell script
python main_simulation.py --help
```

### Project Main Scripts  
- [main_simulation.py](./main_simulation.py): Main Dock Worker Robot Simulation.  
- [deterministic_test.py](./deterministic_test.py): Dock Worker Robot Simulation Deterministic Test Routine.  
- [stochastic_test.py](./stochastic_test.py):Dock Worker Robot Simulation Stochastic Test Routine.  
  

### Project Requirements
- Python 3.x
- Python libraries listed in [requirements.txt](./requirements.txt)


### Contributors
- Yash Bansod  
- Shivam Mishra  
