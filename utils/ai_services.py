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

        # Create enhanced professional prompt
        if language == 'zh':
            prompt = """
            你是一位具有15年临床经验的皮肤科主任医师，专攻头皮疾病诊断和毛发医学。请以医学专家的标准对这张头皮图像进行深度分析。

            **🔬 临床分析框架**（必须按此顺序）：

            **1️⃣ 系统性视觉检查**（逐项记录观察结果）：
            - 头皮颜色：正常粉红/充血红/苍白/黄色/色素沉着
            - 皮脂状态：干燥/正常/油腻/过度油腻（T区和枕部分别评估）
            - 鳞屑特征：无/细小白色/大片银白/黄色油腻/厚层痂皮
            - 炎症程度：无/轻度红斑/中度丘疹/重度脓疱/结节
            - 毛囊情况：开放通畅/轻度堵塞/明显角化/炎症/萎缩
            - 发量密度：正常(>100根/cm²)/轻度稀疏(60-100)/中度(40-60)/重度(<40)
            - 发干状态：健康有光泽/干燥/断裂/细软化/异常卷曲
            - 头皮纹理：光滑/轻度粗糙/明显增厚/萎缩/瘢痕

            **2️⃣ 疾病鉴别诊断**（使用临床诊断标准，提供鉴别依据）：

            **脂溢性皮炎** (ICD-10: L21.0):
            - 典型特征：黄色油腻性鳞屑、红斑、瘙痒、T区和耳后明显
            - 鉴别要点：与银屑病的鳞屑颜色差异、分布部位

            **银屑病/头皮型牛皮癣** (ICD-10: L40.0):
            - 典型特征：银白色干燥鳞屑、边界清楚的红斑、Auspitz征
            - 鉴别要点：鳞屑厚度、去除鳞屑后点状出血

            **毛囊炎** (ICD-10: L73.9):
            - 典型特征：毛囊口红色丘疹/脓疱、触痛、成簇分布
            - 鉴别要点：细菌性vs真菌性（分布、脓疱大小）

            **雄激素性脱发** (ICD-10: L64):
            - 男性型（M型后退、头顶稀疏、Hamilton-Norwood分级）
            - 女性型（顶部弥漫性稀疏、Ludwig分级）
            - 微观特征：毛干直径缩小、毳毛增多

            **斑秃** (ICD-10: L63):
            - 典型特征：圆形/椭圆形脱发斑、边缘"感叹号"样毛发
            - 活动期vs静止期判断

            **头癣** (ICD-10: B35.0):
            - 典型特征：鳞屑、断发、黑点、脱发斑、可能化脓
            - 需排除其他鳞屑性疾病

            **接触性皮炎** (ICD-10: L23):
            - 急性期：红斑、水肿、渗出、水疱
            - 慢性期：干燥、皲裂、苔藓化

            **休止期脱发** (ICD-10: L65.0):
            - 特征：弥漫性脱发、拉发试验阳性、无炎症
            - 需询问诱因（应激、产后、疾病）

            **3️⃣ 置信度评估标准**（必须提供依据）：
            - **80-100%**：存在3个以上典型临床特征，符合诊断金标准
            - **60-79%**：存在2个典型特征，但需排除其他可能
            - **40-59%**：仅有1-2个提示性特征，需进一步检查
            - **<40%**：仅有轻微可疑迹象，不足以确诊

            **4️⃣ 健康评分体系**（严格按临床标准）：
            - **95-100分**：完全健康，无任何异常（极少见）
            - **85-94分**：轻微异常（轻度油脂/少量头屑，无需治疗）
            - **70-84分**：轻度问题（需日常护理改善）
            - **50-69分**：中度问题（建议专业治疗）
            - **30-49分**：重度问题（需要及时就医）
            - **0-29分**：严重疾病（急需皮肤科诊治）

            **5️⃣ 专业治疗建议**（分级推荐）：
            - 一线治疗：首选方案（药物名称、浓度、用法）
            - 二线治疗：替代方案
            - 辅助措施：生活方式、护理建议
            - 禁忌事项：需要避免的行为或产品

            **📋 JSON返回格式**（严格遵守）：
            {
                "scalp_type": "油性/干性/正常/混合/敏感",
                "scalp_zone_analysis": {
                    "frontal": "前额区域详细观察",
                    "vertex": "头顶区域详细观察",
                    "temporal": "颞部区域详细观察",
                    "occipital": "枕部区域详细观察"
                },
                "conditions": [
                    {
                        "name_cn": "疾病中文名",
                        "name_en": "Disease English Name",
                        "icd10_code": "ICD-10编码",
                        "severity": "轻度/中度/重度",
                        "confidence": 置信度(0-100),
                        "diagnostic_evidence": "支持该诊断的3-5个具体临床证据",
                        "differential_diagnosis": "需要鉴别的2-3个疾病及鉴别要点",
                        "symptoms": ["观察到的客观体征"],
                        "description": "专业医学描述（含病理机制）"
                    }
                ],
                "health_score": 评分(0-100),
                "score_breakdown": {
                    "scalp_condition": "头皮状态评分(0-30)",
                    "hair_health": "毛发健康评分(0-30)",
                    "inflammation": "炎症情况评分(0-20)",
                    "overall_hygiene": "整体卫生评分(0-20)"
                },
                "recommendations": [
                    {
                        "category": "药物治疗/护理建议/生活方式",
                        "priority": "高/中/低",
                        "content": "具体建议内容",
                        "evidence_level": "A/B/C级证据"
                    }
                ],
                "need_doctor": true/false,
                "urgency_level": "紧急/尽快/建议/观察",
                "suggested_tests": ["建议进行的进一步检查（如真菌镜检、毛发镜检等）"],
                "analysis_summary": "200-300字的专业综合评估报告"
            }

            **⚠️ 专业标准（必须遵守）**：
            1. 使用循证医学证据，避免主观臆断
            2. 置信度必须有明确的临床依据支持
            3. 不确定时明确说明，不过度诊断
            4. 建议必须符合最新临床指南
            5. 严重情况必须建议就医，不可仅给护理建议
            6. 如非头皮照片，返回错误格式（如之前定义）

            **只返回JSON格式，无其他文字。**
            """
        else:
            prompt = """
            You are an experienced dermatologist specializing in scalp health diagnosis. Please carefully analyze this scalp image and provide a professional medical assessment.

            **Analysis Requirements** (strictly follow):
            1. Observe every detail in the image carefully
            2. Do NOT easily judge as "completely normal" - point out any minor issues
            3. Even for healthy scalps, indicate potential risk factors or improvement suggestions
            4. Use professional medical terminology while explaining clearly

            **Items to Check**:
            1. Scalp color (normal/redness/pale/yellow)
            2. Sebum secretion (excessive/normal/insufficient)
            3. Dandruff condition (none/mild/moderate/severe)
            4. Inflammation signs (erythema/papules/pustules)
            5. Follicle status (healthy/clogged/inflamed)
            6. Hair density (normal/sparse/loss)
            7. Skin texture (smooth/rough/scaly)
            8. Abnormal patches or lesions

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
                "scalp_type": "scalp type (oily/dry/normal/combination/sensitive)",
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
                "analysis_summary": "comprehensive analysis summary, including main issues and overall assessment"
            }

            **Important Notes**:
            - List any abnormalities, even if very minor
            - Don't easily give 90+ scores, be strict in assessment
            - Even for healthy-looking scalps, provide prevention advice
            - Symptom descriptions should be specific, not vague
            """

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Claude 3 Haiku - 快速且经济
                max_tokens=3000,  # 增加到3000，允许更详细的分析
                temperature=0,  # 0表示最确定性的输出，适合医学诊断
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
                    json_str = json_match.group()
                    result = json.loads(json_str)

                    # Save raw response for debugging
                    result['ai_raw_response'] = response_text
                else:
                    # If no JSON found, create structured response
                    result = {
                        "scalp_type": "Unknown",
                        "conditions": [],
                        "health_score": 50,
                        "recommendations": [response_text],
                        "need_doctor": False,
                        "analysis_summary": response_text,
                        "ai_raw_response": response_text
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
                    "parse_error": str(e)
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
            你是一位经验丰富的皮肤科医生，专门从事头皮健康诊断。请仔细分析这张头皮图像，进行专业的医学评估。

            **分析要求**（请严格遵守）：
            1. 仔细观察图像的每个细节
            2. 不要轻易判断为"完全正常"，任何轻微问题都应该指出
            3. 即使是健康的头皮，也要指出可能的风险因素或改善建议
            4. 使用专业医学术语，同时解释清楚

            **必须检查的项目**：
            1. 头皮颜色（正常/发红/苍白/黄色）
            2. 皮脂分泌（过多/正常/过少）
            3. 头屑情况（无/轻度/中度/严重）
            4. 炎症迹象（红斑/丘疹/脓疱）
            5. 毛囊状态（健康/堵塞/发炎）
            6. 头发密度（正常/稀疏/脱落）
            7. 皮肤纹理（光滑/粗糙/鳞屑）
            8. 异常斑块或病变

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
                "scalp_type": "头皮类型（油性/干性/正常/混合/敏感）",
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
                "analysis_summary": "综合分析总结，包括主要问题和整体评估"
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
            You are an experienced dermatologist specializing in scalp health diagnosis. Please carefully analyze this scalp image and provide a professional medical assessment.

            **Analysis Requirements** (strictly follow):
            1. Observe every detail in the image carefully
            2. Do NOT easily judge as "completely normal" - point out any minor issues
            3. Even for healthy scalps, indicate potential risk factors or improvement suggestions
            4. Use professional medical terminology while explaining clearly

            **Items to Check**:
            1. Scalp color (normal/redness/pale/yellow)
            2. Sebum secretion (excessive/normal/insufficient)
            3. Dandruff condition (none/mild/moderate/severe)
            4. Inflammation signs (erythema/papules/pustules)
            5. Follicle status (healthy/clogged/inflamed)
            6. Hair density (normal/sparse/loss)
            7. Skin texture (smooth/rough/scaly)
            8. Abnormal patches or lesions

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
                "scalp_type": "scalp type (oily/dry/normal/combination/sensitive)",
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
                "analysis_summary": "comprehensive analysis summary, including main issues and overall assessment"
            }

            **Important Notes**:
            - List any abnormalities, even if very minor
            - Don't easily give 90+ scores, be strict in assessment
            - Even for healthy-looking scalps, provide prevention advice
            - Symptom descriptions should be specific, not vague
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
                                        "text": prompt
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
                    used_model = model  # 记录成功使用的模型
                    print(f"[INFO] Successfully using model: {model}")  # 日志记录
                    break  # Success, exit loop

                except Exception as e:
                    error_msg = str(e)
                    last_error = e

                    # If model not found, try next model
                    if "model_not_found" in error_msg or "does not exist" in error_msg:
                        print(f"[WARN] Model {model} not available, trying next...")
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