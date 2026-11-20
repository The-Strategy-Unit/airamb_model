import pandas as pd
from airamb_model.model import Model, g

# This represents a batch of simulation runs, and will contain methods to run a batch of runs, as well as store, record and display results from the trial.


class Trial:
    # We will store the key results from each run against run number, with run number as the index.
    def __init__(self):
        self.df_trial_results = pd.DataFrame()
        self.df_trial_results["Run Number"] = [0]
        self.df_trial_results["Number of Jobs"] = [0]
        self.df_trial_results["Proportion of Jobs Conveyed"] = [0.0]
        self.df_trial_results["Proportion of Jobs Stood Down"] = [0.0]
        self.df_trial_results["Average Job Cycle Time"] = [0.0]
        self.df_trial_results.set_index("Run Number", inplace=True)

    # Print the trial results dataframe to the console
    def print_trial_results(self):
        print("Trial Results")
        print(self.df_trial_results)

    # Run a trial
    def run_trial(self):
        # Run the simulation for the number of runs specified in g class.
        # For each run, we create a new instance of the Model class and call its
        # run method, which sets everything else in motion.  Once the run has
        # completed, we grab out the stored run results and store it against
        # the run number in the trial results dataframe.
        for run in range(g.number_of_runs):
            my_model = Model(run)
            my_model.run()

            self.df_trial_results.loc[run] = [
                my_model.number_of_jobs,
                my_model.proportion_conveyed,
                my_model.proportion_stood_down,
                my_model.average_job_cycle_time,
            ]

        # Once the trial (ie all runs) has completed, print the final results
        self.print_trial_results()
