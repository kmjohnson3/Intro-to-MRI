# Intro-to-MRI
This is Jupyter notebook/python code developed for a UW-Madison introductory MRI class. The notebooks were made to support Google colab markdown but they should also open up in a standard jupyter enviroment. Most notebooks have a link on top of the page to allow you to open it directly from github. 

# Notebooks
1. [Intro to Bloch Solvers](NoteBooks/Intro_MRI_Bloch_Solvers.ipynb) : This notebooks introduces two ways to simulate the Bloch equations using either standard solvers or solvers assuming periods of free relaxation.
2. [Spoiled Gradient Echo](NoteBooks/Spoiled_Gradient_Echo.ipynb) : This notebook simulates spoiled gradient echo as a means to create contrast in images.
3. [Spin Echo](NoteBooks/Spin_Echo.ipynb) : This notebook simulates spin echo as a means to create contrast in images.
4. [Spatial Selective RF](NoteBooks/Selective_RF_Excitation.ipynb) : This uses sinc pulses to investigate the tradeoffs in RF pulse choices.
5. [Cartesian Sampling](NoteBooks/Simulated_Sampling.ipynb) : This uses fake data to examine undersampling and reconstruction.
6. [Cartesian Sampling Real Data](NoteBooks/Recon_Example.ipynb) : This uses real data to examine undersampling and reconstruction.
7. [Magnetics Field Generation](NoteBooks/Field_Generation.ipynb) : Code to create magnetic fields from loops of wire.

s
# Advanced Notebooks
1. [Variation Networks](AdvancedNoteBooks/VarNetToyExample.ipynb) : Toy example of using model based machine reconstruction to reconstruction images with reduced artifacts.
2. [Compressed Sensing](AdvancedNoteBooks/Constrained_Reconstruction_Demo.ipynb) : Example using parallel imaging and compressed SENSING

# Simulations 
1. [EPI Distortions](Simulations/epi_distortions.py) : Python code to simulate EPI distortions using brute force forward model with off-resonance. 
2. [Spiral Distortions](Simulations/spiral_distortions.py) : Python code to simulate spiral distortions using brute force forward model with off-resonance. 
3. [Complex Demodulation](Simulations/demodulation_example.py) : Python code which shows the basic steps to convert real valued detected signal to complex signal in the rotating frame.

