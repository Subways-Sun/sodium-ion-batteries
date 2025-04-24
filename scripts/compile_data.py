import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

def process_json_files(directory_path):
    """Process all JSON files in a directory and extract battery material data."""
    all_materials = []
    all_properties = []
    all_starting_materials = []
    
    # Get list of JSON files
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files to process.")
    
    for filename in json_files:
        try:
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
                            "source_file": filename
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
                                    "source_file": filename
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
                                    "source_file": filename
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
        numeric_cols = ['capacity_value', 'current_density_value', 'cycle']
        for col in numeric_cols:
            if col in properties_df.columns:
                properties_df[col] = pd.to_numeric(properties_df[col], errors='coerce')
    
    if not starting_materials_df.empty:
        if 'amount_value' in starting_materials_df.columns:
            starting_materials_df['amount_value'] = pd.to_numeric(starting_materials_df['amount_value'], errors='coerce')
    
    return materials_df, properties_df, starting_materials_df

def analyze_data(materials_df, properties_df, starting_materials_df):
    """Analyze the data and generate insights."""
    results = {}
    
    # Basic statistics
    results["total_materials"] = len(materials_df)
    
    if not materials_df.empty:
        results["material_types"] = materials_df["material_type"].value_counts().to_dict()
    
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
    
    if not starting_materials_df.empty:
        # Common starting materials
        common_starting_materials = Counter(starting_materials_df["starting_material_name"])
        results["common_starting_materials"] = dict(common_starting_materials.most_common(10))
    
    return results

def generate_visualizations(materials_df, properties_df, starting_materials_df, output_dir):
    """Generate visualizations from the data."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
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
            
        # 4. Most common starting materials
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
    directory_path = input("Enter the directory path containing JSON files: ")
    output_dir = "battery_analysis_results"
    compiled_json_file = os.path.join(output_dir, "compiled_battery_data.json")
    analysis_json_file = os.path.join(output_dir, "battery_data_analysis.json")
    excel_output_file = os.path.join(output_dir, "battery_data.xlsx")
    
    # Process the data
    materials, properties, starting_materials = process_json_files(directory_path)
    
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
    
    print("\nAnalysis complete. Key findings:")
    print(f"- Total materials analyzed: {analysis_results.get('total_materials', 0)}")
    
    if 'top_materials_1C' in analysis_results:
        print("- Top performing materials at 1C rate:")
        for material, capacity in list(analysis_results['top_materials_1C'].items())[:3]:
            print(f"  * {material}: {capacity:.2f} mAh g−1")
    
    print("\nCheck the output directory for detailed results and visualizations.")

if __name__ == "__main__":
    main()