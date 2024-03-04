from jira import JIRA
import pandas as pd
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
jira = JIRA(options=jira_options, basic_auth=('inuruev','04021999google'))

# issue = jira.issue(f'FERZLSUP-{numbers}')
# Список номеров задач для СУЗ


number = []

def jira_transition(number, comm=None):
    # for i in number:
        # Итерация для изменения метки для задач
    issue = jira.issue(f'{number}')
    # Проставление метки
    issue.fields.labels.append(u'NSD_PCY')
    # апдейт
    issue.update(fields={"labels": issue.fields.labels})
    # перевод задачи на себя
    issue.update(assignee={'name': 'inuruev'})
    # коммент
    jira.add_comment(issue, "Добрый день. По Вашей заявке сведения актуализированы. При возникновении вопросов просьба создать новую заявку с обязательным приложением фактуры по указанным случаям. Текущая заявка закрыта.")
    print(number, issue.fields.status)


def jira_del_labels(number):
    for i in number:
        # Итерация для изменения метки для задач
        issue = jira.issue(f'FERZLSUP-{i}')
        # Удаление всех меток
        issue.fields.labels.clear()
        # апдейт
        issue.update(fields={"labels": issue.fields.labels})
        # коммент
        # jira.add_comment(issue)


def export_jira_issues(jql, max_result):
    # Поиск задач Jira по jql поиску
    jira_key = jira.search_issues(jql, maxResults=max_result)
    # Объявляю массив для записи
    history_log = []
    # Прохожусь по id ключам, записываю необходимые поля в массив
    for keyid in range(len(jira_key)):
        key_name = str(jira_key[keyid])
        issue = jira.issue(key_name)
        history_log.append([key_name, issue.fields.summary, issue.fields.description, issue.fields.labels])
    # Сохраняю output в пандасовский датафрейм
    df = pd.DataFrame(history_log)
    # df = df.rename(columns={'issue_key': 0, 'summary': 1, 'description': 2, 'labels': 3})
    df.to_excel(dirRep + 'Out_Jira_Tasks.xlsx')


jql_request = 'project = FERZLSUP AND issuetype = "Запрос на изменение" AND status in (Открыта, "В работе Л2", "Запрос информации", "В работе Л3", "В ожидании", "Передано на рассмотрение ФОМС") AND labels = ГР_Объединение_персон ORDER BY resolved ASC, created ASC'

jql_epotehin = 'project = FERZLSUP AND status in (Открыта, "В работе Л2", "Запрос информации", "В работе Л3", "В ожидании", "Передано на рассмотрение ФОМС") AND assignee in (epotehin)'

jql_my_tasks = 'project = FERZLSUP AND status in (Закрыта, Решено) AND resolved >= -7d AND assignee in (currentUser())'
# iparashkov
# currentUser()
# data = pd.read_excel(dirRep+'data_SUZ.xlsx', 'Лист4')
#
# for suz_number in data['Номер заявки']:
#     jira_transition(suz_number)

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

collect_task(jql_epotehin, 3)
