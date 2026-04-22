from dataclasse import dataclass, field
from enum import Enum
from typing import Callable, Dict

@dataclass
class StateMachine[G: Enum, S: Enum, s: Enum]:
	
