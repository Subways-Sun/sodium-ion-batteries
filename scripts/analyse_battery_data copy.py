import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
import re
from datetime import datetime

def load_metadata(metadata_file_path):
    """Load paper metadata from JSON file and create a DOI to publication year mapping."""
    doi_to_year = {}
    
    try:
        with open(metadata_file_path, 'r', encoding='utf-8') as file:
            # Check if the metadata is a list or a single object
            metadata_content = json.load(file)
            
            # Convert to list if it's a single object
            metadata = metadata_content if isinstance(metadata_content, list) else [metadata_content]
            
            # Process each paper in the metadata
            for paper in metadata:
                # Check if paper is a dictionary (valid JSON object)
                if not isinstance(paper, dict):
                    continue
                    
                # Extract DOI - handle different possible structures
                doi = None
                if "externalIds" in paper and isinstance(paper["externalIds"], dict) and "DOI" in paper["externalIds"]:
                    doi = paper["externalIds"]["DOI"].lower()  # Convert to lowercase for case-insensitive matching
                elif "DOI" in paper:
                    doi = paper["DOI"].lower()
                
                if not doi:
                    continue
                
                # Extract publication year from the publicationDate with flexible date format handling
                pub_year = None
                if "publicationDate" in paper and paper["publicationDate"]:
                    try:
                        pub_date = paper["publicationDate"]
                        
                        # Try different date formats
                        for date_format in ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%Y"]:
                            try:
                                date_obj = datetime.strptime(pub_date, date_format)
                                pub_year = date_obj.year
                                break
                            except ValueError:
                                continue
                        
                        # If date parsing failed, try to extract year using regex
                        if pub_year is None:
                            year_match = re.search(r'(\d{4})', pub_date)
                            if year_match:
                                pub_year = int(year_match.group(1))
                                
                        if pub_year and 1900 <= pub_year <= 2025:  # Validate year is reasonable
                            doi_to_year[doi] = pub_year
                    except Exception as e:
                        print(f"Error parsing publication date for DOI {doi}: {str(e)}")
                
                # If publication date not found or invalid, try to extract year from other fields
                if pub_year is None and "year" in paper:
                    try:
                        year_value = paper["year"]
                        if isinstance(year_value, int) and 1900 <= year_value <= 2025:
                            doi_to_year[doi] = year_value
                        elif isinstance(year_value, str):
                            year_match = re.search(r'(\d{4})', year_value)
                            if year_match:
                                pub_year = int(year_match.group(1))
                                if 1900 <= pub_year <= 2025:
                                    doi_to_year[doi] = pub_year
                    except Exception as e:
                        print(f"Error extracting year for DOI {doi}: {str(e)}")
    
    except Exception as e:
        print(f"Error loading metadata file: {str(e)}")
        print(f"Please check that the metadata file exists and contains valid JSON.")
    
    print(f"Loaded publication years for {len(doi_to_year)} papers from metadata.")
    return doi_to_year

def extract_doi_from_filename(filename):
    """Extract DOI from filename by replacing first '-' with '/'."""
    # Remove file extension
    base_name = os.path.splitext(filename)[0]
    
    # Replace first '-' with '/'
    parts = base_name.split('-', 1)
    if len(parts) > 1:
        doi = f"{parts[0]}/{parts[1]}"
        return doi.lower()  # Convert to lowercase for case-insensitive matching
    else:
        # If no hyphen found, return the base name as is (might be a valid DOI already)
        print(f"Warning: Could not extract DOI from filename {filename} using hyphen replacement method")
        return base_name.lower()


