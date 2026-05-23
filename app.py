from flask import Flask, make_response,request, render_template_string,render_template,url_for, redirect, url_for, send_from_directory
import sqlite3
import base64
import uuid
from datetime import datetime
from chargily_pay import ChargilyClient
from chargily_pay.settings import CHARGILIY_TEST_URL
from chargily_pay import ChargilyClient
from chargily_pay.entity import Checkout
key = "test_pk_X1bOC5YF2eCQi6G6JLyp63Ag3T1q9mqDlJJ9AxYH"
secret = "test_sk_RN8EptRiIVs9exz8pCDWenEqkhtA4fZFmdJOr0fB"
chargily = ChargilyClient(key, secret, CHARGILIY_TEST_URL)
app = Flask(__name__)
from ultralytics import YOLO
import os, json, numpy as np
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# LOAD MODEL + DB
# =========================
model = YOLO("best_yolov8s.pt")

with open("nutrition_db.json") as f:
    nutrition_db = json.load(f)

print("✅ Model loaded")


# =========================
# SERVE IMAGES
# =========================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# =========================
# CALC FUNCTION
# =========================
def estimate_calories(image_path):
    results = model(image_path, conf=0.3)[0]

    detected_foods = []
    total_calories = total_protein = total_carbs = total_fat = 0

    if results.masks is None:
        return [], None

    for mask, box, conf in zip(
        results.masks.data,
        results.boxes,
        results.boxes.conf
    ):
        class_id = int(box.cls.item())
        food_name = results.names[class_id]
        confidence = float(conf.item())

        mask_np = mask.cpu().numpy()
        portion_ratio = float(mask_np.sum()) / float(mask_np.size)
        grams = portion_ratio * 500

        if food_name in nutrition_db:
            n = nutrition_db[food_name]
            factor = grams / 100

            calories = n["calories"] * factor
            protein  = n["protein"] * factor
            carbs    = n["carbs"] * factor
            fat      = n["fat"] * factor
        else:
            calories = protein = carbs = fat = 0

        detected_foods.append({
            "name": food_name,
            "conf": round(confidence, 2),
            "grams": round(grams, 1),
            "cal": round(calories, 1),
            "protein": round(protein, 1),
            "carbs": round(carbs, 1),
            "fat": round(fat, 1),
        })

        total_calories += calories
        total_protein += protein
        total_carbs += carbs
        total_fat += fat

    totals = {
        "cal": round(total_calories, 1),
        "protein": round(total_protein, 1),
        "carbs": round(total_carbs, 1),
        "fat": round(total_fat, 1),
    }

    return detected_foods, totals


# =========================
# /calories PAGE
# =========================
@app.route("/calories", methods=["GET", "POST"])
def calories():
    foods = None
    totals = None
    image_url = None

    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            foods, totals = estimate_calories(path)
            image_url = "/uploads/" + filename

    return render_template("calories.html", foods=foods, totals=totals, image_url=image_url)

