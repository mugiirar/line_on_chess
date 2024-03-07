from flask import Flask, request, jsonify

app = Flask(__name__)

array = []

@app.route('/upload', methods=['POST'])
def receive_data():
    global array
    try:
        # Get the JSON data containing the array and player_id
        data = request.get_json()
        
        # Extract the array and player_id from the JSON data
        array = data['array']
        player_id = data['player_id']
        
        # Process the array and player_id (you can do whatever you want with them)
        print("Received array:", array)
        print("Received player ID:", player_id)
        
        # Return a response
        return jsonify({'message': 'Data received successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def array_pass():
    global array
    if array == []:
        array = [
                 ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],  # Black back rank
                 ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # Black pawns
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],  # White pawns
                 ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]   # White back rank
        ]
    return jsonify(array=array)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
