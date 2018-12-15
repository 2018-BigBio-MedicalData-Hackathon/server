import pandas as pd

def getName(codes):
    df_kcdInfo = pd.read_csv('./data/KCD_CODE.csv')
    result=[]
    for code in codes:
        temp=df_kcdInfo[df_kcdInfo['code']==code]
        result.append(temp.values.tolist())
    return result

if __name__ == '__main__':
    codes=['Z99.8','D98.3']
    print(getName(codes))