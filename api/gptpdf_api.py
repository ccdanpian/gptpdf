import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from gptpdf import parse_pdf
import dotenv

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

@app.route('/parse_pdf', methods=['POST'])
def api_parse_pdf():
    print("Received request to parse PDF")
    if 'file' not in request.files:
        print("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        try:
            # 使用接收到的文件名（即 fileId）
            pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
            print(f"Saving file to: {pdf_path}")
            file.save(pdf_path)
            
            if not os.path.exists(pdf_path):
                print(f"File was not saved successfully: {pdf_path}")
                return jsonify({"error": "File was not saved successfully"}), 500

            # 设置输出目录
            output_dir = os.path.join(OUTPUT_FOLDER, os.path.splitext(file.filename)[0])
            print(f"Output directory: {output_dir}")
            
            # 解析PDF
            api_key = os.getenv('OPENAI_API_KEY')
            base_url = os.getenv('OPENAI_API_BASE')
            print("Starting PDF parsing")
            content, image_paths = parse_pdf(pdf_path, output_dir=output_dir, api_key=api_key, base_url=base_url, model='gpt-4o', gpt_worker=6)
            
            print("PDF parsing completed")
            return jsonify({
                "content": content,
                "image_paths": image_paths
            })
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            # 清理临时文件
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                print(f"Temporary file removed: {pdf_path}")

if __name__ == '__main__':
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    app.run(debug=True, port=5000)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from gptpdf import parse_pdf
import dotenv

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

@app.route('/parse_pdf', methods=['POST'])
def api_parse_pdf():
    print("Received request to parse PDF")
    if 'file' not in request.files:
        print("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        try:
            # 使用接收到的文件名（即 fileId）
            pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
            print(f"Saving file to: {pdf_path}")
            file.save(pdf_path)
            
            if not os.path.exists(pdf_path):
                print(f"File was not saved successfully: {pdf_path}")
                return jsonify({"error": "File was not saved successfully"}), 500

            # 设置输出目录
            output_dir = os.path.join(OUTPUT_FOLDER, os.path.splitext(file.filename)[0])
            print(f"Output directory: {output_dir}")
            
            # 解析PDF
            api_key = os.getenv('OPENAI_API_KEY')
            base_url = os.getenv('OPENAI_API_BASE')
            print("Starting PDF parsing")
            content, image_paths = parse_pdf(pdf_path, output_dir=output_dir, api_key=api_key, base_url=base_url, model='gpt-4o', gpt_worker=6)
            
            print("PDF parsing completed")
            return jsonify({
                "content": content,
                "image_paths": image_paths
            })
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            # 清理临时文件
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                print(f"Temporary file removed: {pdf_path}")

if __name__ == '__main__':
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    app.run(debug=True, port=5000)
