from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response
from flask_login import login_required, current_user
from .models import User, Upload, Diabetes, Heart, Park, Note, Appoint, To_Dos, Storage, Insurance
from . import db
from .diabetes import my_diabetes
from .heart import my_heart
from .parkinson import my_park
import json
import face_recognition
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
from PIL import Image
from urllib.request import urlopen
# from deepface import Deepface
import google.generativeai as palm
import smtplib
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv
load_dotenv()

views = Blueprint('views', __name__)

@views.route('/test/<string:dict_values>', methods=['POST'])
def test(dict_values):
    result = json.loads(dict_values) #this converts the json output to a python dictionary
    # output = request.get_json()
    # print(output) # This is the output that was stored in the JSON within the browser
    # print(type(output))
    print(result) # Printing the new dictionary
    print(type(result))#this shows the json converted as a python dictionary
    return redirect(url_for('auth.login'))

@views.route("/blockchainTable", methods=['POST', 'GET'])
def blockchainTable():
    return render_template("blockchainTable.html")

@views.route("/chatbotSubmit", methods=['POST', 'GET'])
def chatbotSubmit():
    user_input = str(request.form['chatbot-input'])
    palm.configure(api_key='AIzaSyCTwrVMMQHTPq1Ax1Il6_mNYpYrvQvXwxM')
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    # print(model)

    # prompt = "What is diabetes? Explain like I'm 5."

    completion = palm.generate_text(
        model=model,
        prompt=user_input,
        temperature=0.95,
        # The maximum length of the response
        max_output_tokens=200,
    )
    final_answer = completion.result
    if str(final_answer) == "None":
        final_answer = "I care for you, hence, I suggest you to consult our doctors for this question."
    # else:
    #     final_answer = final_answer.replace("*", "")
    print(final_answer)
    return render_template('healthcareBot.html', answer=final_answer, user_input=user_input, user=current_user)

@views.route('/healthcareBot')
def healthcareBot():
    return render_template("healthcareBot.html", user=current_user)

@views.route('/emergency_popup')
def emergency_popup():
    return render_template("emergency_popup.html")

@views.route('/emer_reg_user')
def emer_reg_user():
    return render_template("emer_reg_user.html")

@views.route('/emer_non_reg_user')
def emer_non_reg_user():
    return render_template("emer_non_reg_user.html")

@views.route('/user_location')
def user_location():
    url = 'http://ipinfo.io/json' 
    response = urlopen(url)
    data = json.load(response)
    print(data)
    data_str = data['loc']
    i = len(data_str) - 1
    final = ""
    while(data_str[i] != ","):
        final = final + data_str[i]
        i = i - 1
    longitude = final[::-1]
    j = 0
    result = ""
    while(data_str[j] != ","):
        result = result + data_str[j]
        j = j + 1
    latitude = result
    lat = float(latitude)
    long = float(longitude)
    print(lat, long)
    return render_template("user_location.html")

@views.route('/user_map')
def user_map():
    return render_template("user_map.html", user=current_user)

@views.route('/enter')
def enter():
    return render_template("hospital_entry.html")

@views.route('/lobby')
def lobby():
    return render_template('lobby.html', user=current_user)

@views.route('/room')
def room():
    return render_template('room.html', user=current_user)

@views.route('/meditate')
def meditate():
    return render_template("meditate.html", user=current_user)

"""
def gen_frames(camera, known_face_encodings, known_face_names, face_locations, face_encodings, face_names, process_this_frame):  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
            

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
"""

