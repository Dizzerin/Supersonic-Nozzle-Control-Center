from abc import abstractmethod, ABC
import dearpygui.dearpygui as dpg
import helpers
from typing import Callable, Optional


class IWindow(ABC):
    def __init__(self):
        self._name = ""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def update(self) -> Optional["IWindow"]:
        pass


class ReadDataInterface:
    pass


class RecordingWindow(IWindow):
    def __init__(self, read: ReadDataInterface):
        self._read = read
        pass


class IFileSelector:
    def get_file_from_user(self, starting_dir: str):
        pass

class DearPyGuiSelector(IFileSelector):
    def __init__(self, parent_window):
        self._parent = parent_window

    def get_file_from_user(self, starting_dir: str):
        # I didn't look up how this works
        with self._parent:
            # probably maybe use Modal instead???
            dpg.add_file_dialog(directory_selector=True, show=True, )

class SelectRecordingFileUseCase:
    def __init__(self, selector: IFileSelector):
        self._selector = selector

    def get_file(self, base_path: str) -> str:
        file = self._selector.get_file_from_user(base_path)
        if file not exists:
            file.create()
        return file.name


class MainWindow(IWindow):
    def __init__(self):
        self._name = "MainWindow"
        self._next_window = None

    def get_name(self) -> str:
        return self._name

    def _change_window_callback(self):
        self._next_window = MainWindow()

    def show(self):
        with dpg.add_window(tag=self._name):
            dpg.add_text(label="Main Window")
            dpg.add_button(label="Change Window", callback=self._change_window_callback)

    @staticmethod
    def remove(self):
        dpg.delete_item(self.name())

    def update(self) -> Optional[IWindow]:
        if self._next_window is not None:
            return self._next_window
