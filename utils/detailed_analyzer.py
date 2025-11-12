"""
Enhanced Scalp Detailed Analysis Module
增强版头皮详细分析模块
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple
import colorsys

class DetailedScalpAnalyzer:
    """详细头皮分析器"""

    @staticmethod
    def analyze_scalp_layers(img_array: np.ndarray, img_hsv: np.ndarray) -> Dict:
        """
        分析头皮层结构
        Analyze scalp layer structure
        """
        layers_analysis = {
            'epidermis': {  # 表皮层
                'thickness': 'normal',  # 厚度
                'keratinization': 'normal',  # 角质化程度
                'barrier_function': 'good',  # 屏障功能
                'cell_turnover': 'normal',  # 细胞更新
                'issues': []
            },
            'dermis': {  # 真皮层
                'collagen_density': 'normal',  # 胶原蛋白密度
                'elasticity': 'good',  # 弹性
                'blood_circulation': 'normal',  # 血液循环
                'inflammation': 'none',  # 炎症
                'issues': []
            },
            'follicles': {  # 毛囊
                'density': 0,  # 密度
                'health': 'normal',  # 健康状态
                'blockage': 'none',  # 堵塞情况
                'inflammation': 'none',  # 炎症
                'miniaturization': 'none',  # 毛囊萎缩
                'issues': []
            },
            'sebaceous_glands': {  # 皮脂腺
                'activity': 'normal',  # 活动性
                'secretion_level': 'moderate',  # 分泌水平
                'blockage': 'none',  # 堵塞
                'inflammation': 'none',  # 炎症
                'issues': []
            }
        }

        # 分析角质层（通过纹理和颜色）
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        texture = cv2.Laplacian(gray, cv2.CV_64F)
        texture_std = np.std(texture)

        if texture_std > 40:
            layers_analysis['epidermis']['keratinization'] = 'excessive'
            layers_analysis['epidermis']['issues'].append('角质层过厚')
        elif texture_std < 15:
            layers_analysis['epidermis']['thickness'] = 'thin'
            layers_analysis['epidermis']['barrier_function'] = 'weak'
            layers_analysis['epidermis']['issues'].append('表皮层薄弱')

        # 分析血液循环（通过红色成分）
        red_channel = img_array[:, :, 0]
        red_mean = np.mean(red_channel)

        if red_mean > 150:
            layers_analysis['dermis']['blood_circulation'] = 'hyperemic'
            layers_analysis['dermis']['inflammation'] = 'mild'
            layers_analysis['dermis']['issues'].append('充血状态')
        elif red_mean < 100:
            layers_analysis['dermis']['blood_circulation'] = 'poor'
            layers_analysis['dermis']['issues'].append('血液循环不良')

        # 分析皮脂腺活动（通过油光检测）
        brightness = img_hsv[:, :, 2]
        bright_pixels = np.sum(brightness > 200) / brightness.size

        if bright_pixels > 0.3:
            layers_analysis['sebaceous_glands']['activity'] = 'hyperactive'
            layers_analysis['sebaceous_glands']['secretion_level'] = 'excessive'
            layers_analysis['sebaceous_glands']['issues'].append('皮脂分泌过多')
        elif bright_pixels < 0.05:
            layers_analysis['sebaceous_glands']['activity'] = 'hypoactive'
            layers_analysis['sebaceous_glands']['secretion_level'] = 'insufficient'
            layers_analysis['sebaceous_glands']['issues'].append('皮脂分泌不足')

        return layers_analysis

    @staticmethod
    def detect_micro_symptoms(img_array: np.ndarray, img_hsv: np.ndarray) -> Dict:
        """
        检测微观症状
        Detect microscopic symptoms
        """
        symptoms = {
            'red_dots': [],  # 红点
            'white_flakes': [],  # 白色鳞屑
            'yellow_crusts': [],  # 黄色结痂
            'pustules': [],  # 脓包
            'papules': [],  # 丘疹
            'telangiectasia': [],  # 毛细血管扩张
            'pigmentation': [],  # 色素沉着
            'erosions': [],  # 糜烂
            'excoriations': [],  # 抓痕
            'comedones': []  # 黑头/白头
        }

        # 检测红点和红斑
        red_dots = DetailedScalpAnalyzer._detect_red_dots(img_array, img_hsv)
        symptoms['red_dots'] = red_dots

        # 检测白色鳞屑
        white_flakes = DetailedScalpAnalyzer._detect_white_flakes(img_array, img_hsv)
        symptoms['white_flakes'] = white_flakes

        # 检测脓包和丘疹
        pustules = DetailedScalpAnalyzer._detect_pustules(img_array)
        symptoms['pustules'] = pustules

        # 检测毛细血管扩张
        telangiectasia = DetailedScalpAnalyzer._detect_telangiectasia(img_array)
        symptoms['telangiectasia'] = telangiectasia

        # 检测色素沉着
        pigmentation = DetailedScalpAnalyzer._detect_pigmentation(img_array, img_hsv)
        symptoms['pigmentation'] = pigmentation

        return symptoms

    @staticmethod
    def _detect_red_dots(img_array: np.ndarray, img_hsv: np.ndarray) -> List[Dict]:
        """检测红点/红斑 - 增强版"""
        red_dots = []

        # 方法1: 在HSV中检测红色区域（显微镜模式 - 检测粉红色调）
        # 显微镜照片中红色区域通常呈现粉红色（高亮度，低饱和度）
        lower_red1 = np.array([0, 5, 150])      # 显微镜模式: 极低饱和，高亮度粉红色
        upper_red1 = np.array([15, 80, 255])    # 扩大色调和饱和度范围
        lower_red2 = np.array([160, 5, 150])    # 显微镜模式: 粉红色调
        upper_red2 = np.array([180, 80, 255])

        mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
        hsv_red_mask = mask1 + mask2

        # 方法2: 在RGB空间检测红色（显微镜模式 - 检测高亮粉红区）
        # 红色通道略高于其他通道，且整体亮度高
        r_channel = img_array[:, :, 0].astype(float)
        g_channel = img_array[:, :, 1].astype(float)
        b_channel = img_array[:, :, 2].astype(float)

        # 粉红色检测（显微镜模式：轻微红色优势 + 高亮度）
        red_dominance = (r_channel - g_channel) + (r_channel - b_channel)
        brightness = (r_channel + g_channel + b_channel) / 3
        rgb_red_mask = ((red_dominance > 3) & (r_channel > 150) & (brightness > 140)).astype(np.uint8) * 255  # 显微镜模式

        # 合并两种检测方法
        red_mask = cv2.bitwise_or(hsv_red_mask, rgb_red_mask)

        # 形态学操作去除噪声（最小化处理以保留更多特征）
        kernel_small = np.ones((1, 1), np.uint8)  # 减小 (2,2)->(1,1)
        kernel_large = np.ones((2, 2), np.uint8)  # 减小 (3,3)->(2,2)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel_small)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel_large)

        # 调试输出
        print(f"[DEBUG RED] HSV mask pixels: {np.sum(hsv_red_mask > 0)}")
        print(f"[DEBUG RED] RGB mask pixels: {np.sum(rgb_red_mask > 0)}")
        print(f"[DEBUG RED] Combined mask pixels: {np.sum(red_mask > 0)}")

        # 查找轮廓
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"[DEBUG RED] Found {len(contours)} contours")

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1:  # 极低面积阈值 (3->1)
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # 计算红点大小
                    radius = int(np.sqrt(area / np.pi))

                    red_dots.append({
                        'center': (cx, cy),  # 修改：使用'center'而不是'position'以匹配标注器
                        'position': (cx, cy),  # 保留兼容性
                        'size': radius,
                        'area': area,
                        'intensity': 'high' if area > 50 else 'moderate' if area > 20 else 'low',
                        'type': '红斑' if area > 100 else '红点'
                    })

        print(f"[DEBUG RED] Total red_dots appended: {len(red_dots)}")
        return red_dots

    @staticmethod
    def _detect_white_flakes(img_array: np.ndarray, img_hsv: np.ndarray) -> List[Dict]:
        """检测白色鳞屑/头皮屑 - 增强版"""
        white_flakes = []

        # 转换到LAB色彩空间（对白色检测更准确）
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)

        # 提取HSV通道
        saturation = img_hsv[:, :, 1]
        value = img_hsv[:, :, 2]

        # 方法1: 高亮度低饱和度检测（纯白色鳞屑）- 针对显微镜照片的极亮白点
        pure_white_mask = np.logical_and(
            np.logical_and(value > 200, saturation < 100),  # 显微镜模式: 检测极亮白点
            l_channel > 180  # 显微镜模式: 极高亮度
        ).astype(np.uint8) * 255

        # 方法2: 银白色鳞屑检测（中高亮度，极低饱和度）- 针对显微镜反光
        silver_white_mask = np.logical_and(
            np.logical_and(value > 180, saturation < 80),  # 显微镜模式: 高亮反光
            np.logical_and(l_channel > 160, l_channel <= 220)  # 显微镜模式: 亮区
        ).astype(np.uint8) * 255

        # 方法3: 黄色油腻性鳞屑检测（脂溢性皮炎特征）- 显微镜下的油脂反光
        # 黄色：低饱和度，中等亮度，b通道偏正（黄色）
        yellow_flakes_mask = np.logical_and(
            np.logical_and(value > 150, value < 245),  # 显微镜模式: 高亮油脂
            np.logical_and(saturation > 5, saturation < 60)  # 显微镜模式: 低饱和
        )
        yellow_flakes_mask = np.logical_and(yellow_flakes_mask, b_channel > 125).astype(np.uint8) * 255  # 显微镜模式

        # 合并所有鳞屑类型
        white_mask = cv2.bitwise_or(pure_white_mask, silver_white_mask)
        white_mask = cv2.bitwise_or(white_mask, yellow_flakes_mask)

        # 使用边缘检测增强鳞屑轮廓
        edges = cv2.Canny(img_array, 50, 150)
        white_mask = cv2.bitwise_and(white_mask, cv2.dilate(edges, np.ones((2, 2), np.uint8)))

        # 形态学操作（更精细）
        kernel_small = np.ones((2, 2), np.uint8)
        kernel = np.ones((3, 3), np.uint8)
        white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, kernel_small)
        white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel)

        # 调试输出
        print(f"[DEBUG FLAKE] Pure white mask pixels: {np.sum(pure_white_mask > 0)}")
        print(f"[DEBUG FLAKE] Silver mask pixels: {np.sum(silver_white_mask > 0)}")
        print(f"[DEBUG FLAKE] Yellow mask pixels: {np.sum(yellow_flakes_mask > 0)}")
        print(f"[DEBUG FLAKE] Combined mask pixels: {np.sum(white_mask > 0)}")

        # 查找轮廓
        contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"[DEBUG FLAKE] Found {len(contours)} contours")

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1:  # 极度降低阈值，检测更小的鳞屑 (4->1)
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # 计算形状特征
                    perimeter = cv2.arcLength(contour, True)
                    circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0

                    # 分析鳞屑颜色类型
                    mask = np.zeros(img_array.shape[:2], np.uint8)
                    cv2.drawContours(mask, [contour], -1, 255, -1)

                    # 计算该区域的平均颜色
                    mean_color = cv2.mean(img_array, mask=mask)[:3]
                    mean_sat = cv2.mean(img_hsv[:, :, 1], mask=mask)[0]
                    mean_b = cv2.mean(b_channel, mask=mask)[0]

                    # 判断鳞屑类型
                    if mean_sat < 30 and mean_color[0] > 200:
                        flake_color = '纯白色'
                        flake_nature = '干性'
                    elif mean_sat < 40 and mean_color[0] > 180:
                        flake_color = '银白色'
                        flake_nature = '干性'
                    elif mean_b > 130 and mean_sat > 20:
                        flake_color = '黄色'
                        flake_nature = '油性'
                    else:
                        flake_color = '灰白色'
                        flake_nature = '混合'

                    white_flakes.append({
                        'center': (cx, cy),  # 修改：使用'center'而不是'position'以匹配标注器
                        'position': (cx, cy),  # 保留兼容性
                        'area': area,
                        'type': '大片鳞屑' if area > 200 else '中等鳞屑' if area > 50 else '小片鳞屑' if area > 20 else '细小皮屑',
                        'color': flake_color,
                        'nature': flake_nature,
                        'shape': 'circular' if circularity > 0.7 else 'irregular',
                        'severity': 'severe' if area > 200 else 'moderate' if area > 50 else 'mild'
                    })

        print(f"[DEBUG FLAKE] Total white_flakes appended: {len(white_flakes)}")
        return white_flakes

    @staticmethod
    def _detect_pustules(img_array: np.ndarray) -> List[Dict]:
        """检测脓包和炎性丘疹"""
        pustules = []

        # 转换为灰度图
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # 使用自适应阈值检测凸起
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)

        # 形态学操作
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # 查找轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if 20 < area < 500:  # 脓包的典型大小范围
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # 检查中心是否有白色/黄色（脓液）
                    center_color = img_array[cy, cx] if cy < img_array.shape[0] and cx < img_array.shape[1] else [0, 0, 0]
                    is_pustule = center_color[0] > 200 and center_color[1] > 180  # 黄白色

                    pustules.append({
                        'position': (cx, cy),
                        'area': area,
                        'type': '脓包' if is_pustule else '炎性丘疹',
                        'stage': 'mature' if is_pustule else 'developing',
                        'severity': 'severe' if area > 100 else 'moderate' if area > 50 else 'mild'
                    })

        return pustules

    @staticmethod
    def _detect_telangiectasia(img_array: np.ndarray) -> List[Dict]:
        """检测毛细血管扩张"""
        vessels = []

        # 提取红色通道
        red_channel = img_array[:, :, 0]

        # 使用Gabor滤波器检测线性结构
        ksize = 31
        sigma = 4.0
        theta = np.pi / 4
        lamda = 10.0
        gamma = 0.5

        kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)
        filtered = cv2.filter2D(red_channel, cv2.CV_8UC3, kernel)

        # 阈值处理
        _, binary = cv2.threshold(filtered, 150, 255, cv2.THRESH_BINARY)

        # 使用形态学操作代替细化处理
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        thinned = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

        # 查找轮廓
        contours, _ = cv2.findContours(thinned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            length = cv2.arcLength(contour, False)
            if length > 20:  # 只检测较长的血管
                vessels.append({
                    'length': length,
                    'type': 'telangiectasia',
                    'severity': 'prominent' if length > 50 else 'visible'
                })

        return vessels

    @staticmethod
    def _detect_pigmentation(img_array: np.ndarray, img_hsv: np.ndarray) -> List[Dict]:
        """检测色素沉着"""
        pigmentations = []

        # 转换为LAB颜色空间更好地检测色素
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)

        # 检测暗区（色素沉着）
        dark_mask = l < 100

        # 形态学操作
        kernel = np.ones((5, 5), np.uint8)
        dark_mask = cv2.morphologyEx(dark_mask.astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)

        # 查找轮廓
        contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # 计算色素深度
                    mask = np.zeros(l.shape, np.uint8)
                    cv2.drawContours(mask, [contour], -1, 255, -1)
                    mean_darkness = np.mean(l[mask == 255])

                    pigmentations.append({
                        'position': (cx, cy),
                        'area': area,
                        'darkness_level': mean_darkness,
                        'type': '炎症后色素沉着' if mean_darkness < 80 else '轻度色素沉着',
                        'severity': 'severe' if mean_darkness < 60 else 'moderate' if mean_darkness < 80 else 'mild'
                    })

        return pigmentations

    @staticmethod
    def analyze_scalp_condition_detailed(img_array: np.ndarray) -> Dict:
        """
        执行完整的详细头皮分析
        Perform complete detailed scalp analysis
        """
        # 转换颜色空间
        img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        # 分析头皮层
        layers = DetailedScalpAnalyzer.analyze_scalp_layers(img_array, img_hsv)

        # 检测微观症状
        symptoms = DetailedScalpAnalyzer.detect_micro_symptoms(img_array, img_hsv)

        # 统计分析
        total_red_dots = len(symptoms['red_dots'])
        total_flakes = len(symptoms['white_flakes'])
        total_pustules = len(symptoms['pustules'])
        total_vessels = len(symptoms['telangiectasia'])
        total_pigmentation = len(symptoms['pigmentation'])

        # 生成综合诊断
        diagnosis_details = {
            'layer_analysis': layers,
            'micro_symptoms': symptoms,
            'statistics': {
                'red_dots_count': total_red_dots,
                'flakes_count': total_flakes,
                'pustules_count': total_pustules,
                'vessels_visible': total_vessels,
                'pigmentation_areas': total_pigmentation
            },
            'severity_assessment': {
                'inflammation': DetailedScalpAnalyzer._assess_inflammation(symptoms, layers),
                'dryness': DetailedScalpAnalyzer._assess_dryness(symptoms, layers),
                'oiliness': DetailedScalpAnalyzer._assess_oiliness(layers),
                'sensitivity': DetailedScalpAnalyzer._assess_sensitivity(symptoms, layers),
                'damage': DetailedScalpAnalyzer._assess_damage(symptoms, layers)
            },
            'detailed_findings': DetailedScalpAnalyzer._generate_detailed_findings(symptoms, layers)
        }

        return diagnosis_details

    @staticmethod
    def _assess_inflammation(symptoms: Dict, layers: Dict) -> Dict:
        """评估炎症程度"""
        red_dots = len(symptoms['red_dots'])
        pustules = len(symptoms['pustules'])
        dermal_inflammation = layers['dermis']['inflammation']

        # 计算炎症分数
        inflammation_score = 0
        if red_dots > 10:
            inflammation_score += 3
        elif red_dots > 5:
            inflammation_score += 2
        elif red_dots > 0:
            inflammation_score += 1

        if pustules > 5:
            inflammation_score += 3
        elif pustules > 2:
            inflammation_score += 2
        elif pustules > 0:
            inflammation_score += 1

        if dermal_inflammation == 'mild':
            inflammation_score += 1
        elif dermal_inflammation == 'moderate':
            inflammation_score += 2
        elif dermal_inflammation == 'severe':
            inflammation_score += 3

        return {
            'score': inflammation_score,
            'level': 'severe' if inflammation_score >= 6 else 'moderate' if inflammation_score >= 3 else 'mild' if inflammation_score > 0 else 'none',
            'description': DetailedScalpAnalyzer._get_inflammation_description(inflammation_score)
        }

    @staticmethod
    def _assess_dryness(symptoms: Dict, layers: Dict) -> Dict:
        """评估干燥程度"""
        flakes = len(symptoms['white_flakes'])
        barrier_function = layers['epidermis']['barrier_function']
        sebum_level = layers['sebaceous_glands']['secretion_level']

        dryness_score = 0
        if flakes > 10:
            dryness_score += 3
        elif flakes > 5:
            dryness_score += 2
        elif flakes > 0:
            dryness_score += 1

        if barrier_function == 'weak':
            dryness_score += 2

        if sebum_level == 'insufficient':
            dryness_score += 2

        return {
            'score': dryness_score,
            'level': 'severe' if dryness_score >= 5 else 'moderate' if dryness_score >= 3 else 'mild' if dryness_score > 0 else 'normal',
            'description': DetailedScalpAnalyzer._get_dryness_description(dryness_score)
        }

    @staticmethod
    def _assess_oiliness(layers: Dict) -> Dict:
        """评估油腻程度"""
        sebum_activity = layers['sebaceous_glands']['activity']
        sebum_level = layers['sebaceous_glands']['secretion_level']

        if sebum_activity == 'hyperactive' and sebum_level == 'excessive':
            return {
                'level': 'severe',
                'description': '皮脂分泌严重过多，头皮非常油腻'
            }
        elif sebum_activity == 'hyperactive' or sebum_level == 'excessive':
            return {
                'level': 'moderate',
                'description': '皮脂分泌偏多，头皮较油腻'
            }
        else:
            return {
                'level': 'normal',
                'description': '皮脂分泌正常'
            }

    @staticmethod
    def _assess_sensitivity(symptoms: Dict, layers: Dict) -> Dict:
        """评估敏感程度"""
        red_dots = len(symptoms['red_dots'])
        vessels = len(symptoms['telangiectasia'])
        barrier = layers['epidermis']['barrier_function']

        sensitivity_score = 0
        if red_dots > 5:
            sensitivity_score += 2
        elif red_dots > 0:
            sensitivity_score += 1

        if vessels > 3:
            sensitivity_score += 2
        elif vessels > 0:
            sensitivity_score += 1

        if barrier == 'weak':
            sensitivity_score += 2

        return {
            'score': sensitivity_score,
            'level': 'high' if sensitivity_score >= 4 else 'moderate' if sensitivity_score >= 2 else 'low',
            'description': DetailedScalpAnalyzer._get_sensitivity_description(sensitivity_score)
        }

    @staticmethod
    def _assess_damage(symptoms: Dict, layers: Dict) -> Dict:
        """评估损伤程度"""
        total_issues = sum(len(layer.get('issues', [])) for layer in layers.values())
        total_symptoms = sum(len(symptom_list) for symptom_list in symptoms.values())

        damage_score = 0
        if total_issues > 5:
            damage_score += 3
        elif total_issues > 2:
            damage_score += 2
        elif total_issues > 0:
            damage_score += 1

        if total_symptoms > 20:
            damage_score += 3
        elif total_symptoms > 10:
            damage_score += 2
        elif total_symptoms > 5:
            damage_score += 1

        return {
            'score': damage_score,
            'level': 'severe' if damage_score >= 5 else 'moderate' if damage_score >= 3 else 'mild' if damage_score > 0 else 'minimal',
            'description': DetailedScalpAnalyzer._get_damage_description(damage_score)
        }

    @staticmethod
    def _generate_detailed_findings(symptoms: Dict, layers: Dict) -> List[str]:
        """生成详细发现列表"""
        findings = []

        # 红点发现
        if symptoms['red_dots']:
            count = len(symptoms['red_dots'])
            findings.append(f"发现{count}处红点/红斑，提示可能存在炎症反应")

        # 鳞屑发现
        if symptoms['white_flakes']:
            count = len(symptoms['white_flakes'])
            severe_flakes = [f for f in symptoms['white_flakes'] if f['severity'] == 'severe']
            if severe_flakes:
                findings.append(f"发现{count}处鳞屑，其中{len(severe_flakes)}处为大片鳞屑")
            else:
                findings.append(f"发现{count}处轻度鳞屑")

        # 脓包发现
        if symptoms['pustules']:
            count = len(symptoms['pustules'])
            findings.append(f"发现{count}个脓包/炎性丘疹，需要抗炎治疗")

        # 毛细血管扩张
        if symptoms['telangiectasia']:
            findings.append("发现毛细血管扩张，头皮较敏感")

        # 色素沉着
        if symptoms['pigmentation']:
            count = len(symptoms['pigmentation'])
            findings.append(f"发现{count}处色素沉着区域")

        # 头皮层问题
        for layer_name, layer_data in layers.items():
            if layer_data.get('issues'):
                for issue in layer_data['issues']:
                    findings.append(issue)

        return findings

    @staticmethod
    def _get_inflammation_description(score: int) -> str:
        """获取炎症描述"""
        if score >= 6:
            return "重度炎症：头皮存在明显的炎症反应，多处红肿、脓包，需要及时就医"
        elif score >= 3:
            return "中度炎症：头皮有炎症表现，存在红点和轻度肿胀，建议使用抗炎产品"
        elif score > 0:
            return "轻度炎症：头皮有轻微炎症迹象，注意清洁和护理"
        else:
            return "无明显炎症"

    @staticmethod
    def _get_dryness_description(score: int) -> str:
        """获取干燥描述"""
        if score >= 5:
            return "重度干燥：头皮严重缺水，大量脱屑，需要深度滋润"
        elif score >= 3:
            return "中度干燥：头皮干燥，有脱屑现象，需要保湿护理"
        elif score > 0:
            return "轻度干燥：头皮略显干燥，建议使用保湿产品"
        else:
            return "水分平衡正常"

    @staticmethod
    def _get_sensitivity_description(score: int) -> str:
        """获取敏感描述"""
        if score >= 4:
            return "高度敏感：头皮非常敏感，容易过敏，需使用温和产品"
        elif score >= 2:
            return "中度敏感：头皮较敏感，避免刺激性产品"
        else:
            return "低敏感性：头皮耐受性好"

    @staticmethod
    def _get_damage_description(score: int) -> str:
        """获取损伤描述"""
        if score >= 5:
            return "严重损伤：头皮多处损伤，需要修复治疗"
        elif score >= 3:
            return "中度损伤：头皮有损伤，需要护理修复"
        elif score > 0:
            return "轻度损伤：头皮有轻微损伤迹象"
        else:
            return "头皮健康，无明显损伤"