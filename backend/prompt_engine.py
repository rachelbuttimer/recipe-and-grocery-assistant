import sys
from pathlib import Path

# find root directory
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
  sys.path.insert(0, str(root_dir))

from prompt_templates.system_prompt import SYSTEM_PROMPT

def build(user_input: str, profile: dict) -> dict:
  return {
      "system_instruction": SYSTEM_PROMPT,
      "user_prompt": f"Profile: {profile}\nRequest: {user_input}",
  }