# AML
Pipeline for task4 of the course of AML

The following Repo has the pipeline for running the detection of anormalities of in the cardiac rithm of patients. 

1. model_selection.py -> calls the models that will be used for label classification or fitting.
2. pipeline.py -> sets the pipeline
3. confiparse.py -> sets the configuration.

In the folder models:
1. feature_selection.py -> extracts the heart QRS complex
2. preprocessing.py -> filters the signal
3. regression.py -> Performs a regresion in the data, fit and prediction
4. clasification.py -> Performs Random Forest classification or a Suppor Vector Machine over the data.