@app.route("/update_availability", methods=["POST"])
def update_availability():
    availability = request.form.get("availability")

    # 🔑 récupérer email depuis cookie
    coach_email = request.cookies.get("EID")

    if not coach_email:
        return redirect("/login")

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE coach
        SET availability = ?
        WHERE email = ?
    """, (availability, coach_email))

    conn.commit()
    conn.close()

    return redirect("/nutritionist")
@app.route("/joinmeet")
def joinmeet():

    user_email = request.cookies.get("EID")

    if not user_email:
        return redirect("/login")

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    # get coach id (email)
    cur.execute("SELECT coid FROM client WHERE email=?", (user_email,))
    result = cur.fetchone()

    if not result or not result[0]:
        conn.close()
        return "No coach assigned", 400

    coach_email = result[0]
    conn.close()

    # remove domain (before @)
    user_name = user_email.split("@")[0]
    coach_name = coach_email.split("@")[0]

    room_name = f"75554{user_name}-{coach_name}75555"

    return render_template("joinmeet.html", room=room_name)
@app.route('/joinmeetcoach')
def join_meet_coach():
    # 1. Get client mail from the 'Open' button link
    client_email = request.args.get('client_email')
    
    # 2. Get coach ID (mail without domain) from cookies
    coach_name = request.cookies.get('EID')


    # 3. Extract client name (part before @)
    user_name = client_email.split("@")[0]
    coach_namee = coach_name.split("@")[0]
    # 4. Create the room name using your format: user-coach
    room_name = f"75554{user_name}-{coach_namee}75555"

    # 5. Render the meeting page
    return render_template("joinmeet.html", room=room_name)
@app.route("/nutseeclient")
def nutseeclient():

    cid = request.args.get("eid")
    if not cid:
        return "Missing client email", 400

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    # ================= PROGRESS (GRAPH) =================
    cur.execute("""
        SELECT date, weight, bc, ce
        FROM progres
        WHERE email=?
        ORDER BY date ASC
        LIMIT 10
    """, (cid,))
    progress = cur.fetchall()

    # ================= REPAS (dietrep) =================
    cur.execute("""
        SELECT dietid, mustcontain, calories, minerals, hour
        FROM dietrep
        WHERE cid=?
        ORDER BY dietid DESC
    """, (cid,))
    repas = cur.fetchall()

    conn.close()

    return render_template(
        "nutseeclient.html",
        cid=cid,
        data=progress,
        repas=repas
    )

@app.route("/add_repas", methods=["POST"])
def add_repas():

    cid = request.form["cid"]
    coid = request.cookies.get("EID")

    mustcontain = request.form["mustcontain"]
    calories = request.form["calories"]
    minerals = request.form["minerals"]
    hour = request.form["hour"]

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO dietrep (cid, coid, calories, mustcontain, minerals, hour)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cid, coid, calories, mustcontain, minerals, hour))

    conn.commit()
    conn.close()

    return redirect(url_for("nutseeclient", eid=cid))
@app.route("/delete_repas", methods=["POST"])
def delete_repas():

    dietid = request.form["dietid"]
    cid = request.form["cid"]

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM dietrep WHERE dietid=?", (dietid,))

    conn.commit()
    conn.close()

    return redirect(url_for("nutseeclient", eid=cid))


@app.route("/acceptco", methods=["POST"])
def acceptco():
    admin = request.cookies.get("EID")
    if not admin:
        return "Unauthorized", 403

    email = request.form.get("email")

    if not email:
        return "Missing email", 400

    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()


    cursor.execute("UPDATE coach SET acs = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    return redirect(url_for("apanel"))
@app.route("/rejectco", methods=["POST"])
def rejectco():
    admin = request.cookies.get("EID")

    # 🔒 Check admin cookie
    if not admin:
        return "Unauthorized", 403

    email = request.form.get("email")

    if not email:
        return "Missing email", 400

    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()

    # ❌ Delete coach
    cursor.execute("DELETE FROM coach WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    return redirect(url_for("apanel"))
@app.route("/deleto", methods=["POST"])
def deleto():
    admin = request.cookies.get("EID")

    # 🔒 Check admin cookie
    if not admin:
        return "Unauthorized", 403

    email = request.form.get("email")

    if not email:
        return "Missing email", 400

    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()

    # ❌ Delete user
    cursor.execute("DELETE FROM client WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    return redirect(url_for("apanel"))  # change if needed
@app.route("/accepto", methods=["POST"])
def accepto():
    admin = request.cookies.get("EID")

    # 🔒 Check admin cookie
    if not admin:
        return "Unauthorized", 403

    email = request.form.get("email")

    if not email:
        return "Missing email", 400

    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()

    # ✅ Activate account
    cursor.execute("UPDATE client SET ac = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    return redirect(url_for("apanel")) 

@app.route("/progres", methods=["POST"])
def progres():

   
    email = request.cookies.get("EID")
    if not email:
        return "Unauthorized", 403


    date = request.form.get("date")
    ce = request.form.get("calories_eaten")
    bc = request.form.get("calories_burned")
    plates = request.form.get("plates_eaten")
    minerals = request.form.get("missing_minerals")
    weight = request.form.get("weight")

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()


    cur.execute("""
        INSERT INTO progres (email, date, ce, bc, weight, npe, mm)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (email, date, ce, bc, weight, plates, minerals))

    conn.commit()
    conn.close()
    return redirect(url_for("upanel"))
