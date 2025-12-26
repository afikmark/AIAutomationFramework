from pydantic import BaseModel, Field
from requests import Response
from typing import Optional


class Category(BaseModel):
    """Category model for pets"""

    id: int = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")


class Tag(BaseModel):
    """Tag model for pets"""

    id: int = Field(..., description="Tag ID")
    name: str = Field(..., description="Tag name")


class PetStoreAddPetRequest(BaseModel):
    """Request model for adding a new pet to the store"""

    id: Optional[int] = Field(
        None, description="Pet ID (auto-generated if not provided)"
    )
    category: Optional[Category] = Field(None, description="Pet category")
    name: str = Field(..., description="Pet name")
    photoUrls: list[str] = Field(..., description="Array of photo URLs")
    tags: Optional[list[Tag]] = Field(None, description="Array of tags")
    status: Optional[str] = Field(
        "available", description="Pet status: available, pending, or sold"
    )


class PetStoreAddPetResponse(BaseModel):
    """Response model for adding a new pet"""

    id: int = Field(..., description="Pet ID")
    category: Optional[Category] = Field(None, description="Pet category")
    name: str = Field(..., description="Pet name")
    photoUrls: list[str] = Field(..., description="Array of photo URLs")
    tags: Optional[list[Tag]] = Field(None, description="Array of tags")
    status: str = Field(..., description="Pet status")

    @classmethod
    def from_response(cls, response: Response) -> "PetStoreAddPetResponse":
        """Create response model from requests.Response object"""
        return cls.model_validate_json(response.text)


class PetStoreGetPetResponse(BaseModel):
    """Response model for getting a pet by ID"""

    id: int = Field(..., description="Pet ID")
    category: Optional[Category] = Field(None, description="Pet category")
    name: str = Field(..., description="Pet name")
    photoUrls: list[str] = Field(..., description="Array of photo URLs")
    tags: Optional[list[Tag]] = Field(None, description="Array of tags")
    status: str = Field(..., description="Pet status")

    @classmethod
    def from_response(cls, response: Response) -> "PetStoreGetPetResponse":
        """Create response model from requests.Response object"""
        return cls.model_validate_json(response.text)


class PetStoreDeletePetResponse(BaseModel):
    """Response model for deleting a pet"""

    code: int = Field(..., description="Response code")
    type: str = Field(..., description="Response type")
    message: str = Field(..., description="Response message")

    @classmethod
    def from_response(cls, response: Response) -> "PetStoreDeletePetResponse":
        """Create response model from requests.Response object"""
        return cls.model_validate_json(response.text)
