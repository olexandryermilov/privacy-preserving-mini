git clone https://github.com/huggingface/transformers.git
cd transformers
pip3 install requirements.txt
pip3 install datasets
pip3 install evaluate
pip3 install rouge_score
pip3 install git+https://github.com/huggingface/transformers
pip3 install spacy
pip3 install torch
python3 -m spacy download en_core_web_sm
python3 -m spacy download de_core_news_sm