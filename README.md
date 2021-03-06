# PyroRPC
PyroRPC is a Discord's Rich Presence client built with Python.

## Features
### 1. Discord Rich Presence
PyroRPC is a Discord's Rich Presence client. 
You can apply custom rich presences on your discord profile.

![example](resources/previews/rich_presence.png)
### 2. GUI based application (WIP)
PyroRPC is GUI-based application, so users can easily interact with it.

### 3. Script features (Beta)
PyroRPC supports scripting with Python, which help users to implement fully customized features on there Rich Presense!

```python
from src.script_support import Script, ScriptEngine

@ScriptEngine.register
class Test(Script):
    def onLoad(self) -> None:
        print('Script is loaded :)')

    def onUnload(self) -> None:
        print('Script is unloaded :(')
```

