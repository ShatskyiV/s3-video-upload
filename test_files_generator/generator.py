import os
from test_files_generator.test_file import TestFile

class TestFileGenerator:
    def __init__(self, test_file: TestFile):
        self.test_file = test_file

    def generate(self):
        with self.test_file.path.open('wb') as tf:
            size_bytes = int(self.test_file.size_gb * 1024**3)
            tf.seek(size_bytes - 1)
            tf.write(b"\0")
