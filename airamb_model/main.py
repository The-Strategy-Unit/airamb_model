# In this module we'll run the experiment

from airamb_model.trial import Trial


def main():
    print("Starting trial")

    # Create a new trial
    my_trial = Trial()

    # Run the trial
    my_trial.run_trial()

    print("Trial completed")


if __name__ == "__main__":
    main()
