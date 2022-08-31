import csv


def get_csv(dialogs):
    headers = ["dlg_id", "line_n", "role", "text", "hellow", "goodbye", "name", "company"]
    with open('result.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for dialog in dialogs:
            rows = dialog.get_messages()
            for row in rows:
                writer.writerow(row)