@views.route('/demo', methods=['POST', 'GET'])
def demo():
    if request.method == 'POST':
        image_file = request.files['image_file']
        if not image_file:
            return 'No image uploaded!', 400
        else:
            # my_file = "E:/Users/Alston Soares/Desktop/Demo-Codlions/website/static/profile_pics/Alston.png"
            # path2 = "E:/Users/Alston Soares/Desktop/Demo-Codlions/website/static/uploads/"
            # filename = secure_filename(image_file.filename)
            # fullpath2 = os.path.join(path2, filename)
            # image_file.save(fullpath2)

            for i in User.query.all():
                # uname = str(i.username)
                # ftype = str(i.filetype)
                if i.id != 1:
                    global glob_name
                    users = os.path.join(views.root_path, f"static/profile_pics/{i.username}.{i.filetype}")
                    picture_of_me = face_recognition.load_image_file(users)
                    # my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

                    encodings = face_recognition.face_encodings(picture_of_me)
                    if len(encodings) > 0:
                        my_face_encoding = encodings[0]
                    else:
                        glob_name = "Unknown"
                        break
                        

                        # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

                    # unknown_file = f"E:/Users/Alston Soares/Desktop/Demo-Codlions/website/static/uploads/{filename}"
                    # im = Image.open(unknown_file, mode='r', formats=None)

                    unknown_file = image_file

                    unknown_picture = face_recognition.load_image_file(unknown_file)
                    # unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

                    unk_encodings = face_recognition.face_encodings(unknown_picture)
                    if len(unk_encodings) > 0:
                        unknown_face_encoding = unk_encodings[0]
                    else:
                        glob_name = "Unknown"
                        flash("No faces found in image!", category="error")
                        break
                        # Now we can see the two face encodings are of the same person with `compare_faces`!

                    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

                    if results[0] == True:
                        flash(f"It's a picture of {i.username}! Emergency Number: {i.emerNumber}, Emergency Email: {i.emerEmail}", category="success")

                        email_sender = 'swasth249@gmail.com'
                        email_password = os.getenv("EMAIL_PASS")
                        email_receiver = str(i.emerEmail)
                        subject = "Critical Condition"
                        body = f"{i.username} is in a critical condition. Please come to the Hospital as soon as possible"
                        em = EmailMessage()
                        em['From'] = email_sender
                        em['To'] = email_receiver
                        em['Subject'] = subject
                        em.set_content(body)
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(email_sender, email_password)
                        server.sendmail(email_sender, email_receiver, em.as_string())
                        
                        # context = ssl.create_default_context()
                        # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        #     smtp.login(email_sender, email_password)
                        #     smtp.sendmail(email_sender, email_receiver, em.as_string())

                        glob_name = i.username
                        path3 = os.path.join(views.root_path, "static/uploads")
                        # image_type = image_file.mimetype
                        # i = len(image_type) - 1
                        # final = ""
                        # while(image_type[i] != "/"):
                        #     final = final + image_type[i]
                        #     i = i - 1
                        # filetype = final[::-1]
                        # result = f'{glob_name}.{filetype}'
                        fullpath3 = os.path.join(path3, secure_filename(image_file.filename))
                        image_file.save(fullpath3)
                        break
                    else:
                        print("It's not a picture of me!")
                        glob_name = "Unknown"
                        continue
    if glob_name == "Unknown":
        flash("No Record!", category="error")
        return render_template("capture.html")
    else:
        # user = User.query.filter_by(username = glob_name).first()
        # return render_template("records.html", user=user)
        return redirect('/enter')


# global glob_name 
# glob_name = "Alston"

@views.route('/capture')
def capture():
    return render_template("capture.html")

"""
@views.route('/face_rec')
def face_rec():
    camera = cv2.VideoCapture(0)
    # Load a sample picture and learn how to recognize it.
    user_image = face_recognition.load_image_file("Alston3.png") # f"static/profile_pics/{current_user.username}.{current_user.filetype}"
    user_face_encoding = face_recognition.face_encodings(user_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        user_face_encoding
    ]
    known_face_names = [
        "Alston"
    ]
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    return Response(gen_frames(camera, known_face_encodings, known_face_names, face_locations, face_encodings, face_names, process_this_frame), mimetype='multipart/x-mixed-replace; boundary=frame')
"""

@views.route('/listPatient', methods=['GET', 'POST'])
@login_required
def listPatient():
    if request.method == "POST":
        global glob_user_name
        glob_user_name = str(request.form['user_name'])
        user = User.query.filter_by(username=glob_user_name).first()
        my_user = User.query.filter_by(id=(user.id-1)).first()
        allusers = User.query.all()
        return render_template("listPatient.html", user=user, my_user=my_user, allusers=allusers)
    allusers = User.query.all()
    return render_template("listPatient.html", user=current_user, allusers=allusers)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.id != 1:
        return render_template("home.html", user=current_user)
    else:
        return render_template("admin.html", user=current_user)

