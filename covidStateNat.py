import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey="iSqWGzwAwAmj1J9dcTV7Sb6LqtbQgZ0eW45VLfOBy4ZF7MOQXFl1v14RHHKNE6jj52UJ4Q4LvdkMURdWpInnbQ=="

#[CODE 1]
def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


#[CODE 2]
def getCovidStatsItem(startCreateDt, endCreateDt):
    service_url = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19NatInfStateJson"
    parameters = "?_type=json&serviceKey=" + ServiceKey   #인증키
    parameters += "&startCreateDt=" + str(startCreateDt)
    parameters += "&endCreateDt=" + str(endCreateDt)
    url = service_url + parameters

    retData = getRequestUrl(url)   #[CODE 1]

    if (retData == None):
        return None
    else:
        return json.loads(retData)


#[CODE 3]
def getCovidStatsService(startCreateDt, endCreateDt):

    jsonData = getCovidStatsItem(startCreateDt, endCreateDt) #[CODE 2]

    js = jsonData['response']['body']['items']['item']
    df = pd.DataFrame(js)
    df = df.sort_values(['seq'], ascending=True)
    return df

#[CODE 0]
def main():
    print("<<코로나 감염 현황 데이터를 수집합니다.>>")
    today = int(datetime.date.today().isoformat().replace('-', ''))
    print('오늘의 날짜는 ', today, '입니다.')
    startCreateDt =int(input('데이터를 언제부터 수집할까요? ex)20200310 : '))
    endCreateDt = int(input('데이터를 언제까지 수집할까요?(미입력시 오늘까지의 데이터를 수집합니다.) : ') or today)

    df =getCovidStatsService(startCreateDt, endCreateDt) #[CODE 3]

    df.to_json('./해외코로나현황_%d_%d.json' % (startCreateDt, endCreateDt))
    print('./해외코로나현황_%d_%d.json SAVED' % (startCreateDt, endCreateDt))

    df = df.rename(columns={'seq':'게시글 번호','stateDt':'기준일', 'stateTime':'기준시간', 'decideCnt':'확진자 수', 'deathCnt':'사망자수',
                            'accExamCnt':'누적 의심 검사 수', 'accDefRate':'누적 확진률', 'createDt':'등록일시분초','updateDt':'수정일시분초'})
    print(df)
    df.to_csv('./해외코로나현황_%d_%d.csv' % (startCreateDt, endCreateDt), encoding='utf-8-sig')
    print('./해외코로나현황_%d_%d.csv SAVED' % (startCreateDt, endCreateDt))
if __name__ == '__main__':
    main()