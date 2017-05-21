#!/bin/bash
echo "Product Evaluation Engine v1.1"
# echo "Reading data from demo_files..."
# echo "Filtering..."
# python filter_input.py demo_files/
# echo "Done"
# echo "Sentiment labelling..."
# python sentiment_label.py
# echo "Done"
# echo "Extracting features..."
# python feature_extraction.py
# echo "Done"
# echo "Generating conclusion..."
# python conclusion.py
# echo "Done"
echo "Processing data..."
python review_analyze.py review_data/
echo "Done!"
echo "result is stored in result.json"
