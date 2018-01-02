class Action(object):
    """The action base class.

    To create an action, create a subclass of `Action` with a descriprive
    docstring and override the `__call__` method.

    """
    def __init__(self, admin_only=False):
        self.admin_only = admin_only

    def __call__(self, schedule_entry_name, task_id):
        raise NotImplementedError("Implement action logic.")

    @property
    def summary(self):
        try:
            return self.description.splitlines()[0]
        except IndexError:
            return "Summary not provided."

    @property
    def description(self):
        return self.__doc__
