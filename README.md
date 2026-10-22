# Book Genre Classifier: Fiction vs Nonfiction

An end-to-end machine learning project with scraping of data from a website and predicting whether a book is **fiction** or **nonfiction** from its title and description.

## Results

| Model | Accuracy | Fiction recall | Nonfiction recall |
|---|---|---|---|
| Baseline (always predict "nonfiction") | 63.6% | 0% | 100% |
| Logistic Regression | 64% | 6% | 96% |
| + balanced class weights | 77% | 50% | 93% |
| + balanced class weights + stop-word removal | 80% | 62% | 89% |

*Evaluated on a test set of 44 books.*

**Key finding:** the first model's 64% accuracy looked reasonable, but it is misleading. From the confusion matrix, we learn it predicted "nonfiction" for almost every book, which matches the class distribution + is no better than the baseline. Re-weighting the classes during training made the model actually learn to recognize fiction: fiction recall went from 6% to 50%.

## Data

- **Source:** [Books to Scrape](http://books.toscrape.com/), a site built for web scraping practice
- **Collected:** title, cover image URL, description and category for every book in the fiction and nonfiction categories
- **Size:** 175 books (65 fiction, 110 nonfiction)
- **Imbalance in the data:** about 63% nonfiction and 37% fiction

## Approach

### 1. Web scraping
Used `requests` and `BeautifulSoup`. The scraper finds the category pages, follows pagination and visits each book's page to collect its details. Scraping logic can be found in the functions in `functions.py` file.

### 2. Cleaning
- Responses are decoded from raw bytes as UTF-8
- Removed the `...more` truncation marker from descriptions
- Combined title and description into a single text field

### 3. Features: TF-IDF
Each book becomes a vector with one weight per vocabulary word, around 6000. The vectorizer is fitted on the training set only and then applied to the test set, in order to avoid data leakage.

### 4. Modeling and experiments
Chose Logistic Regression because it works well on small text datasets. In each of the three experiments, I made one change at a time:
1. **Plain logistic regression.** Matches the baseline + almost never predicts fiction
2. **`class_weight="balanced"`.** Largest improvement, errors on the fiction category (minority class) cost more during training
3. **English stop-word removal.** Small gain, shrinks the vocabulary from 6,259 to 6,007 words

### 5. Evaluation
Provided accuracy, per-class precision and recall, confusion matrices and predicted probabilities after every experiment, all compared against a baseline.

## Project structure

```
├── book_classification.ipynb   # scraping, modeling, evaluation
├── functions.py                # helper functions
├── dataset_books.csv           # scraped dataset
└── README.md
```

## How to run

```bash
git clone https://github.com/cristina1512/book-genre-classifier.git
pip install requests beautifulsoup4 pandas numpy matplotlib scikit-learn jupyter
cd book-genre-classifier
jupyter notebook book_classification.ipynb
```

## Tech stack

Python · requests · BeautifulSoup · pandas · NumPy · scikit-learn · Matplotlib
