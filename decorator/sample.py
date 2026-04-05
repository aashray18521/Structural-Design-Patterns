from abc import ABC, abstractclassmethod


# NOTE: This is Decorator DP. This is different from Python's @decorator syntax.
# This is an object Composition Pattern for adding behavior at runtime.

class DataSource(ABC):
    @abstractmethod
    def write_data(self, data: str) -> None:
        pass

    @abstractmethod
    def read_data(self) -> str:
        pass


class FileDataSource(DataSource):
    def __init__(self, filename: str):
        self.filename = filename

    def write_data(self, data: str) -> None:
        # write to file
        # return super().write_data(data)
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(data)
        return
    
    def read_data(self) -> str:
        # Read from file
        # return super().read_data()
        with open(self.filename, "r", encoding="utf-8") as f:
            return f.read()
    
class EncryptionDecorator(DataSource):
    def __init__(self, source: DataSource):
        self._wrapped = source
    
    def write_data(self, data: str) -> None:
        encrypted = self._encrypt(data)
        self._wrapped.write_data(encrypted) # Delegate to wrapped object
    def read_data(self) -> str:
        # return super().read_data()
        data = self._wrapped.read_data()
        return self._decrypt(data)
    
    def _encrypt(self, data: str) -> str:
        return f"encrypted : {data}"
    
    def _decrypt(self, data: str) -> str:
        return data.replace("encrypted:", "")
    
class CompressionDecorator(DataSource):
    def __init__(self, source: DataSource):
        self._wrapped = source
    
    def write_data(self, data) -> None:
        compressed = self._compressed(data)
        self._wrapped.write_data(compressed) # Delegate to wrapped object

    def read_data(self) -> str:
        data = self._wrapped.read_data()
        return self._decompress(data)
    
    def _compress(self, data: str) -> str:
        return f"compressed: {data}"
    
    def _decompress(self, data: str) -> str:
        return data.replace("compressed:", "")

   
## USAGE
source = FileDataSource("data.txt")
source = EncryptionDecorator(source)
source = CompressionDecorator(source)
source.write_data("sensitive info")

# Data gets compressed, then encrypted, then writted to file