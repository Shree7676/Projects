
def signUp(un,pwd):

    if len(un)==0:   # un==""
        return "Username cant be blank"
    db=open("P4_All in one\database.txt", "r")
    for data in db:
        u,p=data.split(",")
        if un==u:
            db.close()
            return "User id already occupied"
    db.close()

    if len(pwd)<4:
        return "pwd is too short"

    db = open("P4_All in one\database.txt", "a")
    details=un+","+pwd+"\n"
    db.write(details)
    db.close()
    return "Successfully signed up"

def login(uname,pwds):
    db = open("P4_All in one\database.txt", "r")
    flag=0
    for data in db:
        u, p,*r =data.split(",")

        if uname==u:
            flag=1
            break
    db.close()
    if flag==0:
        ans="Please enter valid username"
        return ans

    else:   #pwd check
        if pwds+"\n"==p:
            ans="Succuesfully logged in"

            return ans

        else:
            ans="Pwd not matching1"
            return ans

