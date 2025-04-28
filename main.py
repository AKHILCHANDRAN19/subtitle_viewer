from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB max upload size

# HTML template for upload form and displaying subtitles
TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>SRT Viewer</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2em; }
    h1 { margin-bottom: 1em; }
    table { width: 100%; border-collapse: collapse; margin-top: 1em; }
    th, td { border: 1px solid #ccc; padding: 0.5em; text-align: left; }
    th { background-color: #f4f4f4; }
  </style>
</head>
<body>
  <h1>Upload an SRT File</h1>
  <form action="/" method="post" enctype="multipart/form-data">
    <input type="file" name="srt_file" accept=".srt" required>
    <button type="submit">Upload</button>
  </form>

  {% if subtitles %}
  <h2>Subtitles</h2>
  <table>
    <tr><th>#</th><th>Timestamp</th><th>Text</th></tr>
    {% for entry in subtitles %}
    <tr>
      <td>{{ entry.index }}</td>
      <td>{{ entry.timestamp }}</td>
      <td>{{ entry.text }}</td>
    </tr>
    {% endfor %}
  </table>
  {% endif %}
</body>
</html>
"""

def parse_srt(content):
    """Parse SRT content into a list of dicts with index, timestamp, and text."""
    entries = []
    blocks = content.strip().split('\n\n')
    for block in blocks:
        lines = block.splitlines()
        if len(lines) >= 3:
            idx = lines[0].strip()
            timestamp = lines[1].strip()
            text = ' '.join(line.strip() for line in lines[2:])
            entries.append({'index': idx, 'timestamp': timestamp, 'text': text})
    return entries

@app.route('/', methods=['GET', 'POST'])
def upload_and_display():
    subtitles = None
    if request.method == 'POST':
        file = request.files.get('srt_file')
        if file and file.filename.lower().endswith('.srt'):
            content = file.read().decode('utf-8', errors='ignore')
            subtitles = parse_srt(content)
    return render_template_string(TEMPLATE, subtitles=subtitles)

if __name__ == '__main__':
    # For deployment, use a proper WSGI server instead of Flask's built-in
    app.run(host='0.0.0.0', port=5000, debug=True)
