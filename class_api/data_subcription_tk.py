from datetime import datetime
import time



class PayloadSubTk():
    payload_tickets = []
    def timestamp_to_date(timestamp):
        date = datetime.fromtimestamp(timestamp)
        return date

    def received_data(id, data):
        payload = PayloadSubTk.payload_tickets
        count_payload_tk = len(payload)
        if count_payload_tk != 0:
            for i in range(count_payload_tk):
                a = (payload[i]['id'] == id)
                data_time = PayloadSubTk.timestamp_to_date(payload[i]['timestamp'])
                current_time = PayloadSubTk.timestamp_to_date(round(time.time()))
                if a:
                    payload.pop(i)
                    break
            payload.append(data)
        else:
            payload.append(data)
        PayloadSubTk.payload_tickets = payload
        print(PayloadSubTk.payload_tickets)

