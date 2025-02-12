import fitz
import sys
import os
import argparse


def pdf_to_img(pdf_path, img_path_pattern, img_format="png"):
    """
    将PDF文件转换为图片
    :param pdf_path: PDF文件路径
    :param img_path_pattern: 图片路径模板（包含格式化占位符）
    :param img_format: 图片格式（如 png, jpg 等）
    """
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            image = page.get_pixmap()
            img_path = img_path_pattern.format(page_num)
            image.save(f"{img_path}.{img_format}")
        print(f"Saved: {img_path}.{img_format}")
        pdf_document.close()
    except Exception as e:
        print(f"Error during PDF to image conversion: {e}")
        raise


def set_defalut_output_folder(pdf_path):
    """
    设置默认输出文件夹
    :param pdf_path: PDF文件路径
    :return: 默认输出文件夹路径
    """
    # 获取PDF文件所在目录
    pdf_dir = os.path.dirname(pdf_path)
    # 默认图片文件夹位置为PDF文件夹下的output_images文件夹
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(pdf_dir, f"{pdf_name}_output_images")
    return output_folder


def main():
    parser = argparse.ArgumentParser(description="convert PDF to image")
    parser.add_argument("pdf_path", type=str, help="PDF file path")
    parser.add_argument(
        "--output_folder",
        type=str,
        help="Output folder path (default: PDF folder/output_images)",
    )
    parser.add_argument(
        "--img_format",
        type=str,
        help="Image format(png, jpg, etc)",
        default="png",
        choices=["png", "jpg", "jpeg", "bmp", "tiff", "ppm", "pgm", "pbm"],
    )

    args = parser.parse_args()
    pdf_path = args.pdf_path
    output_folder = args.output_folder
    img_format = args.img_format

    if not os.path.exists(pdf_path):
        print("PDF file does not exist!")
        sys.exit(1)

    if output_folder is None:
        output_folder = set_defalut_output_folder(pdf_path)

    # 如果输出文件夹不存在，则创建文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    img_path_pattern = os.path.join(output_folder, "page_{}")
    pdf_to_img(pdf_path, img_path_pattern, img_format)
    print("PDF to Image conversion completed!")


if __name__ == "__main__":
    main()
