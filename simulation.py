# Import model classes
from digital_infrastructure import DigitalInfrastructureModel
from digital_government import DigitalGovernmentModel
from digital_economy import DigitalEconomyModel
from digital_skills import DigitalSkillsModel
from cybersecurity import CybersecurityModel
from digital_inclusion import DigitalInclusionModel
from emerging_technology import EmergingTechnologyModel
from innovation_ecosystem import InnovationEcosystemModel
from sectoral_transformation import SectoralTransformationModel
from digital_policy import DigitalPolicyModel
from digital_society import DigitalSocietyModel
from international_integration import InternationalIntegrationModel

# Import support classes
from data_handler import DigitalDataHandler # Assuming this handles data loading
from analysis_engine import DigitalAnalysisEngine # Assuming this handles results analysis

class BangladeshDigitalTransformationSimulation:
    """Main simulation environment integrating all components for Bangladesh Digital Transformation."""
    def __init__(self, config, scenario_name="baseline"):
        """Initialize simulation with configuration parameters.

        Args:
            config (dict): Configuration dictionary. Should potentially include paths for
                           data handler, model parameters, etc.
            scenario_name (str): The name of the policy scenario to run.
        """
        print("Initializing Bangladesh Digital Transformation Simulation...")
        self.config = config
        self.start_year = 2025
        self.end_year = 2035
        self.current_year = self.start_year
        self.results_history = [] # To store results from each year

        # --- Data Handling --- 
        # You would typically load data first using DigitalDataHandler
        # data_handler = DigitalDataHandler(config.get('data_sources', {}))
        # historical_data = data_handler.load_historical_data()
        # initial_conditions = data_handler.get_initial_conditions(self.start_year)
        # model_configs = {model_name: data_handler.get_config_for_model(model_name) ...}
        # For now, using placeholder config for each model
        print("Note: Using placeholder configurations for models.")

        # --- Initialize Models ---
        # Pass relevant parts of the config/initial_conditions to each model
        model_config = self.config.get('model_params', {}) # Simplified placeholder

        self.digital_infrastructure = DigitalInfrastructureModel(model_config.get('infra', {}))
        self.digital_government = DigitalGovernmentModel(model_config.get('gov', {}))
        self.digital_economy = DigitalEconomyModel(model_config.get('econ', {}))
        self.digital_skills = DigitalSkillsModel(model_config.get('skills', {}))
        self.cybersecurity = CybersecurityModel(model_config.get('cyber', {}))
        self.digital_inclusion = DigitalInclusionModel(model_config.get('inclusion', {}))
        self.emerging_technology = EmergingTechnologyModel(model_config.get('emerging', {}))
        self.innovation_ecosystem = InnovationEcosystemModel(model_config.get('innovation', {}))
        self.sectoral_transformation = SectoralTransformationModel(model_config.get('sectoral', {}))
        self.digital_policy = DigitalPolicyModel(model_config.get('policy', {}))
        self.digital_society = DigitalSocietyModel(model_config.get('society', {}))
        self.international_integration = InternationalIntegrationModel(model_config.get('integration', {}))

        # Set the policy scenario
        self.scenario_name = scenario_name
        self.digital_policy.set_scenario(self.scenario_name)

        print("Simulation Initialized.")

    def run_simulation(self, years=None):
        """Execute simulation from start_year to end_year.

        Args:
            years (int, optional): Number of years to simulate. Defaults to end_year - start_year + 1.
        """
        if years is None:
            simulation_years = self.end_year - self.start_year + 1
        else:
            simulation_years = years
        
        final_year = self.start_year + simulation_years - 1

        print(f"\n--- Starting Simulation Run: {self.start_year} - {final_year} (Scenario: {self.scenario_name}) ---")

        for year in range(self.start_year, final_year + 1):
            self.current_year = year
            print(f"\n--- Simulating Year: {self.current_year} ---")

            # --- Execute models in a logical order (dependencies matter!) ---
            # Example Order: Policy -> Infra -> Skills -> Society/Inclusion -> Innovation -> 
            #                Emerging Tech -> Economy -> Sectoral -> Gov -> Cybersecurity -> Integration
            # Note: This is a simplified linear flow; real dependencies might require iterations within a year.
            
            policy_state = self.digital_policy.simulate_step(year)
            infra_state = self.digital_infrastructure.simulate_step(year)
            # Skills depend on economy(demand), inclusion(access), society(adoption)
            # Need results from later models? --> Requires iteration or passing previous year's state
            # Using placeholder empty dicts for now where dependencies are complex/circular
            skills_state = self.digital_skills.simulate_step(year, {}, {}, {})
            inclusion_state = self.digital_inclusion.simulate_step(year, infra_state, skills_state, policy_state)
            cybersecurity_state = self.cybersecurity.simulate_step(year, infra_state, policy_state, {})
            society_state = self.digital_society.simulate_step(year, infra_state, inclusion_state, cybersecurity_state)
            innovation_state = self.innovation_ecosystem.simulate_step(year, {}, skills_state, policy_state)
            emerging_tech_state = self.emerging_technology.simulate_step(year, infra_state, skills_state, innovation_state)
            economy_state = self.digital_economy.simulate_step(year, infra_state, skills_state, policy_state)
            sectoral_state = self.sectoral_transformation.simulate_step(year, infra_state, skills_state, economy_state, emerging_tech_state)
            gov_state = self.digital_government.simulate_step(year, infra_state, policy_state)
            integration_state = self.international_integration.simulate_step(year, infra_state, economy_state, policy_state)

            # --- Collect results for this year --- 
            yearly_results = {'year': year}
            yearly_results.update({f"policy_{k}": v for k, v in policy_state.items()})
            yearly_results.update({f"infra_{k}": v for k, v in infra_state.items()})
            yearly_results.update({f"skills_{k}": v for k, v in skills_state.items()})
            yearly_results.update({f"inclusion_{k}": v for k, v in inclusion_state.items()})
            yearly_results.update({f"cyber_{k}": v for k, v in cybersecurity_state.items()})
            yearly_results.update({f"society_{k}": v for k, v in society_state.items()})
            yearly_results.update({f"innovation_{k}": v for k, v in innovation_state.items()})
            yearly_results.update({f"emerging_{k}": v for k, v in emerging_tech_state.items()})
            yearly_results.update({f"economy_{k}": v for k, v in economy_state.items()})
            yearly_results.update({f"sectoral_{k}": v for k, v in sectoral_state.items()})
            yearly_results.update({f"gov_{k}": v for k, v in gov_state.items()})
            yearly_results.update({f"integration_{k}": v for k, v in integration_state.items()})
            
            self.results_history.append(yearly_results)

        print(f"\n--- Simulation Run Completed: {self.start_year} - {final_year} (Scenario: {self.scenario_name}) ---")
        return self.results_history

    def analyze_results(self):
        """Analyze the results using the Analysis Engine."""
        if not self.results_history:
            print("No simulation results to analyze. Run simulation first.")
            return None
        
        print("\n--- Analyzing Simulation Results ---")
        analyzer = DigitalAnalysisEngine(self.results_history, scenario_name=self.scenario_name)
        analyzer.run_full_analysis()
        print("--- Analysis Complete ---")
        return analyzer # Return the analyzer object for further interaction

