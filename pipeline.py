import os

CACHE_DIR = "cachedData"


class Pipeline:
    def __init__(self):
        self.actions = []

    def add_action(self, action):
        """Add an action to the pipeline. The action must be a callable."""
        self.actions.append(action)
        return self  # Allows chaining

    def execute(self, config):
        """Execute all actions in the pipeline."""
        result = None
        for action in self.actions:
            result = action.run(config, result)
            if result is None:
                break