@views.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    return render_template("about.html", user=current_user)

@views.route('/landing')
def landing():
    return render_template("Landingpg.html")

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@views.route('/admin_board', methods=['GET', 'POST'])
@login_required
def admin_board():
    return render_template("admin_board.html", user=current_user)

@views.route('/records', methods=['GET', 'POST'])
@login_required
def records():
    if 'glob_name' in globals():
        if glob_name == "Unknown":
            flash('No Record!', category='error')
            return redirect('/admin')
        else:
            user = User.query.filter_by(username=glob_name).first() # glob_name is declared in demo() function
            return render_template("records.html", user=user)
    else:
        flash('No Record!', category='error')
        return redirect('/admin')
    
@views.route('/get_records', methods=['GET', 'POST'])
@login_required
def get_records():
    if 'glob_user_name' in globals():
        user = User.query.filter_by(username=glob_user_name).first()
        return render_template("get_records.html", user=user)
    else:
        flash('No Record!', category='error')
        return redirect('/listPatient')
    
@views.route('/analytical_tests', methods=['GET', 'POST'])
@login_required
def analytical_tests():
    user = User.query.filter_by(username=glob_user_name).first()
    return render_template("analytical_tests.html", user=user)
 
@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.id == 1: 
        return render_template("admin.html", user=current_user)
    else:
        return 

@views.route('/storage')
def store():
    return render_template("storage.html", user=current_user) 

@views.route('/insurance')
def insurance():
    return render_template("insurance.html", user=current_user) 

@views.route('/fill_details', methods=['GET', 'POST'])
def fill_details():
    if request.method == 'POST':
        if(Upload.query.filter_by(user_id=current_user.id).count() > 0):
            upload = Upload.query.filter_by(user_id=current_user.id).first()
            emy_name= upload.my_name
            eage= upload.age
            edob= upload.dob
            egender= upload.gender
            eheight= upload.height
            eweight= upload.weight
            eblood_grp= upload.blood_grp
            eheart_attack= upload.heart_attack
            eregion= upload.region
            epincode= upload.pincode
            eallergies= upload.allergies
            emedic= upload.medic
            epast_medic= upload.past_medic
            ediabet= upload.diabet
            eparkin= upload.parkin
            eheart_dis= upload.heart_dis
            db.session.delete(upload)
            db.session.commit()
        else:
            emy_name= ""
            eage= ""
            edob= ""
            egender= ""
            eheight= ""
            eweight= ""
            eblood_grp= ""
            eheart_attack= ""
            eregion= ""
            epincode= ""
            eallergies= ""
            emedic= ""
            epast_medic= ""
            ediabet= ""
            eparkin= ""
            eheart_dis= ""
        
        if request.form.get('my_name', None): 
            my_name = request.form['my_name']
        else:
            my_name = emy_name
        if request.form.get('age', None):
            age = request.form['age']
        else:
            age = eage
        if request.form.get('dob', None):
            dob = request.form['dob']
        else:
            dob = edob
        if request.form.get('gender', None):
            gender = request.form['gender']
        else:
            gender = egender
        if request.form.get('height', None):
            height = request.form['height']
        else:
            height = eheight
        if request.form.get('weight', None): 
            weight = request.form['weight']
        else:
            weight = eweight
        if request.form.get('blood_grp', None): 
            blood_grp = request.form['blood_grp']
        else:
            blood_grp = eblood_grp
        if request.form.get('heart_attack', None): 
            heart_attack = request.form['heart_attack']
        else:
            heart_attack = eheart_attack
        if request.form.get('region', None): 
            region = request.form['region']
        else:
            region = eregion
        if request.form.get('pincode', None): 
            pincode = request.form['pincode']
        else:
            pincode = epincode
        if request.form.get('allergies', None): 
            allergies = request.form['allergies']
        else:
             allergies = eallergies
        if request.form.get('medic', None): 
            medic = request.form['medic']
        else:
            medic = emedic
        if request.form.get('past_medic', None): 
            past_medic = request.form['past_medic']
        else:
            past_medic = epast_medic
        if request.form.get('diabet', None): 
            diabet = request.form['diabet']
        else:
            diabet = ediabet
        if request.form.get('parkin', None): 
            parkin = request.form['parkin']
        else:
            parkin = eparkin
        if request.form.get('heart_dis', None): 
            heart_dis = request.form['heart_dis']
        else:
            heart_dis = eheart_dis
        new_upload = Upload(my_name=my_name, age=age, dob=dob, gender=gender, height=height, weight=weight,  blood_grp=blood_grp, heart_attack=heart_attack, region=region, pincode=pincode, allergies=allergies, medic=medic, past_medic=past_medic, diabet=diabet, parkin=parkin, heart_dis=heart_dis, user_id = current_user.id)
        db.session.add(new_upload)
        db.session.commit()
    return render_template("fill_details.html", user=current_user)

