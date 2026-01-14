"""
Integration tests for the documentation analysis tool.
"""
import pytest
import tempfile
import os
from pathlib import Path

from src.doc_analyzer.document_reader import DocumentReader
from src.services.nlp_service import NLPServer
from src.doc_analyzer.scenario_extractor import ScenarioExtractor
from src.doc_analyzer.real_world_mapper import RealWorldMapper
from src.doc_analyzer.test_plan_generator import TestPlanGenerator
from src.utils.config_loader import ConfigLoader


class TestEndToEnd:
    
    def setup_method(self):
        """Setup method to initialize components for each test."""
        # Initialize all components
        try:
            self.nlp_service = NLPServer("en_core_web_sm")
        except OSError:
            # If the model is not available, use a basic one
            self.nlp_service = NLPServer()
        
        self.document_reader = DocumentReader()
        self.scenario_extractor = ScenarioExtractor(self.nlp_service)
        self.real_world_mapper = RealWorldMapper()
        self.test_plan_generator = TestPlanGenerator()
        self.config_loader = ConfigLoader()
    
    def test_document_analysis_pipeline(self):
        """Test the complete document analysis pipeline."""
        # Create a temporary directory with test documents
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test documents
            doc1_path = os.path.join(temp_dir, "authentication.md")
            with open(doc1_path, 'w', encoding='utf-8') as f:
                f.write("""
# Authentication System

## User Login
When a user wants to access the system, they must provide valid credentials.
The system should verify the credentials against the user database.
If credentials are valid, the user should be granted access.
If credentials are invalid, an error message should be displayed.

## Password Reset
Users should be able to reset their password if they forget it.
The system must send a reset link to the user's registered email.
Critical: The system must prevent brute force attacks.
                """)
            
            doc2_path = os.path.join(temp_dir, "export.html")
            with open(doc2_path, 'w', encoding='utf-8') as f:
                f.write("""
<html>
<head><title>Data Export</title></head>
<body>
<h1>Data Export Feature</h1>
<p>Users can export their data in various formats.</p>
<p>The system supports CSV, JSON, and Excel formats.</p>
<p>When exporting large datasets, the system should show progress.</p>
</body>
</html>
                """)
            
            # Step 1: Read documents
            documents = self.document_reader.read_documents_from_directory(temp_dir)
            assert len(documents) == 2
            
            # Step 2: Extract scenarios
            all_scenarios = []
            for doc in documents:
                scenarios = self.scenario_extractor.extract_scenarios(doc)
                all_scenarios.extend(scenarios)
            
            assert len(all_scenarios) > 0  # Should have extracted some scenarios
            
            # Step 3: Map scenarios to real-world usage
            mapped_scenarios = self.real_world_mapper.map_scenarios_to_real_world(all_scenarios)
            assert len(mapped_scenarios) == len(all_scenarios)
            
            # Step 4: Generate test plan
            test_plan = self.test_plan_generator.generate_test_plan(
                title="Integration Test Plan",
                description="Test plan generated from integration test documents",
                scenarios=mapped_scenarios,
                documents=documents
            )
            
            # Assertions
            assert test_plan.title == "Integration Test Plan"
            assert len(test_plan.test_cases) == len(mapped_scenarios)  # One test case per scenario
            assert len(test_plan.generated_from_docs) == 2  # Two documents
            assert test_plan.coverage_metrics.covered_scenarios == len(mapped_scenarios)
    
    def test_cli_integration_simulation(self):
        """Simulate the CLI integration by testing the main workflow components."""
        # Create a temporary directory with a test document
        with tempfile.TemporaryDirectory() as temp_dir:
            doc_path = os.path.join(temp_dir, "api_spec.md")
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write("""
# API Specification

## User Registration
When a new user wants to use our service, they must register first.
The user provides their email, username, and password.
The system validates the input and creates a new user account.
The user receives a confirmation email.

## Data Access
Registered users can access their personal data through the API.
The system must authenticate the user before providing access.
Important: API requests must be rate-limited to prevent abuse.
                """)
            
            # Read the document
            document = self.document_reader.read_document(doc_path)
            assert document.title == "api_spec"
            
            # Extract scenarios
            scenarios = self.scenario_extractor.extract_scenarios(document)
            assert len(scenarios) > 0
            
            # Map to real-world usage
            mapped_scenarios = self.real_world_mapper.map_scenarios_to_real_world(scenarios)
            assert len(mapped_scenarios) >= len(scenarios)
            
            # Generate test plan
            test_plan = self.test_plan_generator.generate_test_plan(
                title="API Test Plan",
                description="Test plan for API functionality",
                scenarios=mapped_scenarios,
                documents=[document]
            )
            
            # Verify the test plan
            assert test_plan.title == "API Test Plan"
            assert "API" in test_plan.description
            assert len(test_plan.test_cases) > 0
            assert test_plan.coverage_metrics.coverage_percentage >= 0
    
    def test_configuration_integration(self):
        """Test that configuration settings are properly applied."""
        # Create a custom configuration
        config_path = os.path.join(tempfile.gettempdir(), "test_config.yaml")
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write("""
processing:
  max_file_size: "5MB"
  supported_formats: ["md", "txt"]
  max_total_size: "50MB"

output:
  format: "yaml"
  include_traceability: true
  priority_threshold: "P2"

nlp:
  model: "en_core_web_sm"
  accuracy_threshold: 0.75
            """)
        
        # Load the configuration
        config = ConfigLoader(config_path)
        config.validate_config()
        
        # Verify configuration values
        assert config.get("processing.max_file_size") == "5MB"
        assert config.get("output.format") == "yaml"
        assert config.get("nlp.accuracy_threshold") == 0.75
        assert "md" in config.get("processing.supported_formats")
        
        # Clean up
        os.remove(config_path)