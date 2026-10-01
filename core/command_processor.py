from skills import greeting


class CommandProcessor:
    def __init__(self):
        # Ordered list of skills. First skill to return a non-None
        # response wins. More skills get appended here later.
        self.skills = [greeting]

    def process(self, command):
        command = command.lower().strip()

        for skill in self.skills:
            response = skill.handle(command)
            if response is not None:
                return response

        # Fallback if no skill matched
        return f"I heard you say: {command}"