"""
AI Services Integration Module
Supports Claude API, OpenAI Vision API, and other AI services
for enhanced scalp analysis
"""

import os
import base64
import json
import requests
from typing import Dict, Optional, Tuple, Any
from PIL import Image
import io
import streamlit as st

# Try to import optional libraries
try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIServiceBase:
    """Base class for AI services"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def analyze_scalp_image(self, image: Image.Image, language: str = 'zh') -> Dict:
        """Analyze scalp image using AI service"""
        raise NotImplementedError

class ClaudeService(AIServiceBase):
    """Claude AI service for scalp analysis"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        if not CLAUDE_AVAILABLE:
            raise ImportError("Please install anthropic: pip install anthropic")
        self.client = Anthropic(api_key=api_key)

    def analyze_scalp_image(self, image: Image.Image, language: str = 'zh') -> Dict:
        """Use Claude to analyze scalp image"""

        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Create prompt based on language
        if language == 'zh':
            prompt = """
            请分析这张头皮图像，提供专业的医学诊断。请包含以下信息：

            1. 头皮类型（油性/干性/正常/敏感）
            2. 检测到的具体疾病或问题：
               - 斑秃（Alopecia Areata）
               - 脂溢性皮炎（Seborrheic Dermatitis）
               - 银屑病（Psoriasis）
               - 毛囊炎（Folliculitis）
               - 头癣（Tinea Capitis）
               - 其他皮肤问题
            3. 严重程度（轻度/中度/重度）
            4. 具体症状描述
            5. 治疗建议
            6. 是否需要就医

            请以JSON格式返回，包含以下字段：
            {
                "scalp_type": "类型",
                "conditions": [
                    {
                        "name_cn": "中文名",
                        "name_en": "English name",
                        "severity": "严重程度",
                        "confidence": 置信度(0-100),
                        "symptoms": ["症状1", "症状2"],
                        "description": "详细描述"
                    }
                ],
                "health_score": 健康评分(0-100),
                "recommendations": ["建议1", "建议2"],
                "need_doctor": true/false,
                "analysis_summary": "总体分析"
            }
            """
        else:
            prompt = """
            Please analyze this scalp image and provide professional medical diagnosis. Include:

            1. Scalp type (Oily/Dry/Normal/Sensitive)
            2. Detected conditions:
               - Alopecia Areata
               - Seborrheic Dermatitis
               - Psoriasis
               - Folliculitis
               - Tinea Capitis
               - Other conditions
            3. Severity (Mild/Moderate/Severe)
            4. Specific symptoms
            5. Treatment recommendations
            6. Whether medical consultation is needed

            Return in JSON format with these fields:
            {
                "scalp_type": "type",
                "conditions": [
                    {
                        "name_cn": "Chinese name",
                        "name_en": "English name",
                        "severity": "severity",
                        "confidence": confidence(0-100),
                        "symptoms": ["symptom1", "symptom2"],
                        "description": "detailed description"
                    }
                ],
                "health_score": score(0-100),
                "recommendations": ["recommendation1", "recommendation2"],
                "need_doctor": true/false,
                "analysis_summary": "overall analysis"
            }
            """

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Claude 3 Haiku - 快速且经济
                max_tokens=1500,
                temperature=0,
                system="You are a professional dermatologist specializing in scalp health analysis.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": img_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )

            # Parse response
            response_text = message.content[0].text

            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    # If no JSON found, create structured response
                    result = {
                        "scalp_type": "Unknown",
                        "conditions": [],
                        "health_score": 50,
                        "recommendations": [response_text],
                        "need_doctor": False,
                        "analysis_summary": response_text
                    }
            except json.JSONDecodeError:
                result = {
                    "scalp_type": "Analysis Complete",
                    "conditions": [],
                    "health_score": 50,
                    "recommendations": [response_text],
                    "need_doctor": False,
                    "analysis_summary": response_text
                }

            return result

        except Exception as e:
            return {
                "error": f"Claude API error: {str(e)}",
                "scalp_type": "Error",
                "conditions": [],
                "health_score": 0,
                "recommendations": ["Unable to analyze image"],
                "need_doctor": False,
                "analysis_summary": f"Error: {str(e)}"
            }

