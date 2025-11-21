from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List
from enum import Enum


class Category(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: Optional[int] = None
    name: Optional[str] = None


class Tags(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: int
    category: Optional[Category] = None
    name: Optional[str] = None
    photoUrls: List[str] = Field(default_factory=list)
    tags: List[Tags] = Field(default_factory=list)
    status: Optional[str] = None

    @field_validator('photoUrls', mode='before')
    @classmethod
    def validate_photo_urls(cls, v):
        if v is None:
            return []
        return v

    @field_validator('tags', mode='before')
    @classmethod
    def validate_tags(cls, v):
        if v is None:
            return []
        return v

    def dict(self, **kwargs):
        """Для обратной совместимости"""
        return super().model_dump(exclude_none=True, **kwargs)


class PetMessage(BaseModel):
    code: Optional[int]
    type: Optional[str]
    message: Optional[str]
