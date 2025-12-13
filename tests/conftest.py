import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dna_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
from src.dna_context_engineering.skills_system_final import ContextAnalysisSkill, ContextOptimizationSkill, CognitiveTemplateSkill
from src.dna_context_engineering.skills_manager import ContextEngineeringSkillsManager


@pytest.fixture
def context_analysis_skill():
    return ContextAnalysisSkill()


@pytest.fixture
def context_optimization_skill():
    return ContextOptimizationSkill()


@pytest.fixture
def cognitive_template_skill():
    return CognitiveTemplateSkill()


@pytest.fixture
def context_engineering_system():
    return ContextEngineeringSystemSkill()


@pytest.fixture
def skills_manager():
    return ContextEngineeringSkillsManager()


@pytest.fixture
def sample_context():
    return "This is a sample context for testing purposes that needs analysis and optimization."