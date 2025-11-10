# -*- coding: utf-8 -*-
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

# Import OpenAI library
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

class OpenAIService(AIServiceBase):
    """OpenAI GPT-4 Vision service for scalp analysis"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        if not OPENAI_AVAILABLE:
            raise ImportError("Please install openai: pip install openai")
        self.client = OpenAI(api_key=api_key)

    def _enhance_image_quality(self, image: Image.Image) -> Image.Image:
        """Enhance image quality for better AI analysis"""
        from PIL import ImageEnhance

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize if too large (max 1920px on longest side for quality/cost balance)
        max_size = 1920
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        # Enhance sharpness (subtle, helps with scalp detail)
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.2)

        # Enhance contrast (subtle, helps identify inflammation/redness)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)

        # Enhance color saturation (very subtle, helps differentiate skin tones)
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.05)

        return image

    def analyze_scalp_image(self, image: Image.Image, language: str = 'zh') -> Dict:
        """Use GPT-4 Vision to analyze scalp image"""

        # Enhance image quality before analysis
        image = self._enhance_image_quality(image)

        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG", quality=95)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Create prompt based on language (使用与Claude相同的详细prompt)
        if language == 'zh':
            prompt = """
            你是一位具有20年临床经验的皮肤科主任医师和毛发病理学专家，专攻头皮疾病诊断、毛囊显微分析和毛发医学。请以最高医学标准对这张头皮图像进行深度分析。

            **🔬 图像类型识别**（重要！）：
            本系统接受以下类型的头皮图像，请先识别图像类型：

            1. **显微镜放大图/特写镜头**（放大倍数：10x-200x）
               - 特征：可以清楚看到毛囊口、皮脂、角质细节、微小鳞屑
               - 分析重点：毛囊堵塞、角质堆积、皮脂状态、微观炎症、细小皮屑
               - 这是**有效的头皮图像**，必须进行详细分析！

            2. **常规头皮照片**（正常距离拍摄）
               - 特征：能看到整体头皮区域、发际线、头发分布
               - 分析重点：整体色调、大面积红斑、发量密度、明显鳞屑

            3. **无效图像**（非头皮照片）
               - 如果图像完全不是头皮或头发相关（如风景、物品、其他身体部位等），
                 才返回错误格式

            ⚠️ **关键提示**：
            - 显微镜头皮图/特写镜头是**完全有效**的头皮图像，必须分析！
            - 不要因为图像是放大图就认为"无法识别"
            - 显微镜图能看到更多细节，反而更有利于精准诊断

            **分析要求**（请严格遵守）：
            1. 仔细观察图像的每个细节（无论是显微镜图还是常规照片）
            2. 不要轻易判断为"完全正常"，任何轻微问题都应该指出
            3. 即使是健康的头皮，也要指出可能的风险因素或改善建议
            4. 使用专业医学术语，同时解释清楚
            5. **对于显微镜图像，要特别关注微观特征**（毛囊口状态、角质颗粒、皮脂质地等）

            **必须检查的项目**（根据图像类型选择重点）：

            **常规照片检查项**：
            1. 头皮颜色（正常粉红/潮红/苍白/黄褐色）
            2. 皮脂分泌整体状态（过多/正常/过少）
            3. 可见头屑情况（无/轻度/中度/严重）
            4. 炎症迹象（红斑/丘疹/脓疱）
            5. 头发密度（正常/稀疏/脱落）
            6. 整体皮肤纹理（光滑/粗糙/鳞屑）
            7. 异常斑块或病变

            **显微镜图/特写照检查项**（重点！）：
            1. **毛囊口细节**：
               - 开口状态：通畅/轻度角化/明显堵塞/完全闭塞
               - 毛囊周围：正常/轻微红晕/明显发红/炎症
               - 皮脂栓塞：无/轻微/明显（白色或黄色）

            2. **角质与皮屑微观特征**：
               - 白色颗粒状物质（干性皮屑）的数量和大小
               - 黄色油腻性鳞屑（脂溢性）的分布
               - 角质层厚度（正常/过度角化/萎缩）

            3. **皮脂腺活动**：
               - 油光程度（0-10级）
               - 皮脂质地（清亮/浑浊/蜡质）
               - 油脂分布模式（均匀/聚集在毛囊口）

            4. **微观炎症标志**：
               - 局部红点或红斑（数量、大小）
               - 毛囊周围红晕
               - 微小脓点或白头

            5. **头皮表面纹理**：
               - 皮肤光滑度（细腻/粗糙/颗粒感）
               - 细小裂纹或干燥迹象
               - 表面光泽（健康光泽/过度油亮/暗淡无光）

            **需要诊断的疾病**（至少列出可能存在的风险）：
            - 脂溢性皮炎（头皮油腻、黄色鳞屑）
            - 银屑病/牛皮癣（银白色鳞屑、红斑）
            - 毛囊炎（红色丘疹、脓疱）
            - 斑秃（圆形脱发区域）
            - 脂溢性脱发/雄激素性脱发（头发稀疏、细软）
            - 头癣（真菌感染、鳞屑、断发）
            - 接触性皮炎（过敏、瘙痒）
            - 休止期脱发（弥漫性脱发）
            - 头皮干燥或敏感

            **健康评分标准**（请严格评分）：
            - 90-100分：头皮极其健康，无任何问题
            - 70-89分：轻微问题（如轻度油脂、轻微头屑）
            - 50-69分：中度问题（明显油脂、中度头屑、轻度炎症）
            - 30-49分：严重问题（重度炎症、脱发、明显病变）
            - 0-29分：极其严重（需要立即就医）

            **返回格式**（必须是有效的JSON）：
            {
                "image_type": "图像类型（显微镜图/特写照/常规照片）",
                "scalp_type": "头皮类型（油性/干性/正常/混合/敏感）",
                "microscopic_findings": {
                    "follicle_condition": "毛囊状态描述（仅显微镜图需要）",
                    "keratin_buildup": "角质堆积情况（仅显微镜图需要）",
                    "sebum_status": "皮脂状态描述（仅显微镜图需要）",
                    "micro_inflammation": "微观炎症描述（仅显微镜图需要）"
                },
                "conditions": [
                    {
                        "name_cn": "疾病中文名",
                        "name_en": "Disease English Name",
                        "severity": "严重程度（轻度/中度/重度）",
                        "confidence": 置信度数字(0-100),
                        "symptoms": ["具体观察到的症状1", "症状2", "症状3"],
                        "description": "详细的医学描述，包括为什么这样判断"
                    }
                ],
                "health_score": 健康评分(0-100，请严格评分),
                "recommendations": ["具体的治疗或护理建议1", "建议2", "建议3"],
                "need_doctor": true或false（是否需要就医），
                "analysis_summary": "综合分析总结，包括主要问题和整体评估。如果是显微镜图，要明确说明这是显微镜下的观察结果。"
            }

            **重要提示**：
            - 如果看到任何异常，哪怕很轻微，都要列出来
            - 健康评分不要随便给90分以上，要严格评估
            - 即使头皮看起来健康，也要提供预防建议
            - 症状描述要具体，不要模糊

            **关键要求（必须遵守）**：
            - 无论如何，必须返回有效的 JSON 格式
            - 如果图片不是头皮照片，返回：
            {
                "scalp_type": "无法识别 (Invalid Image)",
                "conditions": [],
                "health_score": 0,
                "recommendations": ["请上传清晰的头皮照片", "确保照片包含头发和头皮细节"],
                "need_doctor": false,
                "analysis_summary": "图像不是头皮照片或质量不足，无法进行分析"
            }
            - 只返回 JSON，不要添加任何其他文字说明
            """
        else:
            prompt = """
            You are a senior dermatologist with 20 years of experience specializing in scalp pathology and trichology. Please analyze this scalp image with the highest medical standards.

            **🔬 Image Type Recognition** (IMPORTANT!):
            This system accepts the following types of scalp images. Please identify the image type first:

            1. **Microscopic/Close-up Images** (10x-200x magnification)
               - Features: Clear view of follicle openings, sebum, keratin details, micro-scales
               - Analysis focus: Follicle blockage, keratin buildup, sebum status, micro-inflammation, tiny flakes
               - This is a **VALID scalp image** - you MUST analyze it in detail!

            2. **Regular Scalp Photos** (normal distance)
               - Features: Overall scalp area, hairline, hair distribution visible
               - Analysis focus: Overall tone, large red patches, hair density, obvious scales

            3. **Invalid Images** (non-scalp photos)
               - Only return error format if the image is completely unrelated to scalp/hair
                 (like landscapes, objects, other body parts, etc.)

            ⚠️ **KEY REMINDERS**:
            - Microscopic scalp images/close-ups are **COMPLETELY VALID** scalp images - MUST analyze!
            - Do NOT reject images just because they are magnified
            - Microscopic images show more details, which is better for precise diagnosis

            **Analysis Requirements** (strictly follow):
            1. Observe every detail carefully (whether microscopic or regular photo)
            2. Do NOT easily judge as "completely normal" - point out any minor issues
            3. Even for healthy scalps, indicate potential risk factors or improvement suggestions
            4. Use professional medical terminology while explaining clearly
            5. **For microscopic images, pay special attention to micro-features** (follicle openings, keratin particles, sebum texture, etc.)

            **Items to Check** (focus based on image type):

            **For Regular Photos**:
            1. Scalp color (normal pink/redness/pale/yellow-brown)
            2. Overall sebum secretion (excessive/normal/insufficient)
            3. Visible dandruff (none/mild/moderate/severe)
            4. Inflammation signs (erythema/papules/pustules)
            5. Hair density (normal/sparse/loss)
            6. Overall skin texture (smooth/rough/scaly)
            7. Abnormal patches or lesions

            **For Microscopic/Close-up Images** (FOCUS!):
            1. **Follicle Opening Details**:
               - Opening status: clear/mild keratinization/blocked/completely occluded
               - Perifollicluar area: normal/mild redness/obvious inflammation
               - Sebum plugs: none/mild/obvious (white or yellow)

            2. **Keratin & Flake Micro-features**:
               - White granular material (dry flakes) - quantity and size
               - Yellow oily scales (seborrheic) - distribution
               - Stratum corneum thickness (normal/hyperkeratosis/atrophy)

            3. **Sebaceous Gland Activity**:
               - Oiliness level (0-10 scale)
               - Sebum texture (clear/turbid/waxy)
               - Oil distribution pattern (even/concentrated at follicle openings)

            4. **Micro-inflammation Markers**:
               - Small red dots or patches (count, size)
               - Perifollicular redness
               - Tiny pustules or whiteheads

            5. **Scalp Surface Texture**:
               - Skin smoothness (fine/rough/granular)
               - Fine cracks or dryness signs
               - Surface luster (healthy shine/overly oily/dull)

            **Conditions to Diagnose** (list at least potential risks):
            - Seborrheic Dermatitis (oily scalp, yellow scales)
            - Psoriasis (silvery scales, red patches)
            - Folliculitis (red papules, pustules)
            - Alopecia Areata (circular hair loss areas)
            - Androgenetic Alopecia (thinning hair, fine texture)
            - Tinea Capitis (fungal infection, scales, broken hair)
            - Contact Dermatitis (allergy, itching)
            - Telogen Effluvium (diffuse hair loss)
            - Dry or sensitive scalp

            **Health Score Standards** (strict scoring):
            - 90-100: Extremely healthy scalp, no issues
            - 70-89: Minor issues (mild oil, slight dandruff)
            - 50-69: Moderate problems (obvious oil, moderate dandruff, mild inflammation)
            - 30-49: Severe problems (heavy inflammation, hair loss, obvious lesions)
            - 0-29: Extremely severe (immediate medical attention needed)

            **Return Format** (must be valid JSON):
            {
                "image_type": "image type (Microscopic/Close-up/Regular Photo)",
                "scalp_type": "scalp type (oily/dry/normal/combination/sensitive)",
                "microscopic_findings": {
                    "follicle_condition": "follicle status description (microscopic only)",
                    "keratin_buildup": "keratin accumulation status (microscopic only)",
                    "sebum_status": "sebum status description (microscopic only)",
                    "micro_inflammation": "micro-inflammation description (microscopic only)"
                },
                "conditions": [
                    {
                        "name_cn": "Chinese disease name",
                        "name_en": "English Disease Name",
                        "severity": "severity (mild/moderate/severe)",
                        "confidence": confidence_number(0-100),
                        "symptoms": ["specific observed symptom1", "symptom2", "symptom3"],
                        "description": "detailed medical description, including reasoning"
                    }
                ],
                "health_score": health_score(0-100, strict scoring),
                "recommendations": ["specific treatment or care recommendation1", "recommendation2", "recommendation3"],
                "need_doctor": true_or_false (whether medical consultation needed),
                "analysis_summary": "comprehensive analysis summary, including main issues and overall assessment. If microscopic image, clearly state these are observations under magnification."
            }

            **Important Notes**:
            - **ACCEPT microscopic/close-up scalp images as valid images**
            - List any abnormalities, even if very minor
            - Don't easily give 90+ scores, be strict in assessment
            - Even for healthy-looking scalps, provide prevention advice
            - Symptom descriptions should be specific, not vague
            - For microscopic images, describe what you see at micro-level
            """

        try:
            # 尝试多个模型，按优先级顺序（性能 > 可用性 > 成本）
            models_to_try = [
                # GPT-4 系列 (当前推荐和可用) ⭐
                "gpt-4o",                   # GPT-4 Omni - 最新最强
                "gpt-4o-mini",              # GPT-4 Omni Mini - 经济实惠，大多数用户可用
                "gpt-4-turbo",              # GPT-4 Turbo - 高性能
                "gpt-4-vision-preview"      # GPT-4 Vision - 较旧但稳定
            ]

            last_error = None
            response = None
            used_model = None  # 记录使用的模型

            for model in models_to_try:
                try:
                    # 新模型使用 max_completion_tokens，旧模型使用 max_tokens
                    # GPT-4o 及更新的模型需要 max_completion_tokens
                    uses_new_api = model in ["gpt-4o", "gpt-4o-mini"]

                    # 确保prompt是UTF-8编码的字符串
                    prompt_text = prompt if isinstance(prompt, str) else str(prompt)

                    # 构建基础参数
                    api_params = {
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a professional dermatologist specializing in scalp health analysis."
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{img_base64}",
                                            "detail": "high"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": prompt_text
                                    }
                                ]
                            }
                        ]
                    }

                    # 只对旧模型添加 temperature，新模型使用默认值
                    if not uses_new_api:
                        api_params["temperature"] = 0

                    # 根据模型版本添加正确的 token 限制参数
                    if uses_new_api:
                        api_params["max_completion_tokens"] = 3000
                    else:
                        api_params["max_tokens"] = 3000

                    response = self.client.chat.completions.create(**api_params)
                    used_model = model
                    break  # Success, exit loop

                except Exception as e:
                    error_msg = str(e)
                    last_error = e

                    # If model not found, try next model
                    if "model_not_found" in error_msg or "does not exist" in error_msg:
                        continue
                    else:
                        # Other errors (like API key error), raise immediately
                        raise e

            # If all models failed
            if response is None:
                raise Exception(f"All models unavailable. Last error: {str(last_error)}")

            response_text = response.choices[0].message.content

            # Parse JSON response
            try:
                import re
                # Try to extract JSON
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)

                    # Save raw response for debugging
                    result['ai_raw_response'] = response_text
                    # 添加使用的模型信息
                    result['used_model'] = used_model
                else:
                    result = {
                        "scalp_type": "Analysis Complete",
                        "conditions": [],
                        "health_score": 50,
                        "recommendations": [response_text],
                        "need_doctor": False,
                        "analysis_summary": response_text,
                        "ai_raw_response": response_text,
                        "used_model": used_model
                    }
            except json.JSONDecodeError as e:
                result = {
                    "scalp_type": "Analysis Complete",
                    "conditions": [],
                    "health_score": 50,
                    "recommendations": [response_text],
                    "need_doctor": False,
                    "analysis_summary": response_text,
                    "ai_raw_response": response_text,
                    "parse_error": str(e),
                    "used_model": used_model
                }

            # 添加模型显示名称
            model_display_names = {
                "gpt-4o": "GPT-4o (Latest)",
                "gpt-4o-mini": "GPT-4o Mini (Economy)",
                "gpt-4-turbo": "GPT-4 Turbo",
                "gpt-4-vision-preview": "GPT-4 Vision"
            }
            result['model_display_name'] = model_display_names.get(used_model, used_model)

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
            "GPT-4 Vision (OpenAI)": OPENAI_AVAILABLE,
            "Local Analysis (Rule-based)": True
        }

    @staticmethod
    def create_service(service_type: str, api_key: str) -> Optional[AIServiceBase]:
        """Create an AI service instance"""
        if service_type == "GPT-4 Vision (OpenAI)":
            if not api_key:
                st.error("Please provide OpenAI API key")
                return None
            return OpenAIService(api_key)
        else:
            return None

    @staticmethod
    def _normalize_condition(cond: Dict) -> Dict:
        """Normalize a condition dict to include all required fields for UI display"""
        # Disease icon mapping
        icon_map = {
            '脂溢性皮炎': '🔴',
            'seborrheic dermatitis': '🔴',
            '银屑病': '🔵',
            'psoriasis': '🔵',
            '毛囊炎': '🟡',
            'folliculitis': '🟡',
            '斑秃': '⚪',
            'alopecia areata': '⚪',
            '脂溢性脱发': '🟠',
            'androgenetic alopecia': '🟠',
            '头癣': '🟢',
            'tinea capitis': '🟢',
            '接触性皮炎': '🟣',
            'contact dermatitis': '🟣',
            '休止期脱发': '⚫',
            'telogen effluvium': '⚫',
        }

        normalized = cond.copy()

        # Add icon if missing
        if 'icon' not in normalized:
            name_cn = normalized.get('name_cn', '').lower()
            name_en = normalized.get('name_en', '').lower()
            normalized['icon'] = '🔴'  # default
            for key, icon in icon_map.items():
                if key.lower() in name_cn or key.lower() in name_en:
                    normalized['icon'] = icon
                    break

        # Add common_name if missing
        if 'common_name' not in normalized:
            normalized['common_name'] = normalized.get('name_cn', '未知')

        # Ensure all required fields exist
        normalized.setdefault('name_cn', '未知疾病')
        normalized.setdefault('name_en', 'Unknown Condition')
        normalized.setdefault('severity', '中度')
        normalized.setdefault('description', '详细信息不可用')

        # Fix confidence if it's 0 or None (AI should provide actual confidence)
        confidence = normalized.get('confidence', None)

        # Debug: Check original confidence value
        original_confidence = confidence

        if confidence is None or confidence == 0 or confidence == '':
            # If no confidence provided, estimate based on severity
            severity = normalized.get('severity', '中度')
            if severity in ['重度', '晚期']:
                normalized['confidence'] = 75  # Severe conditions usually have clear signs
            elif severity == '中度':
                normalized['confidence'] = 60  # Moderate confidence
            else:
                normalized['confidence'] = 50  # Mild conditions may be less certain
        else:
            # Ensure confidence is an integer
            try:
                normalized['confidence'] = int(float(confidence))
            except (ValueError, TypeError):
                normalized['confidence'] = 50

        return normalized

    @staticmethod
    def combine_analyses(ai_result: Dict, local_result: Dict) -> Dict:
        """Combine AI and local analysis results - AI takes priority"""

        # Start with AI result as base (AI is more accurate)
        combined = ai_result.copy() if ai_result and 'error' not in ai_result else local_result.copy()

        # If AI result is valid, use it as primary source
        if ai_result and 'error' not in ai_result:
            # Map AI conditions to the expected format and normalize them
            ai_conditions = ai_result.get('conditions', [])
            normalized_conditions = [AIServiceManager._normalize_condition(cond) for cond in ai_conditions]
            combined['diagnosed_conditions'] = normalized_conditions

            # Optionally add unique local conditions as supplementary
            if local_result.get('diagnosed_conditions'):
                local_conditions = local_result.get('diagnosed_conditions', [])
                condition_map = {cond.get('name_en', cond.get('name_cn', '')): cond for cond in normalized_conditions}

                for cond in local_conditions:
                    key = cond.get('name_en', cond.get('name_cn', ''))
                    if key not in condition_map:
                        # Add local condition with lower confidence
                        cond_copy = AIServiceManager._normalize_condition(cond)
                        cond_copy['source'] = 'local_analysis'
                        combined['diagnosed_conditions'].append(cond_copy)

            # Use AI recommendations as primary
            combined['concerns'] = ai_result.get('recommendations', [])

            # Add local concerns as supplementary if not already covered
            if local_result.get('concerns'):
                local_concerns = local_result.get('concerns', [])
                combined['concerns'].extend([f"[本地分析] {c}" for c in local_concerns[:2]])

            # Ensure all AI fields are preserved
            if 'analysis_summary' in ai_result:
                combined['ai_analysis'] = ai_result['analysis_summary']

            if 'need_doctor' in ai_result:
                combined['need_doctor'] = ai_result['need_doctor']

            # Add metrics from local analysis if AI doesn't provide them
            if 'metrics' not in combined and 'metrics' in local_result:
                combined['metrics'] = local_result['metrics']

            # Calculate overall confidence from diagnosed conditions
            if 'diagnosed_conditions' in combined and combined['diagnosed_conditions']:
                # Calculate average confidence from all diagnosed conditions
                confidences = [
                    cond.get('confidence', 0)
                    for cond in combined['diagnosed_conditions']
                ]
                if confidences:
                    combined['confidence'] = int(sum(confidences) / len(confidences))
                else:
                    combined['confidence'] = 0
            else:
                combined['confidence'] = 0

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