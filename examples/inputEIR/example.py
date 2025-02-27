#!/usr/bin/env python3

import pathlib  # for a join
from functools import \
    partial  # for setting Run_Number. In Jonathan Future World, Run_Number is set by dtk_pre_proc based on generic param_sweep_value...

# idmtools ...
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment

# emodpy
import emodpy.emod_task as emod_task
from emodpy.utils import EradicationBambooBuilds
from emodpy.bamboo import get_model_files

import manifest


# ****************************************************************
# This is an example template with the most basic functions
# which create config and demographics from pre-set defaults
# and adds one intervention to campaign file. Runs the simulation
# and writes experiment id into experiment_id
#
# ****************************************************************


def build_campaign():
    """
        Creating a campaign file with an InputEIR intervention in it
    Returns:
        campaign object
    """

    import emod_api.campaign as campaign
    from emodpy_malaria.interventions.inputeir import add_scheduled_input_eir

    # we need to give the campaign the schema path, so it can check our campaign format
    campaign.set_schema(manifest.schema_file)

    # this creates a scheduled campaign with InputEIR intervention and adds it, after creating, to campaign.json file
    monthly_eir = [21, 234, 535, 687, 874, 761, 513, 459, 371, 51, 45, 3]
    add_scheduled_input_eir(campaign=campaign, start_day=33, monthly_eir=monthly_eir,
                            age_dependence="SURFACE_AREA_DEPENDENT",
                            node_ids=None)
    # using Daily_EIR parameter. You can use monthly or daily, not both
    daily_eir = [x for x in range(365)]
    add_scheduled_input_eir(campaign=campaign, start_day=3, daily_eir=daily_eir, age_dependence="OFF",
                            node_ids=None)

    return campaign


def set_config_parameters(config):
    """
    This function is a callback that is passed to emod-api.config to set parameters The Right Way.
    """
    # You have to set simulation type explicitly before you set other parameters for the simulation
    # sets "default" malaria parameters as determined by the malaria team
    import emodpy_malaria.malaria_config as malaria_config
    config = malaria_config.set_team_defaults(config, manifest)
    malaria_config.add_species(config, manifest, ["gambiae"])
    config.parameters.Simulation_Duration = 80

    return config


def build_demographics():
    """
    Build a demographics input file for the DTK using emod_api.
    Right now this function creates the file and returns the filename. If calling code just needs an asset that's fine.
    Also right now this function takes care of the config updates that are required as a result of specific demog
    settings. We do NOT want the emodpy-disease developers to have to know that. It needs to be done automatically in
    emod-api as much as possible.

    """
    import emodpy_malaria.demographics.MalariaDemographics as Demographics  # OK to call into emod-api

    demographics = Demographics.from_template_node(lat=0, lon=0, pop=10000, name=1, forced_id=1)
    return demographics


def general_sim():
    """
        This function is designed to be a parameterized version of the sequence of things we do
    every time we run an emod experiment.
    Returns:
        Nothing
    """

    # Set platform
    # use Platform("SLURMStage") to run on comps2.idmod.org for testing/dev work
    platform = Platform("Calculon", node_group="idm_48cores", priority="Highest")

    experiment_name = "InputEIR_example"

    # create EMODTask
    print("Creating EMODTask (from files)...")
    task = emod_task.EMODTask.from_default2(
        config_path="config.json",
        eradication_path=manifest.eradication_path,
        campaign_builder=build_campaign,
        schema_path=manifest.schema_file,
        ep4_custom_cb=None,
        param_custom_cb=set_config_parameters,
        demog_builder=build_demographics
    )
    
    # set the singularity image to be used when running this experiment
    task.set_sif(manifest.sif_path)
    
    # We are creating one-simulation experiment straight from task.
    # If you are doing a sweep, please see sweep_* examples.
    experiment = Experiment.from_task(task=task, name=experiment_name)

    # The last step is to call run() on the ExperimentManager to run the simulations.
    experiment.run(wait_until_done=True, platform=platform)

    # Check result
    if not experiment.succeeded:
        print(f"Experiment {experiment.id} failed.\n")
        exit()

    print(f"Experiment {experiment.id} succeeded.")

    # Save experiment id to file
    with open("experiment_id", "w") as fd:
        fd.write(experiment.id)


if __name__ == "__main__":
    import emod_malaria.bootstrap as dtk
    import pathlib

    dtk.setup(pathlib.Path(manifest.eradication_path).parent)
    general_sim()
