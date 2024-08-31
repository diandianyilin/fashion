# tfashion - A model to identify fashion-related words
## Step 1. Get a non-fashion Chinese corpus
- Chinese Wikipedia Dump
- Use WikiExtractor to convert the XML dump into plain text
- Get extracted_texts
- Filter Non-Fashion Content from the Extracted Texts, using fashion keywords

## Step 2. Prepare Data for Model Training
- Tokenize the Non-Fashion Texts
- Combine with Fashion-Related Tokens

## Step 3. Train the Model
- Split the Data into Training and Validation Sets
- Fine-Tune BERT

## (Optional) Check data before training
- Check Data Shapes
- Check for Any 'NaN' Values
- Check Data Distribution
- Inspect a Few Examples
- Check Label Value Range
- Verify Dataset Splitting
- Check for Duplicates

## Step 4. Evaluate the Model
 - evaluation resutls:

## Step 5. Apply the model
- prepare post data
  - input: poster_test_fashion_nlpclean.csv
  - Combine 'post_title' and 'post_content' into 'post_text'
  - Clean and Tokenize 'post_text'
- Filter Non-Fashion Words Using the Model
- output: post_filtered.csv
