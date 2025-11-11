# -*- coding: utf-8 -*-
"""
图像标注模块 - 在头皮图像上标注检测到的问题区域
Image Annotation Module - Annotate detected issues on scalp images
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Tuple, Any
import os


class ScalpImageAnnotator:
    """头皮图像标注器 - 标注检测到的问题"""

    # 颜色定义 (BGR格式用于OpenCV) - 使用高对比度鲜艳颜色
    COLORS = {
        'red_dots': (0, 0, 255),        # 纯红色 - 红点/炎症
        'white_flakes': (0, 255, 255),  # 纯黄色 - 白色鳞屑（更鲜艳）
        'follicles': (0, 255, 0),       # 纯绿色 - 毛囊
        'oil': (0, 128, 255),           # 橙色 - 油脂区域
        'text': (255, 255, 255),        # 白色 - 文字
        'background': (0, 0, 0),        # 黑色 - 文字背景
        'highlight': (255, 0, 255)      # 品红色 - 高亮标记
    }

    def __init__(self):
        """初始化标注器"""
        pass

    def annotate_analysis_results(
        self,
        image: Image.Image,
        local_results: Dict[str, Any],
        show_labels: bool = True,
        show_legend: bool = True
    ) -> Image.Image:
        """
        在图像上标注分析结果

        Args:
            image: 原始PIL图像
            local_results: 本地分析结果字典
            show_labels: 是否显示标签文字
            show_legend: 是否显示图例

        Returns:
            标注后的PIL图像
        """
        # 转换为OpenCV格式
        img_array = np.array(image)
        if len(img_array.shape) == 2:  # 灰度图
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        elif img_array.shape[2] == 4:  # RGBA
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
        else:  # RGB
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # 创建标注图层
        annotated = img_array.copy()

        # 标注红点/红斑
        if 'red_dots' in local_results and local_results['red_dots']:
            annotated = self._annotate_red_dots(
                annotated,
                local_results['red_dots'],
                show_labels
            )

        # 标注白色鳞屑
        if 'white_flakes' in local_results and local_results['white_flakes']:
            annotated = self._annotate_white_flakes(
                annotated,
                local_results['white_flakes'],
                show_labels
            )

        # 标注毛囊
        if 'follicle_info' in local_results and local_results['follicle_info']:
            follicle_data = local_results['follicle_info']
            if 'detected_follicles' in follicle_data:
                annotated = self._annotate_follicles(
                    annotated,
                    follicle_data['detected_follicles'],
                    show_labels
                )

        # 添加图例
        if show_legend:
            annotated = self._add_legend(annotated, local_results)

        # 转换回PIL格式
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        return Image.fromarray(annotated_rgb)

    def _annotate_red_dots(
        self,
        img: np.ndarray,
        red_dots: List[Dict],
        show_labels: bool
    ) -> np.ndarray:
        """标注红点/红斑 - 增强版"""
        # 创建半透明overlay层
        overlay = img.copy()

        for i, dot in enumerate(red_dots):
            x, y = dot['center']
            area = dot.get('area', 0)

            # 根据面积决定圆圈大小（增大显示）
            radius = max(20, int(np.sqrt(area / np.pi)) + 10)

            # 绘制半透明填充圆
            cv2.circle(overlay, (x, y), radius, self.COLORS['red_dots'], -1)

            # 绘制粗边框圆圈（更粗更明显）
            cv2.circle(img, (x, y), radius, self.COLORS['red_dots'], 4)

            # 绘制内圈增强对比
            cv2.circle(img, (x, y), radius - 3, self.COLORS['red_dots'], 2)

            # 绘制中心点（更大）
            cv2.circle(img, (x, y), 5, (255, 255, 255), -1)  # 白色中心点
            cv2.circle(img, (x, y), 4, self.COLORS['red_dots'], -1)

            # 添加标签（更大字体）
            if show_labels and i < 15:  # 增加标注数量
                label = f"R{i+1}"
                self._draw_label(img, label, (x, y - radius - 10), self.COLORS['red_dots'], font_scale=0.6)

        # 混合overlay层（半透明效果）
        cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

        return img

    def _annotate_white_flakes(
        self,
        img: np.ndarray,
        white_flakes: List[Dict],
        show_labels: bool
    ) -> np.ndarray:
        """标注白色鳞屑 - 增强版"""
        # 创建半透明overlay层
        overlay = img.copy()

        for i, flake in enumerate(white_flakes):
            x, y = flake['center']
            area = flake.get('area', 0)

            # 根据面积决定方框大小（增大显示）
            size = max(18, int(np.sqrt(area)) + 8)

            # 绘制矩形框坐标
            pt1 = (x - size, y - size)
            pt2 = (x + size, y + size)

            # 绘制半透明填充矩形
            cv2.rectangle(overlay, pt1, pt2, self.COLORS['white_flakes'], -1)

            # 绘制粗边框矩形（更粗更明显）
            cv2.rectangle(img, pt1, pt2, self.COLORS['white_flakes'], 4)

            # 绘制内框增强对比
            cv2.rectangle(img,
                         (x - size + 3, y - size + 3),
                         (x + size - 3, y + size - 3),
                         self.COLORS['white_flakes'], 2)

            # 绘制中心十字标记（更明显）
            cv2.line(img, (x - 8, y), (x + 8, y), self.COLORS['white_flakes'], 3)
            cv2.line(img, (x, y - 8), (x, y + 8), self.COLORS['white_flakes'], 3)

            # 添加标签（更大字体）
            if show_labels and i < 15:  # 增加标注数量
                label = f"F{i+1}"
                flake_type = flake.get('type', '')
                if flake_type:
                    label += f"({flake_type[:1]})"  # 添加类型首字母
                self._draw_label(img, label, (x, y - size - 10), self.COLORS['white_flakes'], font_scale=0.6)

        # 混合overlay层（半透明效果）
        cv2.addWeighted(overlay, 0.25, img, 0.75, 0, img)

        return img

    def _annotate_follicles(
        self,
        img: np.ndarray,
        follicles: List[Dict],
        show_labels: bool
    ) -> np.ndarray:
        """标注毛囊"""
        # 只标注部分毛囊，避免图像过于拥挤
        max_follicles = min(len(follicles), 15)

        for i, follicle in enumerate(follicles[:max_follicles]):
            x, y = follicle['center']

            # 绘制小圆圈
            cv2.circle(img, (x, y), 8, self.COLORS['follicles'], 1)
            cv2.circle(img, (x, y), 2, self.COLORS['follicles'], -1)

        return img

    def _draw_label(
        self,
        img: np.ndarray,
        text: str,
        position: Tuple[int, int],
        color: Tuple[int, int, int],
        font_scale: float = 0.6
    ):
        """绘制文字标签 - 增强版"""
        x, y = position

        # 设置字体（更大更粗）
        font = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 2  # 增加字体粗细

        # 获取文字大小
        (text_width, text_height), baseline = cv2.getTextSize(
            text, font, font_scale, thickness
        )

        # 绘制带白边的背景矩形（更明显）
        padding = 4
        # 外层白边
        cv2.rectangle(
            img,
            (x - padding - 2, y - text_height - padding - 2),
            (x + text_width + padding + 2, y + baseline + padding + 2),
            (255, 255, 255),
            -1
        )
        # 内层黑色背景
        cv2.rectangle(
            img,
            (x - padding, y - text_height - padding),
            (x + text_width + padding, y + baseline + padding),
            self.COLORS['background'],
            -1
        )

        # 绘制文字
        cv2.putText(
            img,
            text,
            (x, y),
            font,
            font_scale,
            color,
            thickness,
            cv2.LINE_AA
        )

    def _add_legend(
        self,
        img: np.ndarray,
        results: Dict[str, Any]
    ) -> np.ndarray:
        """添加图例说明"""
        height, width = img.shape[:2]

        # 图例位置（右上角）
        legend_x = width - 180
        legend_y = 20
        legend_width = 170

        # 统计各类问题数量
        red_count = len(results.get('red_dots', []))
        flake_count = len(results.get('white_flakes', []))
        follicle_count = 0
        if 'follicle_info' in results:
            follicle_count = len(results['follicle_info'].get('detected_follicles', []))

        # 绘制半透明背景（更大更明显）
        overlay = img.copy()
        legend_height = 30 + (red_count > 0) * 35 + (flake_count > 0) * 35 + (follicle_count > 0) * 35 + 15

        # 外层白边
        cv2.rectangle(
            overlay,
            (legend_x - 15, legend_y - 15),
            (legend_x + legend_width + 5, legend_y + legend_height),
            (255, 255, 255),
            -1
        )
        # 内层黑色背景
        cv2.rectangle(
            overlay,
            (legend_x - 12, legend_y - 12),
            (legend_x + legend_width + 2, legend_y + legend_height - 3),
            (0, 0, 0),
            -1
        )
        cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)

        # 绘制图例项（更大更明显）
        y_offset = legend_y
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6  # 增大字体
        thickness = 2     # 增加粗细

        if red_count > 0:
            # 绘制更大的圆形标记
            cv2.circle(img, (legend_x, y_offset + 8), 8, self.COLORS['red_dots'], -1)
            cv2.circle(img, (legend_x, y_offset + 8), 8, self.COLORS['red_dots'], 2)
            cv2.putText(
                img,
                f"Red Dots: {red_count}",
                (legend_x + 20, y_offset + 15),
                font,
                font_scale,
                self.COLORS['text'],
                thickness,
                cv2.LINE_AA
            )
            y_offset += 35

        if flake_count > 0:
            # 绘制更大的矩形标记
            cv2.rectangle(
                img,
                (legend_x - 8, y_offset),
                (legend_x + 8, y_offset + 16),
                self.COLORS['white_flakes'],
                3
            )
            cv2.putText(
                img,
                f"Flakes: {flake_count}",
                (legend_x + 20, y_offset + 15),
                font,
                font_scale,
                self.COLORS['text'],
                thickness,
                cv2.LINE_AA
            )
            y_offset += 25

        if follicle_count > 0:
            cv2.circle(img, (legend_x, y_offset + 5), 5, self.COLORS['follicles'], 1)
            cv2.putText(
                img,
                f"Follicles: {follicle_count}",
                (legend_x + 15, y_offset + 10),
                font,
                font_scale,
                self.COLORS['text'],
                thickness,
                cv2.LINE_AA
            )

        return img

    def create_multi_image_comparison(
        self,
        images_with_labels: List[Tuple[Image.Image, str]],
        annotated_images: List[Image.Image] = None,
        grid_cols: int = 2
    ) -> Image.Image:
        """
        创建多图对比视图

        Args:
            images_with_labels: [(图像, 标签), ...] 列表
            annotated_images: 对应的标注图像列表（可选）
            grid_cols: 网格列数

        Returns:
            组合后的PIL图像
        """
        n_images = len(images_with_labels)
        if n_images == 0:
            return None

        # 如果有标注图像，则每个原图配一个标注图
        if annotated_images:
            n_images = n_images * 2
            grid_cols = 2

        # 计算网格尺寸
        grid_rows = (n_images + grid_cols - 1) // grid_cols

        # 调整所有图像到相同大小
        target_size = (400, 400)

        # 创建空白画布
        canvas_width = target_size[0] * grid_cols + 20 * (grid_cols + 1)
        canvas_height = target_size[1] * grid_rows + 60 * grid_rows + 20
        canvas = Image.new('RGB', (canvas_width, canvas_height), color='white')
        draw = ImageDraw.Draw(canvas)

        # 尝试加载字体
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()

        # 放置图像
        for idx, (img, label) in enumerate(images_with_labels):
            # 调整大小
            img_resized = img.copy()
            img_resized.thumbnail(target_size, Image.Resampling.LANCZOS)

            # 计算位置
            if annotated_images:
                # 原图和标注图并排显示
                row = idx
                col_orig = 0
                col_anno = 1

                x_orig = 20 + col_orig * (target_size[0] + 20)
                x_anno = 20 + col_anno * (target_size[0] + 20)
                y = 20 + row * (target_size[1] + 60)

                # 放置原图
                canvas.paste(img_resized, (x_orig, y + 40))
                draw.text((x_orig, y + 10), f"{label} - Original", fill='black', font=font)

                # 放置标注图
                if idx < len(annotated_images):
                    anno_resized = annotated_images[idx].copy()
                    anno_resized.thumbnail(target_size, Image.Resampling.LANCZOS)
                    canvas.paste(anno_resized, (x_anno, y + 40))
                    draw.text((x_anno, y + 10), f"{label} - Annotated", fill='black', font=font)
            else:
                # 普通网格布局
                row = idx // grid_cols
                col = idx % grid_cols

                x = 20 + col * (target_size[0] + 20)
                y = 20 + row * (target_size[1] + 60)

                # 放置图像
                canvas.paste(img_resized, (x, y + 40))
                draw.text((x, y + 10), label, fill='black', font=font)

        return canvas
