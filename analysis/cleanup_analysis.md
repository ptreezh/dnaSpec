# Directory Analysis for Cleanup

## Cache Directories (Safe to Remove):
- .pytest_cache/ - Test cache, can be regenerated
- dist/ - Distribution files, can be rebuilt
- workspaces/ - Likely temporary workspaces
- task_workspaces/ - Temporary task workspaces
- test_project/ - Test project, can be recreated if needed

## IDE/Scaffolding Directories to Archive:
- .claude/ - Claude-specific config
- .codebuddy/ - Codebuddy config
- .copilot/ - Copilot config
- .gemini/ - Gemini config
- .qodercli/ - QoderCLI config
- .qwen/ - Qwen config
- .iflow/ - iFlow config
- .vibedev/ - Vibedev config

## Potentially Redundant Directories to Archive:
- doc/ - Possibly duplicate of docs/
- specs/ - May be duplicate content
- spec-kit/ - Old spec kit structure
- spec_kit_requirements/ - Older requirements structure
- claude_skills_repo/ - Possibly redundant skills repo
- skillsadvanceden/ - Potentially duplicate of skills/advanced
- skillsbasicen/ - Potentially duplicate of skills/basic
- skillsworkflowsen/ - Potentially duplicate of skills/workflows

## Archive Before Potential Cleanup:
- archive/ - Already an archive directory
- package/ - May contain distributable code
- tdd_plans/ - Contains development plans

## Core Directories to Preserve:
- skills/ - Main skills implementation
- src/ - Source code
- docs/ - Documentation
- tests/ - Test files
- tests_new/ - New test files