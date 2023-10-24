from dataclasses import dataclass

@dataclass
class Job:
    names: list[str]
    job: callable
    depends_on: list[str] = None
    children: list['Job'] = None

    async def run(self):
        try:
            result = await self.job()
            return result
        except Exception as e:
            print(e)
            return False

    def __repr__(self):
        return f"{self.names}, {self.job}"