@app.route("/book_consultation", methods=["POST"])
def book_consultation():
    client_email = request.form.get("client_email")
    date = request.form.get("date")
    notes = request.form.get("notes")  # optional

    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()


    cursor.execute("SELECT coid FROM client WHERE email = ?", (client_email,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return "Client or coach not found", 400

    nutemail = result[0]

    # 2. Generate request date (current time)
    reqdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 3. Insert into consultation table
    cursor.execute("""
        INSERT INTO consultation (cemail, nutemail, date, status, reqdate,obs)
        VALUES (?, ?, ?, ?, ?,?)
    """, (client_email, nutemail, date, "confirmed", reqdate,notes))

    conn.commit()
    conn.close()

    return redirect(url_for("upanel"))  # or your dashboard route
@app.route("/upanel")
def upanel():
    cid = request.cookies.get("EID")  # client email saved in cookie at login
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT calories, mustcontain, minerals, coid ,hour
        FROM dietrep 
        WHERE cid=?
        ORDER BY dietid ASC
    """, (cid,))
    diets = cur.fetchall()
    conn.close()

    connn = sqlite3.connect("db.db")
    cur = connn.cursor()

    cur.execute("""SELECT date, ce, bc, weight FROM progres WHERE email=? ORDER BY date ASC """, (cid,))
    
    data = cur.fetchall()
    connn.close()
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT coid
        FROM client
        WHERE email=?
    """, (cid,))
    result = cur.fetchone()

    availability = None

    if result and result[0]:
        coach_id = result[0]

        cur.execute("""
            SELECT availability
            FROM coach
            WHERE email=?
        """, (coach_id,))

        coach = cur.fetchone()

        if coach:
            availability = coach[0]

    conn.close()

    return render_template("upanel.html", diets=diets,data=data,availability=availability)
@app.route("/logincaaa", methods=["POST"])
def logincaaa():

    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM coach 
    WHERE email=? AND password=?
    """, (email, password))

    coach = cur.fetchone()

    conn.close()

    if coach:
        resp = make_response(redirect("/nutritionist"))
        resp.set_cookie("EID", email)  # save coach email in cookie
        return resp

    else:
        return render_template("login.html", err="Invalid email or password")



@app.route("/nutritionist")
def nutritionist():

    coach_email = request.cookies.get("EID")  

    if not coach_email:
        return redirect("/loginca")

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT * 
    FROM consultation 
    WHERE nutemail=? 
    ORDER BY reqdate ASC
    """, (coach_email,))
    
    requests = cur.fetchall()


    cur.execute("""
    SELECT email, fullname, phone 
    FROM client 
    WHERE ac=1 AND coid=? 
    """, (coach_email,))
    
    clients = cur.fetchall()

    conn.close()
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("SELECT availability FROM coach WHERE email=?", (coach_email,))
    row = cur.fetchone()

    availability = row[0] if row else ""

    conn.close()
    return render_template("netpanel.html", requests=requests, clients=clients,availability =availability )



@app.route("/accept_req", methods=["POST"])
def accept_req():

    coach_email = request.cookies.get("EID")
    id = request.form["id"]

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
    UPDATE consultation 
    SET status='accepted' 
    WHERE id=? AND nutemail=?
    """, (id, coach_email))

    conn.commit()
    conn.close()

    return redirect("/nutritionist")


@app.route("/decline_req", methods=["POST"])
def decline_req():

    coach_email = request.cookies.get("EID")
    id = request.form["id"]

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
    UPDATE consultation 
    SET status='rejected' 
    WHERE id=? AND nutemail=?
    """, (id, coach_email))

    conn.commit()
    conn.close()

    return redirect("/nutritionist")



def chc():
  EID = request.cookies.get('EID')
  EID=str(EID)
  if EID=="" or EID==0 or EID=="0" or EID=="None":return redirect(url_for("index"))
@app.route('/') 
def index():
     return render_template('home.html')
@app.route('/login') 
def login():
     return render_template('login.html')
@app.route('/homeba') 
def homeba():
     return render_template('homeba.html')
