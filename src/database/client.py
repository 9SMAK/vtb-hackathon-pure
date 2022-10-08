from src.api.schemas import SqlReturn


class PSqlClient:
    def dummy_return(self, username: str) -> SqlReturn:
        return SqlReturn(username=username, value=42)


PSQL_CLIENT = PSqlClient()
