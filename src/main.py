import agentops
from loguru import logger
import os


if __name__ == "__main__":
  from ai_agents.config.config import config
  import yaml
  from crews import TripCrew

  logger.info("\n\nWelcome to Trip Planner Crew\n\n")
  os.environ["SERPER_API_KEY"] = config.serper_api_key


  # Define file paths for YAML configurations
  files = {
    'agents': '/home/jorger/travel-agent/ai-agents/config/agents.yaml',
    'tasks': '/home/jorger/travel-agent/ai-agents/config/tasks.yaml'
  }

  # Load configurations from YAML files
  configs = {}
  for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
      configs[config_type] = yaml.safe_load(file)

  # Assign loaded configurations to specific variables
  agents_config = configs['agents']
  tasks_config = configs['tasks']

  # Initialize the TripCrew with the configuration 
  agentops.init(api_key='703a78b8-2e98-4be3-9cca-29a572aec8dc', default_tags=["crew-trip-planner"])

  trip_crew = TripCrew( 
    inputs=config.inputs,
    model=config.gemini_model,
    api_key=config.gcp_key,
    agents_config=agents_config,
    tasks_config=tasks_config
  )

  # Run the crew
  try:  
    result = trip_crew.run()
  except Exception as e:
    # This is only necessary for AgentOps testing automation which is headless and will not have user input
    print("Stdin not implemented. Skipping run()")
    agentops.end_session("Indeterminate")

  logger.info("## Here is you Trip Plan")
  logger.info(result)
  
  agentops.end_session("Success")