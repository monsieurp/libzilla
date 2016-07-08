from string import Template

"""The RESTURLMaker class helps build URLs for the Bugzilla REST API."""


class RESTURLMaker:
    def __init__(self, url=''):
        self.url = url
        self.token = ''

    def make_login_url(self, username='', password=''):
        return Template('$url/login?login=$username&password=$password').substitute(
            url=self.url,
            username=username,
            password=password
        )

    def make_bug_url(self, token=True, bug_number=''):
        if token:
            t = Template('$url/bug?token=$token&id=$bug_number').substitute(
                url=self.url,
                token=self.token,
                bug_number=bug_number
            )
        else:
            t = Template('$url/bug/$bug_number').substitute(
                url=self.url,
                bug_number=bug_number
            )

        return t
