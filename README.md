# Run2HTT_Combine
Central Repository for Combine Harvester models and running scripts

## Setup
This repository is designed to go in as a module, or just straight cloned into an existing CMS Combine Harvester respository. 
Please see [here](https://github.com/cms-analysis/CombineHarvester) for instructions on setting up the original respository. Once a Combine
Harvester repository has been setup, this repository can be set up with the following steps:

```
cd $CMSSW_BASE/src/CombineHarvester/
git clone https://github.com/aloeliger/Run2HTT_Combine
cd Run2HTT_Combine/
scram b
```

In addition many elements of this repository will look in a specific directory called "auxiliaries/shapes/" to find input. These directories
must be placed in the src directory of the current CMSSW environment. Create these directories with:

```
cd $CMSSW_BASE/src/
mkdir auxiliaries
cd auxiliaries/
mkdir shapes
```

## Contents

### bin

Contains models for individual years and channels. Each model is it's own seperate combine harvester code, named SMHTT[Year]_[Channel].cpp
Each of these models must be built before running, and all should have several common features. Each takes a number of running options, the first is the Output directorty to place the created card in,
passing -s will disable all shape uncertainties in the model for debugging, -e will disable the use of the embedded distribution and related uncertainties
, -b will disable the use of CombineHarvester's Bin-By-Bin uncertainties (please note, this option is default in RunCombineFits.py),
-g will disable STXS split ggH processes and only use an inclusive ggH distribution, and -q will disable STXS split qqh processes and 
will only use inclusive qqH processes. There is also an option called `--Categories` which takes any number of options
after it, and it will attempt to load these categories from the file. Each looks for a file named "smh[year][channel(mt,tt,etc.)].root" in the shapes folder to run on.
 
### interface

Contains the definitions of some helper classes and functions:

- `InputParserUtility.h`: contains the definition for a simple option parsing utility I found online. Use this to read options for models in /bin/
- `UtilityFunctions.h`: contains code for the helper function `AddShapeIfNotEmpty()`. Combine will throw errors if empty signal processes and shapes
are added (which can happen with low stats STXS bins in certain categories) so `AddShapeIfNotEmpty()` attempts to only add shapes if to 
processes if it can demonstrate at least one of distributions, up, down, or nominal is not empty.

### src

contains some source code used by helper functions.

### python

contains modules used by the master fit running script

- `SplitUncertainty.py`: This module contains a class which will mark up the datacard with groups and then calculate
the uncertainty of a measurement split into Unc=Statistics+Systematics+Bin-By-Bin errors.

- `ThreadManager.py`: This module contains a class which will create and manage threads for combine fits. Output when using this is created in text files in 
in the usual output directories.

### scripts

This directory largely contains one off scripts used for preparing certain aspects of the data cards before any expected fits are run:

(use `--help` to see options with these)

- `MergeStats.py`: A complicated algorithm I wrote to try merging low stats bins to end up with all bin uncertainties < 30%. It affects sensitivities
too much and so is no longer used, but contains some useful code.

- `PrepDecorrelatedCard.py`: A simple macro using regexes to try and make copies of distributions with year tags attached for use in correllating/decorrellating
shapes in combine harvester models. Has a `--TrimYears` option for removing the years from histograms, instead of 
adding them if necessary

- `SimpleMergeStats.py`: The now in use merging algorithm. It uses regexes to match categories and distributions, and simply halves the number
of bins the last three slices of the Zero Jet PTH 0-10 category, and in the last slice of the VBF PTH GE 200 Category

- `Smooth.py`: A simple shape smoothing tool used for smoothing out bad statistics in shape uncertainties. If it finds more than half the bins
of a slice are the same between up and nominal or down and nominal shapes, it smooths out the ncertaintiy over all bins. It takes a large number of 
arguments to make sure it has all the right bins and slices, please run with `--help` to see all required options.

### RunCombineFits.py

This is the main tool used for extracting expected fits. It takes a moderate number of options, use `--help` to see them in shell.

- Main Options
  - `--years` accepts 2016, 2017 and or 2018. Lists all years and models to be run as a part of this fit. Will attempt to make data cards 
  for all of these years.
  - `--channels` currently accepts mt (mu tau), et (e tau), or tt (tau tau) and defines the channels to make datacards
  and run models for
- Other Options
  - `--DisableCategoryFits` Disables fits done based on analysis categories, currently recommended for any measurement which goes across channels, or where the cards fed to combine don't contain similarly named directories.
  - `--RunShapeless` Disables shape uncertainties in all models.
  - `--RunWithBinByBin` Reenables bin by bin uncertainties in the code. This should be run with `--RunWithoutAutoMCStats`
  - `--RunWithoutAutoMCStats` Disables autoMCStats in the data cards.
  - `--RunInclusiveggH` Uses the inclusive ggH distribution, and does not attemp to do any STXS fitting
  - `--RunInclusiveqqH` Same as the above, but for qqH
  - `--ComputeSignificance` less used option, disables a large number of fits, and just attempts to compute the significance of the main
  inclusive workspace/fit
  - `--ComputeImpacts` Computes the impacts for the Inclusive POI
  - `--Timeout` Terminate combine commands after a certain amount of time
  - `--TimeoutTime` Sets the time for the `--Timeout` command. Default: 180s.
  - `--SplitUncertainties` Creates and calls an uncertainty splitter to make sure data cards are grouped in such a way that they can
   call the prototype uncertainty splits later. The splitter can try and split measurements into an `Unc=Stat+Syst+Bin-By-Bin` format.
  - `--SplitInclusive` The inclusive signal strength measurement will attempt to split the inlusive signal strength measurement. 
   Requires that `--SplitUncertainties` has been called.
   - `--SplitSignals` The splitter will attemp to measure the ggH,qqH,WH and ZH measurements split into `Unc=Stat+Syst+Bin-By-Bin`. 
   Requires that `--SplitUncertainties` has been called.
   - `--SplitSTXS` The splitter will attemp to measure the ggH and qqH STXS bin measurements split into `Unc=Stat+Syst+Bin-By-Bin`. 
   Requires that `--SplitUncertainties` has been called.
   - `--RunParallel` Runs major fits in parallel by creating threads for the fits. Output is dumped to the usual output area in text files labeled by parameter.
   = `--numthreads` Dictates the number of threads that `--RunParallel` is allowed to use to concserve system resources.
   Default: 12.
  
   To try and keep output seperate, and archived, and the main directory clean, each time this script is run, it will generate 
  a tag with the date, and a random string assigned to it. All output of the script can be found in HTT_Output (it will make this directory
  if it is not already present) in a directory called Output_[Date]_[String Tag].

  #### CategoryConfigurations.py
  This contains a few dictionaries in {"Category_Name":"Directory_Loaded_From_File"} format to define what categories the script will 
  look to try to load from the files. Please edit this if you are changing how the channels will run.

  #### EmbeddedConfiguration.py
  This contains year and channel combinations and whether the model will attempt to run using embedded distributions and uncertainties
  or not. Please modify this if your year and channel has embedded distributions available.
  
### sortingSTXS.py

This is kind of plug-in of RunCombineFits.py. 

If you save printed output of RunCombineFits.py as a file, `sortingSTXS.py` help you to print out limits in orgarnized table form.

For example, https://www.dropbox.com/s/a0ra91pwzol2pw5/2017.png?dl=0
![Sorted Output](https://uc1bd7e9de0cb96691611ad52484.previews.dropboxusercontent.com/p/thumb/AAj6sE9g34trO3k_R8BxL4G2wHhNuFXsCK_5jkCuLDKkC00lwX58Tk9oyThxUYOXZY1O11caOiiooUdczRJmXusF8mpQ1O0ID7cHk2xs6g20aBQ2igWSPDUx3gppFWnXir4m7ljVaqj82nfx0v3gCxxi5P7AhIHAt1iaYEy9yRYe6wk3u-i2LsSO5FnM2wCjlP-alhu9hOUQtx9WKAmwHLzDYdevnRz0Ow5R1kQTmOdkJgzUtzxryvkTUEqzZGfY6zAX6vU2pwMOw28FHCSQLu8ouIkKgUmuy5d1g1jmrsq4SdkAMDorpGEnOGp6bxI3tyyWAKGfF46ZRM8e1YhUR1V3pCTjJ6Z-5erbOf78EZjWE1EREt3V1oayUvLXyvRGbqiDUDWQFdGlPUuBwjlUYhn1cL8urWvyQtTuKJHdmNu9uUz-B22_ISNW1Qz07mM-6_AaJaMFTLNv5mOUpgQtq5p-PkOiOolYqqvBY9nKlLyNSw/p.png?fv_content=true&size_mode=5)

- How to run
  - Run `RunCombineFits.py` as usual but add `> outputTxtFile.txt` to save print. 
  - Extract limits lines only. `awk '/%/' outputTxtFile.txt > limitExtracted.txt`
  - To run the script, `python sortingSTXS.py limitExtracted.txt`


## Prefit plot code

- This is contained in 2 files: plotterFinal.py and varCfgPlotter.py.

- You only need to edit the FileMap in varCfgPlotter.py for running the code in your own workspaces. FileMap has the default locations where the code will look for input.

How to run :

 - Main Options
  - `--years` accepts 2016, 2017 and/or 2018.
  
  - `--channels` currently accepts mt (mu tau), et (e tau), em (e mu) or tt (tau tau)  
  
  -  `--inputFile` the path to the input root file that contains the hisograms. 

 
 - Other Options
  - `higgsSF` provides the Scale Factor for the SM-Higgs signals.  1 is default
  - `--prefix` provides prefix for TDirectory holding histograms such as 'prefit_' or postfin_'.  Default is ''
  - `--isLog`  1=TRUE, 0=FALSE. Do we want a log plot?
 
Example on how to run it: 

python plotterFinal.py --channel mt --year 2017 

(You will have to change the default address of the files stored in varCfgPlotter.py for above command to work. You may choose to provede `--inputFile` option in addition in which case you need not worry about varCfgPlotter.py)

## Usage

My typical workflow looks something like this: 

1. I make root files with distributions, that include STXS split and inclusive ggH and qqH distributions in them in case I want to run on inclusive 
or STXS split distributions for any reason.
2. Before they can be run on, these files must be Decorrellated.
3. Once the root files are properly prepared, they can be put in the auxiliaries/shapes/ directory.
4. Once all root files have been prepared this way, `RunCombineFits.py` can be used to extract expected uncertainties across all parameters

## Troubleshooting
### RunCombineFits broke and all my fits tell me that the workspace has problems and probably wasn't closed...

This can happen during the stage where `Text2Workspace.py` builds the final root workspace from text based cards. Python
is limited to a set amount of memory given to it by the system and the shell, and in very high memory required workspaces 
(STXS on full Run 2 for example) it can exceed this, in which case python itself segfaults when the C code it is based on 
allocates memory outside of its accepted range (With some dissapointingly un-verbose errors). At the moment, the best fix I have 
for this is to up the memory you are allocating to your processes using the built in `ulimit -s` command. I recommend caution with this.
I've seen this error for the default value of 8515, so I just doubled it to 17030, but I would imagine lower values work, in which case 
I recommend using that. The general process goes like so:
```
ulimit -s 17030
python RunCombineFits.py ...
```

## Adding your own code

All added models should be added to the bin directory and added into the buildfile. `RunCombineFits.py` can be modified to then run this model too, but it should
take all standard options I have mentioned here. This repository is not an exhaustive system by any means, so any improvements are welcome.

--Andrew Loeliger
