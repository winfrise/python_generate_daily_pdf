from PIL import Image
from config import STAMP_PATH, FONT_PATH
import fitz  # PyMuPDF
import os


def crop_seal_piece(input_path, seal_path):
    if not os.path.exists(input_path) or not os.path.exists(seal_path):
        print("错误：文件路径不存在")
        return

    # 1. 打开 PDF 和 印章图片
    doc = fitz.open(input_path)
    total_pages = len(doc)
    seal_img = Image.open(seal_path).convert("RGBA")  # 确保是 RGBA 模式以支持透明背景

    if total_pages == 0:
        print("PDF 为空")
        return

    # 2. 计算切割参数
    seal_width, seal_height = seal_img.size
    # 每一份切片的宽度
    slice_width = seal_width // total_pages

    print(f"正在处理 {total_pages} 页文档...")

    input_path_dir = os.path.dirname(input_path)
    seal_piece_dir = os.path.join(input_path_dir, "seal_images")

    for i in range(total_pages):

        # --- A. 切割印章 ---å
        # 计算当前页面的切片位置 (左, 上, 右, 下)
        left = i * slice_width
        # 最后一页取剩余所有部分，防止除不尽导致的像素丢失
        right = (i + 1) * slice_width if i < total_pages - 1 else seal_width
        piece = seal_img.crop((left, 0, right, seal_height))
        
        # 步骤 3：创建文件夹（exist_ok=True 避免重复创建报错）
        os.makedirs(seal_piece_dir, exist_ok=True)

        # 步骤 4：构造 PNG 文件路径并保存（PNG 格式默认支持透明）
        png_path = os.path.join(seal_piece_dir, f"{i+1}.png")  # 文件名可自定义（如 f"page_{i+1}.png"）
        piece.save(png_path, format="PNG")  # 显式指定格式为 PNG，确保透明通道保留
    
    doc.close()
    print('Seal裁剪完成')


def add_cross_page_seal(input_path, seal_path, add_list):
    """
    给 PDF 添加骑缝章
    :param pdf_path: 原始 PDF 路径
    :param seal_path: 印章图片路径 (支持 PNG/JPG)
    """
    if not os.path.exists(input_path) or not os.path.exists(seal_path):
        print("错误：文件路径不存在")
        return

    input_path_dir = os.path.dirname(input_path)
    seal_piece_dir = os.path.join(input_path_dir, "seal_images")

    base_name, ext = os.path.splitext(input_path)
    output_path = f"{base_name}_page_seal{ext}"

    doc = fitz.open(input_path)
    total_pages = len(doc)

    for i, page in enumerate(doc):
        page_num = i + 1
        img_name = f"{page_num}.png"
        img_path = os.path.join(seal_piece_dir, img_name)

        # 检查图片是否存在
        if not os.path.exists(img_path):
            print(f"[跳过] 第 {page_num} 页对应的图片未找到: {img_name}")
            continue

        if 'seal' in add_list: 
            # 临时解决方案：把切片保存
            crop_seal_piece(input_path, seal_image_path)

            # ========== A. 添加骑缝章 ==========
            # --- 配置参数 ---
            TARGET_HEIGHT_CM = 4  # 目标高度：4 厘米
            CM_TO_PT = 28.3465    # 厘米转点的换算系数 (1cm ≈ 28.35pt)
            MARGIN_RIGHT = 2     # 距离右边界的边距 (单位: pt)
            # ----------------

            # 1. 计算固定的目标高度 (转换为 PDF 的点)
            target_height_pt = TARGET_HEIGHT_CM * CM_TO_PT

            page_rect = page.rect
            page_w = page_rect.width
            page_h = page_rect.height

            # 3. 获取图片原始尺寸并计算等比缩放后的宽度
            # 使用 fitz.open 快速读取图片信息，无需加载整个图像到内存
            img_info = fitz.open(img_path)
            original_w = img_info[0].rect.width
            original_h = img_info[0].rect.height
            img_info.close()

            # 核心算法：(原宽 / 原高) * 目标高度 = 目标宽度
            scale_ratio = original_w / original_h
            target_width_pt = target_height_pt * scale_ratio

            # 4. 计算插入坐标 (右下角 + 垂直居中)
            # x0: 页面总宽 - 右边距 - 图片宽度
            x0 = page_w - MARGIN_RIGHT - target_width_pt
            y0 = (page_h - target_height_pt) / 2  # 垂直居中

            # 构建矩形区域 (x0, y0, x1, y1)
            rect = fitz.Rect(x0, y0, x0 + target_width_pt, y0 + target_height_pt)

            # 5. 插入图片
            page.insert_image(rect, filename=img_path)
            print(f"[成功] 第 {page_num} 页已添加印章 (尺寸: {target_width_pt:.1f} x {target_height_pt:.1f} pt)")


        if 'page' in add_list:
            # ========== B. 添加底部居中页码 ==========

            # 1. 加载宋体字体
            page.insert_font(fontfile=FONT_PATH, fontname="SimSun")
            SimSun_FONT = fitz.Font(fontfile=FONT_PATH, fontname="SimSun")

            text = f"第 {page_num} 页，共 {total_pages} 页"
            fontsize = 8

            # 2. 计算文本宽度
            # text_width = fitz.get_text_length(text, fontname="宋体", fontsize=fontsize)
            # 或者用 Font 对象的方法（更准确）
            text_width = SimSun_FONT.text_length(text, fontsize=fontsize)

            # 3. 获取页面宽度，计算居中位置
            position_x_center = (page_w - text_width) / 2  # 水平居中起始 X 坐标
            position_y = page_h - 10  # 垂直位置，可以自己调整


            # 插入文本 (不再使用 align 参数)
            page.insert_text(
                (position_x_center, position_y),
                text,
                fontname="SimSun", 
                fontsize=fontsize,
                color=(0, 0, 0)
            )


    # 3. 子集化字体（只保留用到的字符）
    doc.subset_fonts()

    # 4. 保存并压缩
    doc.ez_save(output_path)

    doc.close()
    print(f"处理完成，文件已保存至: {output_path}")



if __name__ == "__main__":
    input_path = "/Users/teacher/Downloads/百度网盘下载/水/111_2026年06月18日08时19分40秒.pdf"
    seal_image_path = STAMP_PATH
    add_list = ('page', 'seal')

    add_cross_page_seal(input_path, seal_image_path, add_list)