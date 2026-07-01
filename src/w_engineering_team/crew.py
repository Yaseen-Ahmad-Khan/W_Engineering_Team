from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from .tools.custom_tool import ( write_file,
    read_file,
    list_directory,
    create_folder,
    run_command)

# Configure LLM globally with retry logic and disabled safety settings to avoid rate limits and blocks
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

default_llm = LLM(
    model=os.environ.get("MODEL"),
    api_key=os.environ.get("your_api_key"),
    num_retries=5,
    safety_settings=safety_settings
)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class WEngineeringTeam():
    """WEngineeringTeam crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def lead_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_engineer"],
            llm=default_llm,
            max_rpm=3,
            verbose=True
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["frontend_engineer"],
            tools=[write_file, read_file, list_directory, create_folder, run_command],
            llm=default_llm,
            max_rpm=3,
            verbose=True
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["backend_engineer"],
            tools=[write_file, read_file, list_directory, create_folder, run_command],
            llm=default_llm,
            max_rpm=3,
            verbose=True
        )

    @agent
    def qa_tester(self) -> Agent:
        return Agent(
            config=self.agents_config["qa_tester"],
            tools=[read_file, list_directory, run_command],
            llm=default_llm,
            max_rpm=3,
            verbose=True
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["planning_task"],
            output_file="outputs/engineering_plan.md",
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config["frontend_task"],
        )

    @task
    def backend_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_task"],
        )

    @task
    def testing_task(self) -> Task:
        return Task(
            config=self.tasks_config["testing_task"],
            output_file="outputs/qa_report.md",
        )
    @crew
    def crew(self) -> Crew:
        """Creates the WEngineeringTeam crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
