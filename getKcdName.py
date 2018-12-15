import pandas as pd
"""
호출방법 getName(codes) || codes => list type의 code 모음
리턴 [['코드','한글병명','영문병명'],['코드','한글병명','영문병명'],['코드','한글병명','영문병명']...]
"""
def getName(codes):
    # 질병분류기호 csv 불러오기
    df_kcdInfo = pd.read_csv('./data/KCD_CODE.csv')
    result=[]
    for code in codes:
        temp=df_kcdInfo[df_kcdInfo['code']==code]
        result.append(temp.values.tolist())

    # 리스트가 두번 감싸져서 껍질 벗기기용
    result = [row_element for row in result for row_element in row]
    return result

if __name__ == '__main__':
    codes=['Z99.8','A01.3']
    print(getName(codes))
    """ 출력 예시
    >>> [['Z99.8', '기타기능성기계및장치에의존', 'Dependenceonotherenablingmachinesanddevices']], 
    >>> [['A01.3', '파라티푸스C', 'ParatyphoidfeverC']]
    """