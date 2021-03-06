class Pipeline:
    def __init__(self, name=None):
        self.name = name
        self.steps = []

    def add(self, func, desc=None):
        self.steps.append((func, desc))

    def execute(self):
        print('Running pipeline: "{}"'.format(self.name))

        prev_return_vals = None
        # Execute each step
        for (func, desc) in self.steps:
            # TODO: support wrapping certain steps in runtime environments like
            # supercomputer instead of executing directly
            print('- Executing step: "{}"'.format(self.name))

            if prev_return_vals is not None:
                prev_return_vals = func(prev_return_vals)
            else:
                prev_return_vals = func()


    # TODO: support waiting for supercomputer output