def process_json_files(directory_path, doi_to_year):
    """Process all JSON files in a directory and extract battery material data."""
    all_materials = []
    all_properties = []
    all_starting_materials = []
    
    # Get list of JSON files
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files to process.")
    
    for filename in json_files:
        try:
            # Extract DOI from filename
            doi = extract_doi_from_filename(filename)
            
            # Look up publication year
            pub_year = None
            if doi and doi in doi_to_year:
                pub_year = doi_to_year[doi]
            
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Extract materials data
                if "material" in data:
                    for material in data["material"]:
                        # Store basic material info
                        material_info = {
                            "material_name": material.get("material_name", "Unknown"),
                            "material_formula": material.get("material_formula", "Unknown"),
                            "material_type": material.get("material_type", "Unknown"),
                            "source_file": filename,
                            "doi": doi,
                            "publication_year": pub_year
                        }
                        all_materials.append(material_info)
                        
                        # Process properties
                        if "material_properties" in material:
                            for prop in material["material_properties"]:
                                property_data = {
                                    "material_name": material.get("material_name", "Unknown"),
                                    "material_formula": material.get("material_formula", "Unknown"),
                                    "capacity_value": prop.get("capacity_value", None),
                                    "capacity_unit": prop.get("capacity_unit", ""),
                                    "capacity_type": prop.get("capacity_type", ""),
                                    "current_density_value": prop.get("current_density_value", None),
                                    "current_density_unit": prop.get("current_density_unit", ""),
                                    "cycle": prop.get("cycle", -1),
                                    "source_file": filename,
                                    "doi": doi,
                                    "publication_year": pub_year
                                }
                                all_properties.append(property_data)
                        
                        # Process starting materials
                        if "starting_material" in material:
                            for start_mat in material["starting_material"]:
                                starting_material_data = {
                                    "battery_material": material.get("material_name", "Unknown"),
                                    "battery_formula": material.get("material_formula", "Unknown"),
                                    "starting_material_name": start_mat.get("material_name", "Unknown"),
                                    "starting_material_formula": start_mat.get("material_formula", "Unknown"),
                                    "amount_value": start_mat.get("amount", {}).get("value", None),
                                    "amount_unit": start_mat.get("amount", {}).get("unit", ""),
                                    "source_file": filename,
                                    "doi": doi,
                                    "publication_year": pub_year
                                }
                                all_starting_materials.append(starting_material_data)
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    return all_materials, all_properties, all_starting_materials

def create_dataframes(materials, properties, starting_materials):
    """Convert extracted data into pandas DataFrames."""
    materials_df = pd.DataFrame(materials)
    properties_df = pd.DataFrame(properties)
    starting_materials_df = pd.DataFrame(starting_materials)
    
    # Convert numeric columns to appropriate types
    if not properties_df.empty:
        numeric_cols = ['capacity_value', 'current_density_value', 'cycle', 'publication_year']
        for col in numeric_cols:
            if col in properties_df.columns:
                properties_df[col] = pd.to_numeric(properties_df[col], errors='coerce')
    
    if not starting_materials_df.empty:
        if 'amount_value' in starting_materials_df.columns:
            starting_materials_df['amount_value'] = pd.to_numeric(starting_materials_df['amount_value'], errors='coerce')
        if 'publication_year' in starting_materials_df.columns:
            starting_materials_df['publication_year'] = pd.to_numeric(starting_materials_df['publication_year'], errors='coerce')
    
    if not materials_df.empty:
        if 'publication_year' in materials_df.columns:
            materials_df['publication_year'] = pd.to_numeric(materials_df['publication_year'], errors='coerce')
    
    return materials_df, properties_df, starting_materials_df

def analyze_data(materials_df, properties_df, starting_materials_df):
    """Analyze the data and generate insights."""
    results = {}
    
    # Basic statistics
    results["total_materials"] = len(materials_df)
    
    if not materials_df.empty:
        results["material_types"] = materials_df["material_type"].value_counts().to_dict()
        
        # Publication year distribution
        if "publication_year" in materials_df.columns:
            year_counts = materials_df["publication_year"].value_counts().sort_index().to_dict()
            results["materials_by_year"] = year_counts
    
    if not properties_df.empty:
        # Capacity analysis
        properties_df_clean = properties_df[properties_df["capacity_value"].notnull() & 
                                          (properties_df["capacity_unit"] == "mAh g−1")]
        
        if not properties_df_clean.empty:
            # Get capacity at different C-rates
            c_rates = properties_df_clean["current_density_value"].unique()
            capacity_by_c_rate = {}
            
            for c_rate in c_rates:
                if pd.notnull(c_rate):
                    c_rate_data = properties_df_clean[properties_df_clean["current_density_value"] == c_rate]
                    capacity_by_c_rate[c_rate] = {
                        "mean": c_rate_data["capacity_value"].mean(),
                        "median": c_rate_data["capacity_value"].median(),
                        "max": c_rate_data["capacity_value"].max(),
                        "min": c_rate_data["capacity_value"].min(),
                        "count": len(c_rate_data)
                    }
            
            results["capacity_by_c_rate"] = capacity_by_c_rate
            
            # Best performing materials at 1C
            one_c_data = properties_df_clean[properties_df_clean["current_density_value"] == 1]
            if not one_c_data.empty:
                results["top_materials_1C"] = one_c_data.sort_values("capacity_value", ascending=False).head(5)[
                    ["material_name", "capacity_value"]].set_index("material_name").to_dict()["capacity_value"]
                
            # Analyze trends over time
            if "publication_year" in properties_df_clean.columns:
                # Group by year and calculate average capacity
                yearly_capacity = properties_df_clean.groupby("publication_year")["capacity_value"].agg(
                    ["mean", "max", "count"]).reset_index()
                results["capacity_trend_by_year"] = yearly_capacity.to_dict('records')
    
    if not starting_materials_df.empty:
        # Common starting materials
        common_starting_materials = Counter(starting_materials_df["starting_material_name"])
        results["common_starting_materials"] = dict(common_starting_materials.most_common(10))
    
    return results

