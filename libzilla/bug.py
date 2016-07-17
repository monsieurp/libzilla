class Bug:
    def __init__(self,
                 bug_number,
                 comment=None,
                 resolution=None,
                 status=None):

        self.bug_number = bug_number
        self.resolution = resolution
        self.status = status
        self.comment = comment

    def __str__(self):
        return """Bug #: [%s]
RESOLUTION: [%s]
STATUS: [%s]
Comment: %s""" % (
            self.bug_number,
            self.resolution,
            self.status,
            self.comment
        )
