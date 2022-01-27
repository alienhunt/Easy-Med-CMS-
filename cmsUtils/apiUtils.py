from django.contrib.auth.models import User
# from cms.models import to_date
# from cmsUtils.imgToByte import toByteString

# function takes in model object list and returns dict of items with key as index and items as objects item dict
def models_to_dict(models, report=False):

    global base
    data=list()

    for model in models:
        # data["Record "+str(index)] = model.get_dict()
        temp = model.get_dict()
        if report == True:

            if model.report_status == True:
                print(model)
                temp['report'] = model.report_img.name
                temp["report-image"] = model.report_img.url

        data.append(temp)

    return data

def get_contact_or_none(model, user_id):

    try:
        
        contact = model.get(user_id=user_id)
        return contact
    
    except:

        return None

def validate_signup(validated_data):

    contact_keys = ["gender", "dob", "phone", "address"]
    user_keys = ["first_name", "email", "password"]

    for key in contact_keys:

        if key not in validated_data.keys():
            
            return key+" - missing!"
    
    for key in user_keys:

        if key not in validated_data["user"].keys():

            return key+" - missing!"

    if User.objects.filter(email=validated_data["user"]["email"]).exists():

        return "User Already Exists!"

    return None