import random

import pandas as pd
import simpy

from airamb_model.entity import Emergency_Job


class g:
    time_units_between_calls = 10
    mean_job_cycle_time = 2
    mean_job_cycle_time_conveyance = 3
    mean_job_cycle_time_stood_down = 1
    probability_of_conveyance = 0.7
    probability_of_stand_down = 0.2
    number_of_air_ambulances = 3
    sim_duration = 1000
    number_of_runs = 2


class Model:
    # Constructor to set up the model for a run.  We pass in a run number when we create a new model.
    def __init__(self, run_number):
        self.env = simpy.Environment()

        # create a counter for how many emergency jobs we've done - this can be used as a unique job ID for each new job
        self.job_counter = 0

        # now we'll create a resource to represent the air ambulances.  We'll create a resource with a capacity equal to the number of air ambulances we have (which we set in the g class).
        self.air_ambulances = simpy.Resource(
            self.env, capacity=g.number_of_air_ambulances
        )

        # store the run number in the model so we can use it later for reporting
        self.run_number = run_number

        # create a Pandas DataFrame to store the results of this run. We'll use the job_id as the index so we can easily look up the results for a specific job later.
        self.results_df = pd.DataFrame(
            columns=[
                "job_id",
                "patient_conveyed",
                "job_stood_down",
                "job_cycle_time",
            ]
        )
        self.results_df.set_index("job_id", inplace=True)

        # create an attribute to store key metrics for this run
        self.number_of_jobs = None
        self.proportion_conveyed = None
        self.proportion_stood_down = None
        self.average_job_cycle_time = None

    # Now we create a generator function to represent the arrival of emergency jobs.  This function will be called by the SimPy environment to create new emergency jobs at random intervals.
    def generator_emergency_job_arrival(self):
        # we want this to continue indefinitely, so we'll use a while loop that will only stop when the simulation ends.
        while True:
            # increment the job counter to create a new job ID
            self.job_counter += 1

            # create a new emergency job with the current job counter as the job ID
            new_job = Emergency_Job(self.job_counter)

            # now we want to start a process to handle this new emergency job.  We'll call a function called handle_emergency_job and pass in the new job as an argument.
            self.env.process(self.carry_out_emergency_job(new_job))

            # We'll use the random.expovariate function to generate a random number of minutes between calls, based on the mean time between calls that we set in the g class.
            inter_arrival_time = random.expovariate(1.0 / g.time_units_between_calls)

            # freeze this instance of the generator function for the amount of time we just calculated, so that the next emergency job will be created after that amount of time has passed.
            yield self.env.timeout(inter_arrival_time)

    # Now we create a function to represent the handling of an emergency job.  This function will be called by the generator function when a new emergency job is created.
    def carry_out_emergency_job(self, job):
        # we want to request an air ambulance from the resource we created earlier.  We'll use a with statement to request the resource, which will automatically release it when we're done.
        with self.air_ambulances.request() as request:
            # we'll yield the request, which will pause this process until an air ambulance is available.
            yield request

            # at this point the request for an air ambulance has been granted, so we can now simulate the time it takes to carry out the emergency job.
            # We'll use the random.expovariate function again to generate a random number of minutes based on the mean job cycle time that we set in the g class.
            # note that we assumed different mean job cycle times for different types of jobs so first we need to determine what type of job this is.
            # we'll use an if statement to do this and probabilities that were set in the g class.

            # first we'll check if the job was stood down on route
            if random.random() < g.probability_of_stand_down:
                job.job_cycle_time = random.expovariate(
                    1.0 / g.mean_job_cycle_time_stood_down
                )
                job.job_stood_down = True
                job.patient_conveyed = False
            # if the job was not stood down, we'll check if the patient was conveyed
            else:
                job.job_stood_down = False
                if random.random() < g.probability_of_conveyance:
                    job.job_cycle_time = random.expovariate(
                        1.0 / g.mean_job_cycle_time_conveyance
                    )
                    job.patient_conveyed = True
                else:
                    job.job_cycle_time = random.expovariate(1.0 / g.mean_job_cycle_time)
                    job.patient_conveyed = False

            # freeze this process for the amount of time we just calculated, to simulate the time it takes to carry out the emergency job.
            yield self.env.timeout(job.job_cycle_time)

            # finally, we'll add a row to our results DataFrame with the results of this emergency job.
            self.results_df.loc[job.job_id] = [
                job.patient_conveyed,
                job.job_stood_down,
                job.job_cycle_time,
            ]

    # we also want a function that will calculate our metrics of choice
    def calculate_run_results(self):
        self.number_of_jobs = len(self.results_df)
        self.proportion_conveyed = self.results_df["patient_conveyed"].mean()
        self.proportion_stood_down = self.results_df["job_stood_down"].mean()
        self.average_job_cycle_time = self.results_df["job_cycle_time"].mean()

    # finally, we want a function that will run the simulation
    def run(self):
        # start the generator function to create emergency jobs
        self.env.process(self.generator_emergency_job_arrival())

        # run the simulation for the duration we set in the g class
        self.env.run(until=g.sim_duration)

        # after the simulation is complete, we want to calculate our metrics of choice
        self.calculate_run_results()

        # Print the run number with the job-level results from this run of the model
        print(f"Run Number {self.run_number}")
        print(f"Number of Jobs: {self.number_of_jobs}")
        print(f"Proportion of Jobs Conveyed: {self.proportion_conveyed}")
        print(f"Proportion of Jobs Stood Down: {self.proportion_stood_down}")
        print(f"Average Job Cycle Time: {self.average_job_cycle_time}")
        print(self.results_df)
