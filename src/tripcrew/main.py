import agentops
from loguru import logger
import os
from config.config import settings
import yaml
from crew import TripCrew


def dacrew(
        travelers_input: str
        ):
    """
    This function is the main function that will be used to run the crew.
    It will take in a travelers_input and return a result.
    Args:
        travelers_input: The input for the crew
    Returns:
        result: The result of the crew 
    """
    logger.info("\n\nWelcome to Trip Planner Crew\n\n")
    os.environ["SERPER_API_KEY"] = settings.serper_api_key

    # Define file paths for YAML configurations
    files = {   
        "agents": "config/agents.yaml",
        "tasks": "config/tasks.yaml",
        }

    # Load configurations from YAML files
    configs = {}
    for config_type, file_path in files.items():
        with open(file_path, "r") as file:
            configs[config_type] = yaml.safe_load(file)

    # Assign loaded configurations to specific variables
    agents_config = configs["agents"]
    tasks_config = configs["tasks"]

    # Initialize the TripCrew with the configuration
    agentops.init(
        api_key="703a78b8-2e98-4be3-9cca-29a572aec8dc",
        default_tags=["crew-trip-planner"],
    )

    trip_crew = TripCrew(
        travelers_input=travelers_input,
        model=settings.gemini_model,
        api_key=settings.gcp_key,
        agents_config=agents_config,
        tasks_config=tasks_config,
    )
    # Run the crew
    try:
        result = trip_crew.run()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    logger.info("## Here is you Trip Plan")
    logger.info(result)

    agentops.end_session("Success")

    return result


if __name__ == "__main__":
    dacrew()  
