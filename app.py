from flask import Flask, request, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/hy-tmp/tmp'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image provided', 400
    file = request.files['image']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    print('save!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return 'Image saved successfully', 200

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return 'No image provided', 400
    file = request.files['image']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Call the table_ceil.py script using subprocess
    cmd = f"python table_ceil.py --isToExcel True --isToHtml True --jpgPath {file_path}"
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    
    print('----------------------------------')
    print(result)
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)