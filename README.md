# Simsatool - Image+RPC generation from 3D scene

`Simsatool` is a python module for the generation of image-rpc pairs apt to be used in a satellite pipeline. The software was developed as part of the work published in:    
"llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll"

Available at [Link al paper]([https://ww](https://www.fing.edu.uy))  

***
## Requirements

### Simsatool requirements
To install requirements : 
	`pip install -r requirements.txt`

### rpcfit
The module uses this python package [rpcfit](https://github.com/centreborelli/rpcfit) to generate an RPC file from 3D-2D correspondences

### ponomarenko
The module uses this python package [ponomarenko](https://github.com/centreborelli/ponomarenko/tree/master/ponomarenko) to estimate the noise of an image


### Blender

The rendering of the views is done using Blender. An instalation of [Blender](https://www.blender.org/) version >= 2.8 is neccesary. The `blender` command should be available to be called in command line mode.

***
## Usage

To see the usage and test the tool: `python usage.py`  
This example creates two images and the respective RPC files for two views of a 3D scene. It also creates a configuration file to run a stereo reconstruction of the stereo pair on the S2P pipeline.

The **data** folder contains datasets for the test in `usage.py`


***
## How to cite
If you find this software useful please cite:

    @inproceedings{XXXXXXX,
      title={aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa},
      author={bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb},
      booktitle={ccccccccccccccccccccccccccccccccccccccccc},
      pages={ddddddddddddddddd},
      year={2022}
    }