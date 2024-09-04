# tfashion2.0 - A model to identify fashion-related words (hybrid approach)
- note:
  - BERT is generally better suited for sentence-level tasks rather than word-level classification.
  - balanced dataset of fashion and non-fashion corpora is important
- hybrid approach: using BERT to classify the fashion relevance of larger segments (phrases or sentences) instead of individual words, followed by RAKE (keyword extraction technique) to filter out non-fashion words.

## Steps
1. Fine-tune BERT on the fashion corpus (topics0611_filtered.csv) for phrase-level or sentence-level classification.  
2. Classify the fashion-relatedness of each post in cleaned_post_text using BERT.  
3. Extract fashion-related keywords using RAKE from fashion-classified text.  
4. Filter out non-fashion keywords using the fashion corpus or another lexicon.

## Summary
- BERT is used at the sentence level to classify whether a text is fashion-related.
- RAKE is applied to extract keywords from the fashion-related sentences.
- Finally, fashion-related keywords are filtered using a lexicon (from topics0611_filtered.csv) to ensure non-fashion keywords are removed.