def extract_element_from_formula(formula):
    """Extract main element from material formula using regex pattern matching."""
    # Common battery materials often contain these elements
    elements = ["Li", "Na", "K", "V", "Mn", "Fe", "Co", "Ni", "Cu", "P", "O", "S", "F"]
    
    # Remove numbers, parentheses and other non-alphabetic characters
    clean_formula = re.sub(r'[^a-zA-Z]', '', formula)
    
    # Find the first match from our list of elements
    for element in elements:
        if element in clean_formula:
            return element
    
    return "Other"

def generate_visualizations(materials_df, properties_df, starting_materials_df, output_dir):
    """Generate visualizations from the data."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set the default plot style
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Set a consistent color palette
        colors = plt.cm.viridis(np.linspace(0, 1, 10))
        sns.set_palette(sns.color_palette(colors))
        
        # 1. Capacity vs C-rate
        if not properties_df.empty:
            plt.figure(figsize=(12, 8))
            sns.boxplot(x="current_density_value", y="capacity_value", 
                        data=properties_df[properties_df["capacity_unit"] == "mAh g−1"])
            plt.title("Capacity Distribution by C-rate")
            plt.xlabel("C-rate")
            plt.ylabel("Capacity (mAh g−1)")
            plt.savefig(os.path.join(output_dir, "capacity_vs_crate.png"))
            plt.close()
            
            # 2. Cycle stability
            cycle_data = properties_df[(properties_df["cycle"] > 0) & 
                                      (properties_df["capacity_unit"] == "%")]
            if not cycle_data.empty:
                plt.figure(figsize=(12, 8))
                sns.scatterplot(x="cycle", y="capacity_value", 
                               hue="material_name", data=cycle_data)
                plt.title("Capacity Retention vs Cycle Number")
                plt.xlabel("Cycle Number")
                plt.ylabel("Capacity Retention (%)")
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, "cycle_stability.png"))
                plt.close()
            
            # 3. Top materials by capacity
            top_materials = properties_df[
                (properties_df["capacity_unit"] == "mAh g−1") & 
                (properties_df["current_density_value"] == 1)
            ].sort_values("capacity_value", ascending=False).head(10)
            
            if not top_materials.empty:
                plt.figure(figsize=(12, 8))
                sns.barplot(x="capacity_value", y="material_name", data=top_materials)
                plt.title("Top Materials by Capacity at 1C")
                plt.xlabel("Capacity (mAh g−1)")
                plt.ylabel("Material")
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, "top_materials.png"))
                plt.close()
                
            # 4. Publication year trends
            if "publication_year" in properties_df.columns:
                # Filter valid years and mAh g−1 capacity
                year_data = properties_df[
                    (properties_df["publication_year"].notnull()) & 
                    (properties_df["capacity_unit"] == "mAh g−1") &
                    (properties_df["current_density_value"] == 1)
                ]
                
                if not year_data.empty:
                    # Capacity trend over years
                    plt.figure(figsize=(12, 8))
                    year_grouped = year_data.groupby("publication_year")["capacity_value"].agg(
                        ["mean", "max"]).reset_index()
                    
                    plt.plot(year_grouped["publication_year"], year_grouped["mean"], 'o-', label="Average Capacity")
                    plt.plot(year_grouped["publication_year"], year_grouped["max"], 's-', label="Maximum Capacity")
                    plt.title("Sodium-Ion Battery Capacity Trends Over Time (1C Rate)")
                    plt.xlabel("Publication Year")
                    plt.ylabel("Capacity (mAh g−1)")
                    plt.legend()
                    plt.grid(True, linestyle='--', alpha=0.7)
                    plt.savefig(os.path.join(output_dir, "capacity_trend_by_year.png"))
                    plt.close()
                    
                    # Extract element information
                    materials_with_elements = materials_df.copy()
                    materials_with_elements["main_element"] = materials_with_elements["material_formula"].apply(
                        lambda x: extract_element_from_formula(str(x)))
                    
                    # Join with properties
                    element_props = pd.merge(
                        properties_df, 
                        materials_with_elements[["material_name", "material_formula", "main_element"]],
                        on=["material_name", "material_formula"],
                        how="left"
                    )
                    
                    # Element performance over time
                    element_year_data = element_props[
                        (element_props["publication_year"].notnull()) & 
                        (element_props["capacity_unit"] == "mAh g−1") &
                        (element_props["current_density_value"] == 1) &
                        (element_props["main_element"] != "Other")
                    ]
                    
                    if not element_year_data.empty:
                        # Plot top elements
                        top_elements = element_year_data["main_element"].value_counts().nlargest(5).index.tolist()
                        
                        plt.figure(figsize=(14, 8))
                        for element in top_elements:
                            element_data = element_year_data[element_year_data["main_element"] == element]
                            element_grouped = element_data.groupby("publication_year")["capacity_value"].mean().reset_index()
                            if not element_grouped.empty:
                                plt.plot(element_grouped["publication_year"], element_grouped["capacity_value"], 
                                        'o-', label=f"{element}-based")
                        
                        plt.title("Performance Trends by Element Over Time (1C Rate)")
                        plt.xlabel("Publication Year")
                        plt.ylabel("Average Capacity (mAh g−1)")
                        plt.legend()
                        plt.grid(True, linestyle='--', alpha=0.7)
                        plt.savefig(os.path.join(output_dir, "element_trend_by_year.png"))
                        plt.close()
            
        # 5. Most common starting materials
        if not starting_materials_df.empty:
            material_counts = starting_materials_df["starting_material_name"].value_counts().head(15)
            plt.figure(figsize=(12, 8))
            material_counts.plot(kind='barh')
            plt.title("Most Common Starting Materials")
            plt.xlabel("Count")
            plt.ylabel("Starting Material")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "common_starting_materials.png"))
            plt.close()
            
        print(f"Visualizations saved to {output_dir}")
    except Exception as e:
        print(f"Error generating visualizations: {str(e)}")

def save_compiled_data(materials_df, properties_df, starting_materials_df, output_file):
    """Save the compiled data to a single JSON file."""
    compiled_data = {
        "materials": materials_df.to_dict(orient="records"),
        "properties": properties_df.to_dict(orient="records"),
        "starting_materials": starting_materials_df.to_dict(orient="records")
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(compiled_data, f, indent=2)
    
    print(f"Compiled data saved to {output_file}")

def main():
    # Configuration
    directory_path = input("Enter the directory path containing battery JSON files: ")
    metadata_file_path = input("Enter the path to the paper metadata JSON file: ")
    output_dir = "battery_analysis_results"
    compiled_json_file = os.path.join(output_dir, "compiled_battery_data.json")
    analysis_json_file = os.path.join(output_dir, "battery_data_analysis.json")
    excel_output_file = os.path.join(output_dir, "battery_data.xlsx")
    
    # Validate file paths
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
        
    if not os.path.exists(metadata_file_path):
        print(f"Error: Metadata file '{metadata_file_path}' does not exist.")
        return
    
    # Load metadata
    doi_to_year = load_metadata(metadata_file_path)
    
    # Process the data
    materials, properties, starting_materials = process_json_files(directory_path, doi_to_year)
    
    # Convert to DataFrames
    materials_df, properties_df, starting_materials_df = create_dataframes(materials, properties, starting_materials)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save compiled data
    save_compiled_data(materials_df, properties_df, starting_materials_df, compiled_json_file)
    
    # Analyze the data
    analysis_results = analyze_data(materials_df, properties_df, starting_materials_df)
    
    # Save analysis results
    with open(analysis_json_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"Analysis results saved to {analysis_json_file}")
    
    # Generate visualizations
    generate_visualizations(materials_df, properties_df, starting_materials_df, output_dir)
    
    # Save to Excel for easy viewing
    with pd.ExcelWriter(excel_output_file) as writer:
        materials_df.to_excel(writer, sheet_name='Materials', index=False)
        properties_df.to_excel(writer, sheet_name='Properties', index=False)
        starting_materials_df.to_excel(writer, sheet_name='Starting Materials', index=False)
    
    print(f"Data exported to Excel: {excel_output_file}")
    
    # Print summary of findings
    print("\nAnalysis complete. Key findings:")
    print(f"- Total materials analyzed: {analysis_results.get('total_materials', 0)}")
    
    if 'materials_by_year' in analysis_results:
        years = sorted(analysis_results['materials_by_year'].keys())
        if years:
            print(f"- Publication years range: {min(years)} to {max(years)}")
            print(f"- Number of materials by year: {analysis_results['materials_by_year']}")
    
    if 'capacity_trend_by_year' in analysis_results:
        print("- Capacity trends over time:")
        for year_data in analysis_results['capacity_trend_by_year']:
            print(f"  * {year_data['publication_year']}: Avg {year_data['mean']:.2f} mAh g−1, Max {year_data['max']:.2f} mAh g−1 ({year_data['count']} materials)")
    
    if 'top_materials_1C' in analysis_results:
        print("- Top performing materials at 1C rate:")
        for material, capacity in list(analysis_results['top_materials_1C'].items())[:3]:
            print(f"  * {material}: {capacity:.2f} mAh g−1")
    
    print("\nCheck the output directory for detailed results and visualizations.")

if __name__ == "__main__":
    main()