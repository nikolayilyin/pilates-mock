import datetime
import os
import pathlib
import time
import traceback

import yaml


def log(text):
    print(f"{str(datetime.datetime.now())} INFO - {text}", flush=True)


def log_header(header):
    print("#############################################")
    print(f"# {header} #")
    print("#############################################", flush=True)


def finish_step(stage, year, delay_seconds):
    log(f"Imitating processing of step by sleeping for '{delay_seconds}' sec.")
    time.sleep(delay_seconds)
    if year:
        log(f"Completed MOCK.WorkflowStage.{stage} of {year}")
    else:
        log(f"Completed MOCK.WorkflowStage.{stage}")


def create_files(parent_folder, list_of_files, params):
    base_output = params['base_output']
    folder = pathlib.Path(base_output) / parent_folder
    folder.mkdir(parents=True, exist_ok=True)
    log(f"Created folder '{folder}'")
    for file_name in list_of_files:
        full_file_path = (folder / file_name).resolve()
        file_mode = "a+" if full_file_path.exists() else "w+"
        with open(full_file_path, file_mode) as file:
            a_record = f"this MOCK record written at {str(datetime.datetime.now())}\n"
            file.write(a_record)


def do_activitysim_step(year, params):
    log_header("MOCK: RUNNING ACTIVITYSIM")
    create_files("pilates/activitysim",
                 ["persons_in_root.txt", "households_in_root.txt", "skims_in_root.txt"],
                 params)
    create_files("pilates/activitysim/data",
                 ["persons.csv", "households.csv", "skims.csv", "SkimS.csv"],
                 params)
    create_files("pilates/activitysim/output",
                 ["final_something.txt", "final_something_else.txt", "PIPEline.h5.txt", "pipeLINE.h5.txt"],
                 params)
    for iteration in ["1", "2", "3", "4"]:
        create_files(f"pilates/activitysim/output/year-{year}-iteration-{iteration}",
                     [
                         "final_something.txt", "final_something_else.txt", "plans.txt", "pLANs.txt", "persons.txt"
                     ],
                     params)
    delay = params['step_delay_seconds']
    finish_step(stage="ActivitySim", year=year, delay_seconds=delay)


def do_beam_step(sim_city, year, params):
    log_header("MOCK: RUNNING BEAM")
    for iteration in ["1", "2", "3", "4"]:
        beam_base_path = f"pilates/beam/beam_output/{sim_city}/year-{year}-iteration-{iteration}"
        create_files(beam_base_path,
                     ["beam_output_file_1.txt", "beam_output_file_2.txt"],
                     params)
        create_files(beam_base_path + "/ITERS/it.0",
                     [
                         "beam_output_file_3.txt", "beam_output_FILE_3.txt",
                         "BEAM_output_file_3.txt", "beam_output_file_4.txt"
                     ],
                     params)
    delay = params['step_delay_seconds']
    finish_step(stage="BEAM", year=year, delay_seconds=delay)


def do_urbansim_step(year, params):
    log_header("MOCK: RUNNING URBANSIM")
    create_files(f"pilates/urbansim/output/year-{year}",
                 [
                     "urbansim-RESULTS.txt", "URBANSIM-results.txt", "URBANsim-results.txt", "urbanSIM-results.txt"
                 ],
                 params)
    delay = params['step_delay_seconds']
    finish_step(stage="Urbansim", year=year, delay_seconds=delay)


def do_postprocessing_step(years, params):
    log_header("MOCK: RUNNING POSTPROCESSING")
    create_files(f"pilates/postprocessing/output", ["a_post_process_result.txt"], params)
    for year in years:
        create_files(f"pilates/postprocessing/MEP/{year}",
                     ["plans.txt", "persons.txt", "jobs.txt", "households.txt"],
                     params)
    delay = params['step_delay_seconds']
    finish_step(stage="postprocessing", year=None, delay_seconds=delay)


if __name__ == "__main__":
    try:
        settings_file_name = 'settings.yaml'
        with open(settings_file_name) as settings_file:
            settings = yaml.load(settings_file, Loader=yaml.FullLoader)

        log(f"Using following settings from '{settings_file_name}':")
        for k, v in settings.items():
            log(f"->>  '{k}': '{v}'")

        region = settings['region']
        sim_years = list(range(settings['start_year'], settings['end_year']))
        step_delay_seconds = settings['step_delay_seconds']

        dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        base_loc = os.path.expandvars(settings['output_directory'])
        run_name = settings['output_run_name']
        folder_name = "{0}-{1}-{2}".format(settings['region'], run_name, dt)
        folder_path = os.path.join(base_loc, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        settings['base_output'] = folder_path
        log("The output folder is {0}".format(folder_path))

        log(f"Going to run pilates for city {region}, years {sim_years}")
        for sim_year in sim_years:
            log_header(f"PROCESSING YEAR {sim_year}")
            do_activitysim_step(sim_year, settings)
            do_urbansim_step(sim_year, settings)
            do_beam_step(region, sim_year, settings)

        do_postprocessing_step(sim_years, settings)
        log("Finished")

    except Exception as err:
        traceback.print_exc()
        log(f"Exception during execution: {str(err)}")
