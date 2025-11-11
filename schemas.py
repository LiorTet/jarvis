from pydantic import BaseModel, Field

# LLM to identify command
class IdentifiedCommand(BaseModel):
    command: str = Field(description="The internal command/task identified from the user's speech, possible values: \
        ADD_TASK, LIST_TASKS, CLEAR_TASKS, UNRELATED")