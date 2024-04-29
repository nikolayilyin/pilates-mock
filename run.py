import datetime
import pathlib
import time
import traceback

city = "sf-bay"
sim_years = [2077, 2078, 2079]
finish_step_delay_seconds = 1


def log(text):
    print(f"{str(datetime.datetime.now())} {text}")


def finish_step(stage, year):
    log(f"Imitating processing of step by sleeping for '{finish_step_delay_seconds}' sec.")
    time.sleep(finish_step_delay_seconds)
    if year:
        log(f"INFO - Completed MOCK.WorkflowStage.{stage} of {year}")
    else:
        log(f"INFO - Completed MOCK.WorkflowStage.{stage}")


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
    create_files("pilates/activitysim/data",
                 ["persons.txt", "households.txt", "skims.txt"])
    create_files("pilates/activitysim/output",
                 ["final_something.txt", "final_something_else.txt", "pipeline.h5.txt"])
    for iteration in ["1", "2", "3", "4"]:
        create_files(f"pilates/activitysim/output/year-{year}-iteration-{iteration}",
                     ["final_something.txt", "final_something_else.txt", "plans.txt", "persons.txt"])
    finish_step(stage="ActivitySim", year=year)


def do_beam_step(year=2077):
    for iteration in ["1", "2", "3", "4"]:
        beam_base_path = f"pilates/beam/beam_output/{city}/year-{year}-iteration-{iteration}"
        create_files(beam_base_path, ["beam_output_file_1.txt", "beam_output_file_2.txt"])
        create_files(beam_base_path + "/ITERS/it.0", ["beam_output_file_3.txt", "beam_output_file_4.txt"])
    finish_step(stage="BEAM", year=year)


def do_urbansim_step(year=2077):
    create_files(f"pilates/urbansim/output/year-{year}", ["urbansim-results.txt"])
    finish_step(stage="Urbansim", year=year)


def do_postprocessing_step(years):
    create_files(f"pilates/postprocessing/output", ["a_post_process_result.txt"])
    for year in years:
        create_files(f"pilates/postprocessing/MEP/{year}",
                     ["plans.txt", "persons.txt", "jobs.txt", "households.txt"])
    finish_step(stage="Urbansim", year=None)


if __name__ == "__main__":
    try:
        log(f"Going to run pilates for city {city}, years {sim_years}")
        for sim_year in sim_years:
            log(f"Processing year {sim_year}")
            do_activitysim_step(sim_year)
            do_urbansim_step(sim_year)
            do_beam_step(sim_year)

        do_postprocessing_step(sim_years)
        log("Finished")

    except Exception as err:
        traceback.print_exc()
        log(f"Exception during execution: {str(err)}")
