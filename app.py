from flask import Flask,render_template,jsonify,request,session,url_for,redirect    
import firebase_admin
from firebase_admin import credentials, db,firestore,storage,auth
import random
import os
import json
import uuid
cred=credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred,{'databaseURL':'https://rwpd-micro-project-default-rtdb.asia-southeast1.firebasedatabase.app/','storageBucket': 'gs://rwpd-micro-project.appspot.com'})

print("Current working directory:", os.getcwd())
print("Templates folder exists:", os.path.exists("./templates"))

user_id=random.randint(0000000,9999999)
p_id=random.randint(1000,9999)
users_ref=db.reference()
products_ref=db.reference()
bucket = storage.bucket()


Keywordrs_mens_t_shirt=['tshirt for man','men\'s tshirt','t-shirt for men','t-shirt for man','tshirt for men','tshirt','t-shirt','tshirt for men stylish']

Keywordrs_mens_shirt=['shirt','shirt for men','shirt for man','shirt for men stylish latest','shirt for men casusal','shirt for men stylish']

Keywordrs_mens_short=['shorts for men','shorts for boys','shorts for man','short for boy','short','shorts']

Keywordrs_mens_pants=['pants for men','pants for man','pant for man','pant for man','pants for boys','pants for boy','pants for child','pant for boys','pant for boy','pant for child']

Keywordrs_women_t_shirt=['tshirt for women','tshirt for girls','tshirt for woman','tshirt for girl','t-shirt for women','t-shirt for girls','t-shirt for woman','t-shirt for girl','tshirt for women stylish','t-shirt for women combo','tshirt for women combo']

Keywordrs_women_shirt=['shirt for women','shirt for woman','shirts for women','shirts for woman','women\'s shirt','shirts for women stylish western','shirts for women western wear','shirt tops for women','shirts for women combo']

Keywordrs_women_kurti=['kurti for women','kurti set for women','kurti set with dupatta for women','kurtis set with dupatta for women','kurti set','kurti set','kurtis for women stylish latest','kurti pant set for women','kurti for women latest design','kurti for girls','kurtis for girls','kurtis for girl','kurti for girl']

Keywordrs_women_top=['tops for women','tops for women western wear','top for women','top for woman','tops for woman','tops for woman western wear','top for women western wear','top for woman western weat','tops for women stylish','tops for woman stylish','top for women stylish','top for woman stylish','tops for girls','tops for girl','top for girls','top for girl','tops for jeans for women','tops for women cotton','tops for woman cotton','top for women cotton','top for woman cotton']


Keywordrs_women_pants=['pants for women','pants for woman','pant for women','pant for woman','pants for girls','pants for girl','pant for girls','pant for girl','pants for women western wear','pants for women for kurti','pants for women for daily use','pants for women combo','cargo pants for women']

Keywordrs_men_track=['tracks for man','tracks for men','track suit for men','track suit for man','track pant for men','track pant for man','track suit for men for winter wear','track pant for boys','tracksuit men']

Keywordrs_women_track=['tracks for woman','tracks for women','track suit for women','track suit for woman','track pant for women','track pant for woman','track suit for women for winter wear','track pant for girls','tracksuit women']




app=Flask('__main__',template_folder="templates")
app.secret_key = os.urandom(24)

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/add_products',methods=['POST','GET'])
def products():

    return render_template('add_product.html')

@app.route('/added',methods=['GET','POST'])
def added_pro():
    try:
        data = request.form
        print("Form data:", data)
        img_f = request.files['image']

        print("Uploaded file name:", img_f.filename)

        
        bucket = storage.bucket(app=firebase_admin.get_app(), name='rwpd-micro-project.appspot.com')
        blob = bucket.blob(img_f.filename)
            
        print("Before uploading image to Firebase Storage")
        blob.upload_from_file(img_f,content_type='image/jpeg')
        print("After uploading image to Firebase Storage")

        url = f'https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{blob.name}?alt=media'


        print("File uploaded successfully:", url)
        

        product={
            'product_id':p_id,
            'name':data['title'],
            'desc': data['description'],
            'cat':data['category'],
            'quantity':data['quantity'],
            'price':data['price'],
            'img':url
    
        }

        product_ref=db.reference('products').push(product)
        print("data added successfully")
        return redirect('/add_products')
    
    except Exception as e:
        print("Error Occured ",e)
        return render_template('add_product.html',message="product added failed")
    

  


