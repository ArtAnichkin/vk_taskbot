import time
import vk_api
import pickle
#import vk_user

vk = vk_api.VkApi(token = 'mytoken')
upload = vk_api.VkUpload(vk)

param = {
    'count': 1,
    'time_offset': 5,
    'filter': 'unread'
}

counter_f = 'task_counter.data'
answ_f = 'answers.data'
tasks_path = 'tasks\\'


def write_msg(user_id, msg, random):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': msg,
        'random_id': random,
    })


def upload_photo(photo):
    response = upload.photo_messages(photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key


def send_photo(user_id, owner_id, photo_id, access_key, random):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.method('messages.send', {
        'user_id': user_id,
        'random_id': random,
        'attachment': attachment
    })


def main():
    key = input('Выберите режим работы: (о)бновление заданий, (з)апуск бота: ')
    if key == 'о':
        print('Введите ответы, чтобы закончить введите пустую строку')
        answ_list = []
        while(True):
            answ = input()
            if answ == '':
                break
            answ_list.append(answ)

        with open(answ_f, 'wb') as f:
            pickle.dump(answ_list, f)
        with open(counter_f, 'rb') as f:
            counter_dict = pickle.load(f)
        for x in counter_dict:
            counter_dict[x] = -1
        with open(counter_f, 'wb') as f:
            pickle.dump(counter_dict, f)
        print('Не забудте внести фото новых заданий')
        key = input('Запустить бота? (д)а/(н)ет: ')
    if key == 'з' or 'д':
        run()
    elif key == 'n':
        pass
    else:
        print('Неверный ключ, завершение работы')
    print('Завершение работы')


def run():
    with open(counter_f, 'rb') as f:
        counter_dict = pickle.load(f)
    with open(answ_f, 'rb') as f:
        answ_touple = pickle.load(f)
    tasks_num = len(answ_touple)
    tasks_name_list = []
    for i in range(1, tasks_num + 1):
        tasks_name_list.append(f'{tasks_path}{str(i)}.png')
    try:
        while True:
            response = vk.method('messages.getConversations', param)
            if response['items']:
                item = response['items'][0]
                last_mess = item['last_message']
                random = last_mess['random_id']
                my_id = last_mess['peer_id']
                mess = last_mess['text']

                if my_id not in counter_dict:
                    counter_dict[my_id] = 0
                    text = 'Привет! Ни разу тебя тут не видел! Но раз уж ты здесь - лови задание МШ!'
                    write_msg(my_id, text, random)
                    send_photo(my_id, *upload_photo(tasks_name_list[counter_dict[my_id]]), random)
                elif counter_dict[my_id] == -1:
                    counter_dict[my_id] += 1
                    text = 'Привет! Добро пожаловать на МШ! Держи первое задание'
                    write_msg(my_id, text, random)
                    send_photo(my_id, *upload_photo(tasks_name_list[counter_dict[my_id]]), random)
                elif counter_dict[my_id] == tasks_num:
                    text = 'Хей, я еще не обновил свой список заданий, приходи попозже)'
                    write_msg(my_id, text, random)
                else:
                    if mess == answ_touple[counter_dict[my_id]]:
                        if counter_dict[my_id] == tasks_num - 1:
                            text = 'Да, верно, на этом все'
                            write_msg(my_id, text, random)
                        else:
                            text = 'Молодец, верно, держи следующее!'
                            write_msg(my_id, text, random)
                            send_photo(my_id, *upload_photo(tasks_name_list[counter_dict[my_id] + 1]), random)
                        counter_dict[my_id] += 1
                    else:
                        text = 'Блинб, не  верно, давай ка еще раз попробуй'
                        write_msg(my_id, text, random)

            time.sleep(1)
    finally:
        with open(counter_f, 'wb') as f:
            pickle.dump(counter_dict, f)
        print('The program was stopped.')
        print(f'Ключи: {counter_dict}')


if __name__ == '__main__':
    main()
