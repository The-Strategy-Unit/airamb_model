class Emergency_Job:
    def __init__(self, job_id):
        self.job_id = job_id

        # Note: None is a special built-in constant in Python that represents the absence of a value or a null value.
        self.patient_conveyed = None
        self.job_stood_down = None
        self.job_cycle_time = None
