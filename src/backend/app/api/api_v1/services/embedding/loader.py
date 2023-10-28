
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
