from flask import Flask, request, jsonify
from flask_cors import CORS
from summarize import Summarizer

app = Flask(__name__)
CORS(app)

summarizer = Summarizer()

@app.route("/summarize", methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        print(data)
        linkType = data.get('linkType')
        link = data.get('link')
        
        if not link:
            return jsonify({'message': 'No link provided. Please provide a valid link.'}), 400
        
        if linkType not in ['youtube', 'webpage']:
            return jsonify({'message': 'Invalid type. Please select either "youtube" or "webpage".'}), 400
        
        if linkType == 'youtube':
            summary = summarizer.summarize_youtube_video(url=link)
            
            return jsonify({'summary': summary})
        elif linkType == 'webpage':
            summary = summarizer.sumarize_webpage(url=link)

            return jsonify({'summary': summary})
    except Exception as e:
        # If something goes wrong, return an error message
        return jsonify({'message': f'Error occurred: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)