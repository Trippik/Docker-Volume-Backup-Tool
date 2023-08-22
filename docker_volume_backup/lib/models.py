from pydantic import BaseModel

class VolumeBackup(BaseModel):
    name: str
    datetime: str