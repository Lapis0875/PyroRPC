import psutil

from src.script_support import Script, ScriptEngine


@ScriptEngine.register
class Test(Script):
    def __init__(self, client):
        super().__init__(client)

    def onStart(self) -> None:
        print('Hello world from Script[Test]!')

    def onLoad(self, profile) -> None:
        pass

    def onUnload(self, profile) -> None:
        pass

    def onCalled(self, *args, **kwargs) -> None:
        pass


@ScriptEngine.register
class ButtonTest(Script):
    def __init__(self, client):
        super().__init__(client)

    def onStart(self) -> None:
        print('Hello world from Script[ButtonTest]!')
        print(self.client)

    def onClose(self) -> None:
        pass

    def onLoad(self, profile) -> None:
        pass

    def onUnload(self, profile) -> None:
        pass

    def onClick(self, profile, button) -> None:
        pass


@ScriptEngine.register
class HWStatus(Script):
    def __init__(self, client):
        super().__init__(client)

    def onStart(self) -> None:
        print('Hello world from Script[HWStatus]!')
        print(self.client)

    def onClose(self) -> None:
        pass

    def onLoad(self, profile) -> None:
        cpu = round(psutil.cpu_percent())
        ram = round(psutil.virtual_memory().percent, 1)
        profile.state = profile.state.format(cpu=cpu, ram=ram)

    def onUnload(self, profile) -> None:
        pass

    def onUpdate(self, profile) -> None:
        pass