class OpenAIService(AIServiceBase):
    """OpenAI GPT-4 Vision service for scalp analysis"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        if not OPENAI_AVAILABLE:
            raise ImportError("Please install openai: pip install openai")
        self.client = OpenAI(api_key=api_key)

    def analyze_scalp_image(self, image: Image.Image, language: str = 'zh') -> Dict:
        """Use GPT-4 Vision to analyze scalp image"""

        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Create prompt
        if language == 'zh':
            system_prompt = "你是一位专业的皮肤科医生，专门从事头皮健康分析。"
            user_prompt = """
            请分析这张头皮图像，提供专业诊断。返回JSON格式：
            {
                "scalp_type": "头皮类型",
                "conditions": [
                    {
                        "name_cn": "疾病中文名",
                        "name_en": "Disease name",
                        "severity": "严重程度",
                        "confidence": 置信度,
                        "symptoms": ["症状列表"],
                        "description": "描述"
                    }
                ],
                "health_score": 健康评分,
                "recommendations": ["建议列表"],
                "need_doctor": 是否需要就医,
                "analysis_summary": "总体分析"
            }
            """
        else:
            system_prompt = "You are a professional dermatologist specializing in scalp health analysis."
            user_prompt = """
            Analyze this scalp image and provide diagnosis in JSON format:
            {
                "scalp_type": "scalp type",
                "conditions": [
                    {
                        "name_cn": "Chinese name",
                        "name_en": "English name",
                        "severity": "severity",
                        "confidence": confidence_score,
                        "symptoms": ["symptom list"],
                        "description": "description"
                    }
                ],
                "health_score": health_score,
                "recommendations": ["recommendation list"],
                "need_doctor": need_medical_consultation,
                "analysis_summary": "overall analysis"
            }
            """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",  # or gpt-4o for better performance
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1500,
                temperature=0
            )

            response_text = response.choices[0].message.content

            # Parse JSON response
            try:
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = {
                        "scalp_type": "Analysis Complete",
                        "conditions": [],
                        "health_score": 50,
                        "recommendations": [response_text],
                        "need_doctor": False,
                        "analysis_summary": response_text
                    }
            except json.JSONDecodeError:
                result = {
                    "scalp_type": "Analysis Complete",
                    "conditions": [],
                    "health_score": 50,
                    "recommendations": [response_text],
                    "need_doctor": False,
                    "analysis_summary": response_text
                }

            return result

        except Exception as e:
            return {
                "error": f"OpenAI API error: {str(e)}",
                "scalp_type": "Error",
                "conditions": [],
                "health_score": 0,
                "recommendations": ["Unable to analyze image"],
                "need_doctor": False,
                "analysis_summary": f"Error: {str(e)}"
            }

class AIServiceManager:
    """Manager for AI services"""

    @staticmethod
    def get_available_services() -> Dict[str, bool]:
        """Get list of available AI services"""
        return {
            "Claude (Anthropic)": CLAUDE_AVAILABLE,
            "GPT-4 Vision (OpenAI)": OPENAI_AVAILABLE,
            "Local Analysis (Rule-based)": True
        }

    @staticmethod
    def create_service(service_type: str, api_key: str) -> Optional[AIServiceBase]:
        """Create an AI service instance"""
        if service_type == "Claude (Anthropic)":
            if not api_key:
                st.error("Please provide Claude API key")
                return None
            return ClaudeService(api_key)

        elif service_type == "GPT-4 Vision (OpenAI)":
            if not api_key:
                st.error("Please provide OpenAI API key")
                return None
            return OpenAIService(api_key)

        else:
            return None

    @staticmethod
    def combine_analyses(ai_result: Dict, local_result: Dict) -> Dict:
        """Combine AI and local analysis results"""

        # Start with local result as base
        combined = local_result.copy()

        # Override with AI results if available
        if ai_result and 'error' not in ai_result:
            # Use AI's scalp type if available
            if ai_result.get('scalp_type'):
                combined['scalp_type'] = ai_result['scalp_type']

            # Combine conditions from both sources
            ai_conditions = ai_result.get('conditions', [])
            local_conditions = local_result.get('diagnosed_conditions', [])

            # Merge conditions, prioritizing AI results
            condition_map = {}
            for cond in ai_conditions:
                key = cond.get('name_en', cond.get('name_cn', ''))
                condition_map[key] = cond

            for cond in local_conditions:
                key = cond.get('name_en', cond.get('name_cn', ''))
                if key not in condition_map:
                    condition_map[key] = cond

            combined['diagnosed_conditions'] = list(condition_map.values())

            # Use AI's health score if available
            if 'health_score' in ai_result:
                combined['health_score'] = ai_result['health_score']

            # Combine recommendations
            ai_recs = ai_result.get('recommendations', [])
            local_recs = local_result.get('concerns', [])
            combined['concerns'] = local_recs + ai_recs

            # Add AI analysis summary
            if 'analysis_summary' in ai_result:
                combined['ai_analysis'] = ai_result['analysis_summary']

            # Update medical advice
            if ai_result.get('need_doctor', False):
                if 'medical_advice' in combined:
                    combined['medical_advice']['see_doctor'] = True
                    combined['medical_advice']['urgency'] = 'urgent'

        return combined

def test_ai_service():
    """Test function for AI services"""
    print("Testing AI Services...")

    # Check available services
    services = AIServiceManager.get_available_services()
    print("\nAvailable Services:")
    for service, available in services.items():
        status = "✓ Available" if available else "✗ Not installed"
        print(f"  - {service}: {status}")

    # Test with a dummy image
    test_image = Image.new('RGB', (300, 300), color=(200, 180, 160))

    # Test Claude if available
    if CLAUDE_AVAILABLE:
        claude_key = os.getenv("ANTHROPIC_API_KEY", "")
        if claude_key:
            print("\nTesting Claude Service...")
            claude_service = ClaudeService(claude_key)
            result = claude_service.analyze_scalp_image(test_image)
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")

    # Test OpenAI if available
    if OPENAI_AVAILABLE:
        openai_key = os.getenv("OPENAI_API_KEY", "")
        if openai_key:
            print("\nTesting OpenAI Service...")
            openai_service = OpenAIService(openai_key)
            result = openai_service.analyze_scalp_image(test_image)
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    test_ai_service()