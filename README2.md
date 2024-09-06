# tfashion2.0 - A model to identify fashion-related words (hybrid approach)
- Remark:
  - BERT is generally better suited for sentence-level tasks rather than word-level classification.
  - A balanced dataset of fashion and non-fashion corpora is important
- hybrid approach: using BERT to classify the fashion relevance of larger segments (phrases or sentences) instead of individual words, followed by RAKE (keyword extraction technique) and a softer matching to filter out non-fashion words.

## Steps
1. Expand fashion corpus [topics_filtered.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/topics_filtered.csv) and non fashion-corpus (chinese wikipedia)
2. Fine-tune BERT on the fashion corpus [topics_filtered.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/topics_filtered.csv) for phrase-level or sentence-level classification.  
3. Classify the fashion-relatedness of each post in cleaned_post_text using BERT.  
4. Extract fashion-related keywords using RAKE from fashion-classified text.  
5. Apply softer matching only to fashion-related keywords.   
- Therefore, we filter out non-fashion words in the posts using the fashion corpus (the dictionary).

## Summary
- BERT is used at the sentence level to classify whether a text is fashion-related.
- RAKE is applied to extract keywords from the fashion-related sentences.
- Soft matching is applied to extracted fashion keywords.
  
## model performance
![Screenshot 2024-09-06 at 11 02 21](https://github.com/user-attachments/assets/871a5c75-6dac-4070-a981-8dd6f9e214e0)
- Number of fashion-related posts: 15277
- Number of non-fashion-related posts: 345
- Examples of 'non-fashion posts':
![Screenshot 2024-09-06 at 11 10 57](https://github.com/user-attachments/assets/f4f43533-3473-4693-bb7a-b41dab7e3ea8)
- Number of non-empty values in 'filtered_fashion_keywords':
- Examples of original post text:
  1. kk
  2. kk
  3. ll
- Examples of filtered post text:
  1. ll
  2. ll
  3. ll

#### Step 1.1 Expand fashion keyword list using RAKE (Rapid Automatic Keyword Extraction)
1. Tokenize the keyword group column to break down fashion phrases into individual words.
2. Apply RAKE to identify high-importance words from the tokenized text.
3. Expand the fashion keyword list by combining tokenized words and extracted keywords.
4. [topics0611_filtered.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/topics0611_filtered.csv) - 18,793 rows --> [topics_filtered.csv](https://github.com/dengxw66/Multimodal_MKT/blob/diandian_devlop/topics_filtered.csv) - 52,243 rows

#### Step 1.2 Get a non-fashion Chinese corpus
- Chinese Wikipedia Dump
- Use WikiExtractor to convert the XML dump into plain text
- Get extracted_texts
- Filter Non-Fashion Content from the Extracted Texts, using fashion keywords

#### Step 1.3 Prepare Data for Model Training
- Tokenize the Non-Fashion Texts
- Balancing the Dataset: downsample the non-fashion corpus to half the size of the fashion corpus
- Combine with Fashion-Related Tokens
- Shuffling: ensure the model sees both classes during training
- Add class weights to emphasize fashion-related content during training.

#### Step 2 Train the Model
- Split the Data into Training and Validation Sets
- Fine-Tune BERT

#### Step 3 Apply the Model
- prepare post data
  - Combine 'post_title' and 'post_content' into 'post_text'
  - Clean 'post_text'
- Use the Trained Model to Classify Fashion-Related Content

#### Step 4 Apply Keyword Extraction (RAKE) on Fashion-Related Texts
- Initialize RAKE keyword extractor
- Function to extract fashion-related keywords using RAKE
- Apply RAKE on the fashion_text column to extract keywords
- Save the final DataFrame with fashion-related keywords to [post_filtered_rake.csv]()

#### Step 5 Apply Soft Matching
- Load the fashion lexicon from 'topics_filtered.csv'
- Load the post_filtered_rake.csv file
- Initialize the BERT tokenizer and model
- Function to get BERT embeddings for a word
- Precompute embeddings for fashion keywords in the lexicon
- Function to compute cosine similarity between two vectors
- Function to filter keywords with soft matching (similarity threshold = .6)
- Apply the fashion keyword filter with soft matching to non-empty 'fashion_keywords' rows
- Apply the filtering function to the 'fashion_keywords' column
- Save the final output with only fashion-related keywords





