import os
import json
import base64
import re
import fitz  # PyMuPDF
from openai import OpenAI


def call_ocr_api(image_bytes, llm_type, api_key, fields=None):
    """多模型视觉识别路由 (适配全新 Google GenAI SDK + OpenAI 兼容池)"""
    # 构建统一的 Prompt
    field_str = ", ".join(fields) if fields else "所有信息"
    prompt = f"你是一个专业的财务审计专家。请识别图片内容，提取：{field_str}。如果缺失则填'无'。请严格返回纯 JSON，不要包含 Markdown 标签或解释。"

    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        if llm_type == "千问":
            client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
            model_name = "qwen-vl-plus"
        else:
            return None
            
        client_response = client.chat.completions.create(
            model=model_name,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }],
            temperature=0.1
        )
        
        raw_content = client_response.choices[0].message.content.strip()
        
        md_marker = chr(96) * 3
        if raw_content.startswith(md_marker):
            lines = raw_content.split('\n')
            if len(lines) > 2:
                raw_content = '\n'.join(lines[1:-1]).strip()
        
        return json.loads(raw_content)

    except Exception as e:
        print(f"❌ {llm_type} 请求或解析失败: {e}")
        return None


def process_pdf(pdf_path, output_dir, llm_type, api_key, log_callback, fields=None):
    """主流程：PDF -> 图片 -> API -> JSON"""


    doc = fitz.open(pdf_path)
    base_pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_num in range(len(doc)):
        log_callback(f"正在处理第 {page_num + 1}/{len(doc)} 页...")
        page = doc[page_num]
        
        # 1. 渲染为高清图片 (zoom=2.0 提高 DPI 保证识别率)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_bytes = pix.tobytes("png")

        # 2. 调用 API
        result = call_ocr_api(img_bytes, llm_type, api_key, fields)

        if result:
            # 3. 动态命名并保存
            filename = f"{base_pdf_name}_page_{page_num+1}.json"
            
            output_data = {
                "source_file": base_pdf_name,
                "page": page_num + 1,
                "data": result
            }
            
            with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=4)

    doc.close()
    log_callback("🎉 处理完成！")

def process_single_image(image_path, output_dir,llm_type, api_key, log_callback, fields=None):
    """直接读取本地图片并调用 OCR API"""

    # 1. 以二进制格式读取本地图片
    try:
        with open(image_path, "rb") as f:
            img_bytes = f.read()
    except Exception as e:
        log_callback(f"❌ 读取图片文件失败: {e}")
        return
        
    # 2. 直接调用你原有的 call_ocr_api 函数
    result = call_ocr_api(img_bytes, llm_type, api_key, fields)
    img_name = os.path.splitext(os.path.basename(image_path))[0]
    # 3. 输出或保存结果
    if result:
        filename = f"{img_name}.json"
        
        output_data = {
            "source_file": img_name,
            "data": result
        }
        
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

    else:
        log_callback("⚠️ 识别未能返回有效结果。")

