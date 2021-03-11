from typing import Tuple

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

    def getHWStatus(self) -> Tuple[float, float]:
        cpu = round(psutil.cpu_percent())
        ram = round(psutil.virtual_memory().percent, 1)
        return cpu, ram

    def onStart(self) -> None:
        print('Hello world from Script[HWStatus]!')
        print(self.client)

    def onClose(self) -> None:
        pass

    def onLoad(self, profile) -> None:
        cpu, ram = self.getHWStatus()
        profile.state = profile.state.format(cpu=cpu, ram=ram)

    def onUnload(self, profile) -> None:
        pass

    def onReload(self, profile) -> None:
        cpu, ram = self.getHWStatus()
        # TODO : state가 초기에 값이 바뀐 이후로 foramt 문자열이 사라져 더이상 변경이 불가함. 문제 해결을 위한 대책 필요.
        print(profile.state)    # TODO : Support wildcard values for profile objects : keep wildcard expression, but send formatted data.
        text: str = profile.state.format(cpu=cpu, ram=ram)
        print(f'text={text}')
        profile.state = text
        self.client.logger.info(f'Script > sample.HWStatus > cpu={cpu},ram={ram}')

    def onUpdate(self, profile) -> None:
        pass

