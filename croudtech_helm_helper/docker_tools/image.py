class Repository:
    def __init__(self, repository):
        self.client_args = self._get_client_args()
        pass

    def _get_client_args(self):
        pass

    def check_for_image(self, git_commit_ref):

        pass

    def client(self):
        if not hasattr(self, "_client"):
            self._client = DockerRegistryClient(**self.client_args)

        return self._client
