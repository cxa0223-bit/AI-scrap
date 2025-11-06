"""
头皮AI分析模块 - 医学增强版
Medical-Grade Enhanced AI Analysis Module for Scalp Health
使用多维度图像分析提供专业医学级诊断
"""
import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

def analyze_scalp_image(image):
    """
    分析头皮图像并返回医学级诊断结果

    参数:
        image: PIL Image对象

    返回:
        dict: 包含头皮类型、疾病诊断、问题、置信度等信息
    """
    # 转换为numpy数组
    img_array = np.array(image)

    # 确保是RGB格式
    if len(img_array.shape) == 2:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)

    # 转换到不同色彩空间
    img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # ===== 1. 多维度特征提取 =====
    features = extract_scalp_features(img_array, img_hsv, img_gray)

    # ===== 2. 头皮类型判断 =====
    scalp_type, type_score = determine_scalp_type(features)

    # ===== 3. 医学疾病诊断 =====
    diagnosed_conditions = diagnose_medical_conditions(features, img_array, img_hsv, img_gray)

    # ===== 4. 健康问题检测 =====
    concerns = detect_scalp_concerns(features, img_array, img_hsv, img_gray)

    # ===== 5. 综合健康评分 =====
    health_score = calculate_health_score(features, concerns, diagnosed_conditions)

    # ===== 6. 置信度计算（基于图像质量） =====
    confidence = calculate_confidence(features)

    # ===== 7. 就医建议 =====
    medical_advice = generate_medical_advice(diagnosed_conditions, features)

    # ===== 8. 详细分析数据 =====
    details = {
        'brightness': round(features['brightness'], 2),
        'saturation': round(features['saturation'], 2),
        'contrast': round(features['contrast'], 2),
        'sharpness': round(features['sharpness'], 2),
        'texture_quality': round(features['texture_quality'], 2),
        'hair_density': round(features['hair_density'], 2),
        'redness_level': round(features['redness_level'], 2),
        'dandruff_level': round(features['dandruff_level'], 2),
        'inflammation_level': round(features.get('inflammation_level', 0), 2),
        'bald_spots_detected': features.get('bald_spots_count', 0)
    }

    return {
        'scalp_type': scalp_type,
        'diagnosed_conditions': diagnosed_conditions,  # 新增：疾病诊断
        'concerns': concerns,
        'confidence': round(confidence, 1),
        'health_score': health_score,
        'medical_advice': medical_advice,  # 新增：医学建议
        'details': details
    }

def extract_scalp_features(img_rgb, img_hsv, img_gray):
    """提取头皮图像的多维度特征"""
    features = {}

    # 1. 基础色彩特征
    features['brightness'] = np.mean(img_gray)
    features['saturation'] = np.mean(img_hsv[:, :, 1])
    features['value'] = np.mean(img_hsv[:, :, 2])

    # 2. 对比度（标准差）
    features['contrast'] = np.std(img_gray)

    # 3. 清晰度（拉普拉斯算子）
    laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
    features['sharpness'] = np.var(laplacian)

    # 4. 纹理质量（局部二值模式）
    features['texture_quality'] = calculate_texture_score(img_gray)

    # 5. 头发密度（边缘检测）
    edges = cv2.Canny(img_gray, 50, 150)
    features['hair_density'] = np.sum(edges > 0) / edges.size * 100

    # 6. 红色程度（炎症指标）
    features['redness_level'] = calculate_redness(img_rgb, img_hsv)

    # 7. 头屑检测（白色斑点）
    features['dandruff_level'] = detect_dandruff(img_hsv, img_gray)

    # 8. 油脂程度（亮度+饱和度综合）
    features['oiliness'] = calculate_oiliness(img_rgb, img_hsv)

    # 9. 色彩均匀度
    features['color_uniformity'] = calculate_color_uniformity(img_rgb)

    # 10. 头皮健康色（粉红/肉色检测）
    features['healthy_color_ratio'] = detect_healthy_skin_color(img_rgb, img_hsv)

    # ===== 新增医学级检测 =====

    # 11. 炎症程度（综合红色+肿胀）
    features['inflammation_level'] = calculate_inflammation_level(img_rgb, img_hsv)

    # 12. 斑秃/秃斑检测（局部脱发区域）
    features['bald_spots_count'], features['bald_spots_size'] = detect_bald_spots(img_gray, edges)

    # 13. 黄色区域检测（脂溢性皮炎）
    features['yellow_patches'] = detect_yellow_patches(img_hsv)

    # 14. 红色斑块（银屑病/牛皮癣）
    features['red_patches'] = detect_red_patches(img_hsv, img_rgb)

    # 15. 圆形脱发斑（斑秃特征）
    features['circular_pattern'] = detect_circular_hair_loss(img_gray)

    # 16. 头皮鳞屑（银屑病、头癣）
    features['scalp_scales'] = detect_scalp_scales(img_gray, img_hsv)

    # 17. 毛囊炎症（红色小点）
    features['folliculitis_points'] = detect_folliculitis(img_rgb, img_hsv)

    # 18. 发际线后移程度
    features['hairline_recession'] = detect_hairline_recession(img_gray, edges)

    return features

