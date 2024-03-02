from langchain.document_loaders import DirectoryLoader, TextLoader, UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from token_count import num_tokens_from_string
import re 
def analyze_text(text):
  return {
      'num_paragraph_per_doc': len(text.split('\n\n')),
      'num_words_per_doc': len(text.split()),
      'num_sentences_per_doc': len(re.split(r'(?<=[.!?]) +', text)),
      'num_lines_per_doc': len(text.splitlines()),
      'num_tokens_per_doc': num_tokens_from_string(text, "gpt4")
  }
  
directory_path = '/workspace/CS410_CourseProject/src/backend/data/transcripts/'
LOADER = DirectoryLoader(directory_path, glob="**/*txt", loader_cls=TextLoader, 
                                                             loader_kwargs={"encoding": "utf-8"}, use_multithreading=True,
                                                             show_progress=False)

  
# directory_path = '/workspace/CS410_CourseProject/src/backend/data/slides/'
# LOADER = DirectoryLoader(directory_path, glob="**/*pdf", loader_cls=UnstructuredPDFLoader, 
#                                                              loader_kwargs={}, use_multithreading=False,
#                                                              show_progress=True)

DOCUMENTS = LOADER.load()
print(len(DOCUMENTS))
stats = {
    "num_paragraph_per_doc": [],
    "num_words_per_doc": [],
    "num_sentences_per_doc": [],
    "num_lines_per_doc": [],
    "num_tokens_per_doc": [],
}
for doc in DOCUMENTS:
    text_stats = analyze_text(doc.page_content)
    for key, stat in stats.items():
        stat.append(text_stats[key])
avg_result = {f'avg_{key}': sum(values) / len(values) for key, values in stats.items()}
max_result = {f"max_{key}": max(values)  for key, values in stats.items()}
min_result = {f"min_{key}": min(values) for  key, values in stats.items()}

print(avg_result)
print(max_result)
print(min_result)

print(len(stats['num_words_per_doc']))

from app.api.api_v1.services.embedding.core import get_text_splitter, get_token_splitter, get_text_splitter2, chunk_docs

# splitter = get_text_splitter(separators = [".", "\n", "\n\n"], chunk_size=1000, chunk_overlap=200)
splitter = get_text_splitter2('gpt4', separators = ["\n\n", "\n", ".",])
# splitter = get_token_splitter('gpt4')
chunks = chunk_docs(DOCUMENTS, splitter)

chunk = chunks[0]
print(f'TOKEN COUNT {num_tokens_from_string(chunk.page_content, "gpt4")}')


data = [len(doc.page_content) for doc in chunks]
print(f'num chunk {len(chunks)}')
# print(f'chunk lens {data}')
print(f'avg chunk size {sum(data)/len(chunks)}')

import matplotlib.pyplot as plt
import numpy as np

# data= stats['num_tokens_per_doc']
# # Plot
# plt.figure(figsize=(12, 3))
# plt.plot(, linestyle = "None", marker="o")
# plt.title("Section lengths")
# plt.ylabel("# chars")

# # Save plot to PNG file
# plt.savefig("plot.png")


# import scipy
# # Calculate mean and standard deviation
# MU, SIGMA = np.mean(data), np.std(data)

# # Create histogram
# plt.hist(data, bins=50, density=True, alpha=0.6, color="g")

# # Create line plot of Gaussian distribution
# XMIN, XMAX = plt.xlim()
# X = np.linspace(XMIN, XMAX, 100)
# P = scipy.stats.norm.pdf(X, MU, SIGMA)
# plt.plot(X, P, "k", linewidth=2)

# plt.xticks(range(0, int(XMAX) + 1, 500))

# plt.xlabel("Token count")
# # plt.ylabel("P-value")
# # Save plot to PNG file
# plt.savefig("token_gauss.png")



plt.hist(data, bins=range(min(data), max(data), 250))
plt.xlabel("Doc chunk Count")
plt.ylabel("Frequency")
plt.xticks(range(0, max(data) , 500))

plt.savefig("doc_count.png")
