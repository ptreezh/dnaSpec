import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus
from src.context_engineering_skills.context_analysis import ContextAnalysisSkill
from src.context_engineering_skills.context_optimization import ContextOptimizationSkill
from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
from src.context_engineering_skills.system import ContextEngineeringSystem
from src.context_engineering_skills.skills_manager import ContextEngineeringSkillsManager


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
    return ContextEngineeringSystem()


@pytest.fixture
def skills_manager():
    return ContextEngineeringSkillsManager()


@pytest.fixture
def sample_context():
    return "This is a sample context for testing purposes that needs analysis and optimization."