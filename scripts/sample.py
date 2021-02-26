from src.script_support import Script, ScriptEngine


@ScriptEngine.register
class Test(Script):
    def onLoad(self) -> None:
        pass

    def onUnload(self) -> None:
        pass

    def onCalled(self, *args, **kwargs) -> None:
        pass


@ScriptEngine.register
class ButtonTest(Script):
    def onLoad(self) -> None:
        pass

    def onUnload(self) -> None:
        pass

    def onCalled(self, *args, **kwargs) -> None:
        pass