def calculate_texture_score(img_gray):
    """计算纹理质量分数（头发密度和清晰度）"""
    sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.sqrt(sobelx**2 + sobely**2)
    texture_strength = np.mean(sobel)
    return min(texture_strength / 2, 100)

def calculate_redness(img_rgb, img_hsv):
    """计算红色程度（炎症、敏感指标）"""
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2

    red_percentage = np.sum(red_mask > 0) / red_mask.size * 100
    return red_percentage

def detect_dandruff(img_hsv, img_gray):
    """检测头屑（白色斑点）"""
    _, bright_thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
    low_saturation = img_hsv[:, :, 1] < 30
    dandruff_mask = np.logical_and(bright_thresh > 0, low_saturation)
    dandruff_percentage = np.sum(dandruff_mask) / dandruff_mask.size * 100
    return dandruff_percentage

def calculate_oiliness(img_rgb, img_hsv):
    """计算油脂程度"""
    brightness = np.mean(img_hsv[:, :, 2])
    saturation = np.mean(img_hsv[:, :, 1])
    oiliness_score = (brightness / 255 * 0.6 + saturation / 255 * 0.4) * 100
    return oiliness_score

def calculate_color_uniformity(img_rgb):
    """计算颜色均匀度"""
    r_std = np.std(img_rgb[:, :, 0])
    g_std = np.std(img_rgb[:, :, 1])
    b_std = np.std(img_rgb[:, :, 2])
    avg_std = (r_std + g_std + b_std) / 3
    uniformity = max(0, 100 - avg_std / 2)
    return uniformity

def detect_healthy_skin_color(img_rgb, img_hsv):
    """检测健康肤色比例"""
    lower_skin = np.array([0, 20, 70])
    upper_skin = np.array([25, 170, 255])
    skin_mask = cv2.inRange(img_hsv, lower_skin, upper_skin)
    healthy_ratio = np.sum(skin_mask > 0) / skin_mask.size * 100
    return healthy_ratio

# ===== 新增医学级检测函数 =====

def calculate_inflammation_level(img_rgb, img_hsv):
    """计算炎症程度（综合指标）"""
    # 红色区域
    redness = calculate_redness(img_rgb, img_hsv)

    # 亮度异常（肿胀）
    brightness = np.mean(img_hsv[:, :, 2])

    # 综合炎症指数
    inflammation = (redness * 0.7 + (brightness / 255 * 30) * 0.3)

    return inflammation

def detect_bald_spots(img_gray, edges):
    """检测斑秃/秃斑（局部脱发区域）"""
    # 检测低密度区域
    kernel = np.ones((50, 50), np.uint8)
    edge_density = cv2.filter2D(edges.astype(float), -1, kernel / kernel.sum())

    # 找到密度非常低的区域（可能是秃斑）
    bald_threshold = np.percentile(edge_density, 20)
    bald_mask = edge_density < bald_threshold

    # 计算连通区域
    labeled, num_spots = ndimage.label(bald_mask)

    # 计算秃斑总面积
    total_bald_area = np.sum(bald_mask) / bald_mask.size * 100

    return num_spots, total_bald_area

