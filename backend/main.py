from flask import request, jsonify
from config import db, app
from models import Contact


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    
    return jsonify({"contacts": json_contacts})


@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    
    if not first_name or not last_name or not email:
        return jsonify({"message": "You must include all data"}), 400
    
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": f"Error during user creation: {e}"}), 400
    
    return jsonify({"message": "Successfully created new user"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id: int):
    contact = Contact.query.get(user_id)
    
    if not contact:
        return jsonify({"message": f"User with {user_id} id not found"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"message": f"User not updated: {e}"}), 400
    
    return jsonify({"message": "User updated successfully"}), 200
    
    
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id: int):
    contact = Contact.query.get(user_id)
    
    if not contact:
        return jsonify({"message": f"User with {user_id} id not found"}), 404

    try:
        db.session.delete(contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": f"User not deleted: {e}"}), 400
    
    return jsonify({"message": "User deleted successfully"}), 200

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)