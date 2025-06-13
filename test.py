import os
if os.path.exists("DejavuSans.cw127.pkl"):
        os.remove("DejavuSans.cw127.pkl")
        print(f"Deleted DejavuSans.cw127pkl file")
else:
        print("Hi")