import datetime
import pathlib
import time
import traceback

city = "sfbay-1-hour"
sim_years = list(range(2077, 2107))
finish_step_delay_seconds = 40


def log(text):
    print(f"{str(datetime.datetime.now())} INFO - {text}", flush=True)


def log_header(header):
    print("#############################################")
    print(f"# {header} #")
    print("#############################################", flush=True)


def finish_step(stage, year):
    log(f"Imitating processing of step by sleeping for '{finish_step_delay_seconds}' sec.")
    time.sleep(finish_step_delay_seconds)
    if year:
        log(f"Completed MOCK.WorkflowStage.{stage} of {year}")
    else:
        log(f"Completed MOCK.WorkflowStage.{stage}")


def create_files(parent_folder, list_of_files):
    folder = pathlib.Path(parent_folder)
    folder.mkdir(parents=True, exist_ok=True)
    log(f"Created folder '{folder}'")
    for file_name in list_of_files:
        full_file_path = (folder / file_name).resolve()
        file_mode = "a+" if full_file_path.exists() else "w+"
        with open(full_file_path, file_mode) as file:
            a_record = f"this MOCK record written at {str(datetime.datetime.now())}\n"
            file.write(a_record)


def do_activitysim_step(year=2077):
    log_header("MOCK: RUNNING ACTIVITYSIM")
    create_files("pilates/activitysim",
                 ["persons_in_root.txt", "households_in_root.txt", "skims_in_root.txt"])
    create_files("pilates/activitysim/data",
                 ["persons.csv", "households.csv", "skims.csv", "SkimS.csv"])
    create_files("pilates/activitysim/output",
                 ["final_something.txt", "final_something_else.txt", "PIPEline.h5.txt", "pipeLINE.h5.txt"])
    for iteration in ["1", "2", "3", "4"]:
        create_files(f"pilates/activitysim/output/year-{year}-iteration-{iteration}",
                     ["final_something.txt", "final_something_else.txt", "plans.txt", "pLANs.txt", "persons.txt"])
    finish_step(stage="ActivitySim", year=year)


def do_beam_step(year=2077):
    log_header("MOCK: RUNNING BEAM")
    for iteration in ["1", "2", "3", "4"]:
        beam_base_path = f"pilates/beam/beam_output/{city}/year-{year}-iteration-{iteration}"
        create_files(beam_base_path, ["beam_output_file_1.txt", "beam_output_file_2.txt"])
        create_files(beam_base_path + "/ITERS/it.0",
                     ["beam_output_file_3.txt", "beam_output_FILE_3.txt",
                      "BEAM_output_file_3.txt", "beam_output_file_4.txt"])
    finish_step(stage="BEAM", year=year)


def do_urbansim_step(year=2077):
    log_header("MOCK: RUNNING URBANSIM")
    create_files(f"pilates/urbansim/output/year-{year}",
                 ["urbansim-RESULTS.txt", "URBANSIM-results.txt", "URBANsim-results.txt", "urbanSIM-results.txt"])
    finish_step(stage="Urbansim", year=year)


def do_postprocessing_step(years):
    log_header("MOCK: RUNNING POSTPROCESSING")
    create_files(f"pilates/postprocessing/output", ["a_post_process_result.txt"])
    for year in years:
        create_files(f"pilates/postprocessing/MEP/{year}",
                     ["plans.txt", "persons.txt", "jobs.txt", "households.txt"])
    finish_step(stage="Urbansim", year=None)


if __name__ == "__main__":
    try:
        log(f"Going to run pilates for city {city}, years {sim_years}")
        for sim_year in sim_years:
            log_header(f"PROCESSING YEAR {sim_year}")
            do_activitysim_step(sim_year)
            do_urbansim_step(sim_year)
            do_beam_step(sim_year)

        do_postprocessing_step(sim_years)
        log("Finished")

    except Exception as err:
        traceback.print_exc()
        log(f"Exception during execution: {str(err)}")
