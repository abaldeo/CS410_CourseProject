
class DocumentLoader:
    @staticmethod
    def get_files(path: str, filetype: str = '.pdf') -> Iterator[str]:
        try:
            yield from [
                file_name for file_name in os.listdir(f'{path}')
                if file_name.endswith(filetype)
            ]
        except FileNotFoundError as e:
            print(f'\033[31m{e}')

    @staticmethod
    def load_documents(
        file: str,
        filetype: str = '.pdf'
    ) -> Union[CSVLoader, Docx2txtLoader, PyMuPDFLoader, TextLoader]:
        """Loading PDF, Docx, CSV"""
        try:
            if filetype == '.pdf':
                loader = PyMuPDFLoader(file)
            elif filetype == '.docx':
                loader = Docx2txtLoader(file)
            elif filetype == '.csv':
                loader = CSVLoader(file, encoding='utf-8')
            elif filetype == '.txt':
                loader = TextLoader(file, encoding='utf-8')

            return loader.load()

        except Exception as e:
            print(f'\033[31m{e}')
            return []

    @staticmethod
    def split_documents(
        document: Union[CSVLoader, Docx2txtLoader, PyMuPDFLoader, TextLoader],
        chunk_size: int=500,
        chunk_overlap: int=20
    ) -> list:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        return splitter.split_documents(document)



from typing import List, Optional


class CleanTextLoader(TextLoader):
    """Load text files."""

    def __init__(self, file_path: str, encoding: Optional[str] = None):
        """Initialize with file path."""
        self.file_path = file_path
        self.encoding = encoding

    def load(self) -> List[Document]:
        """Load from file path."""
        with open(self.file_path, encoding=self.encoding) as f:
            text = f.read()
        text = self.clean_text(text)
        metadata = {"source": self.file_path}
        return [Document(page_content=text, metadata=metadata)]

    @staticmethod
    def clean_text(text):
        lines = (line.strip() for line in text.splitlines())
        text = " ".join(iter(lines))
        text = " ".join(text.split())
        text = "\n".join((line for line in text.splitlines() if line.strip()))
        return text