@app.route('/signupba') 
def signupba():
     return render_template('signupba.html')
@app.route("/add_admin", methods=["POST"])
def add_admin():

    email=request.form["email"]
    password=request.form["password"]
    fullname=request.form["fullname"]

    
    con=sqlite3.connect("db.db")
    cur=con.cursor()

    cur.execute("""
    INSERT INTO admin (email,password,fullname)
    VALUES (?,?,?)
    """,(email,password,fullname))

    con.commit()
    con.close()

    return redirect("/apanel")
@app.route('/signupco') 
def signupco():
     return render_template('signupco.html')
@app.route("/checkba", methods=["POST"])
def checkba():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("db.db")
    conn.row_factory = sqlite3.Row  
    cur = conn.cursor()

    # Check if the user exists in the database
    cur.execute("SELECT * FROM client WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()

    if user and user["acctype"] == "basic":
        # User exists, set session data
        email = user["email"]
         
        
        # Fetch fullname, email, AND availability from coach
        cur.execute("SELECT fullname, email, availability FROM coach")
        coaches = cur.fetchall()
        
        conn.close()

        # Pass the email and the coaches list to the template
        return render_template("homeba.html", email=email, coaches=coaches)
    else:
        conn.close()
        # If no match is found
        return render_template("login.html", err="credintials err")
@app.route("/coach_signup", methods=["POST"])
def coach_signup():

    email=request.form["email"]
    password=request.form["password"]
    fullname=request.form["fullname"]
    phone=request.form["phone"]
    degree=request.form["degree"]
    spec=request.form["spec"]
    acs=0
    photo = request.files["photo"].read()
    pdl=request.form["pdl"]

    con=sqlite3.connect("db.db")
    cur=con.cursor()

    cur.execute("""
    INSERT INTO coach
    (email,password,fullname,phone,degree,spec,acs,pdl,photo)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,(email,password,fullname,phone,degree,spec,acs,pdl,photo))

    con.commit()
    con.close()

    return render_template("wvc.html")
@app.route("/detailsco")
def details_coach():
    id = request.args.get("id")
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT email, password, fullname, phone, degree, spec, acs, pdl, photo 
        FROM coach 
        WHERE email=?
    """, (id,))
    codet = cur.fetchone()
    conn.close()

   

    return render_template("detailsco.html", codet=codet)
@app.route("/logina", methods=["POST"])
def logina():

    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("SELECT password, ac FROM client WHERE email=?", (email,))
    user = cur.fetchone()

    conn.close()

    if user:

        db_password = user[0]
        ac = user[1]

        if password == db_password:

            if ac == 1:
                       resp = make_response(redirect(url_for("upanel")))
                       resp.set_cookie("EID",email)
                       return resp

            else:
                return render_template("conf.html")

        else:
            return render_template("login.html", err="login credentials err")

    else:
        return render_template("login.html", err="login credentials err")
@app.route('/loginca') 
def loginca():
     return render_template('loginca.html')
@app.route('/blog') 
def blog():
     return render_template('blog.html')
@app.route("/logincaa", methods=["POST"])
def logincaa():

    email = request.form["email"]
    password = request.form["password"]


    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("SELECT password FROM admin WHERE email=?", (email,))
    user = cur.fetchone()

    conn.close()

    if user:

        db_password = user[0]

        if password == db_password:
               resp = make_response(redirect(url_for("apanel")))
               resp.set_cookie("EID",email)
               return resp
              
        else:
            return render_template("loginca.html", err="login credentials err")

    else:
        return render_template("login.html", err="login credentials err")
@app.route('/signup')
def signup():
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("SELECT email, fullname FROM coach")
    coaches = cur.fetchall()

    conn.close()

    return render_template('signup.html', coaches=coaches)
from flask import request, redirect
import sqlite3
@app.route("/details", methods=["GET"])
def details():
 conn = sqlite3.connect("db.db")
 cur = conn.cursor()
 cur2 = conn.cursor()
 EID = request.cookies.get('EID')
 EID=str(EID)
 if EID=="" or EID==0 or EID=="0" or EID=="None":return redirect(url_for("index"))
 else:
  idd=request.args.get("id")
  iddd=request.args.get("idd")
  cur.execute("SELECT email, fullname, age, goals, alergies, dss, height, weight, salary, phone FROM client WHERE email=?",(idd,))
  userd = cur.fetchone()
  cur2.execute("SELECT photo FROM client WHERE email=?",(idd,))
  photo = cur2.fetchone()
  img = base64.b64encode(photo[0]).decode("utf-8")
  return render_template("details.html", userd=userd,img=img,idd=idd)


@app.route("/insc", methods=["POST"])
def insc():

    fullname = request.form["fullname"]
    age = request.form["age"]
    email = request.form["email"]
    phone = request.form["phone"]
    password = request.form["password"]
    weight = request.form["weight"]
    height = request.form["height"]
    dss = request.form["dss"]
    goals = request.form["goals"]
    alergies = request.form["alergies"]
    salary = request.form["salary"]
    coid = request.form["coach_email"]
    photo = request.files["photo"].read()

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    # create inactive account
    cur.execute("""
    INSERT INTO client
    (email, fullname, age, password, goals, alergies, dss, height, weight, salary, ac, phone, photo,coid)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    """,
    (email, fullname, age, password, goals, alergies, dss, height, weight, salary, -1, phone, photo,coid)
    )

    conn.commit()
    conn.close()

    # create payment checkout
    checkout_url = create_chargily_checkout(email)

    return checkout_url



def create_chargily_checkout(email):

     success_url= f"http://localhost:5000/payment_success?email={email}"
     failure_url= f"http://localhost:5000/payment_fail?email={email}"
     checkout = chargily.create_checkout(Checkout(items=[{"price": '01kq0taztses2evmw61sb79b2y', "quantity": 1}],success_url=success_url,failure_url=failure_url))
     print(checkout)
     return redirect(checkout["checkout_url"])


@app.route('/conff') 
def conff():
     return render_template('conf.html')
@app.route("/payment_success")
def payment_success():
    email = request.args.get("email")

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    # activate account
    cur.execute("UPDATE client SET ac = 0 WHERE email = ?", (email,))
    
    conn.commit()
    conn.close()

    return render_template("conf.html")
@app.route("/payment_fail")
def payment_fail():
    email = request.args.get("email")

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    # delete user
    cur.execute("DELETE FROM client WHERE email = ?", (email,))
    
    conn.commit()
    conn.close()

    return redirect("/signup")

@app.route('/panel')

def panel():
  EID = request.cookies.get('EID')
  EID=str(EID)
  if EID=="" or EID==0 or EID=="0" or EID=="None":return redirect(url_for("login"))
  else:
   return render_template('cpanel.html')
@app.route("/inscb", methods=["POST"])
def inscb():
    # Retrieve form data matching your HTML name attributes
    fullname = request.form["fullname"]
    age = request.form["age"]
    email = request.form["email"]
    phone = request.form["phone"]
    password = request.form["password"]
    weight = request.form["weight"]
    height = request.form["height"]
    dss = request.form["dss"]
    goals = request.form["goals"]
    alergies = request.form["alergies"]
    salary = request.form["salary"]
    
    # Read image as BLOB using the same logic as your other routes
    photo = request.files["photo"].read()
    
    # Your rule: ac is always 1 for this route
    ac = 1
    
    # coid is not in this specific HTML form, so we set it to None (NULL in DB)
    coid = None 

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO client
    (email, fullname, age, password, goals, alergies, dss, height, weight, salary, ac, phone, photo, coid)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (email, fullname, age, password, goals, alergies, dss, height, weight, salary, ac, phone, photo, coid)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("conff"))
@app.route("/apanel")
def apanel():
 EID = request.cookies.get('EID')
 EID=str(EID)
 if EID=="" or EID==0 or EID=="0" or EID=="None":return redirect(url_for("index"))
 else:
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    cur2 = conn.cursor()
    cur.execute("SELECT fullname, phone, email FROM client WHERE ac=0")
    cur2.execute("SELECT fullname, phone, email FROM coach WHERE acs=0")
    users = cur.fetchall()
    coaches=cur2.fetchall()
    conn.close()
     
    return render_template("apanel.html", users=users ,coaches=coaches)
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)