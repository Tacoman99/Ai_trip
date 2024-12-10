from crewai import Agent,LLM,Task,Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from config.base_models import City_guide
from tools.google_places import GooglePlacesTool


class TripCrew:
  """
  A crew of agents to plan a trip
  """

  def __init__(
      self, 
      model: str, 
      api_key: str,
      inputs: dict,
      agents_config: dict,
      tasks_config: dict
      ):
    """
    Initialize the TripCrew

    Args:
      model: The model to use
      api_key: The API key to use
      inputs: The inputs for the crew
      agents_config: The configuration for the agents
      tasks_config: The configuration for the tasks

    Returns:
      result: The result of the crew
    """
    self.llm = LLM(model = model, api_key = api_key, timeout=30)
    self.model = model
    self.api_key = api_key
    self.inputs = inputs
    self.agents_config = agents_config
    self.tasks_config = tasks_config 

  def run(self):

    # Initialize the agents
    local_expert_agent = Agent(
      llm=self.llm,
      config=self.agents_config['local_expert_agent'],
      cache=True,
      tools=[SerperDevTool(), ScrapeWebsiteTool(), GooglePlacesTool()]
    )

    itinerary_agent = Agent(
      llm=self.llm,
      config=self.agents_config['itinerary_agent'],
    )
    

    # Initialize the tasks

    gather_task = Task(
      agent=local_expert_agent,
      config=self.tasks_config['gather_task'],
      output_json=City_guide
    )
    plan_task = Task(
      agent=itinerary_agent, 
      config=self.tasks_config['plan_task'],
      context=[gather_task]
    )

    crew = Crew(
      agents=[
         local_expert_agent, itinerary_agent
      ],
      tasks=[ gather_task, plan_task],
      verbose=True,
    )

    result = crew.kickoff(inputs=self.inputs)
    return result
