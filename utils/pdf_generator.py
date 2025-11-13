"""
PDF报告生成器 - 头皮健康AI分析系统
PDF Report Generator - Scalp Health AI Analysis System
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from PIL import Image as PILImage
import io
import os


class ScalpAnalysisPDFGenerator:
    """头皮分析PDF报告生成器"""

    def __init__(self):
        """初始化PDF生成器"""
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_fonts()
        self._setup_custom_styles()

    def _setup_fonts(self):
        """设置字体支持中文"""
        try:
            # 尝试注册系统中文字体
            # Windows系统
            if os.name == 'nt':
                font_paths = [
                    'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
                    'C:/Windows/Fonts/simhei.ttf',  # 黑体
                    'C:/Windows/Fonts/simsun.ttc',  # 宋体
                ]
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        self.has_chinese_font = True
                        return
            # Mac系统
            elif os.name == 'posix':
                font_paths = [
                    '/System/Library/Fonts/PingFang.ttc',
                    '/Library/Fonts/Arial Unicode.ttf',
                ]
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        self.has_chinese_font = True
                        return
        except Exception as e:
            print(f"Warning: Could not load Chinese font: {e}")

        self.has_chinese_font = False

    def _setup_custom_styles(self):
        """设置自定义样式"""
        # 根据是否有中文字体选择字体
        font_name = 'ChineseFont' if self.has_chinese_font else 'Helvetica'
        font_name_bold = 'ChineseFont' if self.has_chinese_font else 'Helvetica-Bold'

        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=25,
            alignment=TA_CENTER,
            fontName=font_name_bold,
            leading=28
        )

        # 副标题样式
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=15,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            spaceBefore=16,
            fontName=font_name_bold,
            leading=20
        )

        # 正文样式
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            leading=15,
            alignment=TA_LEFT,
            spaceAfter=10,
            fontName=font_name,
            wordWrap='CJK'  # 支持中文换行
        )

        # 小标题样式
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=8,
            spaceBefore=12,
            fontName=font_name_bold,
            leading=16
        )

    def generate_report(
        self,
        output_path: str,
        analysis_result: dict,
        images: list = None,
        annotated_images: list = None,
        user_info: dict = None
    ):
        """
        生成PDF报告

        Args:
            output_path: PDF输出路径
            analysis_result: 分析结果字典
            images: 原始图片列表
            annotated_images: 标注图片列表
            user_info: 用户信息（可选）
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # 构建PDF内容
        story = []

        # 1. 添加标题和日期
        story.extend(self._create_header(user_info))

        # 2. 添加概述部分
        story.extend(self._create_summary(analysis_result))

        # 3. 添加图片对比（原图 vs 标注图）
        if images and annotated_images:
            story.extend(self._create_image_comparison(images, annotated_images))

        # 4. 添加详细诊断
        story.extend(self._create_diagnosis_section(analysis_result))

        # 5. 添加护理建议
        story.extend(self._create_recommendations_section(analysis_result))

        # 6. 添加产品推荐（如果有）
        if 'recommended_products' in analysis_result:
            story.extend(self._create_products_section(analysis_result))

        # 7. 添加免责声明
        story.extend(self._create_disclaimer())

        # 8. 添加页脚
        story.extend(self._create_footer())

        # 生成PDF
        doc.build(story)

        return output_path

    def _create_header(self, user_info: dict = None):
        """创建报告头部"""
        elements = []

        # 主标题
        title = Paragraph("Scalp Health Analysis Report<br/>头皮健康分析报告", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))

        # 报告信息表格
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_id = datetime.now().strftime("%Y%m%d%H%M%S")

        data = [
            ["Report ID | 报告编号:", report_id],
            ["Date | 日期:", report_date],
            ["Analysis Type | 分析类型:", "AI-Powered Scalp Analysis | AI智能头皮分析"]
        ]

        if user_info:
            if 'name' in user_info:
                data.insert(1, ["Patient Name | 患者姓名:", user_info['name']])
            if 'age' in user_info:
                data.insert(2, ["Age | 年龄:", str(user_info['age'])])

        # 使用中文字体
        font_name = 'ChineseFont' if self.has_chinese_font else 'Helvetica'

        table = Table(data, colWidths=[3.5*inch, 3*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.4*inch))

        return elements

    def _create_summary(self, result: dict):
        """创建分析概述"""
        elements = []

        # 章节标题
        elements.append(Paragraph("Analysis Summary | 分析概述", self.subtitle_style))

        # 核心指标表格
        scalp_type = result.get('scalp_type', 'Unknown')
        confidence = result.get('confidence', 0)
        health_score = result.get('health_score', 0)

        # 确定健康评级
        if health_score >= 80:
            health_status = "Excellent | 优秀"
            status_color = colors.green
        elif health_score >= 60:
            health_status = "Good | 良好"
            status_color = colors.blue
        elif health_score >= 40:
            health_status = "Fair | 一般"
            status_color = colors.orange
        else:
            health_status = "Poor | 较差"
            status_color = colors.red

        data = [
            ["Scalp Type | 头皮类型", scalp_type],
            ["Confidence Level | 置信度", f"{confidence}%"],
            ["Health Score | 健康评分", f"{health_score}/100"],
            ["Health Status | 健康状态", health_status]
        ]

        font_name = 'ChineseFont' if self.has_chinese_font else 'Helvetica'

        table = Table(data, colWidths=[3*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (1, 3), (1, 3), status_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f2f6')),
            ('ROWHEIGHT', (0, 0), (-1, -1), 0.4*inch),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _create_image_comparison(self, images: list, annotated_images: list):
        """创建图片对比部分"""
        elements = []

        elements.append(Paragraph("Image Analysis | 图像分析", self.subtitle_style))

        # 只显示第一张图片的对比
        if images and annotated_images:
            # 转换PIL图片为字节流
            original_img = images[0]
            annotated_img = annotated_images[0]

            # 调整图片大小
            max_width = 2.8 * inch
            max_height = 2.5 * inch

            try:
                # 创建内存字节流
                original_buffer = io.BytesIO()
                annotated_buffer = io.BytesIO()

                # 保存图片到字节流
                original_img.save(original_buffer, format='PNG')
                annotated_img.save(annotated_buffer, format='PNG')

                # 重置指针到开始
                original_buffer.seek(0)
                annotated_buffer.seek(0)

                # 直接使用字节流创建Image对象
                original_image_obj = Image(original_buffer, width=max_width, height=max_height)
                annotated_image_obj = Image(annotated_buffer, width=max_width, height=max_height)

                # 创建图片表格
                img_data = [
                    [
                        Paragraph("<b>Original Image | 原始图像</b>", self.body_style),
                        Paragraph("<b>Annotated Image | 标注图像</b>", self.body_style)
                    ],
                    [
                        original_image_obj,
                        annotated_image_obj
                    ]
                ]

                img_table = Table(img_data, colWidths=[3.2*inch, 3.2*inch])
                img_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f2f6'))
                ]))

                elements.append(img_table)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                # 如果图片处理失败，添加说明文字
                elements.append(Paragraph(
                    f"<i>Image comparison unavailable | 图像对比不可用</i>",
                    self.body_style
                ))
                print(f"Error creating image comparison: {e}")

        elements.append(Spacer(1, 0.3*inch))
        return elements

    def _create_diagnosis_section(self, result: dict):
        """创建诊断部分"""
        elements = []

        elements.append(Paragraph("Medical Diagnosis | 医学诊断", self.subtitle_style))

        diagnosed_conditions = result.get('diagnosed_conditions', [])

        if diagnosed_conditions:
            for i, condition in enumerate(diagnosed_conditions, 1):
                # 疾病标题
                name_cn = condition.get('name_cn', 'Unknown')
                name_en = condition.get('name_en', 'Unknown')
                severity = condition.get('severity', 'N/A')
                confidence = condition.get('confidence', 0)

                condition_title = f"{i}. {name_cn} ({name_en})"
                elements.append(Paragraph(condition_title, self.heading_style))

                # 疾病详情
                details = [
                    ["Severity | 严重程度:", severity],
                    ["Confidence | 置信度:", f"{confidence}%"],
                ]

                if 'icd10_code' in condition:
                    details.append(["ICD-10 Code | 疾病编码:", condition['icd10_code']])

                font_name = 'ChineseFont' if self.has_chinese_font else 'Helvetica'

                detail_table = Table(details, colWidths=[2.5*inch, 4*inch])
                detail_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), font_name),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
                ]))

                elements.append(detail_table)
                elements.append(Spacer(1, 0.1*inch))

                # 症状描述
                description = condition.get('description', 'No description available.')
                elements.append(Paragraph(f"<b>Description | 描述:</b> {description}", self.body_style))

                # 观察到的症状
                if 'symptoms' in condition and condition['symptoms']:
                    symptoms_text = "<b>Observed Symptoms | 观察到的症状:</b><br/>"
                    for symptom in condition['symptoms']:
                        symptoms_text += f"• {symptom}<br/>"
                    elements.append(Paragraph(symptoms_text, self.body_style))

                elements.append(Spacer(1, 0.2*inch))
        else:
            elements.append(Paragraph("No significant conditions detected. | 未检测到明显问题。", self.body_style))

        elements.append(Spacer(1, 0.2*inch))
        return elements

    def _create_recommendations_section(self, result: dict):
        """创建护理建议部分"""
        elements = []

        elements.append(Paragraph("Care Recommendations | 护理建议", self.subtitle_style))

        recommendations = result.get('recommendations', [])

        if recommendations:
            rec_text = ""
            for i, rec in enumerate(recommendations, 1):
                rec_text += f"{i}. {rec}<br/>"
            elements.append(Paragraph(rec_text, self.body_style))
        else:
            elements.append(Paragraph("Continue with regular scalp care routine. | 继续保持日常头皮护理。", self.body_style))

        elements.append(Spacer(1, 0.3*inch))
        return elements

    def _create_products_section(self, result: dict):
        """创建产品推荐部分"""
        elements = []

        elements.append(Paragraph("Recommended Products | 推荐产品", self.subtitle_style))

        products = result.get('recommended_products', [])

        if products:
            for i, product in enumerate(products, 1):
                product_name = product.get('name', 'Unknown Product')
                brand = product.get('brand', 'Unknown Brand')
                price = product.get('price_myr', 'N/A')

                product_text = f"<b>{i}. {product_name}</b><br/>"
                product_text += f"Brand | 品牌: {brand}<br/>"
                product_text += f"Price | 价格: RM {price}<br/>"

                if 'description' in product:
                    product_text += f"Description | 说明: {product['description']}<br/>"

                elements.append(Paragraph(product_text, self.body_style))
                elements.append(Spacer(1, 0.15*inch))

        elements.append(Spacer(1, 0.2*inch))
        return elements

    def _create_disclaimer(self):
        """创建免责声明"""
        elements = []

        elements.append(Paragraph("Disclaimer | 免责声明", self.subtitle_style))

        disclaimer_text = """
        <b>Important Notice:</b> This report is generated by an AI-powered analysis system and is for
        reference purposes only. It should not be considered as a substitute for professional medical
        advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider
        with any questions you may have regarding a medical condition.<br/><br/>

        <b>重要提示：</b>本报告由AI分析系统生成，仅供参考。不应被视为专业医疗建议、诊断或治疗的替代品。
        如有任何健康问题，请务必咨询合格的医疗保健提供者。
        """

        elements.append(Paragraph(disclaimer_text, self.body_style))
        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _create_footer(self):
        """创建页脚"""
        elements = []

        footer_text = """
        <para align=center>
        <b>Scalp Health AI Analyzer</b><br/>
        Professional Scalp Analysis for Malaysia | 马来西亚专业头皮分析<br/>
        © 2024 All Rights Reserved<br/>
        📧 support@scalpanalyzer.my | 📱 +60 12-345 6789
        </para>
        """

        footer_style = ParagraphStyle(
            'Footer',
            parent=self.body_style,
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )

        elements.append(Paragraph(footer_text, footer_style))

        return elements


def generate_analysis_pdf(
    output_path: str,
    analysis_result: dict,
    images: list = None,
    annotated_images: list = None,
    user_info: dict = None
) -> str:
    """
    便捷函数：生成分析PDF报告

    Args:
        output_path: PDF输出路径
        analysis_result: 分析结果
        images: 原始图片列表
        annotated_images: 标注图片列表
        user_info: 用户信息

    Returns:
        生成的PDF文件路径
    """
    generator = ScalpAnalysisPDFGenerator()
    return generator.generate_report(
        output_path,
        analysis_result,
        images,
        annotated_images,
        user_info
    )
