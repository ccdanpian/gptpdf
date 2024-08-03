import os
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from gptpdf import parse_pdf
import dotenv
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
dotenv.load_dotenv()

# 获取当前脚本的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

# 确保上传和输出目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logger.info(f"Upload folder: {UPLOAD_FOLDER}")
logger.info(f"Output folder: {OUTPUT_FOLDER}")

@app.route('/parse_pdf', methods=['POST'])
def api_parse_pdf():
    logger.info("Received request to parse PDF")
    if 'file' not in request.files:
        logger.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        try:
            # 使用接收到的文件名（即 fileId）
            fileId = file.filename
            pdf_path = os.path.join(UPLOAD_FOLDER, fileId)
            logger.info(f"Saving file to: {pdf_path}")
            file.save(pdf_path)
            
            if not os.path.exists(pdf_path):
                logger.error(f"File was not saved successfully: {pdf_path}")
                return jsonify({"error": "File was not saved successfully"}), 500

            # 设置输出目录
            output_dir = os.path.join(OUTPUT_FOLDER, os.path.splitext(fileId)[0])
            logger.info(f"Output directory: {output_dir}")
            
            # 解析PDF
            api_key = os.getenv('OPENAI_API_KEY')
            base_url = os.getenv('OPENAI_API_BASE')
            logger.info("Starting PDF parsing")
            content, _ = parse_pdf(pdf_path, output_dir=output_dir, api_key=api_key, base_url=base_url, model='gpt-4o', gpt_worker=6)
            logger.info("PDF parsing completed")

            # 读取输出目录中的所有图片文件
            image_data = []
            logger.info(f"Scanning for images in: {output_dir}")
            for filename in os.listdir(output_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    full_image_path = os.path.join(output_dir, filename)
                    logger.debug(f"Processing image: {full_image_path}")
                    with open(full_image_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                        image_data.append({
                            "filename": filename,
                            "data": encoded_string
                        })
                    logger.debug(f"Image processed: {filename}")

            logger.info(f"Total images processed: {len(image_data)}")
            logger.info("PDF parsing and image encoding completed")

            return jsonify({
                "content": content,
                "images": image_data
            })
        except Exception as e:
            logger.exception(f"Error occurred: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            # 清理临时文件
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                logger.info(f"Temporary file removed: {pdf_path}")

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, port=5000)
