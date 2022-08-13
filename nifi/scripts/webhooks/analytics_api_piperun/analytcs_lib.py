import os 
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/../../..')
path = r'{}'.format(os.path.normpath(path + '/Auth/ana.json'))

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = path
VIEW_ID = '174266719'
#CLIENT_ID = "497201865.1647866958"
#endDate : "2022-12-31"

credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, scopes=SCOPES)


analytics = build('analyticsreporting', 'v4', credentials=credentials)
ana = analytics.reports()

origins_list = [345521, 347249, 83307, 339125]

class analy:

    def __init__(self,deal_origin_id):
        self.deal_origin_id = deal_origin_id

    def userActivity(CLIENT_ID,endDate):
        return  analytics.userActivity().search(
                body = {
                    
                    "viewId": VIEW_ID,
                    "user": {
                            "type": "CLIENT_ID",
                            "userId": CLIENT_ID
                    },
                    "dateRange": {
                            "startDate": "2016-01-01",
                            "endDate": endDate 
                    },
                    "pageSize": 40000
                }
        ).execute()


    def getLastchannelGrouping(data):

        try: 
            lastchannelGrouping  = data['sessions'][0]['activities'][0]['channelGrouping']
            return lastchannelGrouping 
        except:
            return "Não foi possível capturar o último channelGrouping."


    def firstSessionIndex(data):
        return len(data['sessions'])-1


    def getFirstChannelGrouping(data):

    
        firstSessionIndex = len(data['sessions'])-1

        firstSession = data['sessions'][firstSessionIndex]
        firstSessionActivities = firstSession['activities']
        firstActivityIndex = len(firstSessionActivities)-1

        firstActivity = firstSession['activities'][firstActivityIndex]
        
        try: 
            firstChannelGrouping = firstActivity['channelGrouping']
            return firstChannelGrouping

        except:
            return "Não foi possível capturar o primeiro channelGrouping."        


    def getActivitiesFilteredByPageviews(data):
        sessions = data['sessions']

        for i in range(len(sessions)):
            activities = sessions[i]['activities']

            atv = []
            for atvs in activities:
                if atvs['activityType'] == 'PAGEVIEW':
                    atv.append(atvs)

            sessions[i]['activities'] = atv

        return sessions      




    # Função da contagem de pageviews não duplicadas anteriores à conversão.
    def countPageviewsBeforeConversion(data,deal_origin_id):
        sessions = analy.getActivitiesFilteredByPageviews(data)
        allSessions = data['sessions']
        count = 0
        sessionPages = []
        for session in sessions:
            activities = session['activities']
            pagePaths = []
            previousPagePath = ''
            for act in activities:
                thisPagePath = act['pageview']['pagePath']
                if len(thisPagePath) > 1 and thisPagePath.endswith('/'):
                    thisPagePath = thisPagePath[:-1]
                
                if thisPagePath != previousPagePath:
                    pagePaths.append(thisPagePath)  
                    previousPagePath = thisPagePath

            # n = len(pagePaths)
            sessionPages.append(pagePaths)
        # count= count+len(sessionPages) 

        # Count all pages in sessions
        for sessionPage in sessionPages:
            count = count+len(sessionPage) 

        # If origin is {formulario-de-cadastro-padrao} (Teste gratis).
        # if deal_origin == 345521:
        if deal_origin_id == origins_list[0]:
            for i in range(len(sessionPages[0])):
                thisPagePath = sessionPages[0][i]

                afterPagePath = sessionPages[0][i-1] if sessionPages[0][i-1] != None else ''

                if afterPagePath == '/pagina-agradecimento-pos-cadastro-teste-gratis' and thisPagePath == '/teste-gratis-poli':
                    break
                else: 
                    count = count - 1


        # If origin is {formulario-landing-page-instagram}
        # if deal_origin == 347249:
        if deal_origin_id == origins_list[1]:
            for i in range(len(sessionPages[0])):
                thisPagePath = sessionPages[0][i]

                afterPagePath = sessionPages[0][i-1] if sessionPages[0][i-1] != None else ""

                if afterPagePath == "/obrigado-lista-de-espera-instagram-api" and thisPagePath == "/instagram":
                    break
                else: 
                    count = count - 1
        
        
        # If origin is {zapform}
        # if deal_origin == 83307:
        if deal_origin_id == origins_list[2]:
            activities = allSessions[0]["activities"]
            previousPagePath = ""
            for activity in activities:
                if (activity["activityType"] == "EVENT" and activity["event"]["eventCategory"] == "JoinChat" and activity["event"]["eventAction"] == "click"):
                    if activity["activityType"] == "PAGEVIEW":
                        thisPagePath = activity['pageview']['pagePath']
                        if len(thisPagePath) > 1 and thisPagePath.endswith('/'):
                            thisPagePath = thisPagePath[:-1]

                        if thisPagePath != previousPagePath:
                            count = count - 1
                            previousPagePath = thisPagePath
                    

        # If origin is {pop-up-novos-visitantes}
        # if deal_origin == 339125:
        if deal_origin_id == origins_list[3]:
            activities = allSessions[0]["activities"]
            previousPagePath = ""
            for activity in activities:
                if (activity["activityType"] == "EVENT" and activity["event"]["eventLabel"] == "pop-up-novos-visitantes" and activity["event"]["eventAction"] == "Viewed"):
                    if activity["activityType"] == "PAGEVIEW":
                        thisPagePath = activity['pageview']['pagePath']
                        if len(thisPagePath) > 1 and thisPagePath.endswith('/'):
                            thisPagePath = thisPagePath[:-1]

                        if thisPagePath != previousPagePath:
                            count = count - 1
                            previousPagePath = thisPagePath

        

        # return count
        if count > -1:
            return count 
        else:
            return -99 # display error



    def getFirstPageViewed(data):
        firstSessionIndex = len(data['sessions']) -1
        activities = data['sessions'][firstSessionIndex]['activities']

        activities_first_index = len(activities) - 1 

        if type(activities_first_index) == int:
            firstSessionIndex = len(data['sessions']) -1
            activities = data['sessions'][firstSessionIndex]['activities']

            for act in activities[::-1]:
                if act['activityType'] == "PAGEVIEW":
                    firstPageView = "https://" + act['hostname'] + act['pageview']['pagePath']
                    return firstPageView

                else:
                    return "Não foi possível capturar a 1º pageview."   




    def getLastSource(data):
        activities = data['sessions'][0]['activities']

        activities = data['sessions'][0]['activities']

        for act in activities:
            lastSource = act['source']
            return lastSource

        return "Não foi possível capturar a última origem."        


    def getLastMedium(data):
        activities = data['sessions'][0]['activities']

        activities = data['sessions'][0]['activities']

        for act in activities:
            lastMedium = act['medium']
            return lastMedium

        return "Não foi possível capturar a última mídia." 



    def getFirstMedium(data):
        firstSessionIndex = len(data['sessions']) -1
        activities = data['sessions'][firstSessionIndex]['activities']

        activities_first_index = len(activities) - 1 

        if type(activities_first_index) == int:
            firstSessionIndex = len(data['sessions']) -1
            activities = data['sessions'][firstSessionIndex]['activities']

            for act in activities[::-1]:
                firstMedium = act['medium']
                return firstMedium

            return "Não foi possível capturar a 1º mídia." 


    def getFirstSource(data):
        firstSessionIndex = len(data['sessions']) -1
        activities = data['sessions'][firstSessionIndex]['activities']

        activities_first_index = len(activities) - 1 

        if type(activities_first_index) == int:
            firstSessionIndex = len(data['sessions']) -1
            activities = data['sessions'][firstSessionIndex]['activities']

            for act in activities[::-1]:
                firstSource = act['source']
                return firstSource

            return "Não foi possível capturar a 1º origem."   



    def getDataFields(data,deal_origin_id):
        fields = {
            "lastChannelGrouping" : analy.getLastchannelGrouping(data),
            "lastSource" : analy.getLastSource(data),
            "lastMedium" : analy.getLastMedium(data),
            "firstChannelGrouping" : analy.getFirstChannelGrouping(data),
            "firstPageView" : analy.getFirstPageViewed(data),
            "firstSource" : analy.getFirstSource(data),
            "firstMedium" : analy.getFirstMedium(data),
            "isFirstVisit" : "Sim" if len(data['sessions']) == 1 else "Não",
            "countPageviewsBeforeConversion" : analy.countPageviewsBeforeConversion(data,deal_origin_id)
        }

        return fields                       


    