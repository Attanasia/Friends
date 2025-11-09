from flask import Flask, jsonify, request
import pandas as pd
import logging


# Setup
app = Flask(__name__)

LOG_FILE = "friends_analysis.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load CSV data into memory
try:
    df = pd.read_csv("friends_data.csv")
    logging.info("CSV loaded successfully.")
except Exception as e:
    logging.error(f"Error loading CSV: {str(e)}")
    df = pd.DataFrame()  # empty DataFrame if error occurs

# Step 3: Pagination Endpoint
@app.route("/characters", methods=["GET"])
def get_characters():
    try:
        # Get query params for pagination
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        
        if page < 1 or per_page < 1:
            return jsonify({"error": "page and per_page must be positive integers"}), 400
        
        # Calculate start/end indices
        start = (page - 1) * per_page
        end = start + per_page
        
        # Slice the DataFrame
        data = df.iloc[start:end].to_dict(orient="records")
        
        # Pagination metadata
        meta = {
            "page": page,
            "per_page": per_page,
            "total_records": len(df),
            "total_pages": (len(df) + per_page - 1) // per_page
        }
        
        return jsonify({"meta": meta, "data": data})
    
    except Exception as e:
        logging.error(f"Error in /characters endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Step 4: Search Endpoint
@app.route("/characters/search", methods=["GET"])
def search_characters():
    try:
        # Get query parameters
        first_name = request.args.get("first_name", "").strip().lower()
        last_name = request.args.get("last_name", "").strip().lower()
        
        if not first_name and not last_name:
            return jsonify({"error": "Provide at least first_name or last_name"}), 400
        
        # Filter DataFrame
        filtered_df = df.copy()
        if first_name:
            filtered_df = filtered_df[filtered_df['first_name'].str.lower().str.contains(first_name)]
        if last_name:
            filtered_df = filtered_df[filtered_df['last_name'].str.lower().str.contains(last_name)]
        
        # Convert to dict
        data = filtered_df.to_dict(orient="records")
        
        return jsonify({"total_matches": len(data), "data": data})
    
    except Exception as e:
        logging.error(f"Error in /characters/search endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/characters/<int:char_id>", methods=["PUT"])
def update_character(char_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request must contain JSON body"}), 400

        global df  # so we can modify the global DataFrame

        # Find the row with the matching ID
        if char_id not in df['id'].values:
            return jsonify({"error": f"Character with id {char_id} not found"}), 404

        # Update the fields in that row
        for key, value in data.items():
            if key in df.columns:
                df.loc[df['id'] == char_id, key] = value
            else:
                logging.warning(f"Invalid field ignored: {key}")

        # Save updated DataFrame back to CSV
        df.to_csv("friends_data.csv", index=False)
        logging.info(f"Character {char_id} updated successfully.")

        # Return success message
        updated_record = df[df['id'] == char_id].to_dict(orient="records")[0]
        return jsonify({
            "message": f"Character {char_id} updated successfully",
            "updated_record": updated_record
        }), 200

    except Exception as e:
        logging.error(f"Error updating character {char_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/characters/<int:char_id>", methods=["DELETE"])
def delete_character(char_id):
    try:
        global df

        # Check if ID exists
        if char_id not in df['id'].values:
            return jsonify({"error": f"Character with id {char_id} not found"}), 404

        # Remove the character
        df = df[df['id'] != char_id]

        # Save updated CSV
        df.to_csv("friends_data.csv", index=False)
        logging.info(f"Character {char_id} deleted successfully.")

        return jsonify({
            "message": f"Character {char_id} deleted successfully",
            "remaining_records": len(df)
        }), 200

    except Exception as e:
        logging.error(f"Error deleting character {char_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Friends Cast REST API!",

    }), 200


# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