@views.route('/diabetes', methods=['POST', 'GET'])
def diabetes():
    if request.method == 'POST':
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        bloodpressure = float(request.form['bloodpressure'])
        skinthickness = float(request.form['skinthickness'])
        insulin = float(request.form['insulin'])
        BMI = float(request.form['BMI'])
        DiabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']
        age = float(request.form['age'])
        pred_diabetes = my_diabetes(pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age)
        my_user = User.query.filter_by(username=glob_user_name).first()
        new_diabetes = Diabetes(pregnancies=pregnancies, glucose=glucose, bloodpressure=bloodpressure, skinthickness=skinthickness, insulin=insulin, BMI=BMI, DiabetesPedigreeFunction=DiabetesPedigreeFunction, age=age, pred_diabetes=pred_diabetes[0], user_id = my_user.id)
        db.session.add(new_diabetes)
        db.session.commit()
        if pred_diabetes[0] == 1:
            flash('You can have Diabetes', category="error")
            print("Probability for diabetes: ", pred_diabetes[1])
            # return redirect('/diab_yes')
        else: 
            flash('You cannot have Diabetes', category="success")
            # return redirect('/diab_no')
    my_user = User.query.filter_by(username=glob_user_name).first()
    return render_template('diabetes_form.html', user=my_user)

@views.route('/heart', methods=['POST', 'GET'])
def heart():
    if request.method == 'POST':
        age = float(request.form['age'])
        s = request.form['sex']
        if s == 'M':
            sex = 1.0
        else:
            sex = 0.0
        cp = float(request.form['cp'])
        rbp = float(request.form['rbp'])
        chol = float(request.form['chol'])
        fbs = float(request.form['fbs'])
        recg = float(request.form['recg'])
        mhra = float(request.form['mhra'])
        exia = float(request.form['exia'])
        oldpeak = float(request.form['oldpeak'])
        slope = float(request.form['slope'])
        vcf = float(request.form['vcf'])
        thal = float(request.form['thal'])
        pred_heart = my_heart(age, sex, cp, rbp, chol, fbs, recg, mhra, exia, oldpeak, slope, vcf, thal)
        my_user = User.query.filter_by(username=glob_user_name).first()
        new_heart = Heart(age=age, sex=sex, cp=cp, rbp=rbp, chol=chol, fbs=fbs, recg=recg, mhra=mhra, exia=exia, oldpeak=oldpeak, slope=slope, vcf=vcf, thal=thal, pred_heart=pred_heart[0], user_id = my_user.id)
        db.session.add(new_heart)
        db.session.commit()
        if pred_heart[0] == 1:
            flash("You can have Heart Disease.", category="error")

        else: 
            flash('You cannot have Heart Disease', category="success")
    my_user = User.query.filter_by(username=glob_user_name).first()
    return render_template('heart_form.html', user=my_user)

