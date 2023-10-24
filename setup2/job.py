from dataclasses import dataclass
from typing import List

@dataclass
class Job:
    names: List[str]
    job: callable
    description: str
    depends_on: List[str] = None
    children: List['Job'] = None

    async def run(self):
        try:
            result = await self.job()
        except Exception as e:
            print(e)
            result = False
        return result

    def __repr__(self):
        return f"{self.names}, {self.job}"
