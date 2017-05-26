#!/bin/bash
echo "Product Evaluation Engine v1.2"
echo "Extracting dataset..."
python data_extraction_scripts/extract_data.py
echo "Done! Dataset extracted as Filtered_Dataset"
echo "Extracting sentiment classifier training dataset..."
python classifier_training/extract_sentiment_classified_textblob.py
echo "Done! Sentiment dataset extracted as Sentiment_Classifier_Training_Data"
echo "Running scripts for classifier training..."
python classifier_training/naive_bayes_trainer.py
echo "Done! classifier and word features stored in saved_classifiers"
echo "Restarting mongodb server..."
sudo service mongod restart
echo "Feeding database..."
python product_evaluation_scripts/feed_database.py
echo "Done! Database ready!"
