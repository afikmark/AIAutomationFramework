from pydantic import BaseModel, Field
from requests import Response


class PetStoreLoginRequest(BaseModel):
    username: str = Field(..., description="The username for login")
    password: str = Field(..., description="The password for login")


class PetStoreLoginResponse(BaseModel):
    code: int = Field(..., description="Response code")
    type: str = Field(..., description="Response type")
    message: str = Field(..., description="Response message")

    @classmethod
    def from_response(cls, response: Response) -> "PetStoreLoginResponse":
        """Create a PetStoreLoginResponse from a requests.Response object

        Args:
            response: The requests.Response object

        Returns:
            PetStoreLoginResponse instance
        """
        return cls.model_validate_json(response.text)
