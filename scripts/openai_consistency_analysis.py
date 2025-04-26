import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

# ============= CONFIG SECTION =============
# Update these paths to match your environment
INPUT_FILE = r"data_annotated\search_20241106-223705_50irrelevant_openai_repeat.json"    # Path to your JSON file
OUTPUT_DIR = r"openai_consistency"     # Folder to save results
# =========================================

def main():
    """Simplified approach focused on getting correct alpha values"""
    print("Starting basic agreement analysis...")
    
    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Load data
    try:
        print(f"Loading data from {INPUT_FILE}...")
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully loaded {len(data)} items")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Extract ratings - keep it simple
    items_data = []
    
    for item in data:
        item_id = item.get('id')
        title = item.get('title', '')
        
        # Extract all ratings
        ratings = []
        for i in range(10):
            key = f'label_openai_raw_{i}'
            if key in item:
                ratings.append(item[key])
            else:
                ratings.append(None)  # Mark missing data
        
        # Only include items with complete data
        if None not in ratings:
            items_data.append({
                'id': item_id,
                'title': title,
                'ratings': ratings
            })
    
    print(f"Extracted {len(items_data)} items with complete data")
    
    # Show some samples to verify data extraction
    print("\nSample data (first 5 items):")
    for i in range(min(5, len(items_data))):
        print(f"ID: {items_data[i]['id']}, Title: {items_data[i]['title']}")
        print(f"  Ratings: {items_data[i]['ratings']}")
    
    # Calculate percentage agreement (simplest measure)
    total_pairs = 0
    agreeing_pairs = 0
    
    for item in items_data:
        ratings = item['ratings']
        
        # Count all pairs of ratings
        for i in range(9):
            for j in range(i+1, 10):
                total_pairs += 1
                if ratings[i] == ratings[j]:
                    agreeing_pairs += 1
    
    percent_agreement = (agreeing_pairs / total_pairs) * 100 if total_pairs > 0 else 0
    print(f"\nPercentage agreement: {percent_agreement:.2f}%")
    print(f"  Agreeing pairs: {agreeing_pairs}")
    print(f"  Total pairs: {total_pairs}")
    
    # Find the distribution of categories
    all_categories = Counter()
    for item in items_data:
        all_categories.update(item['ratings'])
    
    print(f"\nCategory distribution:")
    for category, count in all_categories.most_common():
        print(f"  {category}: {count} ({count / sum(all_categories.values()):.1%})")
    
    # Create a mapping from categories to integers (for computation)
    category_map = {cat: i for i, cat in enumerate(sorted(all_categories.keys()))}
    reverse_map = {i: cat for cat, i in category_map.items()}
    
    # Convert ratings to numeric form
    for item in items_data:
        item['numeric_ratings'] = [category_map[r] for r in item['ratings']]
    
    # Calculate agreement matrix between raters
    agreement_matrix = np.zeros((10, 10))
    
    for i in range(10):
        for j in range(10):
            matching = 0
            for item in items_data:
                if item['numeric_ratings'][i] == item['numeric_ratings'][j]:
                    matching += 1
            agreement_matrix[i, j] = matching / len(items_data)
    
    # Calculate mean pairwise agreement
    mean_agreement = 0
    pair_count = 0
    for i in range(9):
        for j in range(i+1, 10):
            mean_agreement += agreement_matrix[i, j]
            pair_count += 1
    
    mean_agreement = mean_agreement / pair_count if pair_count > 0 else 0
    print(f"\nMean pairwise agreement: {mean_agreement:.4f}")
    
    # Calculate Scott's Pi (similar to Krippendorff's alpha but simpler)
    # First, get the probability of each category
    category_probs = {cat: count / sum(all_categories.values()) 
                    for cat, count in all_categories.items()}
    
    # Expected agreement by chance
    chance_agreement = sum(p * p for p in category_probs.values())
    
    # Scott's Pi = (observed agreement - chance agreement) / (1 - chance agreement)
    scotts_pi = (mean_agreement - chance_agreement) / (1 - chance_agreement)
    print(f"\nScott's Pi: {scotts_pi:.4f}")
    
    # Fleiss' Kappa - another alternative
    # For each item, calculate the proportion of raters who assigned each category
    p_i = []
    for item in items_data:
        counts = Counter(item['numeric_ratings'])
        props = {cat: count/10 for cat, count in counts.items()}
        p_i.append(props)
    
    # Calculate P-bar (mean proportion of agreement)
    P_bar = 0
    for props in p_i:
        sum_squares = sum(p*p for p in props.values())
        P_bar += sum_squares
    
    P_bar = P_bar / len(p_i)
    
    # Calculate P_e (expected proportion of agreement)
    P_e = 0
    for cat, count in all_categories.items():
        cat_prop = count / (len(items_data) * 10)
        P_e += cat_prop * cat_prop
    
    # Fleiss' Kappa
    fleiss_kappa = (P_bar - P_e) / (1 - P_e)
    print(f"Fleiss' Kappa: {fleiss_kappa:.4f}")
    
    # Visualize rater agreement
    plt.figure(figsize=(10, 8))
    sns.heatmap(agreement_matrix, annot=True, cmap='viridis', vmin=0, vmax=1)
    plt.title('Agreement Between GPT Classification Runs')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'agreement_matrix.png'))
    
    # Analyze items with most disagreement
    item_disagreement = []
    for item in items_data:
        # Calculate entropy (higher means more disagreement)
        counts = Counter(item['numeric_ratings'])
        entropy = 0
        for count in counts.values():
            p = count / 10
            entropy -= p * np.log2(p)
        
        item_disagreement.append({
            'id': item['id'],
            'title': item['title'],
            'entropy': entropy,
            'unique_categories': len(counts),
            'category_counts': {reverse_map[cat]: count for cat, count in counts.items()}
        })
    
    # Sort by entropy (higher = more disagreement)
    item_disagreement.sort(key=lambda x: x['entropy'], reverse=True)
    
    # Save results
    print("\nSaving results...")
    
    # 1. Summary text report
    with open(os.path.join(OUTPUT_DIR, 'summary.txt'), 'w', encoding='utf-8') as f:
        f.write("GPT Classification Agreement Analysis\n")
        f.write("===================================\n\n")
        f.write(f"Number of items analyzed: {len(items_data)}\n")
        f.write(f"Percentage agreement: {percent_agreement:.2f}%\n")
        f.write(f"Mean pairwise agreement: {mean_agreement:.4f}\n")
        f.write(f"Scott's Pi: {scotts_pi:.4f}\n")
        f.write(f"Fleiss' Kappa: {fleiss_kappa:.4f}\n\n")
        
        f.write("Category Distribution:\n")
        f.write("-------------------\n")
        for category, count in all_categories.most_common():
            f.write(f"{category}: {count} ({count / sum(all_categories.values()):.1%})\n")
        
        f.write("\nTop 10 Items with Most Disagreement:\n")
        f.write("--------------------------------\n")
        for i, item in enumerate(item_disagreement[:10]):
            f.write(f"{i+1}. ID: {item['id']}, Title: {item['title']}\n")
            f.write(f"   Unique categories: {item['unique_categories']}\n")
            f.write(f"   Category counts: {item['category_counts']}\n")
            f.write(f"   Entropy: {item['entropy']:.4f}\n\n")
    
    # 2. Save items data
    with open(os.path.join(OUTPUT_DIR, 'items_data.json'), 'w', encoding='utf-8') as f:
        # Convert to serializable format
        serializable_items = []
        for item in items_data:
            serializable_item = {
                'id': item['id'],
                'title': item['title'],
                'ratings': item['ratings']
            }
            serializable_items.append(serializable_item)
        
        json.dump(serializable_items, f, indent=2)
    
    # 3. Save disagreement analysis
    with open(os.path.join(OUTPUT_DIR, 'disagreement_analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(item_disagreement, f, indent=2)
    
    print(f"Analysis complete! Results saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()