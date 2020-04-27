def d_wri(txt,filename):
    with open(".\\d_file\\"+filename,mode="w",encoding="utf-8") as f:
        f.write(txt)
        f.close()
    return