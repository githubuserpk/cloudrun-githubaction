import google.auth
from google.auth.transport.requests import Request
from google.cloud import artifactregistry_v1
from google.api_core import exceptions

def delete_all_images(project_id, location, repository):
    """Delete all images in the specified Artifact Registry repository."""
    client = artifactregistry_v1.ArtifactRegistryClient()

    # The resource name of the repository.
    parent = f"projects/{project_id}/locations/{location}/repositories/{repository}"

    try:
        # List all Docker images
        request = artifactregistry_v1.ListDockerImagesRequest(parent=parent)
        page_result = client.list_docker_images(request=request)

        for image in page_result:
            print(f"Attempting to delete image: {image.name}")
            try:
                # Construct the correct package name
                package_name = f"projects/{project_id}/locations/{location}/repositories/{repository}/packages/{image.name.split('/')[-1].split('@')[0]}"
                client.delete_package(name=package_name)
                print(f"Successfully deleted image: {image.name}")
            except exceptions.GoogleAPICallError as e:
                print(f"Failed to delete image {image.name}: {e}")
                if hasattr(e, 'details'):
                    print(f"Error details: {e.details()}")

        print("Image deletion process completed.")
    except Exception as e:
        print(f"An error occurred while listing or deleting images: {e}")
        if hasattr(e, 'details'):
            print(f"Error details: {e.details()}")

if __name__ == "__main__":
    import os
    
    # Get these values from environment variables
    project_id = os.environ.get('PROJECT_ID')
    location = os.environ.get('LOCATION')
    repository = os.environ.get('REPOSITORY')

    if not all([project_id, location, repository]):
        print("Error: Missing required environment variables.")
        print(f"PROJECT_ID: {project_id}")
        print(f"LOCATION: {location}")
        print(f"REPOSITORY: {repository}")
        exit(1)

    delete_all_images(project_id, location, repository)
