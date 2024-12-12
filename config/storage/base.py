# Imports
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# Custom S3 Boto3 Storage
class CustomS3Boto3Storage(S3Boto3Storage):
    """Custom S3 Boto3 Storage.

    This class extends the S3 Boto3 Storage class to provide custom functionality.

    Extends:
        S3Boto3Storage

    Attributes:
        endpoint_url (str): The endpoint URL of the S3 bucket.
        custom_domain (str): The custom domain of the S3 bucket.

    Methods:
        url(name, parameters=None, expire=None): Get the URL of the file.
    """

    # Constructor
    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(**kwargs)

        # Set the endpoint URL and custom domain
        self.endpoint_url = settings.AWS_S3_ENDPOINT_URL
        self.custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

    # Method to return the URL of the file
    def url(
        self,
        name: str | None,
        parameters: dict | None = None,
        expire: int | None = None,
    ):
        """Get the URL of the file.

        This method returns the URL of the file.

        Args:
            name (str | None): The name of the file.
            parameters (dict | None): The parameters of the URL.
            expire (int | None): The expiry time of the URL.

        Returns:
            str: The URL of the file.
        """

        # Get the URL
        url = super().url(name, parameters, expire)

        # If the urls starts with https
        if url.startswith("https"):
            # Replace https with http
            url = "http" + url[5:]

        # Return the URL
        return url