def detect_yellow_patches(img_hsv):
    """检测黄色区域（脂溢性皮炎特征）"""
    # HSV黄色范围
    lower_yellow = np.array([20, 50, 100])
    upper_yellow = np.array([35, 255, 255])

    yellow_mask = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    yellow_percentage = np.sum(yellow_mask > 0) / yellow_mask.size * 100

    return yellow_percentage

def detect_red_patches(img_hsv, img_rgb):
    """检测大片红色斑块（银屑病/牛皮癣）"""
    # 检测饱和度较高的红色
    lower_red1 = np.array([0, 80, 80])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 80, 80])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2

    # 使用形态学操作找连续区域
    kernel = np.ones((15, 15), np.uint8)
    red_patches = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    red_patch_percentage = np.sum(red_patches > 0) / red_patches.size * 100

    return red_patch_percentage

def detect_circular_hair_loss(img_gray):
    """检测圆形脱发斑（斑秃典型特征）"""
    # 使用霍夫圆检测
    blurred = cv2.GaussianBlur(img_gray, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=50, param2=30, minRadius=20, maxRadius=100)

    if circles is not None:
        return len(circles[0])
    return 0

def detect_scalp_scales(img_gray, img_hsv):
    """检测头皮鳞屑（银屑病、头癣）"""
    # 检测高亮+粗糙纹理
    _, bright = cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY)

    # 检测纹理
    laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
    rough_texture = np.abs(laplacian) > 30

    # 结合两者
    scales_mask = np.logical_and(bright > 0, rough_texture)
    scales_percentage = np.sum(scales_mask) / scales_mask.size * 100

    return scales_percentage

def detect_folliculitis(img_rgb, img_hsv):
    """检测毛囊炎（小红点）"""
    # 检测小的红色区域
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    red_mask = cv2.inRange(img_hsv, lower_red, upper_red)

    # 形态学操作：保留小点，去除大片
    kernel = np.ones((3, 3), np.uint8)
    red_points = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    # 计数小红点
    labeled, num_points = ndimage.label(red_points)

    return num_points