@views.route('/uploadFile', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        my_file = request.files['image_file']
        if not my_file:
            return 'No file uploaded!', 400
        else:
            path2 = os.path.join(views.root_path, f"static/storage/{current_user.username}")
            result = secure_filename(my_file.filename)
            fullpath2 = os.path.join(path2, result)
            my_file.save(fullpath2)
            my_file_mimetype = my_file.mimetype
            store = Storage(my_file=result, my_file_mimetype=my_file_mimetype, user_id=current_user.id)
            db.session.add(store)
            db.session.commit()
            return redirect('/storage')

@views.route('/uploadInsuranceFile', methods=['POST', 'GET'])
def uploadInsurance():
    if request.method == 'POST':
        my_file = request.files['image_file']
        if not my_file:
            return 'No file uploaded!', 400
        else:
            path2 = os.path.join(views.root_path, f"static/insurance/{current_user.username}")
            result = secure_filename(my_file.filename)
            fullpath2 = os.path.join(path2, result)
            my_file.save(fullpath2)
            my_file_mimetype = my_file.mimetype
            store = Insurance(my_file=result, my_file_mimetype=my_file_mimetype, user_id=current_user.id)
            db.session.add(store)
            db.session.commit()
            return redirect('/insurance')

@views.route('/park', methods=['POST', 'GET'])
def park():
    if request.method == 'POST':
        mdvp_fo = float(request.form['mdvp_fo'])
        mdvp_fhi = float(request.form['mdvp_fhi'])
        mdvp_flo = float(request.form['mdvp_flo'])
        mdvp_jitter = float(request.form['mdvp_jitter'])
        mdvp_jitter_abs = float(request.form['mdvp_jitter_abs'])
        mdvp_rap = float(request.form['mdvp_rap'])
        mdvp_ppq = float(request.form['mdvp_ppq'])
        jitter_ddp = float(request.form['jitter_ddp'])
        mdvp_shimmer = float(request.form['mdvp_shimmer'])
        mdvp_shimmer_db = float(request.form['mdvp_shimmer_db'])
        mdvp_shimmer_apq3 = float(request.form['mdvp_shimmer_apq3'])
        mdvp_shimmer_apq5 = float(request.form['mdvp_shimmer_apq5'])
        mdvp_apq = float(request.form['mdvp_apq'])
        shimmer_dda = float(request.form['shimmer_dda'])
        nhr = float(request.form['nhr'])
        hnr = float(request.form['hnr'])
        rpde = float(request.form['rpde'])
        dfa = float(request.form['dfa'])
        spread1 = float(request.form['spread1'])
        spread2 = float(request.form['spread2'])
        d2 = float(request.form['d2'])
        ppe = float(request.form['ppe'])
        pred_park = my_park(mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitter, mdvp_jitter_abs, mdvp_rap, mdvp_ppq, jitter_ddp, mdvp_shimmer, mdvp_shimmer_db, mdvp_shimmer_apq3, mdvp_shimmer_apq5, mdvp_apq, shimmer_dda, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe)
        my_user = User.query.filter_by(username=glob_user_name).first()
        new_park = Park(mdvp_fo=mdvp_fo, mdvp_fhi=mdvp_fhi, mdvp_flo=mdvp_flo, mdvp_jitter=mdvp_jitter, mdvp_jitter_abs=mdvp_jitter_abs, mdvp_rap=mdvp_rap, mdvp_ppq=mdvp_ppq, jitter_ddp=jitter_ddp, mdvp_shimmer=mdvp_shimmer, mdvp_shimmer_db=mdvp_shimmer_db, mdvp_shimmer_apq3=mdvp_shimmer_apq3, mdvp_shimmer_apq5=mdvp_shimmer_apq5, mdvp_apq=mdvp_apq, shimmer_dda=shimmer_dda, nhr=nhr, hnr=hnr, rpde=rpde, spread2=spread2, d2=d2, dfa=dfa, ppe=ppe, pred_park=pred_park[0], user_id = my_user.id)
        db.session.add(new_park)
        db.session.commit()
        if pred_park[0] == 1:
            flash('You can have Parkinson Disease', category="error")
        else: 
            flash('You cannot have Parkinson Disease', category="success")
    my_user = User.query.filter_by(username=glob_user_name).first()
    return render_template('parkinson_form.html', user=my_user)

@views.route('/note', methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        note = request.form.get('note')
        my_note = str(note)
        if len(my_note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category='success')
    return render_template("notes.html", user=current_user)

@views.route('/todo', methods=['GET', 'POST'])
def todo_html():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) < 1 or len(desc) < 1:
            flash("Prescription is too short!", category='error')
        else:
            user = User.query.filter_by(username=glob_user_name).first()
            todo = To_Dos(title=title, desc=desc, user_id=user.id)
            db.session.add(todo)
            db.session.commit()
            flash("Prescription added!", category='success')
    user = User.query.filter_by(username=glob_user_name).first()
    return render_template("todo.html", user=user)

@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update_todo(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = To_Dos.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/todo')
    user = User.query.filter_by(username=glob_user_name).first()
    todo = To_Dos.query.filter_by(id=id).first()
    return render_template("update.html", todo=todo, user=user)

@views.route('/delete/<int:id>')
def delete_todo(id):
    todo = To_Dos.query.filter_by(id=id).first()
    user = User.query.filter_by(username=glob_user_name).first()
    if todo.user_id == user.id:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/todo')
    todo = To_Dos.query.filter_by(id=id).first()
    return render_template("todo.html", todo=todo, user=user)

@views.route('/store_delete/<int:id>')
def delete_store(id):
    sto = Storage.query.filter_by(id=id).first()
    if sto.user_id == current_user.id:
        my_path = os.path.join(views.root_path, f"static/storage/{current_user.username}/{sto.my_file}")
        if os.path.exists(my_path):
            os.remove(my_path)
        db.session.delete(sto)
        db.session.commit()
        return redirect('/storage')
    sto = Storage.query.filter_by(id=id).first()
    return render_template("storage.html", sto=sto, user=current_user)

@views.route('/insurance_delete/<int:id>')
def delete_insurance(id):
    sto = Insurance.query.filter_by(id=id).first()
    if sto.user_id == current_user.id:
        my_path = os.path.join(views.root_path, f"static/insurance/{current_user.username}/{sto.my_file}")
        if os.path.exists(my_path):
            os.remove(my_path)
        db.session.delete(sto)
        db.session.commit()
        return redirect('/insurance')
    sto = Insurance.query.filter_by(id=id).first()
    return render_template("insurance.html", sto=sto, user=current_user)

@views.route('/appoint', methods=['GET', 'POST'])
def appoint_html():
    if request.method == 'POST':
        t = request.form['t']
        d = request.form['d']
        time = request.form['time']
        # ti = str(t)
        # de = str(d)
        if len(t) < 1:
            flash("Appointment is too short!", category='error')
        else:
            appointed = Appoint(t=t, d=d, time=time, user_id=current_user.id)
            db.session.add(appointed)
            db.session.commit()
            flash("Appointment added!", category='success')
    return render_template("appointment.html", user=current_user)

@views.route('/appoint_update/<int:id>', methods=['GET', 'POST'])
def update_appoint(id):
    if request.method == 'POST':
        t = request.form['t']
        d = request.form['d']
        time = request.form['time']
        appointed = Appoint.query.filter_by(id=id).first()
        appointed.t = t
        appointed.d = d
        appointed.time = time
        db.session.add(appointed)
        db.session.commit()
        return redirect('/appoint')
    appointed = Appoint.query.filter_by(id=id).first()
    return render_template("appoint_update.html", appointed=appointed, user=current_user)

@views.route('/appoint_delete/<int:id>')
def delete_appoint(id):
    appointed = Appoint.query.filter_by(id=id).first()
    if appointed.user_id == current_user.id:
        db.session.delete(appointed)
        db.session.commit()
        return redirect('/appoint')
    appointed = Appoint.query.filter_by(id=id).first()
    return render_template("appointment.html", appointed=appointed, user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            redirect('notes.html')
    return jsonify({})

@views.route('/diab_reversal')
def diab_reversal():
    return render_template("diab_reversal.html", user=current_user)

@views.route('/diab_yes')
def diab_yes():
    return render_template("diab_popup_yes.html", user=current_user)

@views.route('/diab_no')
def diab_no():
    return render_template("diab_popup_no.html", user=current_user)