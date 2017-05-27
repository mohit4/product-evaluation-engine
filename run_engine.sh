#!/bin/bash
echo "Product Evaluation Engine v1.2.0"
echo "running dataset extraction scripts..."
python data_extraction_scripts/extract_data.py
echo "running sentiment dataset extraction scripts..."
python classifier_training/extract_sentiment_classified_textblob.py
echo "running scripts for classifier training..."
python classifier_training/naive_bayes_trainer.py
echo "restarting mongodb server..."
sudo service mongod restart
echo "running data evaluation scripts..."
python product_evaluation_scripts/feed_database.py
echo "Finished. Database ready!"