# --- Example Usage --- (Can be run as a script)
if __name__ == "__main__":
    # Basic configuration (replace with actual data loading)
    sim_config = {
        'data_sources': {
            # Paths to data files would go here
        },
        'model_params': {
            # Initial parameters if not derived from data could go here
        }
    }

    # --- Run Baseline Scenario ---
    print("\n=== RUNNING BASELINE SCENARIO ===")
    baseline_sim = BangladeshDigitalTransformationSimulation(sim_config, scenario_name="baseline")
    baseline_results = baseline_sim.run_simulation()
    baseline_analyzer = baseline_sim.analyze_results()

    # --- Run Pro-Investment Scenario ---
    # print("\n=== RUNNING PRO-INVESTMENT SCENARIO ===")
    # investment_sim = BangladeshDigitalTransformationSimulation(sim_config, scenario_name="pro_investment")
    # investment_results = investment_sim.run_simulation()
    # investment_analyzer = investment_sim.analyze_results()

    # --- Add comparison logic between baseline_analyzer.results and investment_analyzer.results ---
    # Example: 
    # if baseline_analyzer and investment_analyzer:
    #     comparison_df = pd.concat([baseline_analyzer.results.add_suffix('_base'), 
    #                                investment_analyzer.results.add_suffix('_invest')], axis=1)
    #     print("\n--- Scenario Comparison (Final Year) ---")
    #     print(comparison_df.iloc[-1]) 