@app.route('/signup',methods=['POST','GET'])
def users():
    # try:
    #     data=request.form  
    #     users={
    #         'user_id':user_id,
    #         'name':data['name'],
    #         'phone_no':data['phone'],
    #         'dob':data['dob'],
    #         'address':data['address'],
    #         'email':data['email'],
    #         'password':data['password'],
    #         'iscustom':data['option']

    #     }

    #     user_push=db.reference('users').push(users)
        

    # except Exception as e:
    #     return render_template('signup.html',message="failed")
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
     session.pop('user_id', None)
     session.pop('username', None)

     return redirect('/')

@app.route('/successful',methods=['GET','POST'])
def check_is_login():
    
    if request.method=='POST':
        data=request.form
        email=data['email']
        password=data['password']

        try:
            user_ref=db.reference('/users')
            user_data = user_ref.order_by_child('email').equal_to(email).get()
            if not user_data:
                return render_template('log-in.html',msg="User Not Found")
            
            else:
                stored_password_hash = list(user_data.values())[0].get('password')
                if password==stored_password_hash:
                    session['user_id']=user_id
                    print("session created")
                    return redirect('/')
                else:
                    return render_template('log-in.html',msg="User Not Found")


            
        except Exception as e:
            
            print("Error Occured",e)
            return render_template('log-in.html', message="Login Failed. An unexpected error occurred.")
@app.route('/login',methods=['POST','GET'])
def login():
    

    return render_template('log-in.html')
@app.route(f'/search',methods=['GET','POST'])
def search():
 
    try:
        query = request.form['query']
        print("Received search query:", query)
        print(query)
        matched_products_dict={}
        matched_products={}
        if query in Keywordrs_mens_t_shirt:
            category='men\'s t-shirt'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")
            

            
            return render_template('cart.html')

        elif query in Keywordrs_mens_shirt:
            category='men\'s shirt'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")


        
            return render_template('cart.html')

        elif query in Keywordrs_mens_short:
            category='men\'s short'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")

        
            return render_template('cart.html')

        elif query in Keywordrs_mens_pants:
            category='men\'s pants'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")

        
            return render_template('cart.html')

        elif query in Keywordrs_men_track:
            category='men\'s track'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")

            return render_template('cart.html')

        elif query in Keywordrs_women_t_shirt:
            category='women t-shirt'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")

        
            return render_template('cart.html')

        elif query in Keywordrs_women_shirt:
            category='women shirt'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")

        
            return render_template('cart.html')

        elif query in Keywordrs_women_kurti:
            category='women kurti'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")

        
            return render_template('cart.html')

        elif query in Keywordrs_women_top:
            category='women top'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")
        
            return render_template('cart.html')

        elif query in Keywordrs_women_pants:
            category='women pants'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")

        
            return render_template('cart.html')

        elif query in Keywordrs_women_track:
            category='women track'
            print(category)
            
            data=products_ref.get()
            
            print(data)
            for product_id, product_info in data['products'].items():
                cat = product_info['cat']
                if category==cat:
                    matched_products[product_id] = product_info
            
            print(matched_products)
            
            with open('searched_products.json','w') as path_file:
                json.dump(matched_products,path_file,indent=4)
                print("data added to json file")
        
            return render_template('cart.html')
        

        else:
            return render_template('index.html')
            
        
            
    except Exception as e:
        print(f"Error Occured {e}")
        return redirect(url_for('index'))


@app.route('/customize',methods=['GET','POST'])
def customize():
    return render_template('customize.html')

@app.route('/license',methods=['GET'])
def license():
    return render_template('license.html')

@app.route('/terms_and_Conditions',methods=['GET'])
def tnc():
    return render_template("terms&cond.html")

@app.route('/contact_us',methods=['GET'])
def contactus():
    return render_template('contact-us.html')

@app.route('/success',methods=['GET','POST'])
def success():
    try:
        data=request.form  
        
        users={
            'user_id':user_id,
            'name':data['name'],
            'phone_no':data['phone'],
            'dob':data['dob'],
            'address':data['address'],
            'email':data['email'],
            'password':data['password']

        }

        print("User data:", users)
        user = auth.create_user(
            email=data['email'],
            password=data['password'],
            display_name=data['name']
        )
        print("User authenticated")

        user_push=db.reference('users').push(users)

        print("User data pushed to database")

        return render_template('A_S_P.html')
    


    except Exception as e:
       
        message = request.args.get('message', '')
        print("Error Occured",e)  
        return render_template('signup.html', message=message)


@app.route('/jsonfile',methods=['GET','POST'])
def returnjson():
    with open('searched_products.json', 'r') as file:
        data = json.load(file) 
    return jsonify(data)


if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0')