from jira import JIRA
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import telebot


bot = telebot.TeleBot('5404650116:AAHFKuX9poF-wUm52eQZuOzna7UL2xLW-a0')
bot.config['api_key'] = '5404650116:AAHFKuX9poF-wUm52eQZuOzna7UL2xLW-a0'



dirRep = "C:/Users/ilias/OneDrive/Рабочий стол/Мусор/"

# соединение с Jira при помощи логин и пароля
jira_options = {'server':'https://stp.gisoms.ffoms.gov.ru', 'verify':False}
jira = JIRA(options=jira_options, basic_auth=('login','password'))



jql_request = 'project = FERZLSUP AND issuetype = "Запрос на изменение" AND status in (Открыта, "В работе Л2", "Запрос информации", "В работе Л3", "В ожидании", "Передано на рассмотрение ФОМС") AND labels = ГР_Объединение_персон ORDER BY resolved ASC, created ASC'

jql_epotehin = 'project = FERZLSUP AND status in (Открыта, "В работе Л2", "Запрос информации", "В работе Л3", "В ожидании", "Передано на рассмотрение ФОМС") AND assignee in (epotehin)'

jql_my_tasks = 'project = FERZLSUP AND status in (Закрыта, Решено) AND resolved >= -7d AND assignee in (currentUser())'


def collect_task(jql, amount: int):
    cnt_task = 0
    print(bot.send_message(chat_id='-1001660599100', text=f'Начало скрипта, кол-во: {amount} -' + f' {datetime.now()}'))
    while cnt_task <=amount:
        jira_key = jira.search_issues(jql, maxResults = 200)
        for keyid in range(len(jira_key)):
            # if cnt_task <= 3:
            key_name = str(jira_key[keyid])
            # задача в Jira
            issue = jira.issue(key_name)
            # апдейт исполнителя
            issue.update(assignee={'name': 'inuruev'})
            # вывод
            print(issue.fields.assignee, key_name)
            cnt_task = cnt_task + 1
            time.sleep(3)
    print(bot.send_message(chat_id='-1001660599100', text = 'Конец скрипта ' + f'{datetime.now()}'))

"""Ниже необходимо указать кол-во заявок"""
collect_task(jql_epotehin, 1)
