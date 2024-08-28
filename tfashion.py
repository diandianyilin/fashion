import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from torch.utils.data import Dataset
from sklearn.feature_extraction.text import CountVectorizer  

topics_file = '/home/disk1/red_disk1/Multimodal_MKT/topics0611.csv'
posts_file = '/home/disk1/red_disk1/Multimodal_MKT/test/poster_test_fashion_nlpclean.csv'

topics_df = pd.read_csv(topics_file)
posts_df = pd.read_csv(posts_file)

import pandas as pd
import re
import emoji
import jieba

# Load stopwords from the provided file
with open('/home/disk1/red_disk1/Multimodal_MKT/stopwords_cn.txt', 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

# Load the poster_test_fashion_nlpclean.csv file
poster_df = pd.read_csv('/home/disk1/red_disk1/Multimodal_MKT/test/poster_test_fashion_nlpclean.csv')

# Remove duplicate rows based on poster_id and post_id
poster_df = poster_df.drop_duplicates(subset=['poster_id', 'post_id'])

# Ensure that the post_title and post_content columns are filled
poster_df['post_title'] = poster_df['post_title'].fillna('')
poster_df['post_content'] = poster_df['post_comment_content'].fillna('')

# Combine titles and content for searching
poster_df['combined_text'] = poster_df['post_title'] + ' ' + poster_df['post_content']

# Function for text cleaning
def clean_text(text, stopwords):
    # Convert emojis to text
    text = emoji.demojize(text)
    
    # Remove specific patterns
    text = re.sub(r'- 小红书,,', '', text)
    text = re.sub(r',,\d{2}-\d{2},,', '', text)
    text = re.sub(r'#', ' ', text)
    
    # Remove digits
    text = re.sub(r'\d+', '', text)
    
    # Remove special characters
    cleaned_text = ''.join(char for char in text if char.isalnum() or char.isspace())
    
    # Tokenize
    words = jieba.cut(cleaned_text)
    
    # Remove stopwords
    filtered_words = [word for word in words if word not in stopwords]
    
    return ' '.join(filtered_words)

# Apply data cleaning to post_title, post_content, and post_comments
poster_df['post_title_clean'] = poster_df['post_title'].apply(lambda x: clean_text(x, stopwords))
poster_df['post_content_clean'] = poster_df['post_content'].apply(lambda x: clean_text(x, stopwords))
poster_df['post_comments_clean'] = poster_df['post_comment_content'].fillna('').apply(lambda x: clean_text(str(x), stopwords))

# Load the topics0611.csv file containing fashion-related keywords
topics_df = pd.read_csv('/home/disk1/red_disk1/Multimodal_MKT/topics0611.csv')

# Extract fashion-related keywords from the 'keyword group' column
fashion_keywords = topics_df['keyword group'].str.lower().unique()
fashion_df = pd.DataFrame(fashion_keywords, columns=['keyword'])
fashion_df['label'] = 1  # Label as fashion-related

# Check the content of 'post_comments_clean' before vectorization
comments_text = poster_df['post_comments_clean'].fillna('').str.cat(sep=' ')
if not comments_text.strip():  # Check if comments_text is empty or only contains spaces
    print("Warning: comments_text is empty after cleaning!")
else:
    vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')  # Token pattern to capture words
    X_comments = vectorizer.fit_transform([comments_text])
    comment_keywords = vectorizer.get_feature_names_out()  # Extract unique words from comments

    # Filter out fashion-related keywords to get non-fashion-related keywords
    non_fashion_keywords = [kw for kw in comment_keywords if kw not in fashion_keywords]

    # Create DataFrames for fashion and non-fashion keywords
    non_fashion_df = pd.DataFrame(non_fashion_keywords, columns=['keyword'])
    non_fashion_df['label'] = 0  # Label as non-fashion-related

    # Combine fashion and non-fashion keywords into a single DataFrame
    combined_df = pd.concat([fashion_df, non_fashion_df]).reset_index(drop=True)

    # Check the content of the final DataFrame
    print("Combined DataFrame Info:")
    print(combined_df.info())  # Provides a summary of the DataFrame
    # Show the first 10 rows where label is 1 (fashion-related)
    print("\nFirst 10 rows where label is 1 (Fashion-related):")
    print(combined_df[combined_df['label'] == 1].head(10))
    # Show the first 10 rows where label is 0 (Non-fashion-related)
    print("\nFirst 10 rows where label is 0 (Non-Fashion-related):")
    print(combined_df[combined_df['label'] == 0].head(10))

train_df, test_df = train_test_split(combined_df, test_size=0.2, random_state=42)

class KeywordDataset(Dataset):
    def __init__(self, keywords, labels, tokenizer, max_len):
        self.keywords = keywords
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.keywords)

    def __getitem__(self, idx):
        keyword = str(self.keywords[idx])
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            keyword,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# Load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

# Create datasets
MAX_LEN = 16
train_dataset = KeywordDataset(
    keywords=train_df['keyword'].values,
    labels=train_df['label'].values,
    tokenizer=tokenizer,
    max_len=MAX_LEN
)

test_dataset = KeywordDataset(
    keywords=test_df['keyword'].values,
    labels=test_df['label'].values,
    tokenizer=tokenizer,
    max_len=MAX_LEN
)

model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=2)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=4,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy='epoch'
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=lambda p: {
        'accuracy': accuracy_score(p.label_ids, p.predictions.argmax(-1)),
        'precision': precision_score(p.label_ids, p.predictions.argmax(-1)),
        'recall': recall_score(p.label_ids, p.predictions.argmax(-1)),
        'f1': f1_score(p.label_ids, p.predictions.argmax(-1)),
    }
)

trainer.train()

trainer.evaluate()

from torch.utils.data import DataLoader, TensorDataset

# Ensure that the model is on the correct device (GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def identify_fashion_related(text_series, tokenizer, model, batch_size=16, max_len=16):
    # Convert text_series to a DataLoader for batch processing
    inputs = tokenizer(text_series.tolist(), padding=True, truncation=True, max_length=max_len, return_tensors='pt')
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    # Create a DataLoader to iterate over the data in batches
    dataset = TensorDataset(input_ids, attention_mask)
    dataloader = DataLoader(dataset, batch_size=batch_size)

    predictions = []
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():  # Disable gradient computation to save memory
        for batch in dataloader:
            batch_input_ids, batch_attention_mask = batch
            outputs = model(input_ids=batch_input_ids, attention_mask=batch_attention_mask)
            batch_predictions = torch.argmax(outputs.logits, dim=1)
            predictions.extend(batch_predictions.cpu().numpy())

    return torch.tensor(predictions)

# Apply to post_title and post_content
poster_df['title_fashion_related'] = identify_fashion_related(poster_df['post_title_clean'], tokenizer, model)
poster_df['content_fashion_related'] = identify_fashion_related(poster_df['post_content_clean'], tokenizer, model)

print(poster_df[['post_title', 'title_fashion_related', 'post_content', 'content_fashion_related']])

# Save the results to a new DataFrame with selected columns
results_df = poster_df[['post_title', 'title_fashion_related', 'post_content', 'content_fashion_related']]

# Save the final results to a CSV file
results_df.to_csv('/home/disk1/red_disk1/Multimodal_MKT/fashion_related_results.csv', index=False)

print("Results saved to 'fashion_related_results.csv'")