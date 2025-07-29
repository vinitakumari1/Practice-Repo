#write an program which will read the youtube video from - 
#and convert to small chunks and summarize it and save to txt file
#web url - pip install youtube-transcript-api



from youtube_transcript_api import YoutubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os


#Step 1 : Get the Youtube Transcript using YOUTUBE API
video_id = "X5xigVU5mLU"
output_file = "youtube_crawl_summary.txt"
transcript = YoutubeTranscriptApi.get_transcript(video_id)
video_text = "\n".join([t["text"]for t in transcript])
print("/n : Video text : {video_text}")


#step 2 : Split the text and get small chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 50
)

chunks=splitter.split_text(video_text)


