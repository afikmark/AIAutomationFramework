from pydantic import BaseModel, Field
from requests import Response


class PetStoreUserCreateRequest(BaseModel):
    id: int = Field(..., description="Unique identifier for the user")
    username: str = Field(..., description="The username for the user")
    firstName: str = Field(..., description="The first name of the user")
    lastName: str = Field(..., description="The last name of the user")
    email: str = Field(..., description="The email address of the user")
    password: str = Field(..., description="The password for the user")
    phone: str = Field(..., description="The phone number of the user")
    userStatus: int = Field(..., description="The status of the user")


class PetStoreUserCreateResponse(BaseModel):
    code: int = Field(..., description="Response code")
    type: str = Field(..., description="Response type")
    message: str = Field(..., description="Response message")

    @classmethod
    def from_response(cls, response: Response) -> "PetStoreUserCreateResponse":
        """Create a PetStoreUserCreateResponse from a requests.Response object

        Args:
            response: The requests.Response object

        Returns:
            PetStoreUserCreateResponse instance
        """
        return cls.model_validate_json(response.text)
