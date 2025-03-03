from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models import User, Image
from app import db
from app.steganography import encode_image, decode_image
from datetime import datetime

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@main.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        current_app.logger.error(f"Error in index route: {str(e)}")
        return "An error occurred", 500

@main.route('/dashboard')
@login_required
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        current_app.logger.error(f"Error in dashboard route: {str(e)}")
        return "An error occurred", 500

@main.route('/encode', methods=['POST'])
@login_required
def encode():
    try:
        # Ensure upload directory exists
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        if 'image' not in request.files:
            flash('No image uploaded', 'danger')
            return redirect(url_for('main.dashboard'))

        file = request.files['image']
        message = request.form.get('message')

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('main.dashboard'))

        if file and allowed_file(file.filename):
            if file.filename is None:
                flash('Invalid filename', 'danger')
                return redirect(url_for('main.dashboard'))
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                encoded_img = encode_image(filepath, message)
                encoded_filename = f'encoded_{filename}'
                encoded_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], encoded_filename)
                encoded_img.save(encoded_filepath)
                # In encode route
                # Save to database
                image = Image()
                image.filename = encoded_filename
                image.operation_type = 'encode'
                image.user_id = current_user.id
                image.timestamp = datetime.utcnow()
                db.session.add(image)
                db.session.commit()
                # Clean up original file
                if os.path.exists(filepath):
                    os.remove(filepath)

                # Return success page with download link
                return render_template('encode_result.html', filename=encoded_filename)

            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                flash(f'Error encoding message: {str(e)}', 'danger')
                return redirect(url_for('main.dashboard'))

        flash('Invalid file type', 'danger')
        return redirect(url_for('main.dashboard'))

    except Exception as e:
        current_app.logger.error(f"Error in encode route: {str(e)}")
        flash('An error occurred during encoding', 'danger')
        return redirect(url_for('main.dashboard'))

@main.route('/decode', methods=['POST'])
@login_required
def decode():
    try:
        # Ensure upload directory exists
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        if 'encoded_image' not in request.files:
            flash('No image uploaded', 'danger')
            return redirect(url_for('main.dashboard'))

        file = request.files['encoded_image']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('main.dashboard'))

        if file and allowed_file(file.filename):
            if file.filename is None:
                raise ValueError("Filename cannot be None")
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                message = decode_image(filepath)
                # Save to database
                image = Image()
                image.filename = filename
                image.operation_type = 'decode'
                image.user_id = current_user.id
                image.timestamp = datetime.utcnow()
                db.session.add(image)
                db.session.commit()
                # Clean up file
                if os.path.exists(filepath):
                    os.remove(filepath)

                return render_template('result.html', message=message)

            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                flash(f'Error decoding message: {str(e)}', 'danger')
                return redirect(url_for('main.dashboard'))

        flash('Invalid file type', 'danger')
        return redirect(url_for('main.dashboard'))

    except Exception as e:
        current_app.logger.error(f"Error in decode route: {str(e)}")
        flash('An error occurred during decoding', 'danger')
        return redirect(url_for('main.dashboard'))

@main.route('/download/<filename>')
@login_required
def download(filename):
    try:
        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
            flash('File not found', 'danger')
            return redirect(url_for('main.dashboard'))
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        current_app.logger.error(f"Error in download route: {str(e)}")
        flash('Error downloading file', 'danger')
        return redirect(url_for('main.dashboard'))

@main.route('/history')
@login_required
def history():
    try:
        images = Image.query.filter_by(user_id=current_user.id).order_by(Image.timestamp.desc()).all()
        return render_template('history.html', images=images)
    except Exception as e:
        current_app.logger.error(f"Error in history route: {str(e)}")
        return "An error occurred", 500