from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class TemplateAnalysis:
    primary_template: str
    application_type: str
    template_details: List[str]
    recommendations: List[str]

class TemplateAnalyzer:
    def analyze(self, request: str, context: Optional[Dict] = None) -> TemplateAnalysis:
        request_lower = request.lower()

        templates = {
            'understanding': ['理解', 'understanding'],
            'reasoning': ['推理', 'reasoning'],
            'verification': ['验证', 'verification'],
            'design': ['设计', 'design'],
            'problem_solving': ['解决问题', 'problem solving'],
        }

        detected = []
        for tmpl, keywords in templates.items():
            if any(kw in request_lower for kw in keywords):
                detected.append(tmpl)

        primary = detected[0] if detected else 'general'

        # 检测应用类型
        if '创建' in request or 'create' in request_lower or '新建' in request:
            app_type = 'template_creation'
        elif '组合' in request or 'combine' in request_lower:
            app_type = 'template_composition'
        elif '定制' in request or 'custom' in request_lower:
            app_type = 'template_customization'
        else:
            app_type = 'template_application'

        details = []
        if 'understanding' in detected:
            details.append('识别核心问题')
        if 'reasoning' in detected:
            details.append('系统化推理')
        if 'verification' in detected:
            details.append('全面验证')
        if 'design' in detected:
            details.append('架构设计')

        recommendations = []
        if not detected:
            recommendations.append("请选择合适的认知模板类型")

        return TemplateAnalysis(
            primary_template=primary,
            application_type=app_type,
            template_details=details,
            recommendations=recommendations
        )
