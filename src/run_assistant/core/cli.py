from run_assistant.core.cli_chat import CliChat
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts.prompt import PromptSession


class CliApp:
    def __init__(self, agent: CliChat) -> None:
        self.agent = agent
        self.resources = []
        self.prompts = []

        self.history = InMemoryHistory()
        self.session = PromptSession(history=self.history)

    async def initialize(self):
        await self.refresh_resources()
        await self.refresh_prompts()

    async def refresh_resources(self):
        pass

    #     # try:
    #         self.resource = await self.agent.lis

    async def refresh_prompts(self):
        pass

    async def run(self):
        while True:
            try:
                user_input = await self.session.prompt_async("> ")
                if not user_input.strip():
                    continue

                response = await self.agent.run(user_input)

                print(f"\nResponse:\n{response}")

            except KeyboardInterrupt:
                break
