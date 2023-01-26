import dataclasses


@dataclasses.dataclass
class Config:
    dry_run: bool = False
    check: bool = False
    verbose: bool = False


config = Config()
