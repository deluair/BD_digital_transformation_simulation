import pandas as pd
# Import plotting libraries
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import os

class DigitalAnalysisEngine:
    """Analyze and visualize digital transformation simulation results for Bangladesh."""
    def __init__(self, results_history, scenario_name="Scenario"):
        """Initialize the analysis engine with simulation results.

        Args:
            results_history (list): A list of dictionaries, where each dict holds the state/metrics for one year.
            scenario_name (str): The name of the scenario for labeling outputs.
        """
        print("Initializing DigitalAnalysisEngine...")
        self.scenario_name = scenario_name
        self.results = pd.DataFrame(results_history)
        self.figures = {} # To store generated figures
        # Set year as index if present
        if 'year' in self.results.columns:
            self.results.set_index('year', inplace=True)
        else:
            # Add a year index if missing, assuming consecutive years from 0
            self.results.index = pd.Index(range(len(self.results)), name='year_simulated')
            
        print(f"DigitalAnalysisEngine Initialized for '{self.scenario_name}' with {len(self.results)} years of data.")

    def generate_digital_maturity_metrics(self):
        """Calculate composite digital transformation indicators for Bangladesh based on results."""
        print("Generating Digital Maturity Metrics...")
        # Placeholder: Define and calculate composite indices based on available metrics
        # Example: A simple index averaging key metrics (requires normalization in practice)
        key_metrics = [
            'policy_policy_effectiveness', 'infra_infra_metric', 'skills_skills_metric',
            'inclusion_overall_literacy', 'cyber_protection_level', 'society_adoption_rate',
            'innovation_startup_count', 'emerging_ai_adoption', 'economy_econ_metric',
            'sectoral_fin_digital_index', 'gov_gov_metric', 'integration_it_exports'
        ]
        # Normalize (example using min-max scaling between 0 and 1 for demonstration)
        # In a real scenario, normalization should be carefully chosen and applied.
        composite_index_cols = []
        for col in key_metrics:
            if col in self.results.columns:
                min_val = self.results[col].min()
                max_val = self.results[col].max()
                # Avoid division by zero if the metric is constant
                if max_val > min_val:
                     self.results[f'{col}_norm'] = (self.results[col] - min_val) / (max_val - min_val)
                     composite_index_cols.append(f'{col}_norm')
                else:
                    # Handle constant columns - assign a default normalized value (e.g., 0.5)
                    self.results[f'{col}_norm'] = 0.5
                    composite_index_cols.append(f'{col}_norm')
            else:
                 print(f"Warning: Metric {col} not found in results for composite index calculation.")

        if composite_index_cols: # Ensure there are columns to average
             self.results['composite_digital_maturity'] = self.results[composite_index_cols].mean(axis=1)
             print("Calculated 'composite_digital_maturity' index (simple average of normalized key metrics).")
        else:
            print("Warning: Could not calculate composite index due to missing key metrics.")
            self.results['composite_digital_maturity'] = 0.0 # Assign default if calculation fails

        print("Placeholder: More sophisticated composite metric calculation needed.")
        return self.results

    def analyze_digital_evolution(self):
        """Assess digital transformation under different scenarios and generate insights."""
        print(f"Analyzing Digital Evolution for {self.scenario_name}...")
        if not self.results.empty:
            print("\n--- Final Year State (Year {}) --- Scenario: {} ---".format(self.results.index[-1], self.scenario_name))
            # Display relevant columns neatly
            final_state = self.results.iloc[-1]
            print(final_state.to_string())
            print("---------------------------------")
        else:
            print("No results data to analyze.")

        print("Placeholder: Detailed evolution analysis (trends, correlations) needed.")

    def create_visualizations(self):
        """Generate plots based on the simulation results using Plotly."""
        print(f"Creating Visualizations for {self.scenario_name}...")
        if self.results.empty:
            print("No results to visualize.")
            return

        # Example 1: Plotting the composite maturity index
        if 'composite_digital_maturity' in self.results.columns:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=self.results.index, y=self.results['composite_digital_maturity'],
                                      mode='lines+markers', name='Composite Maturity'))
            fig1.update_layout(title=f'Composite Digital Maturity Index ({self.scenario_name})',
                               xaxis_title='Year', yaxis_title='Index Value (Normalized)')
            self.figures['composite_maturity'] = fig1
            print("Generated composite maturity plot.")

        # Example 2: Plotting selected key indicators
        key_indicators_to_plot = [
            'infra_infra_metric', 'economy_econ_metric', 'innovation_startup_count', 'integration_it_exports'
        ]
        
        num_indicators = len(key_indicators_to_plot)
        if num_indicators > 0:
             # Determine subplot layout (e.g., 2 columns)
             rows = (num_indicators + 1) // 2
             fig2 = make_subplots(rows=rows, cols=2, subplot_titles=key_indicators_to_plot)
             current_row = 1
             current_col = 1
             for indicator in key_indicators_to_plot:
                 if indicator in self.results.columns:
                     fig2.add_trace(go.Scatter(x=self.results.index, y=self.results[indicator], 
                                                mode='lines', name=indicator.split('_', 1)[-1]), 
                                    row=current_row, col=current_col)
                     # Update column/row counters
                     current_col += 1
                     if current_col > 2:
                         current_col = 1
                         current_row += 1
                 else:
                      print(f"Warning: Indicator {indicator} not found for plotting.")

             fig2.update_layout(title=f'Selected Key Indicators Evolution ({self.scenario_name})', showlegend=False, height=300*rows)
             self.figures['key_indicators'] = fig2
             print("Generated key indicators subplot.")

        # --- Add more visualizations based on the detailed dashboard list in the prompt ---
        # Requires selecting appropriate columns and chart types (lines, bars, heatmaps etc.)

        print("Placeholder: More detailed visualization generation needed.")

    def generate_html_report(self, filename=None):
        """Generate an HTML report containing analysis summary and visualizations."""
        if filename is None:
            filename = f"simulation_report_{self.scenario_name}.html"
        
        print(f"Generating HTML report: {filename}...")

        # Ensure output directory exists
        output_dir = "reports"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        # Enhanced CSS
        css = """
<style>
  body { 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    line-height: 1.6; 
    margin: 20px; 
    background-color: #f9f9f9; 
    color: #333;
  }
  .container { 
    max-width: 1000px; 
    margin: auto; 
    background: #fff; 
    padding: 25px; 
    box-shadow: 0 0 15px rgba(0,0,0,0.1);
    border-radius: 8px;
  }
  h1, h2, h3 { 
    color: #0056b3; /* A blue shade */
    border-bottom: 2px solid #eee;
    padding-bottom: 5px;
    margin-top: 30px;
  }
  h1 { font-size: 2em; }
  h2 { font-size: 1.5em; }
  h3 { font-size: 1.2em; margin-top: 25px; }
  table { 
    border-collapse: collapse; 
    width: 100%; /* Make table responsive */
    margin-bottom: 25px; 
    box-shadow: 0 2px 3px rgba(0,0,0,0.1);
  }
  th, td { 
    border: 1px solid #ddd; 
    padding: 10px 12px; /* More padding */
    text-align: left; 
  }
  th { 
    background-color: #e9ecef; /* Light grey header */
    font-weight: bold;
    color: #495057;
  }
  tr:nth-child(even) { 
    background-color: #f8f9fa; /* Zebra striping */
  }
  tr:hover {
    background-color: #e2e6ea; /* Hover effect */
  }
  .plotly-graph-div { 
    margin-bottom: 35px; 
    border: 1px solid #eee;
    border-radius: 5px;
    padding: 10px;
  }
  p { margin-bottom: 15px; }
</style>
"""

        with open(filepath, 'w', encoding='utf-8') as f: # Specify encoding
            f.write(f"<!DOCTYPE html><html><head><meta charset=\\"UTF-8\\"><title>Simulation Report: {self.scenario_name}</title>")
            f.write(css) # Inject enhanced CSS
            f.write("</head><body>")
            f.write("<div class=\\"container\\">") # Add container div
            f.write(f"<h1>Simulation Report: {self.scenario_name}</h1>")
            f.write(f"<p>Simulation Period: {self.results.index.min()} - {self.results.index.max()}</p>")
            
            # Add Analysis Summary (e.g., final state table)
            f.write("<h2>Final Year State Summary</h2>")
            if not self.results.empty:
                # Select a subset of columns for the summary table if too many exist
                final_state_df = self.results.iloc[[-1]].copy()
                cols_to_show = [col for col in final_state_df.columns if not col.endswith('_norm')] # Exclude normalized columns
                f.write(final_state_df[cols_to_show[:25]].to_html(escape=False, index=False)) # Limit columns, don't escape HTML, hide index
            else:
                f.write("<p>No results data available.</p>")

            # Embed Figures
            f.write("<h2>Visualizations</h2>")
            if not self.figures:
                 f.write("<p>No figures were generated.</p>")
            else:
                 for name, fig in self.figures.items():
                     f.write(f"<h3>{name.replace('_', ' ').title()}</h3>")
                     # Convert figure to HTML div
                     html_fig = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
                     f.write(html_fig)

            f.write("</div>") # Close container div
            f.write("</body></html>")
        print(f"HTML report saved to {filepath}")

    def run_full_analysis(self):
        """Runs the full sequence of analysis and visualization generation."""
        self.generate_digital_maturity_metrics()
        self.analyze_digital_evolution()
        self.create_visualizations()
        self.generate_html_report() # Generate the report at the end
        print("Full analysis run complete.") 