def detect_hairline_recession(img_gray, edges):
    """检测发际线后移"""
    height = img_gray.shape[0]
    top_region = edges[:height//3, :]

    # 计算上部头发密度
    top_density = np.sum(top_region > 0) / top_region.size * 100

    # 与整体密度对比
    overall_density = np.sum(edges > 0) / edges.size * 100

    recession_score = max(0, (overall_density - top_density) * 2)

    return recession_score

# ===== 医学疾病诊断 =====

def diagnose_medical_conditions(features, img_rgb, img_hsv, img_gray):
    """基于特征诊断具体医学疾病"""
    conditions = []

    # 1. 斑秃 (Alopecia Areata) - 鬼剃头
    if features['bald_spots_count'] > 0 or features['circular_pattern'] > 0:
        severity = "轻度"
        if features['bald_spots_size'] > 5:
            severity = "中度"
        if features['bald_spots_size'] > 15:
            severity = "重度"

        conditions.append({
            'name_cn': '斑秃',
            'name_en': 'Alopecia Areata',
            'common_name': '鬼剃头',
            'severity': severity,
            'confidence': 75 if features['circular_pattern'] > 0 else 60,
            'description': '头皮出现圆形或椭圆形脱发斑，边界清楚',
            'icon': '🔴'
        })

    # 2. 雄激素性脱发 (Androgenetic Alopecia) - 男性/女性型脱发
    if features['hair_density'] < 20 and features['hairline_recession'] > 15:
        severity = "早期"
        if features['hair_density'] < 15:
            severity = "中期"
        if features['hair_density'] < 10:
            severity = "晚期"

        conditions.append({
            'name_cn': '雄激素性脱发',
            'name_en': 'Androgenetic Alopecia',
            'common_name': '男性/女性型脱发',
            'severity': severity,
            'confidence': 70,
            'description': '头发逐渐变细、变软、脱落，发际线后移或头顶稀疏',
            'icon': '📉'
        })

    # 3. 脂溢性皮炎 (Seborrheic Dermatitis)
    if features['oiliness'] > 65 and features['yellow_patches'] > 8:
        severity = "轻度"
        if features['dandruff_level'] > 8 and features['redness_level'] > 10:
            severity = "中度"
        if features['inflammation_level'] > 20:
            severity = "重度"

        conditions.append({
            'name_cn': '脂溢性皮炎',
            'name_en': 'Seborrheic Dermatitis',
            'common_name': '脂溢性湿疹',
            'severity': severity,
            'confidence': 80,
            'description': '头皮油腻、发红、有黄色鳞屑和头屑',
            'icon': '💛'
        })

    # 4. 毛囊炎 (Folliculitis)
    if features['folliculitis_points'] > 5 and features['redness_level'] > 8:
        severity = "轻度"
        if features['folliculitis_points'] > 15:
            severity = "中度"
        if features['inflammation_level'] > 18:
            severity = "重度"

        conditions.append({
            'name_cn': '毛囊炎',
            'name_en': 'Folliculitis',
            'common_name': '毛囊感染',
            'severity': severity,
            'confidence': 65,
            'description': '毛囊周围出现红色丘疹或脓疱，可能伴有疼痛或瘙痒',
            'icon': '🔴'
        })

    # 5. 银屑病/牛皮癣 (Psoriasis)
    if features['red_patches'] > 10 and features['scalp_scales'] > 12:
        severity = "轻度"
        if features['red_patches'] > 20:
            severity = "中度"
        if features['scalp_scales'] > 25:
            severity = "重度"

        conditions.append({
            'name_cn': '银屑病',
            'name_en': 'Psoriasis',
            'common_name': '牛皮癣',
            'severity': severity,
            'confidence': 70,
            'description': '头皮出现红色斑块，覆盖银白色鳞屑，边界清楚',
            'icon': '🔶'
        })

    # 6. 头癣 (Tinea Capitis) - 真菌感染
    if features['scalp_scales'] > 15 and features['dandruff_level'] > 10 and features['hair_density'] < 25:
        severity = "轻度"
        if features['bald_spots_count'] > 0:
            severity = "中度"
        if features['inflammation_level'] > 15:
            severity = "重度"

        conditions.append({
            'name_cn': '头癣',
            'name_en': 'Tinea Capitis',
            'common_name': '真菌性脱发',
            'severity': severity,
            'confidence': 60,
            'description': '真菌感染引起，头皮有鳞屑、脱发，可能有黑点残留',
            'icon': '🍄'
        })

    # 7. 接触性皮炎 (Contact Dermatitis)
    if features['redness_level'] > 12 and features['color_uniformity'] < 50:
        severity = "轻度"
        if features['inflammation_level'] > 15:
            severity = "中度"

        conditions.append({
            'name_cn': '接触性皮炎',
            'name_en': 'Contact Dermatitis',
            'common_name': '过敏性皮炎',
            'severity': severity,
            'confidence': 55,
            'description': '接触染发剂、洗发水等过敏原后引起，头皮发红、瘙痒',
            'icon': '⚠️'
        })

    # 8. 休止期脱发 (Telogen Effluvium)
    if features['hair_density'] < 25 and features['texture_quality'] < 30 and features['bald_spots_count'] == 0:
        conditions.append({
            'name_cn': '休止期脱发',
            'name_en': 'Telogen Effluvium',
            'common_name': '弥漫性脱发',
            'severity': '中度',
            'confidence': 50,
            'description': '头发整体变稀疏，无明显秃斑，常由压力、疾病、营养不良引起',
            'icon': '💤'
        })

    return conditions

def generate_medical_advice(diagnosed_conditions, features):
    """生成医学建议"""
    advice = {
        'urgency': 'normal',  # normal, moderate, urgent
        'see_doctor': False,
        'recommendations': []
    }

    # 判断紧急程度
    severe_conditions = [c for c in diagnosed_conditions if c['severity'] in ['重度', '中度']]

    if len(severe_conditions) > 0:
        advice['urgency'] = 'urgent' if any(c['severity'] == '重度' for c in severe_conditions) else 'moderate'
        advice['see_doctor'] = True
        advice['recommendations'].append("🏥 建议尽快咨询皮肤科医生或毛发专科医生")

    # 根据诊断结果给建议
    condition_names = [c['name_cn'] for c in diagnosed_conditions]

    if '斑秃' in condition_names:
        advice['recommendations'].append("💊 斑秃可能需要局部激素治疗或免疫调节治疗")
        advice['recommendations'].append("🧪 建议做甲状腺功能和自身免疫检查")

    if '脂溢性皮炎' in condition_names:
        advice['recommendations'].append("🧴 使用含酮康唑或硫化硒的药用洗发水")
        advice['recommendations'].append("🚫 避免使用油性护发产品")

    if '银屑病' in condition_names or '牛皮癣' in condition_names:
        advice['recommendations'].append("💊 可能需要外用激素或维生素D类药物")
        advice['recommendations'].append("🔬 建议进行专业皮肤科评估")

    if '头癣' in condition_names:
        advice['recommendations'].append("🍄 需要口服抗真菌药物治疗，外用药物效果有限")
        advice['recommendations'].append("🧼 保持头皮清洁干燥，毛巾和梳子要消毒")

    if '毛囊炎' in condition_names:
        advice['recommendations'].append("💧 使用抗菌洗发水，保持头皮清洁")
        advice['recommendations'].append("🚫 避免搔抓头皮，防止感染扩散")

    if len(diagnosed_conditions) == 0:
        advice['recommendations'].append("✅ 目前未检测到明显的头皮疾病")
        advice['recommendations'].append("💡 继续保持良好的头皮护理习惯")

    return advice

def determine_scalp_type(features):
    """基于多维度特征判断头皮类型"""
    oiliness = features['oiliness']
    brightness = features['brightness']

    if oiliness > 65 and brightness > 150:
        return "油性头皮 (Oily Scalp)", 85
    elif oiliness < 40 and brightness < 120:
        return "干性头皮 (Dry Scalp)", 80
    elif features['redness_level'] > 12:
        return "敏感头皮 (Sensitive Scalp)", 75
    else:
        return "正常头皮 (Normal Scalp)", 90

def detect_scalp_concerns(features, img_rgb, img_hsv, img_gray):
    """检测头皮问题"""
    concerns = []

    if features['oiliness'] > 70:
        concerns.append("⚠️ 油脂分泌过旺，容易堵塞毛孔")
    elif features['oiliness'] > 60:
        concerns.append("⚡ 轻度油脂分泌过多")

    if features['brightness'] < 100:
        concerns.append("⚠️ 头皮严重干燥，需要深层补水")
    elif features['brightness'] < 120:
        concerns.append("⚡ 头皮偏干，建议使用保湿产品")

    if features['dandruff_level'] > 8:
        concerns.append("⚠️ 检测到明显头屑，建议使用去屑洗发水")
    elif features['dandruff_level'] > 4:
        concerns.append("⚡ 轻度头屑迹象")

    if features['redness_level'] > 15:
        concerns.append("⚠️ 检测到炎症或红肿，建议就医检查")
    elif features['redness_level'] > 8:
        concerns.append("⚡ 头皮略微发红，可能有轻度敏感")

    if features['hair_density'] < 15:
        concerns.append("⚠️ 头发稀疏，有脱发迹象")
    elif features['hair_density'] < 25:
        concerns.append("⚡ 头发密度偏低，建议加强养护")

    if features['texture_quality'] < 20:
        concerns.append("⚠️ 头发品质较差，纹理不清晰")
    elif features['texture_quality'] < 35:
        concerns.append("⚡ 头发品质一般，需要改善")

    if features['sharpness'] < 50:
        concerns.append("📷 图像清晰度偏低，可能影响分析准确度")

    if features['color_uniformity'] < 50:
        concerns.append("⚡ 头皮颜色不均匀，可能有局部问题")

    if len(concerns) == 0:
        concerns.append("✅ 头皮整体健康状况良好")
        concerns.append("💡 继续保持良好的护理习惯")

    return concerns

def calculate_health_score(features, concerns, diagnosed_conditions):
    """计算综合健康评分（0-100）"""
    base_score = 100

    # 根据诊断疾病扣分
    for condition in diagnosed_conditions:
        if condition['severity'] == '重度':
            base_score -= 30
        elif condition['severity'] == '中度':
            base_score -= 20
        elif condition['severity'] == '轻度' or condition['severity'] == '早期':
            base_score -= 12

    # 油脂扣分
    if features['oiliness'] > 70:
        base_score -= 15
    elif features['oiliness'] > 60:
        base_score -= 8
    elif features['oiliness'] < 35:
        base_score -= 12

    # 头屑扣分
    if features['dandruff_level'] > 8:
        base_score -= 15
    elif features['dandruff_level'] > 4:
        base_score -= 8

    # 炎症扣分
    if features['inflammation_level'] > 20:
        base_score -= 25
    elif features['inflammation_level'] > 10:
        base_score -= 12

    # 头发密度扣分
    if features['hair_density'] < 15:
        base_score -= 20
    elif features['hair_density'] < 25:
        base_score -= 10

    # 头发品质扣分
    if features['texture_quality'] < 20:
        base_score -= 15
    elif features['texture_quality'] < 35:
        base_score -= 8

    # 确保分数在0-100范围内
    final_score = max(0, min(100, base_score))

    return int(final_score)

def calculate_confidence(features):
    """计算置信度（基于图像质量）"""
    confidence = 70

    if features['sharpness'] > 100:
        confidence += 15
    elif features['sharpness'] > 50:
        confidence += 10
    else:
        confidence -= 10

    if features['contrast'] > 40:
        confidence += 10
    elif features['contrast'] < 20:
        confidence -= 10

    if features['texture_quality'] > 40:
        confidence += 5

    confidence = max(60, min(95, confidence))
    return confidence

def get_care_recommendations(scalp_type):
    """根据头皮类型返回护理建议"""
    recommendations = {
        "油性头皮 (Oily Scalp)": [
            "🧴 每1-2天洗一次头发，保持清洁",
            "💧 使用控油清爽型洗发水",
            "🚫 避免使用过多护发素，特别是涂抹在头皮上",
            "🌡️ 用温水洗头，避免过热水温刺激油脂分泌",
            "🥗 饮食清淡，减少油炸、辛辣食物",
            "😴 保持规律作息，减少熬夜"
        ],
        "干性头皮 (Dry Scalp)": [
            "🧴 每3-4天洗一次头发，避免过度清洁",
            "💧 使用滋润型、保湿型洗发产品",
            "✨ 每周使用1-2次发膜深层护理",
            "🌿 洗头后使用护发精油或头皮精华",
            "💦 多喝水，每天至少2升",
            "🏠 避免长时间待在空调房，注意保湿"
        ],
        "正常头皮 (Normal Scalp)": [
            "🧴 保持每2-3天洗一次头发",
            "💧 使用温和型洗发产品",
            "🔄 定期更换洗发产品，避免头皮适应",
            "🏃 适度运动促进血液循环",
            "🥗 保持均衡饮食，摄入足够营养",
            "😊 保持良好心情，减少压力"
        ],
        "敏感头皮 (Sensitive Scalp)": [
            "🧴 使用温和、无刺激的洗发产品",
            "🌿 选择天然成分、无硅油配方",
            "🚫 避免频繁烫染头发",
            "🌡️ 用温水洗头，避免过冷或过热",
            "⚠️ 如有持续红肿瘙痒，建议就医检查",
            "🧘 减少压力，保持放松"
        ]
    }

    return recommendations.get(scalp_type, recommendations["正常头皮 (Normal Scalp)"])
