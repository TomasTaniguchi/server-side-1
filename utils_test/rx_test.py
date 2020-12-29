from rx import Observable
import json

payload_tickets = {'id_tk': '5493764921348@c.us', 'phone_id': 3387, 'node2': '@Cyffffberlink', 'node3': '#servicio', 'node4': '',
     'timestamp': 1594311359}




payload_tickets= [{'hola': 44, 'como': 444, 'estas': 1128.15657311}, {'hola': 22, 'como': 222, 'estas': 1111}]

for i in range(len(payload_tickets)):
    a = (payload_tickets[i]['hola'] == 22)
    if a:
        print(i)
        payload_tickets.pop(i)
        break

print(payload_tickets)

def tickets():
    return Observable.from_(payload_tickets).filter(lambda i: i['estas']==00)

.\
map(lambda i : print(i)).subscribe()



input("")