# Molecular Communication in Blood

This repository contains the evaluation and plotting code from the paper:

Lisa Y. Debus, Mario J. Wilhelm, Henri Wolff, Luiz C. P. Wille, Tim Rese, Michael Lommel, Jens Kirchner and Falko Dressler, "Blood Makes a Difference: Experimental Evaluation of Molecular Communication in Different Fluids," Proceedings of 9th Workshop on Molecular Communications (WMC 2025), Catania, Italy, April 2025.

> [!NOTE]
> This repository does not include the experimental data. To access the complete experimental dataset and replicate the results from the paper, download the zip file from the accompanying [Zenodo](https://zenodo.org/records/13898880) record and place the contents in the `data` directory.

## Description

The experimental appraisal of existing molecular communication (MC) testbeds and modeling frameworks in real blood is an important step for future Internet of bio-nano-things applications. 
In our paper, we experimentally compare the MC flow characteristics of water, blood substitute, and real porcine blood for a previously presented superparamagnetic iron oxide nanoparticles (SPION) MC testbed. 
This repository contains code to replicate our analysis of the system impulse response behavior of the testbed for the different fluids.
We provide code for our mathematical model and comparison to two existing theoretical SIR models for MC in blood.
Additionally, we provide the source code to replicate all figures from our paper.

## Usage

The directory `data processing` contains the Python scripts for the processing of the experimental data and comparison of the evaluated theoretical system impulse responses (SIRs).
The classes implementing the different SIRs can be found in `mathematical_models` and the necessary helper classes are available under `utils`.

The directory `plotting` contains the code to plot all figures from the paper and the supplementary information.

## Contact Information

Lisa Y. Debus, Telecommunication Networks Group (TKN) at the School of Electrical Engineering and Computer Science, TU Berlin

[![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github)](https://github.com/lyDebus)
[![Email](https://img.shields.io/badge/Email-email-D14836?logo=gmail&logoColor=white)](mailto:debus@ccs-labs.org)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Lisa-blue?logo=linkedin&style=flat-square)](https://www.linkedin.com/in/lisa-yvonne-debus-844876127/)
[![Website Badge](https://img.shields.io/badge/Website-Homepage-blue?logo=web)](https://www.tkn.tu-berlin.de/team/debus/)
