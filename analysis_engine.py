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
        
        # Apply a template for consistent styling
        plot_template = "plotly_white"

        # Example 1: Plotting the composite maturity index - Enhanced Styling
        if 'composite_digital_maturity' in self.results.columns:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=self.results.index, 
                y=self.results['composite_digital_maturity'],
                mode='lines+markers', 
                name='Composite Maturity', 
                line=dict(color='#1a5276', width=3), # Dark blue line
                marker=dict(color='#1a5276', size=7, symbol='circle'),
                hovertemplate='Year: %{x}<br>Index: %{y:.3f}<extra></extra>' # Custom hover
            ))
            fig1.update_layout(
                title=dict(text=f'Composite Digital Maturity Index ({self.scenario_name})', font=dict(size=18)),
                xaxis_title='Simulation Year', 
                yaxis_title='Index Value (Normalized)',
                template=plot_template,
                hovermode='x unified',
                yaxis_range=[0, 1.05], # Set Y-axis range 0 to 1.05
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e9ecef'), # Add light grid
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e9ecef'), # Add light grid
                margin=dict(t=50, b=50, l=50, r=20) # Further reduced margins
            )
            self.figures['composite_maturity'] = fig1
            print("Generated composite maturity plot with enhanced styling.")

        # Example 2: Plotting selected key indicators (NORMALIZED)
        normalized_indicators_to_plot = [
            'infra_infra_metric_norm', 
            'economy_econ_metric_norm', 
            'innovation_startup_count_norm', 
            'integration_it_exports_norm'
        ]
        subplot_titles = [
             'Infrastructure (Norm)', 'Economy (Norm)', 'Startups (Norm)', 'IT Exports (Norm)'
        ]
        
        num_indicators = len(normalized_indicators_to_plot)
        if num_indicators > 0:
             rows = (num_indicators + 1) // 2
             fig2 = make_subplots(rows=rows, cols=2, subplot_titles=subplot_titles)
             current_row = 1
             current_col = 1
             plot_added = False
             for i, indicator in enumerate(normalized_indicators_to_plot):
                 if indicator in self.results.columns:
                     fig2.add_trace(go.Scatter(x=self.results.index, y=self.results[indicator], 
                                                mode='lines', name=subplot_titles[i]), 
                                    row=current_row, col=current_col)
                     plot_added = True
                     # Update column/row counters
                     current_col += 1
                     if current_col > 2:
                         current_col = 1
                         current_row += 1
                 else:
                      print(f"Warning: Indicator {indicator} not found for plotting.")

             if plot_added:
                fig2.update_layout(
                    title=f'Selected Key Indicators Evolution (Normalized) ({self.scenario_name})',
                    showlegend=False, 
                    template=plot_template,
                    height=250*rows + 100, # Adjust height dynamically
                    margin=dict(t=100, b=50, l=50, r=30) # Add margin
                )
                fig2.update_yaxes(title_text="Normalized Value (0-1)", row=1, col=1) # Add Y-axis label example
                self.figures['key_normalized_indicators'] = fig2
                print("Generated key normalized indicators subplot.")
             else:
                 print("No key normalized indicators found to plot.")

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

        # Clearer & Nicer CSS - Updated Styling
        css = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');

  body {
    font-family: 'Lato', sans-serif;
    line-height: 1.75;
    margin: 0;
    padding: 0;
    background-color: #f8f9fa; /* Lighter background */
    color: #495057; /* Softer black */
    font-weight: 300;
  }
  .container {
    max-width: 1200px;
    margin: 40px auto;
    background: #ffffff;
    padding: 30px 50px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.07);
    border-radius: 8px;
  }
  h1, h2, h3 {
    color: #1a5276; /* Darker shade of blue */
    border-bottom: 2px solid #aed6f1; /* Lighter blue */
    padding-bottom: 10px;
    margin-top: 45px;
    margin-bottom: 25px;
    font-weight: 400;
  }
  h1 { font-size: 2.4em; font-weight: 700; border-bottom-width: 3px; }
  h2 { font-size: 1.8em; }
  h3 { font-size: 1.4em; border-bottom: none; color: #2e86c1; margin-top: 30px; margin-bottom: 15px;}
  
  /* Definition List for Summary */
  dl.summary-list {
      background-color: #fff;
      padding: 20px;
      border-radius: 5px;
      border: 1px solid #e9ecef;
      margin-bottom: 30px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* Responsive grid */
      gap: 15px 30px; /* Row and column gap */
  }
  dl.summary-list > div { /* Wrap dt/dd pairs for grid layout */
      border-bottom: 1px dashed #e9ecef;
      padding-bottom: 10px;
  }
  dl.summary-list dt {
      font-weight: 700; /* Bolder terms */
      color: #1a5276;
      margin-bottom: 5px;
      font-size: 0.95em;
  }
  dl.summary-list dd {
      margin-left: 0; /* Reset default margin */
      font-size: 1.1em;
      color: #566573;
  }

  /* Plotly Div Styling */
  .plotly-graph-div {
    /* Removed specific styles, rely on wrapper */
    max-width: 100%; /* Ensure plot div respects container */
    height: auto; /* Allow height to adjust */
    box-sizing: border-box; /* Include padding/border in width/height */
  }
  /* New Wrapper for Plots */
  .plot-container {
      margin: 25px auto 50px auto; /* Center and provide vertical spacing */
      padding: 10px;
      background-color: #fdfdfe;
      border: 1px solid #e9ecef;
      border-radius: 6px;
      box-shadow: 0 3px 6px rgba(0,0,0,0.05);
      max-width: 98%; /* Slightly less than 100% to avoid edge issues */
      overflow: hidden; /* Prevent plot spilling out */
  }

  p {
      margin-bottom: 20px;
      color: #566573;
      font-size: 1.05em;
  }
  a { color: #2e86c1; text-decoration: none; font-weight: 400;}
  a:hover { text-decoration: underline; }
</style>
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("<!DOCTYPE html><html><head>")
            f.write(f'<meta charset="UTF-8"><title>Simulation Report: {self.scenario_name}</title>')
            f.write(css)
            f.write("</head><body>")
            f.write('<div class="container">')
            f.write(f"<h1>Digital Transformation Simulation Report</h1>")
            f.write(f"<h2>Scenario: {self.scenario_name}</h2>")
            f.write(f"<p>Simulation Period: <strong>{self.results.index.min()} - {self.results.index.max()}</strong></p>")
            
            # Add Analysis Summary using Definition List
            f.write("<h2>Final Year State Summary ({})</h2>".format(self.results.index[-1]))
            if not self.results.empty:
                final_state = self.results.iloc[-1]
                cols_to_show = [col for col in final_state.index if not col.endswith('_norm')]
                
                f.write("<dl class=\"summary-list\">")
                for col in cols_to_show[:30]: # Limit items shown
                    metric_name = col.replace('_', ' ').title()
                    value = final_state[col]
                    # Basic formatting for numbers
                    try:
                        value_str = f"{float(value):,.3f}" if isinstance(value, (int, float)) else str(value)
                    except (ValueError, TypeError):
                        value_str = str(value)
                        
                    f.write("<div>") # Wrapper div for grid layout
                    f.write(f"<dt>{metric_name}</dt>")
                    f.write(f"<dd>{value_str}</dd>")
                    f.write("</div>")
                f.write("</dl>")
            else:
                f.write("<p>No results data available.</p>")

            # Embed Figures
            f.write("<h2>Visualizations</h2>")
            if not self.figures:
                 f.write("<p>No figures were generated.</p>")
            else:
                 for name, fig in self.figures.items():
                     f.write(f"<h3>{name.replace('_', ' ').title()}</h3>")
                     
                     # Add responsive config to Plotly HTML generation
                     html_fig = pio.to_html(
                         fig, 
                         full_html=False, 
                         include_plotlyjs='cdn',
                         config={'responsive': True} # Make Plotly chart responsive
                     )
                     # Wrap the plot html in our styled container
                     f.write(f'<div class="plot-container">{html_fig}</div>') 

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
