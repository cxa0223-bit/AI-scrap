"""
测试AI分析器修复效果
测试图像验证和疾病检测阈值调整
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from PIL import Image
import numpy as np
from ai_analyzer import analyze_scalp_image

def test_non_scalp_image():
    """Test if non-scalp images are properly rejected"""
    print("=== Test Non-Scalp Image Recognition ===")

    # 创建一个纯色测试图像（不是头皮）
    solid_color_img = Image.new('RGB', (300, 300), color=(100, 100, 200))
    result = analyze_scalp_image(solid_color_img)

    print(f"Test solid color image:")
    scalp_type = result['scalp_type'].encode('ascii', 'ignore').decode('ascii')
    if not scalp_type:  # If all characters were non-ascii
        scalp_type = "Non-ASCII result (likely Chinese)"
    print(f"  - Scalp type: {scalp_type}")
    print(f"  - Confidence: {result['confidence']}%")
    print(f"  - Diagnosed conditions: {len(result['diagnosed_conditions'])}")

    if 'Unrecognized' in result['scalp_type'] or '无法识别' in result['scalp_type']:
        print("  [OK] Success: Correctly identified as non-scalp image")
    else:
        print("  [FAIL] Failed: Misidentified as scalp image")

    # 创建一个随机噪声图像
    noise_array = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    noise_img = Image.fromarray(noise_array)
    result2 = analyze_scalp_image(noise_img)

    print(f"\nTest random noise image:")
    scalp_type2 = result2['scalp_type'].encode('ascii', 'ignore').decode('ascii')
    if not scalp_type2:  # If all characters were non-ascii
        scalp_type2 = "Non-ASCII result (likely Chinese)"
    print(f"  - Scalp type: {scalp_type2}")
    print(f"  - Confidence: {result2['confidence']}%")
    print(f"  - Diagnosed conditions: {len(result2['diagnosed_conditions'])}")

    if 'Unrecognized' in result2['scalp_type'] or '无法识别' in result2['scalp_type']:
        print("  [OK] Success: Correctly identified as non-scalp image")
    else:
        print("  [FAIL] Failed: Misidentified as scalp image")

    return result, result2

def create_simulated_scalp_image():
    """创建一个模拟的头皮图像用于测试"""
    # 创建肤色背景
    img = np.ones((300, 300, 3), dtype=np.uint8)
    img[:, :, 0] = 220  # R
    img[:, :, 1] = 180  # G
    img[:, :, 2] = 160  # B

    # 添加一些模拟的头发纹理（黑色线条）
    for i in range(0, 300, 10):
        for j in range(0, 300, 8):
            if np.random.rand() > 0.3:
                img[i:i+2, j:j+1] = [50, 30, 20]

    # 添加一些变化
    noise = np.random.randint(-20, 20, (300, 300, 3))
    img = np.clip(img.astype(int) + noise, 0, 255).astype(np.uint8)

    return Image.fromarray(img)

def test_threshold_adjustments():
    """Test disease detection threshold adjustments"""
    print("\n=== Test Disease Detection Thresholds ===")

    # Create simulated normal scalp image
    normal_scalp = create_simulated_scalp_image()
    result = analyze_scalp_image(normal_scalp)

    print(f"Simulated normal scalp image analysis:")
    scalp_type3 = result['scalp_type'].encode('ascii', 'ignore').decode('ascii')
    if not scalp_type3:  # If all characters were non-ascii
        scalp_type3 = "Non-ASCII result (likely Chinese)"
    print(f"  - Scalp type: {scalp_type3}")
    print(f"  - Health score: {result['health_score']}")
    print(f"  - Confidence: {result['confidence']}%")
    print(f"  - Diagnosed conditions: {len(result['diagnosed_conditions'])}")

    if len(result['diagnosed_conditions']) == 0:
        print("  [OK] Success: Normal scalp with no false disease diagnoses")
    else:
        print(f"  [WARNING] Detected {len(result['diagnosed_conditions'])} condition(s):")
        for condition in result['diagnosed_conditions']:
            print(f"    - {condition['name_cn']} (confidence: {condition['confidence']}%)")

    # Print detailed features for debugging
    if 'details' in result:
        print("\n  Detailed features:")
        for key, value in result['details'].items():
            if isinstance(value, (int, float)):
                print(f"    - {key}: {value:.2f}")

    return result

def main():
    """主测试函数"""
    print("=" * 60)
    print("AI Analyzer Fix Test")
    print("=" * 60)

    # Test 1: Non-scalp image recognition
    test_non_scalp_image()

    # Test 2: Threshold adjustment effects
    test_threshold_adjustments()

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("Fix Summary:")
    print("1. Added scalp image validation - non-scalp images will be rejected")
    print("2. Increased disease detection thresholds - reduced false positives")
    print("3. Requires multiple symptoms to diagnose diseases")
    print("=" * 60)

if __name__ == "__main__":
    main()