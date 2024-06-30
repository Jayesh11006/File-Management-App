from flask import Flask, request, render_template, jsonify
import os
import json

app = Flask(__name__)

LOG_FILE = 'rename_log.json'

def rename_files(directory, prefix, sequence_type, new_extension=None):
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as log_file:
            json.dump([], log_file)

    with open(LOG_FILE, 'r') as log_file:
        rename_log = json.load(log_file)

    files = sorted(os.listdir(directory))
    
    if sequence_type == 'descending':
        files.reverse()

    results = []
    for count, filename in enumerate(files):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(filename)
            sequence_num = count + 1 if sequence_type == 'ascending' else len(files) - count
            new_name = f"{prefix}_{sequence_num}{ext if not new_extension else new_extension}"
            new_file_path = os.path.join(directory, new_name)
            os.rename(file_path, new_file_path)
            if ext == ".txt":
                with open(new_file_path, 'a') as file:
                    file.write("\nModified by rename script.")
            results.append(f"Renamed: {filename} to {new_name}")
            rename_log.append({"old_name": file_path, "new_name": new_file_path})

    with open(LOG_FILE, 'w') as log_file:
        json.dump(rename_log, log_file)

    return results

def undo_rename():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, 'r') as log_file:
        rename_log = json.load(log_file)

    for entry in reversed(rename_log):
        os.rename(entry["new_name"], entry["old_name"])

    os.remove(LOG_FILE)
    return [f"Restored: {entry['new_name']} to {entry['old_name']}" for entry in rename_log]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rename', methods=['POST'])
def rename():
    directory = request.form['directory']
    prefix = request.form['prefix']
    sequence_type = request.form['sequence_type']
    new_extension = request.form.get('new_extension', None)
    results = rename_files(directory, prefix, sequence_type, new_extension)
    return jsonify(results)

@app.route('/undo', methods=['POST'])
def undo():
    results = undo_rename()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
